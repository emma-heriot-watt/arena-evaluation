from typing import Callable, Optional

from pydantic import BaseModel

from arena_missions.builders.required_objects_builder import RequiredObjectBuilder
from arena_missions.constants.arena import OfficeLayout, OfficeRoom
from arena_missions.structures import HighLevelKey, RequiredObject, TaskGoal
from arena_missions.structures.task_goal import ObjectGoalState


class ChallengeBuilderOutput(BaseModel):
    """Output of a challenge builder function."""

    start_room: OfficeRoom
    required_objects: list[RequiredObject]
    task_goals: list[TaskGoal]

    # If you want to override the office layout, set this.
    office_layout: Optional[OfficeLayout] = None

    # Whether or not to include all the default objects like open doors, etc.
    # If you don't care, just ignore it.
    include_all_default_objects: Optional[bool] = None


ChallengeBuilder = Callable[[RequiredObjectBuilder], ChallengeBuilderOutput]

CHALLENGE_REGISTRY: dict[HighLevelKey, ChallengeBuilder] = {}  # noqa: WPS407


def register_challenge_builder(
    high_level_key: str,
) -> Callable[[ChallengeBuilder], ChallengeBuilder]:
    """Decorator to register a challenge callable."""
    parsed_key = HighLevelKey.from_string(high_level_key)

    def decorator(func: ChallengeBuilder) -> ChallengeBuilder:
        CHALLENGE_REGISTRY[parsed_key] = func
        return func

    return decorator


@register_challenge_builder("#action=timemachine#target-object=bowl#converted-object=bowl")
@register_challenge_builder("#action=timemachine#target-object=broken-bowl#converted-object=bowl")
def operate_timemachine_with_broken_bowl(
    required_object_builder: RequiredObjectBuilder,
) -> ChallengeBuilderOutput:
    """Operate the time machine with a broken bowl."""
    # Create time machine
    time_machine = required_object_builder.time_machine()
    time_machine.add_state("Unique", "true")

    # Create brokwn bowl
    broken_bowl = RequiredObject.from_string("Bowl_01_1")
    broken_bowl.add_state("isBroken", "true")
    broken_bowl.add_state("Unique", "true")
    broken_bowl.add_state("isPickedUp", "true")

    goals = [
        # Turn on the time machine with the bowl inside
        TaskGoal.from_object_goal_states(
            [
                ObjectGoalState.from_parts(time_machine.name, "isToggledOn", "true"),
                ObjectGoalState.from_parts(time_machine.name, "Contains", broken_bowl.name),
            ],
            relation="and",
        ),
        # Pick up the non-broken bowl
        TaskGoal.from_object_goal_states(
            [
                ObjectGoalState.from_parts(broken_bowl.name, "isBroken", "false"),
                ObjectGoalState.from_parts(broken_bowl.name, "isPickedUp", "true"),
            ],
            relation="and",
        ),
    ]

    return ChallengeBuilderOutput(
        start_room="BreakRoom", required_objects=[time_machine, broken_bowl], task_goals=goals
    )
