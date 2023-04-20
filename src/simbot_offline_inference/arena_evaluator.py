from typing import Optional

import httpx
from loguru import logger

from arena_missions.structures import MissionTrajectory
from simbot_offline_inference.inference_controller import SimBotInferenceController
from simbot_offline_inference.metrics import SimBotEvaluationMetrics, WandBTrajectoryTracker


EXPERIENCE_HUB_HEALTHCHECK_ATTEMPTS = 40


class SimBotArenaEvaluator:
    """Handle the evaluation of the experience hub on the arena."""

    def __init__(
        self,
        inference_controller: SimBotInferenceController,
        evaluation_metrics: SimBotEvaluationMetrics,
        wandb_trajectory_tracker: Optional[WandBTrajectoryTracker] = None,
    ) -> None:
        self._inference_controller = inference_controller
        self._evaluation_metrics = evaluation_metrics
        self._wandb_trajectory_tracker = wandb_trajectory_tracker

    def run_evaluation(self, trajectories: list[MissionTrajectory]) -> None:
        """Run the evaluation on all the test data."""
        with self._inference_controller:
            for instance in trajectories:
                try:
                    self.run_evaluation_step(instance)
                except httpx.ConnectTimeout:
                    logger.error("Failed to establish a connection to the arena.")
                    if self._inference_controller.restart_arena():
                        logger.info("Restarted the arena. Retrying...")
                        self.run_evaluation_step(instance)

            logger.info("Finished evaluation!")

        self._evaluation_metrics.log_overall_metrics()
        self._evaluation_metrics.send_to_s3()

    def run_evaluation_step(self, trajectory: MissionTrajectory) -> None:
        """Run the evaluation on a single instance of the test data."""
        prep_session_id = trajectory.create_preparation_session_id()
        session_id = trajectory.session_id

        if self._evaluation_metrics.has_mission_been_evaluated(session_id):
            logger.info(f"Mission ({session_id}) has already been evaluated. Skipping...")
            return

        logger.info(f"Running evaluation for '{session_id}'")

        # Start tracking the trajectory on WandB
        if self._wandb_trajectory_tracker is not None and trajectory.high_level_key:
            self._wandb_trajectory_tracker.start_trajectory(
                session_id,
                preparation_session_id=prep_session_id,
                high_level_key=trajectory.high_level_key,
                cdf_scene=trajectory.cdf.scene,
            )

        self.prepare_arena(prep_session_id, trajectory)

        actions_for_session = []
        processed_utterance_counter = 0

        for utterance in trajectory.utterances:
            if self._inference_controller.is_all_goals_complete():
                logger.warning("All goals are complete but there are still utterances left.")
                break

            actions_for_utterance = self._inference_controller.handle_utterance(
                session_id, utterance
            )
            actions_for_session.extend(actions_for_utterance)
            processed_utterance_counter += 1

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
            remaining_utterances=trajectory.utterances[processed_utterance_counter:],
        )

        # Stop tracking the trajectory on WandB
        if self._wandb_trajectory_tracker is not None:
            self._wandb_trajectory_tracker.finish_trajectory(
                is_success=goal_completion_status,
                subgoal_completion_status=subgoal_completion_status,
            )

    def prepare_arena(self, preparation_scene_id: str, trajectory: MissionTrajectory) -> None:
        """Prepare the arena with the CDF."""
        logger.info("Launching mission in the Arena")
        self._inference_controller.launch_game(trajectory.cdf)

        logger.debug("Verifying Experience Hub is healthy")
        if not self._inference_controller.healthcheck():
            raise AssertionError("The Experience Hub is not healthy.")

        # Run the preparation steps
        if trajectory.preparation_utterances:
            logger.debug("Running preparation steps")

            for prep_utterance in trajectory.preparation_utterances:
                self._inference_controller.handle_utterance(preparation_scene_id, prep_utterance)

        # Go to random viewpoint
        logger.debug("Going to random viewpoint")
        self._inference_controller.go_to_random_viewpoint(trajectory.cdf.start_room)

        # Randomise the start position
        logger.debug("Randomising start position")
        self._inference_controller.randomise_start_position()
