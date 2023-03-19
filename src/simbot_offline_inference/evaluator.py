import time
from typing import Any

from loguru import logger

from arena_wrapper.enums.object_output_wrapper import ObjectOutputType
from simbot_offline_inference.metrics import (
    SimBotEvaluationMetrics,
    calculate_subgoal_completion_rate,
)
from simbot_offline_inference.orchestrators import ArenaOrchestrator, ExperienceHubOrchestrator
from simbot_offline_inference.prepare_trajectory_data import SimBotTestInstance


class SimBotArenaEvaluator:
    """Handle the evaluation of the experience hub on the arena."""

    def __init__(
        self,
        arena_orchestrator: ArenaOrchestrator,
        experience_hub_orchestrator: ExperienceHubOrchestrator,
        object_output_type: ObjectOutputType = ObjectOutputType.OBJECT_MASK,
        max_loops_for_single_utterance: int = 15,
    ) -> None:
        self._arena_orchestrator = arena_orchestrator
        self._experience_hub_orchestrator = experience_hub_orchestrator
        self._evaluation_metrics = SimBotEvaluationMetrics()

        self._object_output_type = object_output_type
        self._max_loops_for_single_utterance = max_loops_for_single_utterance

    def run_evaluation(self, test_data: list[SimBotTestInstance]) -> None:
        """Run the evaluation on all the test data."""
        with self._experience_hub_orchestrator:
            with self._arena_orchestrator:
                logger.info("Checking experience hub is ready...")
                self._experience_hub_orchestrator.healthcheck(40, 5)

                logger.info("Starting evaluation...")
                for instance in test_data:
                    self.run_evaluation_step(instance)

                logger.info("Finished evaluation!")

        logger.info(f"Overall success rate: {self._evaluation_metrics.overall_success_rate}")
        logger.info(
            f"Overall subgoal completion rate: {self._evaluation_metrics.overall_subgoal_completion_rate}"
        )

    def run_evaluation_step(self, test_data: SimBotTestInstance) -> None:
        """Run the evaluation on a single instance of the test data."""
        logger.info("Launching mission in the Arena")
        self._launch_game(test_data["mission_cdf"])

        logger.debug("Verifying Experience Hub is healthy")
        if not self._experience_hub_orchestrator.healthcheck():
            raise AssertionError("The Experience Hub is not healthy.")

        logger.info(f"Running evaluation for Test #{test_data['test_number']}")
        for utterance in test_data["utterances"]:
            self._handle_utterance(test_data["test_number"], utterance)

        # Check goal status and get results
        logger.debug("Calculating metrics for test")
        (
            _,
            goal_completion_status,
            subgoal_completion_status,
        ) = self._arena_orchestrator.get_goals_status()
        self._evaluation_metrics.add_mission_metrics(
            is_mission_completed=goal_completion_status,
            subgoal_completion_status=subgoal_completion_status,
        )

        logger.info(f"Test #{test_data['test_number']} completed")
        logger.info(f"Mission completion status: {goal_completion_status}")
        logger.info(f"Subgoal completion status: {subgoal_completion_status}")
        logger.info(
            f"Subgoal completion rate for test: {calculate_subgoal_completion_rate(subgoal_completion_status)}"
        )

    def _handle_utterance(self, test_idx: int, utterance: str) -> None:
        """Handle execution of a single utterance in the arena."""
        previous_action_statuses: list[Any] = []

        for loop_idx in range(self._max_loops_for_single_utterance):
            logger.debug(f"Executing step {loop_idx}")

            # Get the auxiliary metadata from the arena
            logger.debug("Getting auxiliary metadata from the arena")
            auxiliary_metadata = self._arena_orchestrator.get_reconstructed_metadata()

            # Get the next actions to take from the ExperienceHub
            logger.debug("Trying to get the next actions to take from the Experience Hub")
            actions, should_return_control = self._experience_hub_orchestrator.get_next_actions(
                test_idx,
                # Only give the utterance on the first loop, otherwise we don't since the user is
                # not instructing us to do anything
                utterance if loop_idx == 0 else None,
                auxiliary_metadata,
                previous_action_statuses,
            )

            # Execute the actions on the arena environment
            logger.debug(f"Executing actions: {actions}")
            return_val, error_code = self._arena_orchestrator.execute_action(
                actions, self._object_output_type, utterance
            )
            logger.debug(f"Received response from arena: {return_val}, {error_code}")

            # If there is an issue completing the action, we need to give that back to the
            # experience hub
            if not return_val:
                # TODO: Convert the error code to the previous action statuses
                previous_action_statuses = []
                logger.error(f"Action could not be completed for the utterance {utterance}")

            # Only break out the loop if we return a dialog action AND there is no error in
            # performing the action
            if should_return_control and return_val:
                logger.debug("Returning control to the user to get the next utterance")
                break

    def _launch_game(self, mission_cdf: Any, attempts: int = 10, interval: int = 5) -> None:
        """Launch the game on the Arena instance.

        We also need to do the dummy actions to make sure the game is ready to go.
        """
        if not self._arena_orchestrator.launch_game(mission_cdf):
            raise AssertionError("Could not launch the game")

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
            return_val, error_code = self._arena_orchestrator.execute_action(
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
