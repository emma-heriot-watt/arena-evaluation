from abc import ABC, abstractmethod
from pathlib import Path
from typing import Literal, Optional

import wandb
import yaml

from arena_missions.structures import CDF, MissionTrajectory
from emma_experience_hub._version import __version__ as experience_hub_version  # noqa: WPS436
from emma_experience_hub.constants import constants_absolute_path
from emma_experience_hub.datamodels.registry import ServiceRegistry
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

    def extract_service_versions_from_registry(self) -> dict[str, str]:
        """Get service and model versions from the service registry."""
        service_registry = ServiceRegistry.parse_obj(
            yaml.safe_load(SERVICE_REGISTRY_PATH.read_bytes())
        )

        output_dict = {}

        for service in service_registry.services:
            output_dict[f"version/{service.name}"] = service.image_version
            output_dict[f"model/{service.name}"] = service.model_url

        return output_dict


class WandBTrajectoryGenerationCallback(WandBCallback):
    """Track each trajectory as a new run in WandB."""

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
                **self.extract_service_versions_from_registry(),
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
        wandb.save(  # type: ignore[call-arg]
            str(self.mission_trajectory_outputs_dir.joinpath(f"{trajectory.session_id}.json")),
            policy="end",
        )
        # Also upload the unity logs
        wandb.save(str(self._unity_logs), policy="end")  # type: ignore[call-arg]

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

    def start_evaluation(self, *, resume: bool = False) -> None:
        """Start running an evaluation."""
        wandb.init(
            entity=self.entity,
            project=self.project,
            group=self.group,
            resume=resume,
            config={
                "num_games": 0,
                "version/experience_hub": experience_hub_version,
                **self.extract_service_versions_from_registry(),
            },
        )

        # Upload the mission trajectory file
        wandb.save(  # type: ignore[call-arg]
            glob_str="**/*.json", base_path=str(self.mission_trajectory_dir)
        )

        # Upload the trajectory results on run completion
        wandb.save(  # type: ignore[call-arg]
            glob_str="**/*.json", base_path=str(self.mission_trajectory_outputs_dir), policy="end"
        )

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
        # If we have mission groups, log them
        if evaluation_metrics.per_mission_group_success_rate:
            wandb.log(
                {
                    mission_group: success_rate.compute()
                    for mission_group, success_rate in evaluation_metrics.per_mission_group_success_rate.items()
                },
                commit=False,
            )

        wandb.log(
            {
                "success_rate": evaluation_metrics.success_rate.compute(),
                "subgoal_success_rate": evaluation_metrics.subgoal_completion_rate.compute(),
            },
            commit=True,
        )

        # Update the number of games in the run config
        try:
            wandb.config["num_games"] += 1
        except KeyError:
            wandb.config["num_games"] = 1

        # Try to add mission group information, if exists
        if trajectory.mission_group:
            try:
                wandb.config[f"count_per_mission_group/{trajectory.mission_group}"] += 1
            except KeyError:
                wandb.config[f"count_per_mission_group/{trajectory.mission_group}"] = 1
