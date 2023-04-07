from typing import Any

from loguru import logger

from simbot_offline_inference.inference_controller import SimBotInferenceController
from simbot_offline_inference.metrics import SimBotEvaluationMetrics
from simbot_offline_inference.structures import SimBotTrajectory


EXPERIENCE_HUB_HEALTHCHECK_ATTEMPTS = 40


class SimBotArenaEvaluator:
    """Handle the evaluation of the experience hub on the arena."""

    def __init__(
        self,
        inference_controller: SimBotInferenceController,
        evaluation_metrics: SimBotEvaluationMetrics,
        session_id_prefix: str,
        *,
        enable_randomness_in_session_id: bool = False,
    ) -> None:
        self._inference_controller = inference_controller
        self._evaluation_metrics = evaluation_metrics
        self._session_id_prefix = session_id_prefix
        self._enable_randomness_in_session_id = enable_randomness_in_session_id

    def run_evaluation(self, trajectories: list[SimBotTrajectory]) -> None:
        """Run the evaluation on all the test data."""
        with self._inference_controller:
            logger.info("Starting evaluation...")
            for instance in trajectories:
                self.run_evaluation_step(instance)

            logger.info("Finished evaluation!")

        self._evaluation_metrics.log_overall_metrics()

        if self._upload_metrics_to_s3:
            self._evaluation_metrics.send_to_s3()

    def run_evaluation_step(self, trajectory: SimBotTrajectory) -> None:
        """Run the evaluation on a single instance of the test data."""
        session_id = trajectory.create_session_id(
            self._session_id_prefix, include_randomness=self._enable_randomness_in_session_id
        )

        if self._evaluation_metrics.has_mission_been_evaluated(session_id):
            logger.info(f"Mission ({session_id}) has already been evaluated. Skipping...")
            return

        logger.info(f"Running evaluation for '{session_id}'")

        self.prepare_cdf_in_arena(trajectory.cdf)

        actions_for_session = []

        for utterance in trajectory.utterances:
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
            mission_name=session_id,
            mission_group=trajectory.mission_group,
            is_mission_completed=goal_completion_status,
            subgoal_completion_status=subgoal_completion_status,
            predicted_actions=actions_for_session,
            last_game_state=self._inference_controller.get_latest_game_state(),
        )

    def prepare_cdf_in_arena(self, cdf: dict[str, Any]) -> None:
        """Prepare the arena with the CDF."""
        logger.info("Launching mission in the Arena")
        self._inference_controller.launch_game(cdf)

        logger.debug("Verifying Experience Hub is healthy")
        if not self._inference_controller.healthcheck():
            raise AssertionError("The Experience Hub is not healthy.")
