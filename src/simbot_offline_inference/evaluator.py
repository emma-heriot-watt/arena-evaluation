from loguru import logger

from arena_wrapper.enums.object_output_wrapper import ObjectOutputType
from simbot_offline_inference.metrics import (
    SimBotEvaluationMetrics,
    calculate_subgoal_completion_rate,
)
from simbot_offline_inference.orchestrators import ArenaOrchestrator, ExperienceHubOrchestrator
from simbot_offline_inference.prepare_trajectory_data import SimBotTestInstance


class SimBotArenaEvaluator:
    def __init__(
        self,
        arena_orchestrator: ArenaOrchestrator,
        experience_hub_orchestrator: ExperienceHubOrchestrator,
        object_output_type: ObjectOutputType = ObjectOutputType.OBJECT_MASK,
    ) -> None:
        self._arena_orchestrator = arena_orchestrator
        self._experience_hub_orchestrator = experience_hub_orchestrator
        self._evaluation_metrics = SimBotEvaluationMetrics()

        self._object_output_type = object_output_type

    def run_evaluation(self, test_data: list[SimBotTestInstance]) -> None:
        with self._arena_orchestrator, self._experience_hub_orchestrator:
            # Make sure experience hub is ready
            logger.info("Checking experience hub is ready...")
            self._experience_hub_orchestrator.healthcheck(1000, 5)

            # Run the evaluation
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
        if not self._arena_orchestrator.launch_game(test_data["mission_cdf"]):
            raise AssertionError("Could not launch the game")

        if not self._experience_hub_orchestrator.healthcheck():
            raise AssertionError("The Experience Hub is not healthy.")

        logger.info(f"Running evaluation for Test #{test_data['test_number']}")

        for utterance in test_data["utterances"]:
            # Get the auxiliary metadata from the arena
            auxiliary_metadata = self._arena_orchestrator.get_reconstructed_metadata()

            # Get the next actions to take from the ExperienceHub
            actions = self._experience_hub_orchestrator.get_next_actions(
                test_data["test_number"], utterance, auxiliary_metadata
            )
            logger.debug(f"Executing actions: {actions}")

            # Execute the actions on the arena environment
            return_val, error_code = self._arena_orchestrator.execute_action(
                actions, self._object_output_type, utterance
            )
            logger.debug(f"Received response from arena: {return_val}, {error_code}")

            if not return_val:
                logger.error(f"Action could not be completed for the utterance {utterance}")

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
