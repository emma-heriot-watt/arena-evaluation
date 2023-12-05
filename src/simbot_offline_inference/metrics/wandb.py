from abc import ABC, abstractmethod
from copy import copy
from pathlib import Path
from typing import Literal, Optional

import torch
import wandb
from loguru import logger

from arena_missions.structures import CDF, MissionTrajectory
from emma_experience_hub._version import __version__ as experience_hub_version  # noqa: WPS436
from emma_experience_hub.constants import constants_absolute_path
from simbot_offline_inference._version import (  # noqa: WPS436
    __version__ as offline_inference_version,
)
from simbot_offline_inference.metrics.evaluation import EvaluationMetrics


SERVICE_REGISTRY_PATH = constants_absolute_path.joinpath("simbot", "registry.yaml")


class WandBCallback(ABC):
    """Base class for sending data to WandB."""

    def __init__(
        self,
        project: str,
        entity: str,
        group: Optional[str],
        mission_trajectory_dir: Path,
        mission_trajectory_outputs_dir: Path,
        unity_logs: Path,
    ) -> None:
        self.project = project
        self.entity = entity
        self.group = group
        self.mission_trajectory_dir = mission_trajectory_dir
        self.mission_trajectory_outputs_dir = mission_trajectory_outputs_dir

        self._unity_logs = unity_logs

        self.__post_init__()

    @abstractmethod
    def __post_init__(self) -> None:
        """Post init actions to perform, if needed.

        This is important to avoid changing the signature of the `__init__` method.
        """
        pass  # noqa: WPS420

    @abstractmethod
    def start_evaluation(self, *, resume: bool = False) -> None:
        """Start a new evaluation session."""
        raise NotImplementedError

    @abstractmethod
    def finish_evaluation(self) -> None:
        """Finish an evaluation session."""
        raise NotImplementedError

    @abstractmethod
    def start_trajectory(self, trajectory: MissionTrajectory, preparation_session_id: str) -> None:
        """Start running a new trajectory."""
        raise NotImplementedError

    @abstractmethod
    def finish_trajectory(
        self,
        trajectory: MissionTrajectory,
        *,
        evaluation_metrics: EvaluationMetrics,
        is_success: bool,
        subgoal_completion_status: list[Literal[0, 1]],
    ) -> None:
        """Finish running a trajectory."""
        raise NotImplementedError


class WandBTrajectoryGenerationCallback(WandBCallback):
    """Track each trajectory as a new run in WandB."""

    def __post_init__(self) -> None:
        """Post init actions to perform, if needed."""
        pass  # noqa: WPS420

    def start_evaluation(self, *, resume: bool = False) -> None:
        """No-op on start evaluation."""
        pass  # noqa: WPS420

    def finish_evaluation(self) -> None:
        """No-op on end evaluation."""
        pass  # noqa: WPS420

    def start_trajectory(self, trajectory: MissionTrajectory, preparation_session_id: str) -> None:
        """Start tracking a trajectory for generation."""
        cdf = trajectory.cdf
        high_level_key = trajectory.high_level_key

        if not high_level_key:
            raise AssertionError("High level key is not set.")

        if isinstance(cdf, CDF):
            cdf_scene = cdf.scene
        else:
            raise AssertionError("CDF is not set.")

        wandb.init(
            name=trajectory.session_id,
            entity=self.entity,
            project=self.project,
            group=self.group,
            config={
                "version/experience_hub": experience_hub_version,
                "version/offline_inference": offline_inference_version,
                "session_id": trajectory.session_id,
                "preparation_session_id": preparation_session_id,
                # CDF
                "cdf/floor_plan": cdf_scene.floor_plan,
                "cdf/scene_id": cdf_scene.scene_id,
                "cdf/room": cdf_scene.room_location[0],
                "cdf/layout": cdf_scene.layout_override,
                # High level key
                "high_level_key": str(high_level_key),
                "high_level_key/action": high_level_key.action,
                "high_level_key/target_object": high_level_key.target_object,
                "high_level_key/target_object_color": high_level_key.target_object_color,
                "high_level_key/target_object_is_ambiguous": high_level_key.target_object_is_ambiguous,
                "high_level_key/interaction_object": high_level_key.interaction_object,
                "high_level_key/interaction_object_color": high_level_key.interaction_object_color,
                "high_level_key/converted_object": high_level_key.converted_object,
                "high_level_key/converted_object_color": high_level_key.converted_object_color,
                "high_level_key/stacked_object": high_level_key.stacked_object,
                "high_level_key/stacked_object_color": high_level_key.stacked_object_color,
                "high_level_key/from_receptacle": high_level_key.from_receptacle,
                "high_level_key/from_receptacle_color": high_level_key.from_receptacle_color,
                "high_level_key/from_receptacle_is_container": high_level_key.from_receptacle_is_container,
                "high_level_key/to_receptacle": high_level_key.to_receptacle,
                "high_level_key/to_receptacle_color": high_level_key.to_receptacle_color,
                "high_level_key/to_receptacle_is_container": high_level_key.to_receptacle_is_container,
            },
        )

        # Upload the mission trajectory file
        wandb.save(str(self.mission_trajectory_dir.joinpath(f"{trajectory.session_id}.json")))

        # Upload the trajectory results on run completion
        # According to wandb docs, this command is correct
        wandb.save(
            str(self.mission_trajectory_outputs_dir.joinpath(f"{trajectory.session_id}.json")),
            policy="end",
        )
        # Also upload the unity logs
        wandb.save(str(self._unity_logs), policy="end")

    def finish_trajectory(
        self,
        trajectory: MissionTrajectory,
        *,
        evaluation_metrics: EvaluationMetrics,
        is_success: bool,
        subgoal_completion_status: list[Literal[0, 1]],
    ) -> None:
        """Finish a trajectory."""
        try:
            subgoal_success_rate = sum(subgoal_completion_status) / len(subgoal_completion_status)
        except ZeroDivisionError:
            subgoal_success_rate = 0

        wandb.log({"is_success": int(is_success), "subgoal_success_rate": subgoal_success_rate})

        # If subgoal success rate is 0, then it means the preparation also failed, therefore mark
        # the run as failed.
        wandb.finish(exit_code=1 if subgoal_success_rate == 0 else None)


