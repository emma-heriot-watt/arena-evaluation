from contextlib import ExitStack
from typing import Any, Literal

from loguru import logger

from arena_missions.structures import CDF
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

        self.randomise_start_position = self._arena_orchestrator.randomise_start_position
        self.go_to_random_viewpoint = self._arena_orchestrator.go_to_random_viewpoint

    def __enter__(self) -> None:
        """Initialize the services."""
        self._exit_stack.enter_context(self._arena_orchestrator)
        self._exit_stack.enter_context(self._experience_hub_orchestrator)

        logger.info("Checking experience hub is ready...")
        self._experience_hub_orchestrator.healthcheck(self._experience_hub_healthcheck_attempts, 5)

        return self._exit_stack.__enter__()  # type: ignore[return-value] # noqa: WPS609

    def __exit__(self, *args: Any, **kwargs: Any) -> bool:
        """Exit the services."""
        return self._exit_stack.__exit__(*args, **kwargs)  # noqa: WPS609

    @property
    def is_arena_running(self) -> bool:
        """Check if the arena is running."""
        return self._arena_orchestrator.is_unity_running

    def healthcheck(self) -> bool:
        """Healthcheck the services."""
        return self._experience_hub_orchestrator.healthcheck()

    def launch_game(self, mission_cdf: CDF, attempts: int = 10, interval: int = 5) -> None:
        """Launch the game on the Arena instance.

        We also need to do the dummy actions to make sure the game is ready to go.
        """
        return self._arena_orchestrator.launch_new_game(
            mission_cdf.dict(by_alias=True), attempts, interval, self._object_output_type
        )

    def get_goal_completion_status(self) -> tuple[bool, list[Literal[0, 1]]]:
        """Get the goal completion status from the Arena instance."""
        (
            _,
            goal_completion_status,
            subgoal_completion_status,
        ) = self._arena_orchestrator.get_goals_status()
        return goal_completion_status, subgoal_completion_status

    def handle_utterance(  # noqa: WPS231
        self, session_id: str, utterance: str
    ) -> list[dict[str, Any]]:
        """Handle execution of a single utterance in the arena.

        Return a list of all actions taken for the current utterance.
        """
        actions_taken: list[dict[str, Any]] = []
        previous_action_statuses: list[Any] = []

        if self.is_all_goals_complete():
            raise AssertionError(
                "Do not send an utterance when all goals are complete. Arena will crash. If you are wanting to do this, there is something wrong in the challenge definition."
            ) from None

        for loop_idx in range(self._max_loops_for_single_utterance):
            if self.is_all_goals_complete():
                logger.warning("All goals are complete, so we are breaking out of the loop")
                break

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

    def is_all_goals_complete(self) -> bool:
        """Check to see if all the goals are complete."""
        arena_response = self._arena_orchestrator.response

        if not arena_response:
            return False

        # If the challenge progress does not exist in the response, then no.
        challenge_progress = arena_response.get("challengeProgress", None)

        if not challenge_progress:
            return False

        challenge_goals = challenge_progress.get("ChallengeGoals", None)

        if not challenge_goals:
            return False

        num_goals = len(challenge_goals)
        finished_goal_count = 0

        for goal in challenge_goals:
            is_finished = goal.get("isFinished", False)
            if is_finished:
                finished_goal_count += 1

        return num_goals == finished_goal_count
