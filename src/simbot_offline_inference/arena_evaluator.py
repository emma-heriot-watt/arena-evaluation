from typing import Any

import httpx
from loguru import logger

from arena_missions.structures import CDF, MissionTrajectory
from arena_wrapper.exceptions import RaycastMissedException
from simbot_offline_inference.inference_controller import SimBotInferenceController
from simbot_offline_inference.metrics import EvaluationMetrics, WandBCallback


class SimBotArenaEvaluator:
    """Handle the evaluation of the experience hub on the arena."""

    def __init__(
        self,
        inference_controller: SimBotInferenceController,
        evaluation_metrics: EvaluationMetrics,
        wandb_callback: WandBCallback,
        *,
        enforce_successful_preparation: bool = False,
        should_resume_previous_wandb_run: bool = False,
    ) -> None:
        self._inference_controller = inference_controller
        self._evaluation_metrics = evaluation_metrics
        self._wandb_callback = wandb_callback

        self._enforce_successful_preparation = enforce_successful_preparation
        self._should_resume_previous_wandb_run = should_resume_previous_wandb_run

    def run_evaluation(self, trajectories: list[MissionTrajectory]) -> None:
        """Run the evaluation on all the test data."""
        with self._inference_controller:
            self._wandb_callback.start_evaluation(resume=self._should_resume_previous_wandb_run)

            for instance in trajectories:
                self.run_evaluation_step(instance)

            self._wandb_callback.finish_evaluation()

            logger.info("Finished evaluation!")

    def run_evaluation_step(self, trajectory: MissionTrajectory) -> None:
        """Run a single evaluation step, with guards in case something goes wrong."""
        if self._has_mission_been_evaluated(trajectory):
            logger.info("Skipping mission because it was already evaluated.")
            return None

        logger.info(f"Running evaluation for '{trajectory.session_id}'")

        try:
            return self.run_trajectory_in_the_arena(trajectory)

        except httpx.ConnectTimeout:
            logger.error("Failed to establish a connection to the arena.")

            if self._inference_controller.restart_arena():
                logger.info("Restarted the arena. Retrying...")
                return self.run_trajectory_in_the_arena(trajectory)

        except RaycastMissedException:
            logger.error("Current trajectory will be ignored due to a RaycastMissed exception.")

            if self._inference_controller.restart_arena():
                logger.info("Successfully restarted arena. Skipping current trajectory...")
                return None

        raise RuntimeError("Failed to run the trajectory in the arena.")

    def run_trajectory_in_the_arena(self, trajectory: MissionTrajectory) -> None:
        """Run a single trajectory in the arena, from start to finish."""
        preparation_session_id = trajectory.create_preparation_session_id()

        self._wandb_callback.start_trajectory(trajectory, preparation_session_id)

        try:
            self.prepare_arena_for_trajectory(trajectory, preparation_session_id)
        except AssertionError:
            logger.warning("Preparation failed. Skipping...")
            self._finish_trajectory(
                trajectory, actions_for_session=[], processed_utterance_counter=0
            )
            return

        actions_for_session: list[Any] = []
        processed_utterance_counter = 0
        for utterance in trajectory.utterances:
            if self._inference_controller.is_all_goals_complete():
                logger.warning("All goals are complete but there are still utterances left.")
                break

            try:
                actions_for_utterance = self._inference_controller.handle_utterance(
                    trajectory.session_id, utterance
                )
            except AssertionError:
                logger.error("Unrecoverable exception occurred, exiting...")
                break

            actions_for_session.extend(actions_for_utterance)
            processed_utterance_counter += 1

        self._finish_trajectory(
            trajectory,
            actions_for_session=actions_for_session,
            processed_utterance_counter=processed_utterance_counter,
        )

    def prepare_arena_for_trajectory(  # noqa: WPS231
        self, trajectory: MissionTrajectory, preparation_session_id: str
    ) -> None:
        """Prepare the arena to run the trajectory."""
        logger.info("Sending CDF to the arena")
        self._inference_controller.launch_game(trajectory.cdf_as_dict)

        logger.debug("Verifying Experience Hub is healthy")
        if not self._inference_controller.healthcheck():
            raise AssertionError("The Experience Hub is not healthy.")

        if trajectory.preparation_utterances:
            logger.debug("Running preparation steps")

            for prep_utterance in trajectory.preparation_utterances:
                self._inference_controller.handle_utterance(preparation_session_id, prep_utterance)

        if self._enforce_successful_preparation:
            if not self._inference_controller.trajectory_preparation_completed:
                raise AssertionError("The subgoal status is 0, so preparation failed")

        if trajectory.randomise_start_position:
            logger.info("Randomising start position")

            # Go to random viewpoint
            logger.debug("Going to random viewpoint")
            if isinstance(trajectory.cdf, CDF):
                self._inference_controller.go_to_random_viewpoint(trajectory.cdf.start_room)

            # Randomise the start position
            logger.debug("Randomising start position")
            self._inference_controller.randomise_start_position()

    def _has_mission_been_evaluated(self, trajectory: MissionTrajectory) -> bool:
        """Check if the mission has already been evaluated.

        See use the mission ID if it exists, otherwise use the session ID.
        """
        if trajectory.mission_id:
            return self._evaluation_metrics.has_mission_been_evaluated(trajectory.mission_id)
        return self._evaluation_metrics.has_mission_been_evaluated(trajectory.session_id)

    def _finish_trajectory(
        self,
        trajectory: MissionTrajectory,
        *,
        actions_for_session: list[Any],
        processed_utterance_counter: int,
    ) -> None:
        """Log the results for the trajectory."""
        (
            goal_completion_status,
            subgoal_completion_status,
        ) = self._inference_controller.get_goal_completion_status()

        self._evaluation_metrics.update(
            mission_id=trajectory.mission_id or trajectory.session_id,
            mission_group=trajectory.mission_group,
            is_mission_completed=goal_completion_status,
            subgoal_completion_status=subgoal_completion_status,
            predicted_actions=actions_for_session,
            last_game_state=self._inference_controller.get_latest_game_state(),
            remaining_utterances=trajectory.utterances[processed_utterance_counter:],
        )

        self._wandb_callback.finish_trajectory(
            trajectory,
            evaluation_metrics=self._evaluation_metrics,
            is_success=goal_completion_status,
            subgoal_completion_status=subgoal_completion_status,
        )
