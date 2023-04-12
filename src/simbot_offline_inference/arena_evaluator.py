from loguru import logger

from arena_missions.structures import CDF, MissionTrajectory
from simbot_offline_inference.inference_controller import SimBotInferenceController
from simbot_offline_inference.metrics import SimBotEvaluationMetrics
from simbot_offline_inference.progress import ArenaEvaluatorProgressTracker


EXPERIENCE_HUB_HEALTHCHECK_ATTEMPTS = 40


class SimBotArenaEvaluator:
    """Handle the evaluation of the experience hub on the arena."""

    def __init__(
        self,
        inference_controller: SimBotInferenceController,
        evaluation_metrics: SimBotEvaluationMetrics,
    ) -> None:
        self._inference_controller = inference_controller
        self._evaluation_metrics = evaluation_metrics

        self._progress = ArenaEvaluatorProgressTracker()

    def run_evaluation(self, trajectories: list[MissionTrajectory]) -> None:
        """Run the evaluation on all the test data."""
        self._progress.start_new_evaluation(len(trajectories))

        with self._progress.display():
            with self._inference_controller:
                self._progress.finish_unity_check()
                for instance in trajectories:
                    self.run_evaluation_step(instance)
                    self._progress.finish_trajectory()

                logger.info("Finished evaluation!")

        self._evaluation_metrics.log_overall_metrics()
        self._evaluation_metrics.send_to_s3()

    def run_evaluation_step(self, trajectory: MissionTrajectory) -> None:
        """Run the evaluation on a single instance of the test data."""
        session_id = trajectory.session_id
        self._progress.start_new_trajectory(session_id, num_utterances=len(trajectory.utterances))

        if self._evaluation_metrics.has_mission_been_evaluated(session_id):
            logger.info(f"Mission ({session_id}) has already been evaluated. Skipping...")
            return

        logger.info(f"Running evaluation for '{session_id}'")

        self._progress.loading_cdf()
        self.prepare_cdf_in_arena(trajectory.cdf)
        self._progress.arena_ready_for_utterance()

        actions_for_session = []

        for utterance in trajectory.utterances:
            actions_for_utterance = self._inference_controller.handle_utterance(
                session_id, utterance
            )
            actions_for_session.extend(actions_for_utterance)
            self._progress.sent_utterance()

        # Check goal status and get results
        logger.debug("Calculating metrics for test")
        (
            goal_completion_status,
            subgoal_completion_status,
        ) = self._inference_controller.get_goal_completion_status()
        self._evaluation_metrics.add_mission_metrics(
            session_id=session_id,
            mission_group=trajectory.mission_group,
            is_mission_completed=goal_completion_status,
            subgoal_completion_status=subgoal_completion_status,
            predicted_actions=actions_for_session,
            last_game_state=self._inference_controller.get_latest_game_state(),
        )

    def prepare_cdf_in_arena(self, cdf: CDF) -> None:
        """Prepare the arena with the CDF."""
        logger.info("Launching mission in the Arena")
        self._inference_controller.launch_game(cdf)

        logger.debug("Verifying Experience Hub is healthy")
        if not self._inference_controller.healthcheck():
            raise AssertionError("The Experience Hub is not healthy.")
