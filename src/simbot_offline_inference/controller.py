import time
from contextlib import ExitStack
from typing import Any, Literal

from loguru import logger

from arena_wrapper.enums.object_output_wrapper import ObjectOutputType
from simbot_offline_inference.orchestrators import ArenaOrchestrator, ExperienceHubOrchestrator


class SimBotInferenceController:
    """Controller for the inference pipeline."""

    def __init__(
        self,
        arena_orchestrator: ArenaOrchestrator,
        experience_hub_orchestrator: ExperienceHubOrchestrator,
        object_output_type: ObjectOutputType = ObjectOutputType.OBJECT_MASK,
        max_loops_for_single_utterance: int = 15,
        experience_hub_healthcheck_attempts: int = 40,
    ) -> None:
        self._arena_orchestrator = arena_orchestrator
        self._experience_hub_orchestrator = experience_hub_orchestrator

        self._object_output_type = object_output_type
        self._max_loops_for_single_utterance = max_loops_for_single_utterance
        self._experience_hub_healthcheck_attempts = experience_hub_healthcheck_attempts

        self._exit_stack = ExitStack()

    def __enter__(self) -> None:
        """Initialize the services."""
        if self.is_controller_running:
            return None

        self._exit_stack.enter_context(self._arena_orchestrator)
        self._exit_stack.enter_context(self._experience_hub_orchestrator)

        logger.info("Checking experience hub is ready...")
        self._experience_hub_orchestrator.healthcheck(self._experience_hub_healthcheck_attempts, 5)

        return self._exit_stack.__enter__()  # type: ignore[return-value] # noqa: WPS609

    def __exit__(self, *args: Any, **kwargs: Any) -> bool:
        """Exit the services."""
        return self._exit_stack.__exit__(*args, **kwargs)  # noqa: WPS609

    @property
    def is_controller_running(self) -> bool:
        """Check if the arena is running."""
        return self._arena_orchestrator.is_unity_running and self.healthcheck()

    def healthcheck(self) -> bool:
        """Healthcheck the services."""
        return self._experience_hub_orchestrator.healthcheck()

    def get_goal_completion_status(self) -> tuple[bool, list[Literal[0, 1]]]:
        """Get the goal completion status from the Arena instance."""
        (
            _,
            goal_completion_status,
            subgoal_completion_status,
        ) = self._arena_orchestrator.get_goals_status()
        return goal_completion_status, subgoal_completion_status

    def launch_game(self, mission_cdf: Any, attempts: int = 10, interval: int = 5) -> None:
        """Launch the game on the Arena instance.

        We also need to do the dummy actions to make sure the game is ready to go.
        """
        self.send_cdf_to_arena(mission_cdf)
        self.send_dummy_actions_to_arena(attempts, interval)

    def send_cdf_to_arena(self, mission_cdf: Any) -> None:
        """Send the CDF to the Arena instance."""
        if not self._arena_orchestrator.launch_game(mission_cdf):
            raise AssertionError("Could not launch the game")

    def send_dummy_actions_to_arena(self, attempts: int = 10, interval: int = 5) -> None:
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
            return_val, _ = self._arena_orchestrator.execute_action(
                dummy_action, self._object_output_type, "Rotate right"
            )

            # If it succeeds, then just exit the loop since it's ready to go
            if return_val:
                return

            logger.error(
                f"Attempt {attempt_idx + 1}/{attempts} failed. Waiting for {interval} seconds before trying again."
            )
            time.sleep(5)

        raise AssertionError("Exhauted all attempts")

    def handle_utterance(  # noqa: WPS231
        self, session_id: str, utterance: str
    ) -> list[dict[str, Any]]:
        """Handle execution of a single utterance in the arena.

        Return a list of all actions taken for the current utterance.
        """
        actions_taken: list[dict[str, Any]] = []
        previous_action_statuses: list[Any] = []

        for loop_idx in range(self._max_loops_for_single_utterance):
            logger.debug(f"Executing step {loop_idx}")

            # Get the auxiliary metadata from the arena
            logger.debug("Getting auxiliary metadata from the arena")
            auxiliary_metadata = self._arena_orchestrator.get_reconstructed_metadata()

            # Get the next actions to take from the ExperienceHub
            logger.debug("Trying to get the next actions to take from the Experience Hub")
            (
                interaction_actions,
                dialog_actions,
                should_return_control,
            ) = self._experience_hub_orchestrator.get_next_actions(
                session_id,
                # Only give the utterance on the first loop, otherwise we don't since the user is
                # not instructing us to do anything
                utterance if loop_idx == 0 else None,
                auxiliary_metadata,
                previous_action_statuses,
            )
            actions_taken.extend(interaction_actions)

            # Execute the actions on the arena environment
            logger.debug(f"Executing actions: {interaction_actions}")
            return_val, action_status = self._arena_orchestrator.execute_action(
                interaction_actions, self._object_output_type, utterance
            )
            logger.debug(f"Received response from arena: {return_val}, {action_status}")

            # Update the previous action statuses so it goes back to the arena
            if not should_return_control or not return_val:
                if action_status is not None:
                    previous_action_statuses = [action_status]

            # If there is an issue completing the action, we need to give that back to the
            # experience hub
            if not return_val:
                logger.error(f"Action could not be completed for the utterance {utterance}")

            if not interaction_actions:
                logger.warning(
                    "There were not actions to perform, so there is just dialog. Returning control back to the user since we didn't do anything in the arena."
                )
                break

            # Only break out the loop if we return a dialog action AND there is no error in
            # performing the action
            if should_return_control and return_val:
                logger.debug("Returning control to the user to get the next utterance")
                break

        return actions_taken

    def get_latest_game_state(self) -> dict[str, Any]:
        """Get the latest game state for the evaluation output."""
        if self._arena_orchestrator.response is None:
            raise AssertionError("There is no response from the Arena")

        exclude_keys = [
            "sceneMetadata",
            "colorImage",
            "depthImage",
            "normalsImage",
            "instanceSegmentationImage",
            "objects",
        ]
        return {
            key: self._arena_orchestrator.response[key]
            for key in self._arena_orchestrator.response
            if key not in exclude_keys
        }
