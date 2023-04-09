from collections.abc import Iterator
from itertools import groupby
from typing import Callable, Optional, Union

from pydantic import BaseModel

from arena_missions.builders.required_objects_builder import RequiredObjectBuilder
from arena_missions.constants.arena import OfficeLayout, OfficeRoom
from arena_missions.structures import HighLevelKey, RequiredObject, TaskGoal
from arena_missions.structures.task_goal import ObjectGoalState


class ChallengeBuilderOutput(BaseModel):
    """Output of a challenge builder function."""

    start_room: OfficeRoom
    required_objects: dict[str, RequiredObject]
    task_goals: list[TaskGoal]
    plans: list[list[str]]

    # If you want to override the office layout, set this.
    office_layout: Optional[OfficeLayout] = None

    # Whether or not to include all the default objects like open doors, etc.
    # If you don't care, just ignore it.
    include_all_default_objects: Optional[bool] = None

    @property
    def required_objects_list(self) -> list[RequiredObject]:
        """Return a list of lists of required objects."""
        return list(self.required_objects.values())


ChallengeBuilderFunction = Callable[[RequiredObjectBuilder], ChallengeBuilderOutput]


class ChallengeBuilder:
    """Registrable-style class that registers challenge builders to easily generate them."""

    _registry: list[tuple[HighLevelKey, ChallengeBuilderFunction]] = []

    def __iter__(self) -> Iterator[tuple[HighLevelKey, ChallengeBuilderFunction]]:
        """Iterate over the registry."""
        yield from self._registry

    @classmethod
    def register(
        cls, high_level_key: Union[str, HighLevelKey]
    ) -> Callable[[ChallengeBuilderFunction], ChallengeBuilderFunction]:
        """Register a challenge builder."""
        # mypy errors if we don't reassign the parsed high-level key to a new variable.
        # Either that is a bug, or it knows something we don't.
        parsed_high_level_key = (
            HighLevelKey.from_string(high_level_key)
            if isinstance(high_level_key, str)
            else high_level_key
        )

        def decorator(func: ChallengeBuilderFunction) -> ChallengeBuilderFunction:
            # Registry count before registering
            registry_count = len(ChallengeBuilder._registry)  # noqa: WPS437

            # Register the challenge builder
            ChallengeBuilder._registry.append((parsed_high_level_key, func))  # noqa: WPS437

            # Get the count after removing duplicates
            registry_count_after_duplicates_removed = len(
                set(ChallengeBuilder._registry)  # noqa: WPS437
            )

            # If the count is the same, then we didn't add a new challenge builder
            if registry_count == registry_count_after_duplicates_removed:
                raise ValueError(
                    f"Challenge builder already registered for: ({parsed_high_level_key}, {func})."
                )

            return func

        return decorator

    @classmethod
    def count_available_functions_per_key(cls) -> dict[HighLevelKey, int]:
        """List all keys and how many functions connect with them."""
        key_counts: dict[HighLevelKey, int] = {}

        # Sort the registry by the high-level key
        sorted_registry = sorted(cls._registry, key=lambda x: x[0].key)

        for k, g in groupby(sorted_registry, key=lambda x: x[0]):
            key_counts[k] = len(list(g))

        return key_counts

    @classmethod
    def list_available(cls) -> list[HighLevelKey]:
        """List all available high-level keys."""
        return list({key for key, _ in cls._registry})


@ChallengeBuilder.register("#action=timemachine#target-object=bowl#converted-object=bowl")
@ChallengeBuilder.register("#action=timemachine#target-object=broken-bowl#converted-object=bowl")
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
        start_room="BreakRoom",
        required_objects={"timemachine": time_machine, "brokenbowl": broken_bowl},
        task_goals=goals,
        plans=[
            [
                "go to the time machine",
                "open the time machine",
                "put the bowl in the time machine",
                "close the time machine",
                "turn on the time machine",
                "open the time machine",
                "pick up the bowl from the time machine",
                "close the time machine",
            ]
        ],
    )


@ChallengeBuilder.register("#action=timemachine#target-object=bowl#converted-object=bowl")
def operate_open_timemachine_with_broken_bowl(
    required_object_builder: RequiredObjectBuilder,
) -> ChallengeBuilderOutput:
    """Operate an open time machine with a broken bowl."""
    # Use the other challenge builder to get the output
    builder_output = operate_timemachine_with_broken_bowl(required_object_builder)

    # Open the time machine
    builder_output.required_objects["timemachine"].add_state("isOpen", "true")

    # Change the plans
    builder_output.plans = [
        [
            "go to the time machine",
            "put the bowl in the time machine",
            "close the time machine",
            "turn on the time machine",
            "open the time machine",
            "pick up the bowl from the time machine",
            "close the time machine",
        ]
    ]

    return builder_output
