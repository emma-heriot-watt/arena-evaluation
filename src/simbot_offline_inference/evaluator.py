import time
from typing import Any

from loguru import logger

from arena_wrapper.enums.object_output_wrapper import ObjectOutputType
from simbot_offline_inference.metrics import SimBotEvaluationMetrics
from simbot_offline_inference.orchestrators import ArenaOrchestrator, ExperienceHubOrchestrator
from simbot_offline_inference.prepare_trajectory_data import SimBotTestInstance
from uuid import uuid4


class SimBotArenaEvaluator:
    """Handle the evaluation of the experience hub on the arena."""

    def __init__(
        self,
        arena_orchestrator: ArenaOrchestrator,
        experience_hub_orchestrator: ExperienceHubOrchestrator,
        evaluation_metrics: SimBotEvaluationMetrics,
        object_output_type: ObjectOutputType = ObjectOutputType.OBJECT_MASK,
        max_loops_for_single_utterance: int = 15,
    ) -> None:
        self._arena_orchestrator = arena_orchestrator
        self._experience_hub_orchestrator = experience_hub_orchestrator
        self._evaluation_metrics = evaluation_metrics

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

        self._evaluation_metrics.log_overall_metrics()
        self._evaluation_metrics.send_to_s3()

    def run_evaluation_step(self, test_data: SimBotTestInstance) -> None:
        """Run the evaluation on a single instance of the test data."""
        if self._evaluation_metrics.has_mission_been_evaluated(test_data["mission_id"]):
            logger.info(
                f"Mission ({test_data['mission_id']}) has already been evaluated. Skipping..."
            )
            return

        logger.info("Launching mission in the Arena")
        self._launch_game(test_data["mission_cdf"])

        logger.debug("Verifying Experience Hub is healthy")
        if not self._experience_hub_orchestrator.healthcheck():
            raise AssertionError("The Experience Hub is not healthy.")

        logger.info(f"Running evaluation for Test #{test_data['test_number']}")
        session_id = f"T2-{uuid4()}"

        actions_for_session = []

        for utterance in test_data["utterances"]:
            actions_for_utterance = self._handle_utterance(session_id, utterance)
            actions_for_session.extend(actions_for_utterance)

        # Check goal status and get results
        logger.debug("Calculating metrics for test")
        (
            _,
            goal_completion_status,
            subgoal_completion_status,
        ) = self._arena_orchestrator.get_goals_status()
        self._evaluation_metrics.add_mission_metrics(
            mission_name=test_data["mission_id"],
            mission_group=test_data["mission_group"],
            is_mission_completed=goal_completion_status,
            subgoal_completion_status=subgoal_completion_status,
            predicted_actions=actions_for_session,
            last_game_state=self._get_latest_game_state(),
        )

    def _handle_utterance(self, session_id: str, utterance: str) -> list[dict[str, Any]]:
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
            actions, should_return_control = self._experience_hub_orchestrator.get_next_actions(
                session_id,
                # Only give the utterance on the first loop, otherwise we don't since the user is
                # not instructing us to do anything
                utterance if loop_idx == 0 else None,
                auxiliary_metadata,
                previous_action_statuses,
            )
            actions_taken.extend(actions)

            # Execute the actions on the arena environment
            logger.debug(f"Executing actions: {actions}")
            return_val, action_status = self._arena_orchestrator.execute_action(
                actions, self._object_output_type, utterance
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

            if not actions:
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

    def _get_latest_game_state(self) -> dict[str, Any]:
        """Get the latest game state for the evaluation output."""
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
