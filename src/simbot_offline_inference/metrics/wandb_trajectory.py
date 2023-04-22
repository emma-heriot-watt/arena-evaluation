from pathlib import Path
from typing import Literal, Optional

import wandb

from arena_missions.structures import CDFScene, HighLevelKey
from emma_experience_hub._version import __version__ as experience_hub_version  # noqa: WPS436


class WandBTrajectoryTracker:
    """Track trajectories with WandB."""

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

    def start_trajectory(
        self,
        session_id: str,
        preparation_session_id: str,
        high_level_key: HighLevelKey,
        cdf_scene: CDFScene,
    ) -> None:
        """Submit a generated trajectory to WandB."""
        wandb.init(
            name=session_id,
            entity=self.entity,
            project=self.project,
            group=self.group,
            config={
                "version/experience_hub": experience_hub_version,
                "session_id": session_id,
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
        wandb.save(str(self.mission_trajectory_dir.joinpath(f"{session_id}.json")))

        # Upload the trajectory results on run completion
        # According to wandb docs, this command is correct
        wandb.save(  # type: ignore[call-arg]
            str(self.mission_trajectory_outputs_dir.joinpath(f"{session_id}.json")), policy="end"
        )
        # Also upload the unity logs
        wandb.save(str(self._unity_logs), policy="end")  # type: ignore[call-arg]

    def finish_trajectory(
        self, *, is_success: bool, subgoal_completion_status: list[Literal[0, 1]]
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
