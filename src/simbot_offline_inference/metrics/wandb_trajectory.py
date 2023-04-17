from typing import Literal

import wandb

from arena_missions.structures import CDFScene, HighLevelKey


class WandBTrajectoryTracker:
    """Track trajectories with WandB."""

    def __init__(self, project: str, entity: str, group: str) -> None:
        self.project = project
        self.entity = entity
        self.group = group

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
                "high_level_key/interaction_object": high_level_key.interaction_object,
                "high_level_key/interaction_object_color": high_level_key.interaction_object_color,
                "high_level_key/converted_object": high_level_key.converted_object,
                "high_level_key/converted_object_color": high_level_key.converted_object_color,
                "high_level_key/from_receptacle": high_level_key.from_receptacle,
                "high_level_key/from_receptacle_color": high_level_key.from_receptacle_color,
                "high_level_key/from_receptacle_is_container": high_level_key.from_receptacle_is_container,
                "high_level_key/to_receptacle": high_level_key.to_receptacle,
                "high_level_key/to_receptacle_color": high_level_key.to_receptacle_color,
                "high_level_key/to_receptacle_is_container": high_level_key.to_receptacle_is_container,
            },
        )

    def finish_trajectory(
        self, *, is_success: bool, subgoal_completion_status: list[Literal[0, 1]]
    ) -> None:
        """Finish a trajectory."""
        try:
            subgoal_success_rate = sum(subgoal_completion_status) / len(subgoal_completion_status)
        except ZeroDivisionError:
            subgoal_success_rate = 0

        wandb.log({"is_success": int(is_success), "subgoal_success_rate": subgoal_success_rate})
        wandb.finish()