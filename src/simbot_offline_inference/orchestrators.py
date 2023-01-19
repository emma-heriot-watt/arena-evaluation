import signal
from multiprocessing import Process
from pathlib import Path
from threading import Event
from time import sleep
from typing import Any
from uuid import uuid4

import httpx
import orjson
from loguru import logger

from arena_wrapper.arena_orchestrator import ArenaOrchestrator as AlexaArenaOrchestrator
from emma_experience_hub.commands.simbot.cli import run_background_services, run_controller_api
from simbot_offline_inference.settings import Settings


class ArenaOrchestrator(AlexaArenaOrchestrator):
    """Wrapper for the ArenaOrchestrator."""

    def __enter__(self) -> None:
        """Initialize the unity instance."""
        if not self.init_unity_instance():
            raise AssertionError("Could not start the unity instance.")

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        """Try to kill the unity instance."""
        if not self.kill_unity_instance():
            logger.warning(
                "Could not kill the Unity instance. You might need to kill it manually."
            )

    def _get_unity_execution_command(self) -> str:
        settings = Settings()

        command = (
            "DISPLAY=:"
            + str(settings.display)
            + " "
            + str(settings.arena_path)
            + " -logfile "
            + str(settings.unity_log_path)
            + "&"
        )

        return command


class ExperienceHubOrchestrator:
    _exit = Event()

    def __init__(
        self,
        healthcheck_endpoint: str,
        predict_endpoint: str,
        auxiliary_metadata_dir: Path,
        cached_extracted_features_dir: Path,
        session_id_prefix: str = "",
    ) -> None:
        self._healthcheck_endpoint = healthcheck_endpoint
        self._predict_endpoint = predict_endpoint
        self._session_id_prefix = session_id_prefix
        self._auxiliary_metadata_dir = auxiliary_metadata_dir
        self._cached_extracted_features_dir = cached_extracted_features_dir

        self._experience_hub_process = Process(
            name="emma-experience-hub-controller-api",
            target=run_controller_api,
            kwargs={
                "auxiliary_metadata_dir": self._auxiliary_metadata_dir,
                "auxiliary_metadata_cache_dir": self._auxiliary_metadata_dir,
                "extracted_features_cache_dir": self._cached_extracted_features_dir,
            },
            daemon=True,
        )

    def __enter__(self) -> None:
        """Start the Experience Hub."""
        # Run the background services
        logger.debug("Starting background services for the experience hub...")
        run_background_services(download_models=True, force_download=True, run_in_background=True)

        # Create the process for the experience hub
        logger.debug("Starting controller API for the experience hub...")
        self._experience_hub_process.start()

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        """Try to kill the experience hub."""
        logger.debug("Trying to stop running the expeirence hub...")

        self._experience_hub_process.join()
        try:
            self._experience_hub_process.close()
        except ValueError:
            logger.info("Experience hub didn't close proeprly, so forcing it.")
            self._experience_hub_process.terminate()

    def _healthcheck(self) -> bool:
        """Verify the health of the experience hub service."""
        logger.debug("Running healthcheck")

        with httpx.Client() as client:
            response = client.get(self._healthcheck_endpoint)

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as err:
            logger.exception("Unable to perform healthcheck", exc_info=err)
            return False

        return True

    def healthcheck(self, attempts: int = 1, interval: int = 0) -> bool:
        """Perform healthcheck, with retry intervals.

        To disable retries, just set the number of attempts to 1.
        """
        self._prepare_exit_signal()

        healthcheck_flag = False

        for attempt in range(attempts):
            healthcheck_flag = self._healthcheck()

            # If the healthcheck flag is all good, break from the loop
            if healthcheck_flag or self._exit.is_set():
                break

            # Otherwise, report a failed attempt
            logger.error(f"Healthcheck attempt {attempt + 1}/{attempts} failed.")

            # If attempt is not the last one, sleep for interval and go again
            if attempt < attempts - 1:
                logger.debug(f"Waiting for {interval} seconds and then trying again.")
                sleep(interval)

        return healthcheck_flag

    def _prepare_exit_signal(self) -> None:
        """Prepare the exit signal to handle KeyboardInterrupt events."""
        for sig in ("TERM", "HUP", "INT"):
            signal.signal(getattr(signal, f"SIG{sig}"), self._break_from_sleep)

    def _break_from_sleep(self, signum: int, _frame: Any) -> None:
        """Break from the sleep."""
        logger.info("Interrupted. Shutting down...")
        self._exit.set()

    def get_next_actions(
        self,
        test_idx: int,
        utterance: str,
        auxiliary_metadata: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Make a prediction for the actions the agent should take."""
        session_id: str = self._create_session_id(test_idx)
        prediction_request_id = str(uuid4())

        self._save_auxiliary_metadata(session_id, prediction_request_id, auxiliary_metadata)

        logger.debug("Building request payload")
        simbot_request = self._build_raw_simbot_request(
            session_id, prediction_request_id, utterance
        )

        logger.debug(f"Sending request: {simbot_request}")
        simbot_response = self._make_request(simbot_request)

        actions = simbot_response.get("actions")
        if not actions:
            raise AssertionError("No actions to return.")
        return actions

    def _create_session_id(self, test_idx: int) -> str:
        """Create the session ID for the example."""
        session_id = ""
        if self._session_id_prefix:
            session_id = f"{self._session_id_prefix}-"

        return f"{session_id}{uuid4()}-{test_idx}"

    def _save_auxiliary_metadata(
        self,
        session_id: str,
        prediction_request_id: str,
        auxiliary_metadata: dict[str, Any],
    ) -> None:
        """Save the auxiliary metadata to the file."""
        output_location = self._auxiliary_metadata_dir.joinpath(
            f"{session_id}/{prediction_request_id}.json"
        )
        output_location.write_bytes(orjson.dumps(auxiliary_metadata))
        logger.debug(f"Wrote auxiliary metadata to `{output_location}`")

    def _build_raw_simbot_request(
        self,
        session_id: str,
        prediction_request_id: str,
        utterance: str,
    ) -> dict[str, Any]:
        """Build the request to send to the Experience Hub."""
        request_header = {
            "sessionId": session_id,
            "predictionRequestId": prediction_request_id,
        }
        raw_auxiliary_metadata_sensor = {
            "type": "GameMetaData",
            "metaData": {"uri": f"efs://{session_id}/{prediction_request_id}.json"},
        }
        raw_speech_recognition_sensor = {
            "type": "SpeechRecognition",
            "recognition": {
                "tokens": [
                    {"value": token, "confidence": {"score": 0.95, "bin": "HIGH"}}
                    for token in utterance.strip().split(" ")
                ]
            },
        }
        return {
            "header": request_header,
            "request": {
                "sensors": [
                    raw_speech_recognition_sensor,
                    raw_auxiliary_metadata_sensor,
                ],
                "previousActions": [],
            },
        }

    def _make_request(self, simbot_request: dict[str, Any]) -> dict[str, Any]:
        """Make the request to the experience hub and return the response."""
        with httpx.Client(timeout=None) as client:
            response = httpx.post(self._predict_endpoint, json=simbot_request)

        try:
            response.raise_for_status()
        except Exception:
            logger.exception("Unable to get response for request.")

        return response.json()