class WandBEvaluationCallback(WandBCallback):
    """Track metrics across the entire validation set.

    According to wandb docs, the various save commands are correct.
    """

    def __post_init__(self) -> None:
        """Post init actions to perform."""
        # The `mission_success_table` tracks the success of each mission during the course of an
        # entire run, and also the session ID for that mission.`
        self._mission_success_table = wandb.Table(columns=["mission_id", "session_id", "success"])

    def start_evaluation(self, *, resume: bool = False) -> None:
        """Start running an evaluation."""
        if resume:
            logger.info("Resuming previous wandb run.")

        wandb.init(
            entity=self.entity,
            project=self.project,
            group=self.group,
            resume=resume,
            config={
                "version/experience_hub": experience_hub_version,
                "version/offline_inference": offline_inference_version,
            },
        )

        # Upload the trajectory results on run completion
        wandb.save(str(self.mission_trajectory_outputs_dir), policy="end")

        # Also upload the unity logs
        wandb.save(str(self._unity_logs))

    def finish_evaluation(self) -> None:
        """Finish running an evaluation."""
        wandb.finish()

    def start_trajectory(self, trajectory: MissionTrajectory, preparation_session_id: str) -> None:
        """No-op when starting a new trajectory."""
        pass  # noqa: WPS420

    def finish_trajectory(
        self,
        trajectory: MissionTrajectory,
        *,
        evaluation_metrics: EvaluationMetrics,
        is_success: bool,
        subgoal_completion_status: list[Literal[0, 1]],
    ) -> None:
        """Finish a trajectory."""
        step_idx = int(evaluation_metrics.games_played.compute().item())

        if trajectory.mission_id:
            # Update the table with the mission output
            self._mission_success_table.add_data(
                trajectory.mission_id, trajectory.session_id, 1 if is_success else 0
            )

            # Log the table to wandb
            wandb.log(
                {"mission_success_table": copy(self._mission_success_table)},
                commit=False,
                step=step_idx,
            )

        # If we have mission groups, log them
        if evaluation_metrics.per_mission_group_success_rate:
            wandb.log(
                {
                    f"success_rate/{mission_group}": torch.nan_to_num(success_rate.compute())
                    for mission_group, success_rate in evaluation_metrics.per_mission_group_success_rate.items()
                },
                commit=False,
                step=step_idx,
            )

        wandb.log(
            {
                "success_rate": evaluation_metrics.success_rate.compute(),
                "subgoal_success_rate": evaluation_metrics.subgoal_completion_rate.compute(),
            },
            commit=True,
            step=step_idx,
        )

        # Save a checkpoint of the evaluation metrics
        evaluation_metrics.save_checkpoint()
