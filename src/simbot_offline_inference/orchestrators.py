import signal
from multiprocessing import Process
from pathlib import Path
from threading import Event
from time import sleep
from typing import Any, NamedTuple, Optional
from uuid import uuid4

import httpx
import orjson
from loguru import logger

from arena_wrapper.arena_orchestrator import ArenaOrchestrator as AlexaArenaOrchestrator
from emma_experience_hub.commands.simbot.cli import run_controller_api
from simbot_offline_inference.settings import Settings


class ExperienceHubNextActions(NamedTuple):
    """Return type after getting the next set of actions from the experience hub."""

    interaction_actions: list[dict[str, Any]]
    dialog_actions: list[dict[str, Any]]
    should_return_control: bool


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
    """Orchestrator for the Experience Hub."""

    _exit = Event()

    def __init__(
        self,
        healthcheck_endpoint: str,
        predict_endpoint: str,
        auxiliary_metadata_dir: Path,
        auxiliary_metadata_cache_dir: Path,
        cached_extracted_features_dir: Path,
        model_storage_dir: Path,
        experience_hub_dir: Path,
        timeout: int = -1,
    ) -> None:
        self._healthcheck_endpoint = healthcheck_endpoint
        self._predict_endpoint = predict_endpoint
        self._auxiliary_metadata_dir = auxiliary_metadata_dir
        self._auxiliary_metadata_cache_dir = auxiliary_metadata_cache_dir
        self._cached_extracted_features_dir = cached_extracted_features_dir
        self._experience_hub_dir = experience_hub_dir
        self._model_storage_dir = model_storage_dir

        self._experience_hub_process = Process(
            target=run_controller_api,
            kwargs={
                "auxiliary_metadata_dir": self._auxiliary_metadata_dir,
                "auxiliary_metadata_cache_dir": self._auxiliary_metadata_cache_dir,
                "extracted_features_cache_dir": self._cached_extracted_features_dir,
                "log_to_cloudwatch": False,
                "traces_to_opensearch": False,
                "workers": 1,
                "timeout": timeout,
            },
            daemon=True,
        )

    def __enter__(self) -> None:
        """Start the Experience Hub."""
        # Create the process for the experience hub
        logger.debug("Starting controller API for the experience hub...")
        self._experience_hub_process.start()

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        """Try to kill the experience hub."""
        self.kill_experience_hub()

    def kill_experience_hub(self) -> None:
        """Kill the experience hub."""
        logger.debug("Trying to stop running the experience hub...")

        self._experience_hub_process.join()
        self._experience_hub_process.close()

        if self._experience_hub_process.is_alive():
            logger.debug("Killing the experience hub...")
            self._experience_hub_process.kill()

        if self._experience_hub_process.is_alive():
            logger.debug("Terminating the experience hub...")
            self._experience_hub_process.terminate()

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

    def get_next_actions(
        self,
        session_id: str,
        utterance: Optional[str],
        auxiliary_metadata: dict[str, Any],
        previous_action_statuses: list[Any],
    ) -> ExperienceHubNextActions:
        """Make a prediction for the actions the agent should take."""
        prediction_request_id = str(uuid4())

        self._save_auxiliary_metadata(session_id, prediction_request_id, auxiliary_metadata)

        logger.debug("Building request payload")
        simbot_request = self._build_raw_simbot_request(
            session_id, prediction_request_id, utterance, previous_action_statuses
        )

        logger.debug(f"Sending request: {simbot_request}")
        simbot_response = self._make_request(simbot_request)

        actions = simbot_response.get("actions")
        if not actions:
            raise AssertionError("No actions to return.")

        return ExperienceHubNextActions(
            interaction_actions=self._filter_dialog_actions(actions),
            dialog_actions=self._filter_interaction_actions(actions),
            should_return_control=self._should_return_control_for_actions(actions),
        )

    def _healthcheck(self) -> bool:
        """Verify the health of the experience hub service."""
        logger.debug("Running healthcheck")

        with httpx.Client() as client:
            try:
                response = client.get(self._healthcheck_endpoint)
            except httpx.ReadTimeout:
                logger.error("Healthcheck timed out")
                return False
            except httpx.ConnectError:
                logger.error("Connection refused")
                return False

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("Healthcheck failed")
            return False

        logger.info("Healthcheck success")
        return True

    def _prepare_exit_signal(self) -> None:
        """Prepare the exit signal to handle KeyboardInterrupt events."""
        for sig in ("TERM", "HUP", "INT"):
            signal.signal(getattr(signal, f"SIG{sig}"), self._break_from_sleep)

    def _break_from_sleep(self, signum: int, _frame: Any) -> None:
        """Break from the sleep."""
        logger.info("Interrupted. Shutting down...")
        self.kill_experience_hub()
        self._exit.set()

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
        output_location.parent.mkdir(parents=True, exist_ok=True)
        output_location.write_bytes(orjson.dumps(auxiliary_metadata))
        logger.debug(f"Wrote auxiliary metadata to `{output_location}`")

    def _build_raw_simbot_request(
        self,
        session_id: str,
        prediction_request_id: str,
        utterance: Optional[str],
        previous_action_statuses: list[Any],
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

        simbot_request: dict[str, Any] = {
            "header": request_header,
            "request": {
                "sensors": [
                    raw_auxiliary_metadata_sensor,
                ],
                "previousActions": previous_action_statuses,
            },
        }

        if utterance:
            simbot_request["request"]["sensors"].append(
                {
                    "type": "SpeechRecognition",
                    "recognition": {
                        "tokens": [
                            {"value": token, "confidence": {"score": 0.95, "bin": "HIGH"}}
                            for token in utterance.strip().split(" ")
                        ]
                    },
                }
            )

        return simbot_request

    def _make_request(self, simbot_request: dict[str, Any]) -> dict[str, Any]:
        """Make the request to the experience hub and return the response."""
        with httpx.Client(timeout=None) as client:
            response = client.post(self._predict_endpoint, json=simbot_request)

        try:
            response.raise_for_status()
        except Exception:
            logger.exception("Unable to get response for request.")

        return response.json()

    def _should_return_control_for_actions(self, actions: list[dict[str, Any]]) -> bool:
        """Is the agent returning control after the actions?

        We only return control on sending the "Dialog" action, and no other time.
        """
        return any([action["type"] == "Dialog" for action in actions])

    def _filter_dialog_actions(self, actions: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Remove any dialog actions from the response."""
        return [
            action for action in actions if action["type"] not in {"Dialog", "LightweightDialog"}
        ]

    def _filter_interaction_actions(self, actions: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Filter out actions that are interaction actions/are not dialog actions."""
        return [action for action in actions if action["type"] in {"Dialog", "LightweightDialog"}]
