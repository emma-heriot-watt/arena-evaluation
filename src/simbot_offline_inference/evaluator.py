from uuid import uuid4

from loguru import logger

from simbot_offline_inference.controller import SimBotInferenceController
from simbot_offline_inference.metrics import SimBotEvaluationMetrics
from simbot_offline_inference.prepare_trajectory_data import SimBotTestInstance


EXPERIENCE_HUB_HEALTHCHECK_ATTEMPTS = 40


class SimBotArenaEvaluator:
    """Handle the evaluation of the experience hub on the arena."""

    def __init__(
        self,
        inference_controller: SimBotInferenceController,
        evaluation_metrics: SimBotEvaluationMetrics,
        session_id_prefix: str,
    ) -> None:
        self._inference_controller = inference_controller
        self._evaluation_metrics = evaluation_metrics
        self._session_id_prefix = session_id_prefix

    def run_evaluation(self, test_data: list[SimBotTestInstance]) -> None:
        """Run the evaluation on all the test data."""
        with self._inference_controller:
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
        self._inference_controller.launch_game(test_data["mission_cdf"])

        logger.debug("Verifying Experience Hub is healthy")
        if not self._inference_controller.healthcheck():
            raise AssertionError("The Experience Hub is not healthy.")

        logger.info(f"Running evaluation for Test #{test_data['test_number']}")
        session_id = f"{self._session_id_prefix}-{uuid4()}"

        actions_for_session = []

        for utterance in test_data["utterances"]:
            actions_for_utterance = self._inference_controller.handle_utterance(
                session_id, utterance
            )
            actions_for_session.extend(actions_for_utterance)

        # Check goal status and get results
        logger.debug("Calculating metrics for test")
        (
            goal_completion_status,
            subgoal_completion_status,
        ) = self._inference_controller.get_goal_completion_status()
        self._evaluation_metrics.add_mission_metrics(
            mission_name=test_data["mission_id"],
            mission_group=test_data["mission_group"],
            is_mission_completed=goal_completion_status,
            subgoal_completion_status=subgoal_completion_status,
            predicted_actions=actions_for_session,
            last_game_state=self._inference_controller.get_latest_game_state(),
        )
