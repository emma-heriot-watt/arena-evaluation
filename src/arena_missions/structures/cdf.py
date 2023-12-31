from typing import Any, Literal, Optional

from pydantic import BaseModel, Field, validator

from arena_missions.constants.arena import OfficeLayout, OfficeRoom
from arena_missions.structures.required_object import RequiredObject
from arena_missions.structures.state_condition import StateCondition
from arena_missions.structures.task_goal import TaskGoal


CDF_GAME_INTERACTIONS: dict[str, Any] = {  # noqa: WPS407
    "camera_movements": {
        "task_beginning": [],
        "task_procedure": [],
        "task_ending": [],
        "object_conditions": [],
    },
    "game_messages": {
        "task_beginning": [],
        "task_procedure": [],
        "task_ending": [],
        "object_conditions": [],
    },
}


class CDFPortal(BaseModel):
    """Portal definition within the CDF."""

    name: Literal["past", "future"] = Field(..., alias="PortalName")
    status: bool = Field(default=False, alias="PortalStatus")


class CDFScene(BaseModel):
    """Scene within a CDF."""

    room_location: list[OfficeRoom] = Field(
        ..., alias="roomLocation", description="Start location of the robot"
    )
    required_objects: list[RequiredObject]
    layout_override: OfficeLayout = Field(
        ..., description="Override the layout", alias="layoutOverride"
    )

    floor_plan: str = Field(
        default="0", description="Controls RNG during scene setup. Set to -1 for random."
    )
    scene_id: str = Field(default="01 (Make_Cereal)")

    # Unused/Ignored fields
    simbot_init: list[Any] = Field(default_factory=list)
    sticky_notes: Optional[list[Any]] = Field(default_factory=list)
    blacklisted_layouts: Optional[list[OfficeLayout]] = None
    completely_random_visual: bool = Field(default=False, alias="completelyRandomVisual")

    @validator("floor_plan")
    @classmethod
    def check_floor_plan_is_numeric(cls, floor_plan: str) -> str:
        """Check that floor plan is a numeric string."""
        try:
            int(floor_plan)
        except ValueError as err:
            raise ValueError(f"Floor plan must be numeric string, got {floor_plan}") from err
        return floor_plan


class CDF(BaseModel):
    """CDF, used to generate scenes in the Arena."""

    scene: CDFScene

    task_goals: list[TaskGoal] = Field(..., min_items=1)
    state_conditions: list[StateCondition] = Field(default_factory=list, alias="stateconditions")

    goal_text: str = ""
    task_description: str = ""
    game_id: str = Field(default="3")
    experimental: str = Field(default="true")

    # Unused/Ignored fields
    game_interactions: dict[str, Any] = CDF_GAME_INTERACTIONS
    past_portals: list[CDFPortal] = Field(
        default=[CDFPortal(PortalName="past")], alias="pastPortals", max_items=1
    )
    future_portals: list[CDFPortal] = Field(
        default=[CDFPortal(PortalName="future")], alias="futurePortals", max_items=1
    )

    @validator("task_goals")
    @classmethod
    def update_goal_ids_in_task_goals(cls, task_goals: list[TaskGoal]) -> list[TaskGoal]:
        """Update goal IDs in task goals."""
        for idx, task_goal in enumerate(task_goals):
            task_goal.goal_id = idx
        return task_goals

    @validator("game_id")
    @classmethod
    def check_game_id_is_numeric(cls, game_id: str) -> str:
        """Check that game ID is a numeric string."""
        if not game_id.isdigit():
            raise ValueError(f"Game ID must be numeric string, got {game_id}")
        return game_id

    @validator("experimental")
    @classmethod
    def check_experimental_is_bool(cls, experimental: str) -> str:
        """Check that experimental is a boolean string."""
        if experimental not in {"true", "false"}:
            raise ValueError(f"Experimental must be boolean string, got {experimental}")
        return experimental

    @property
    def start_room(self) -> OfficeRoom:
        """Get the starting room."""
        return self.scene.room_location[0]
