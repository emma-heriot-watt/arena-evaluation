import random
import subprocess
import time
from pathlib import Path
from typing import Any, NamedTuple, Optional
from uuid import uuid4

import httpx
import orjson
from loguru import logger

from arena_missions.constants.arena import OfficeRoom
from arena_wrapper.arena_orchestrator import ArenaOrchestrator as AlexaArenaOrchestrator
from arena_wrapper.enums.object_output_wrapper import ObjectOutputType
from simbot_offline_inference.arena_action_builder import ArenaActionBuilder
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

    @property
    def unity_log_path(self) -> Path:
        """Get the path to the unity logs."""
        settings = Settings()
        return Path(settings.unity_log_path)

    def launch_new_game(
        self,
        mission_cdf: Any,
        attempts: int = 10,
        interval: int = 5,
        object_output_type: ObjectOutputType = ObjectOutputType.OBJECT_MASK,
    ) -> None:
        """Launch the game on the Arena instance.

        We also need to do the dummy actions to make sure the game is ready to go.
        """
        self.send_cdf_to_arena(mission_cdf)
        self.send_dummy_actions_to_arena(attempts, interval, object_output_type)

    def send_cdf_to_arena(self, mission_cdf: Any) -> None:
        """Send the CDF to the Arena instance."""
        if not self.launch_game(mission_cdf):
            raise AssertionError("Could not launch the game")

    def send_dummy_actions_to_arena(
        self,
        attempts: int = 10,
        interval: int = 5,
        object_output_type: ObjectOutputType = ObjectOutputType.OBJECT_MASK,
    ) -> None:
        """Send dummy actions to the Arena instance to make sure it's ready to go."""
        logger.debug("Sending dummy actions to verify game is ready")
        dummy_action = [
            {
                "id": "1",
                "type": "Rotate",
                "rotation": {
                    "direction": "Right",
                    "magnitude": 0,
                },
            }
        ]

        for attempt_idx in range(attempts):
            return_val, _ = self.execute_action(dummy_action, object_output_type, "Rotate right")

            # If it succeeds, then just exit the loop since it's ready to go
            if return_val:
                return

            logger.error(
                f"Attempt {attempt_idx + 1}/{attempts} failed. Waiting for {interval} seconds before trying again."
            )
            time.sleep(5)

        raise AssertionError("Exhauted all attempts")

    def go_to_random_viewpoint(self, room: OfficeRoom) -> None:
        """Go to a random viewpoint in the given room."""
        if not self.response:
            logger.exception("There is no reponse to get viewpoints from.")
            return

        try:
            viewpoints: dict[str, dict[str, float]] = self.response["sceneMetadata"]["GoToPoints"]
        except KeyError:
            logger.error("Unable to get viewpoints from response.")
            return

        # Get all the viewpoints in the current room
        viewpoints_for_current_room = [
            viewpoint for viewpoint in viewpoints.keys() if viewpoint.startswith(room)
        ]

        # Choose random viewpoint
        chosen_viewpoint = random.choice(viewpoints_for_current_room)

        # Go to the chosen viewpoint
        logger.debug(f"Going to viewpoint: {chosen_viewpoint}")

        action_builder = ArenaActionBuilder()
        return_val, _ = self.execute_action(
            [action_builder.viewpoint(chosen_viewpoint)], ObjectOutputType.OBJECT_MASK, None
        )

        if not return_val:
            logger.warning(
                "Failed to go to a random viewpoint, going to the first one in the room"
            )
            self.execute_action(
                [action_builder.viewpoint(f"{room}_1")], ObjectOutputType.OBJECT_MASK, None
            )

    def randomise_start_position(
        self,
        num_steps: int = 10,
        object_output_type: ObjectOutputType = ObjectOutputType.OBJECT_MASK,
    ) -> None:
        """Randomise the start position of the agent."""
        logger.debug("Randomising start position of the agent")
        action_builder = ArenaActionBuilder()
        actions_to_send = [action_builder.random_navigation() for _ in range(num_steps)]

        for action in actions_to_send:
            return_val, action_response = self.execute_action([action], object_output_type, None)

            # If it fails, raise assertion error
            if not return_val:
                # Explicitly do not raise if these error types occur
                error_types_to_ignore = ("AlternateNavigationUsed", "UnsupportedNavigation")

                if action_response.get("errorType") not in error_types_to_ignore:
                    raise AssertionError("Failed to randomise start position")

            time.sleep(5)

    def _get_unity_execution_command(self) -> str:
        settings = Settings()

        command = (
            "DISPLAY=:"
            + str(settings.display)
            + " "
            + str(settings.arena_path)
            + " -logfile "
            + str(settings.unity_log_path)
            # + " -FastMode "
            + "&"
        )

        return command


class ExperienceHubOrchestrator:
    """Orchestrator for the Experience Hub."""

    def __init__(
        self,
        healthcheck_endpoint: str,
        predict_endpoint: str,
        auxiliary_metadata_dir: Path,
        auxiliary_metadata_cache_dir: Path,
        cached_extracted_features_dir: Path,
        model_storage_dir: Path,
        experience_hub_dir: Path,
    ) -> None:
        self._healthcheck_endpoint = healthcheck_endpoint
        self._predict_endpoint = predict_endpoint
        self._auxiliary_metadata_dir = auxiliary_metadata_dir
        self._auxiliary_metadata_cache_dir = auxiliary_metadata_cache_dir
        self._cached_extracted_features_dir = cached_extracted_features_dir
        self._experience_hub_dir = experience_hub_dir
        self._model_storage_dir = model_storage_dir

    def __enter__(self) -> None:
        """Start the Experience Hub."""
        logger.debug("Starting controller API for the experience hub...")
        subprocess.run(self._build_experience_hub_command(), shell=True)

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        """Try to kill the experience hub."""
        subprocess.run(
            "kill -9 ps -ax | grep 'python -m emma_experience_hub simbot run-controller-api' | awk '{print $1}'",
            shell=True,
        )

    def healthcheck(self, attempts: int = 5, interval: int = 2) -> bool:
        """Perform healthcheck, with retry intervals.

        To disable retries, just set the number of attempts to 1.
        """
        healthcheck_flag = False

        for attempt in range(attempts):
            healthcheck_flag = self._healthcheck()

            # If the healthcheck flag is all good, break from the loop
            if healthcheck_flag:
                break

            # Otherwise, report a failed attempt
            logger.error(f"Healthcheck attempt {attempt + 1}/{attempts} failed.")

            # If attempt is not the last one, sleep for interval and go again
            if attempt < attempts - 1:
                logger.debug(f"Waiting for {interval} seconds and then trying again.")
                time.sleep(interval)

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

    def _build_experience_hub_command(self) -> str:
        """Build the command to run the experience hub."""
        command = "python -m emma_experience_hub simbot run-controller-api --auxiliary-metadata-dir {auxiliary_metadata_dir} --auxiliary-metadata-cache-dir {auxiliary_metadata_cache_dir}  --extracted-features-cache-dir {extracted_features_cache_dir} --timeout 10000000000 &"
        return command.format(
            auxiliary_metadata_dir=self._auxiliary_metadata_dir,
            auxiliary_metadata_cache_dir=self._auxiliary_metadata_cache_dir,
            extracted_features_cache_dir=self._cached_extracted_features_dir,
        )
