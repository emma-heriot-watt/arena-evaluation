from collections.abc import Iterator
from copy import deepcopy
from itertools import groupby
from typing import Any, Callable, Literal, Optional, Union, get_args

from deepmerge import always_merger
from pydantic import BaseModel

from arena_missions.builders.required_objects_builder import RequiredObjectBuilder
from arena_missions.constants.arena import ColorChangerObjectColor, OfficeLayout, OfficeRoom
from arena_missions.structures import (
    HighLevelKey,
    ObjectGoalState,
    ObjectInstanceId,
    RequiredObject,
    RequiredObjectState,
    TaskGoal,
)


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


ChallengeBuilderFunction = Callable[[], ChallengeBuilderOutput]


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
    def register_with_modifiers(
        cls,
        high_level_key: Union[str, HighLevelKey],
        modified_kwargs: dict[str, Any],
    ) -> Callable[[ChallengeBuilderFunction], ChallengeBuilderFunction]:
        """Register a challenge builder with modifiers."""

        def decorator(func: ChallengeBuilderFunction) -> ChallengeBuilderFunction:
            # Register the modified challenge builder
            ChallengeBuilder.register(high_level_key)(
                ChallengeBuilder.modify_challenge_builder_function_output(func, modified_kwargs)
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

    @staticmethod
    def modify_challenge_builder_function_output(  # noqa: WPS602
        function: ChallengeBuilderFunction, modified_kwargs: dict[str, Any]
    ) -> ChallengeBuilderFunction:
        """Modify the output of a challenge builder function."""

        def wrapper() -> ChallengeBuilderOutput:
            # Call the original function
            output = function().dict()
            output = deepcopy(output)
            # Modify the output
            always_merger.merge(output, modified_kwargs)
            # Return the modified output
            return ChallengeBuilderOutput.parse_obj(output)

        return wrapper


def operate_time_machine(
    target_object: RequiredObject,
    converted_object_readable_name: str,
    target_object_goal_states: list[ObjectGoalState],
    *,
    with_color_variants: bool = False,
) -> None:
    """Generate challenges to operate the time machine."""
    required_object_builder = RequiredObjectBuilder()

    # High level key template
    high_level_key_template = "#action=timemachine#target-object={target_object}{target_object_color}#converted-object={converted_object}"

    # Create time machine
    time_machine = required_object_builder.time_machine()
    time_machine.add_state("Unique", "true")

    def operate_time_machine_challenge_builder() -> ChallengeBuilderOutput:
        # Make sure the target object has been picked up and is unique
        target_object.add_state("isPickedUp", "true")
        target_object.add_state("Unique", "true")

        goals = [
            # Turn on the time machine with the bowl inside
            TaskGoal.from_object_goal_states(
                [
                    ObjectGoalState.from_parts(time_machine.name, "isToggledOn", "true"),
                    ObjectGoalState.from_parts(time_machine.name, "Contains", target_object.name),
                ],
                relation="and",
            ),
            # Pick up the new object and make sure the time machine is closed
            TaskGoal.from_object_goal_states(
                [
                    ObjectGoalState.from_parts(time_machine.name, "isOpen", "false"),
                    ObjectGoalState.from_parts(target_object.name, "isPickedUp", "true"),
                    # Also make sure the target color is not changed anymore
                    *target_object_goal_states,
                ],
                relation="and",
            ),
        ]

        plans = [
            [
                "go to the time machine",
                "open the time machine",
                f"put the {target_object.readable_name} in the time machine",
                "close the time machine",
                "turn on the time machine",
                "open the time machine",
                f"pick up the {converted_object_readable_name} from the time machine",
                "close the time machine",
            ]
        ]

        return ChallengeBuilderOutput(
            start_room="BreakRoom",
            required_objects={
                "timemachine": time_machine,
                target_object.readable_name: target_object,
            },
            task_goals=goals,
            plans=plans,
        )

    def operate_open_time_machine_challenge_builder() -> ChallengeBuilderOutput:
        """Create challenge builder to operate an open time machine."""
        # Use the other challenge builder to get the output
        builder_output = operate_time_machine_challenge_builder()
        builder_output = deepcopy(builder_output)

        # Open the time machine
        builder_output.required_objects["timemachine"].add_state("isOpen", "true")
        # Change the plans
        builder_output.plans = [
            [
                "go to the time machine",
                f"put the {target_object.readable_name} in the time machine",
                "close the time machine",
                "turn on the time machine",
                "open the time machine",
                f"pick up the {converted_object_readable_name} from the time machine",
                "close the time machine",
            ]
        ]
        return builder_output

    ChallengeBuilder.register(
        high_level_key_template.format(
            target_object=target_object.readable_name,
            target_object_color="",
            converted_object=converted_object_readable_name,
        )
    )(operate_time_machine_challenge_builder)
    ChallengeBuilder.register(
        high_level_key_template.format(
            target_object=target_object.readable_name,
            target_object_color="",
            converted_object=converted_object_readable_name,
        )
    )(operate_open_time_machine_challenge_builder)

    if with_color_variants:
        for color in get_args(ColorChangerObjectColor):
            high_level_key = high_level_key_template.format(
                target_object=target_object.readable_name,
                target_object_color=f"#target-object-color={color.lower()}",
                converted_object=converted_object_readable_name,
            )
            colored_target_object_kwargs = {
                "required_objects": {
                    target_object.readable_name: {
                        "colors": [color],
                    }
                },
            }

            # Register the challenge builder with the modifications
            ChallengeBuilder.register_with_modifiers(high_level_key, colored_target_object_kwargs)(
                operate_time_machine_challenge_builder
            )
            ChallengeBuilder.register_with_modifiers(high_level_key, colored_target_object_kwargs)(
                operate_open_time_machine_challenge_builder
            )


def pickup_object_from_breakroom_container(
    object_instance_id: ObjectInstanceId,
    container_object: RequiredObject,
    *,
    with_color_variants: bool = False,
) -> None:
    """Generate challenges to pick up objects from containers."""
    # High level key template
    high_level_key_template = "#action=pickup#target-object={object}{target_object_color}#from-receptacle={container}#from-receptacle-is-container"

    def wrapper() -> ChallengeBuilderOutput:
        # Create object
        target_object = RequiredObject(name=object_instance_id)
        target_object.add_state("Unique", "true")

        # Put the object in the container
        target_object.update_receptacle(container_object.name)

        goals = [
            # Pick up the object from an open container
            TaskGoal.from_object_goal_states(
                [
                    ObjectGoalState.from_parts(container_object.name, "isOpen", "true"),
                    ObjectGoalState.from_parts(target_object.name, "isPickedUp", "true"),
                ],
                relation="and",
            ),
            # Close the container
            TaskGoal.from_object_goal_states(
                [ObjectGoalState.from_parts(container_object.name, "isOpen", "false")],
                relation="and",
            ),
        ]

        return ChallengeBuilderOutput(
            start_room="BreakRoom",
            required_objects={
                container_object.name: container_object,
                object_instance_id: target_object,
            },
            task_goals=goals,
            plans=[
                [
                    f"go to the {container_object.readable_name}",
                    f"open the {container_object.readable_name}",
                    f"pick up the {object_instance_id.readable_name}",
                    f"close the {container_object.readable_name}",
                ]
            ],
        )

    def wrapper_open_container() -> ChallengeBuilderOutput:
        wrapper_output = wrapper()
        wrapper_output.required_objects[container_object.name].add_state("isOpen", "true")
        wrapper_output.plans = [
            [
                f"go to the {container_object.readable_name}",
                f"pick up the {object_instance_id.readable_name}",
                f"close the {container_object.readable_name}",
            ]
        ]
        return wrapper_output

    # Register the challenge normally
    ChallengeBuilder.register(
        high_level_key_template.format(
            object=object_instance_id.readable_name,
            target_object_color="",
            container=container_object.readable_name,
        )
    )(wrapper)
    # Register with an open container
    ChallengeBuilder.register(
        high_level_key_template.format(
            object=object_instance_id.readable_name,
            target_object_color="",
            container=container_object.readable_name,
        ),
    )(wrapper_open_container)

    if with_color_variants:
        # Register variants with a specific target-object color
        for color in get_args(ColorChangerObjectColor):
            # Create the high level key
            high_level_key = high_level_key_template.format(
                object=object_instance_id.readable_name,
                target_object_color=f"#target-object-color={color.lower()}",
                container=container_object.readable_name,
            )

            # How should the challenge builder output be modified?
            colored_target_object_kwargs = {
                "required_objects": {
                    object_instance_id: {
                        "colors": [color],
                    }
                },
            }

            # Register the challenge builder with the modifications
            ChallengeBuilder.register_with_modifiers(high_level_key, colored_target_object_kwargs)(
                wrapper
            )
            ChallengeBuilder.register_with_modifiers(high_level_key, colored_target_object_kwargs)(
                wrapper_open_container
            )


def place_object_in_breakroom_container(
    object_instance_id: ObjectInstanceId,
    container_object: RequiredObject,
    *,
    with_color_variants: bool = False,
) -> None:
    """Generate challenges to place objects in containers."""
    # High level key template
    high_level_key_template = "#action=place#target-object={object}{target_object_color}#to-receptacle={container}#to-receptacle-is-container"

    def wrapper() -> ChallengeBuilderOutput:
        # Create object
        target_object = RequiredObject(name=object_instance_id)
        target_object.add_state("Unique", "true")
        target_object.add_state("isPickedUp", "true")

        goals = [
            # Place the object in an open container
            TaskGoal.from_object_goal_states(
                [
                    ObjectGoalState.from_parts(container_object.name, "isOpen", "true"),
                    ObjectGoalState.from_parts(target_object.name, "isPickedUp", "false"),
                    ObjectGoalState.from_parts(
                        container_object.name, "Contains", target_object.name
                    ),
                ],
                relation="and",
            ),
            # Close the container with the object inside
            TaskGoal.from_object_goal_states(
                [
                    ObjectGoalState.from_parts(container_object.name, "isOpen", "false"),
                    ObjectGoalState.from_parts(
                        container_object.name, "Contains", target_object.name
                    ),
                ],
                relation="and",
            ),
        ]

        return ChallengeBuilderOutput(
            start_room="BreakRoom",
            required_objects={
                container_object.name: container_object,
                object_instance_id: target_object,
            },
            task_goals=goals,
            plans=[
                [
                    f"go to the {container_object.readable_name}",
                    f"open the {container_object.readable_name}",
                    f"put the {object_instance_id.readable_name} in the {container_object.readable_name}",
                    f"close the {container_object.readable_name}",
                ]
            ],
        )

    def wrapper_open_container() -> ChallengeBuilderOutput:
        wrapper_output = wrapper()
        wrapper_output.required_objects[container_object.name].add_state("isOpen", "true")
        wrapper_output.plans = [
            [
                f"go to the {container_object.readable_name}",
                f"place the {object_instance_id.readable_name} in the {container_object.readable_name}",
                f"close the {container_object.readable_name}",
            ]
        ]
        return wrapper_output

    # Register the challenge normally
    ChallengeBuilder.register(
        high_level_key_template.format(
            object=object_instance_id.readable_name,
            target_object_color="",
            container=container_object.readable_name,
        )
    )(wrapper)
    # Register with an open container
    ChallengeBuilder.register(
        high_level_key_template.format(
            object=object_instance_id.readable_name,
            target_object_color="",
            container=container_object.readable_name,
        ),
    )(wrapper_open_container)

    if with_color_variants:
        # Register variants with a specific target-object color
        for color in get_args(ColorChangerObjectColor):
            # Create the high level key
            high_level_key = high_level_key_template.format(
                object=object_instance_id.readable_name,
                target_object_color=f"#target-object-color={color.lower()}",
                container=container_object.readable_name,
            )

            # How should the challenge builder output be modified?
            colored_target_object_kwargs = {
                "required_objects": {
                    object_instance_id: {
                        "colors": [color],
                    }
                },
            }

            # Register the challenge builder with the modifications
            ChallengeBuilder.register_with_modifiers(high_level_key, colored_target_object_kwargs)(
                wrapper
            )
            ChallengeBuilder.register_with_modifiers(high_level_key, colored_target_object_kwargs)(
                wrapper_open_container
            )


def clean_dirty_plate(room: Literal["BreakRoom", "Warehouse"]) -> None:
    """Clean a dirty plate."""
    # High level key template
    high_level_key_template = "#action=clean#target-object={object}"

    plate = RequiredObject(name=ObjectInstanceId.parse("FoodPlate_01_1"))
    plate.add_state("Unique", "true")
    plate.add_state("isDirty", "true")
    plate.add_state("isPickedUp", "true")

    sink_template = RequiredObject(
        name=ObjectInstanceId.parse("KitchenCounterSink_01_1"), roomLocation=[room]
    )

    def toggle_sink_before_clean() -> ChallengeBuilderOutput:
        """Fill the sink before cleaning the plate."""
        sink = deepcopy(sink_template)
        sink.update_state("isToggledOn", "false")

        goals = [
            # Fill the sink
            TaskGoal.from_object_goal_states(
                [ObjectGoalState.from_parts(sink.name, "isToggledOn", "true")],
                relation="and",
            ),
            # Clean the plate
            TaskGoal.from_object_goal_states(
                [ObjectGoalState.from_parts(plate.name, "isDirty", "false")],
                relation="and",
            ),
            # Drain the sink
            TaskGoal.from_object_goal_states(
                [ObjectGoalState.from_parts(sink.name, "isToggledOn", "true")],
                relation="and",
            ),
        ]

        plans = [
            ["go to the sink", "toggle the sink", "clean the plate in the sink", "toggle the sink"]
        ]

        return ChallengeBuilderOutput(
            start_room=room,
            required_objects={sink.name: sink, plate.name: plate},
            task_goals=goals,
            plans=plans,
        )

    def sink_already_filled_before_clean() -> ChallengeBuilderOutput:
        """Do not fill the sink before cleaning since it's already filled."""
        sink = deepcopy(sink_template)
        sink.update_state("isToggledOn", "true")

        goals = [
            # Clean the plate
            TaskGoal.from_object_goal_states(
                [ObjectGoalState.from_parts(plate.name, "isDirty", "false")],
                relation="and",
            ),
            # Drain the sink
            TaskGoal.from_object_goal_states(
                [ObjectGoalState.from_parts(sink.name, "isToggledOn", "true")],
                relation="and",
            ),
        ]

        plans = [["go to the sink", "clean the plate in the sink", "toggle the sink"]]
        return ChallengeBuilderOutput(
            start_room=room,
            required_objects={sink.name: sink, plate.name: plate},
            task_goals=goals,
            plans=plans,
        )

    ChallengeBuilder.register(high_level_key_template.format(object=plate.readable_name))(
        toggle_sink_before_clean
    )
    ChallengeBuilder.register(high_level_key_template.format(object=plate.readable_name))(
        sink_already_filled_before_clean
    )

    for layout in get_args(OfficeLayout):
        ChallengeBuilder.register_with_modifiers(
            high_level_key_template.format(object=plate.readable_name),
            {"office_layout": layout},
        )(toggle_sink_before_clean)
        ChallengeBuilder.register_with_modifiers(
            high_level_key_template.format(object=plate.readable_name),
            {"office_layout": layout},
        )(sink_already_filled_before_clean)


def fill_object_in_sink(
    object_instance_id: ObjectInstanceId,
    room: Literal["BreakRoom", "Warehouse"],
    *,
    with_color_variants: bool = False,
) -> None:
    """Generate challenges to fill objects in sinks."""
    # High level key template
    high_level_key_template = "#action=fill#target-object={object}{target_object_color}"

    # Create object
    target_object = RequiredObject(name=object_instance_id)
    target_object.add_state("Unique", "true")
    target_object.add_state("isPickedUp", "true")

    sink = RequiredObject(
        name=ObjectInstanceId.parse("KitchenCounterSink_01_1"), roomLocation=[room]
    )

    def toggle_sink_before_fill() -> ChallengeBuilderOutput:
        goals = [
            # Fill the sink
            TaskGoal.from_object_goal_states(
                [ObjectGoalState.from_parts(sink.name, "isToggledOn", "true")],
                relation="and",
            ),
            # Fill the object
            TaskGoal.from_object_goal_states(
                [ObjectGoalState.from_parts(target_object.name, "isFilled", "Water")],
                relation="and",
            ),
            # Drain the sink
            TaskGoal.from_object_goal_states(
                [ObjectGoalState.from_parts(sink.name, "isToggledOn", "true")],
                relation="and",
            ),
        ]

        return ChallengeBuilderOutput(
            start_room=room,
            required_objects={
                sink.name: sink,
                object_instance_id: target_object,
            },
            task_goals=goals,
            plans=[
                [
                    "go to the sink",
                    "toggle the sink",
                    f"fill the {object_instance_id.readable_name} in the sink",
                    "toggle the sink",
                ]
            ],
        )

    def sink_already_filled_before_fill() -> ChallengeBuilderOutput:
        sink.add_state("isToggledOn", "true")
        goals = [
            # Fill the object
            TaskGoal.from_object_goal_states(
                [ObjectGoalState.from_parts(target_object.name, "isFilled", "Water")],
                relation="and",
            ),
            # Drain the sink
            TaskGoal.from_object_goal_states(
                [ObjectGoalState.from_parts(sink.name, "isToggledOn", "true")],
                relation="and",
            ),
        ]

        return ChallengeBuilderOutput(
            start_room=room,
            required_objects={
                sink.name: sink,
                object_instance_id: target_object,
            },
            task_goals=goals,
            plans=[
                [
                    "go to the sink",
                    f"fill the {object_instance_id.readable_name} in the sink",
                    "toggle the sink",
                ]
            ],
        )

    # Register the challenge normally
    ChallengeBuilder.register(
        high_level_key_template.format(
            object=object_instance_id.readable_name, target_object_color=""
        )
    )(toggle_sink_before_fill)
    # Register with an filled sink
    ChallengeBuilder.register(
        high_level_key_template.format(
            object=object_instance_id.readable_name, target_object_color=""
        )
    )(sink_already_filled_before_fill)
    if with_color_variants:
        # Register variants with a specific target-object color
        for color in get_args(ColorChangerObjectColor):
            # Create the high level key
            high_level_key = high_level_key_template.format(
                object=object_instance_id.readable_name,
                target_object_color=f"#target-object-color={color.lower()}",
            )

            # How should the challenge builder output be modified?
            colored_target_object_kwargs = {
                "required_objects": {
                    object_instance_id: {
                        "colors": [color],
                    }
                },
            }

            # Register the challenge builder with the modifications
            ChallengeBuilder.register_with_modifiers(high_level_key, colored_target_object_kwargs)(
                toggle_sink_before_fill
            )
            ChallengeBuilder.register_with_modifiers(high_level_key, colored_target_object_kwargs)(
                sink_already_filled_before_fill
            )


# Higher-order challenge builders
def register_fridge_interactions() -> None:
    """Register pickup object from fridge challenges."""
    required_objects_builder = RequiredObjectBuilder()
    container_object = required_objects_builder.fridge()

    object_iterator = [
        (ObjectInstanceId.parse("Apple_1"), True),
        (ObjectInstanceId.parse("Banana_01_1"), False),
        (ObjectInstanceId.parse("Cake_02_1"), True),
        (ObjectInstanceId.parse("Carrot_01_1"), True),
        (ObjectInstanceId.parse("CoffeeMug_Boss_1"), False),
        (ObjectInstanceId.parse("CoffeeMug_Yellow_1"), True),
        (ObjectInstanceId.parse("Donut_01_1"), True),
        (ObjectInstanceId.parse("MilkCarton_01_1"), False),
        (ObjectInstanceId.parse("CanSodaNew_01_1"), False),
    ]

    for object_instance_id, with_color_variants in object_iterator:
        pickup_object_from_breakroom_container(
            object_instance_id, container_object, with_color_variants=with_color_variants
        )
        place_object_in_breakroom_container(
            object_instance_id, container_object, with_color_variants=with_color_variants
        )


def register_freezer_interactions() -> None:
    """Register pickup object from freezer challenges."""
    required_objects_builder = RequiredObjectBuilder()
    container_object = required_objects_builder.freezer()

    object_iterator = [
        (ObjectInstanceId.parse("Apple_1"), True),
        (ObjectInstanceId.parse("Banana_01_1"), False),
        (ObjectInstanceId.parse("Cake_02_1"), True),
        (ObjectInstanceId.parse("Carrot_01_1"), True),
        (ObjectInstanceId.parse("CoffeeMug_Boss_1"), False),
        (ObjectInstanceId.parse("CoffeeMug_Yellow_1"), True),
        (ObjectInstanceId.parse("Donut_01_1"), True),
        (ObjectInstanceId.parse("CanSodaNew_01_1"), False),
    ]

    for object_instance_id, with_color_variants in object_iterator:
        pickup_object_from_breakroom_container(
            object_instance_id, container_object, with_color_variants=with_color_variants
        )
        place_object_in_breakroom_container(
            object_instance_id, container_object, with_color_variants=with_color_variants
        )


def register_time_machine_interactions() -> None:
    """Register challenges which operate the time machine."""
    object_iterator = [
        # Restore broken bowls
        (
            RequiredObject(
                name=ObjectInstanceId.parse("Bowl_01_1"),
                state=[RequiredObjectState.from_parts("isBroken", "true")],
            ),
            [ObjectGoalState.from_parts(ObjectInstanceId.parse("Bowl_01_1"), "isBroken", "false")],
            True,
        ),
        # Restore bowls of various colours
        (
            RequiredObject(
                name=ObjectInstanceId.parse("Bowl_01_1"),
                state=[RequiredObjectState.from_parts("isColorChanged", "true")],
            ),
            [
                ObjectGoalState.from_parts(
                    ObjectInstanceId.parse("Bowl_01_1"), "isColorChanged", "false"
                )
            ],
            True,
        ),
    ]

    for target_object, target_object_goal_states, with_color_variants in object_iterator:
        operate_time_machine(
            target_object,
            target_object.readable_name,
            target_object_goal_states,
            with_color_variants=with_color_variants,
        )


def register_fill_interactions() -> None:
    """Register challenges about filling an object in sink challenges."""
    object_iterator = [
        (ObjectInstanceId.parse("Bowl_01_1"), True),
        (ObjectInstanceId.parse("CoffeeMug_Boss_1"), True),
        (ObjectInstanceId.parse("CoffeeMug_Yellow_1"), False),
        (ObjectInstanceId.parse("CoffeePot_01_1"), False),
    ]
    for object_instance_id, with_color_variants in object_iterator:
        fill_object_in_sink(
            object_instance_id,
            room="BreakRoom",
            with_color_variants=with_color_variants,
        )
        fill_object_in_sink(
            object_instance_id,
            room="Warehouse",
            with_color_variants=with_color_variants,
        )


# Run the challenge builder builders
register_fridge_interactions()
register_freezer_interactions()
register_time_machine_interactions()

clean_dirty_plate("BreakRoom")
clean_dirty_plate("Warehouse")
register_fill_interactions()
