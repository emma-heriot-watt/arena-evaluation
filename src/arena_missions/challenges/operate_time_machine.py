from typing import get_args

from arena_missions.builders import ChallengeBuilder, ChallengeBuilderOutput, RequiredObjectBuilder
from arena_missions.constants.arena import ColorChangerObjectColor
from arena_missions.structures import (
    AndExpression,
    ContainsExpression,
    Expression,
    HighLevelKey,
    IsBrokenExpression,
    IsFullOfItemsExpression,
    IsOpenExpression,
    IsPickedUpExpression,
    IsToggledOnExpression,
    NotExpression,
    ObjectGoalState,
    ObjectInstanceId,
    RequiredObject,
    RequiredObjectState,
    StateCondition,
    StateExpression,
    TaskGoal,
)


def create_operate_time_machine_challenges(
    target_object: RequiredObject,
    converted_object: ObjectInstanceId,
    additional_conditions_for_converted_object: list[Expression],
    *,
    with_color_variants: bool = False,
) -> None:
    """Register challeneges."""
    required_object_builder = RequiredObjectBuilder()

    # Make the target object unique
    target_object.add_state("Unique", "true")

    # Create the time machine
    time_machine = required_object_builder.time_machine()
    time_machine.add_state("Unique", "true")

    # Create the breakroom table
    breakroom_table = required_object_builder.breakroom_table()
    target_object.update_receptacle(breakroom_table.name)

    # Success conditions
    conditions = [
        # [PREP] The target object is picked up
        StateCondition(
            stateName="OriginalPickedUp",
            context=target_object.name,
            expression=StateExpression.from_expression(
                IsPickedUpExpression(target=target_object.name, value=True),
            ),
        ),
        # Ensure the machine is used on the target
        StateCondition(
            stateName="MachineUsedOnTarget",
            context=time_machine.name,
            expression=StateExpression.from_expression(
                AndExpression.from_expressions(
                    IsToggledOnExpression(target=time_machine.name, value=True),
                    ContainsExpression(target=time_machine.name, contains=target_object.name),
                )
            ),
        ),
        # Pick up the object
        StateCondition(
            stateName="ConvertedPickedUp",
            context=target_object.name,
            expression=StateExpression.from_expression(
                AndExpression.from_expressions(
                    IsOpenExpression(target=time_machine.name, value=False),
                    IsPickedUpExpression(target=converted_object, value=True),
                    *additional_conditions_for_converted_object,
                )
            ),
        ),
    ]

    # Create mission
    def create_mission() -> ChallengeBuilderOutput:
        return ChallengeBuilderOutput(
            start_room="BreakRoom",
            required_objects={
                time_machine.name: time_machine,
                target_object.name: target_object,
                breakroom_table.name: breakroom_table,
            },
            state_conditions=conditions,
            task_goals=[TaskGoal.from_state_condition(condition) for condition in conditions],
            plan=[
                "go to the time machine",
                "open the time machine",
                f"put the {target_object.readable_name} in the time machine",
                "close the time machine",
                "turn on the time machine",
                "open the time machine",
                f"pick up the {converted_object.readable_name} from the time machine",
                "close the time machine",
            ],
            preparation_plan=["go to the breakroom", f"pick up the {target_object.name}"],
        )

    def create_mission_with_door_open() -> ChallengeBuilderOutput:
        builder_output = create_mission()
        # Open the time machine
        builder_output.required_objects[time_machine.name].add_state("isOpen", "true")
        # Change the plans
        builder_output.plan = [
            "go to the time machine",
            f"put the {target_object.readable_name} in the time machine",
            "close the time machine",
            "turn on the time machine",
            "open the time machine",
            f"pick up the {converted_object.readable_name} from the time machine",
            "close the time machine",
        ]
        return builder_output

    # Register versions of the challenges without color variants
    high_level_key = HighLevelKey(
        action="interact",
        interaction_object=time_machine.object_id,
        target_object=target_object.object_id,
        converted_object=converted_object.object_id,
    )

    ChallengeBuilder.register(high_level_key)(create_mission)
    ChallengeBuilder.register(high_level_key)(create_mission_with_door_open)

    # Register versions of the challenges with color variants
    if with_color_variants:
        for color in get_args(ColorChangerObjectColor):
            colored_target_object_kwargs = {
                "required_objects": {
                    target_object.name: {"colors": [color]},
                }
            }

            high_level_key = HighLevelKey(
                action="interact",
                interaction_object=time_machine.object_id,
                target_object=target_object.object_id,
                target_object_color=color,
                converted_object=converted_object.object_id,
            )
            # Register the challenge builder with the modifications
            ChallengeBuilder.register_with_modifiers(high_level_key, colored_target_object_kwargs)(
                create_mission
            )
            ChallengeBuilder.register_with_modifiers(high_level_key, colored_target_object_kwargs)(
                create_mission_with_door_open
            )


def create_operate_time_machine_with_carrot(
    converted_object: ObjectInstanceId,
    *,
    with_color_variants: bool = False,
) -> None:
    """Create challenges that convert carrots to objects."""
    required_object_builder = RequiredObjectBuilder()

    carrot_object = RequiredObject(
        name=ObjectInstanceId.parse("Carrot_01_1"),
        yesterdayState=converted_object.object_id,
    )
    # Make the target object unique
    carrot_object.add_state("Unique", "true")

    # Blacklist the converted object
    output_object = RequiredObject(name=converted_object)
    output_object.add_state("Blacklist", "true")

    # Create the time machine
    time_machine = required_object_builder.time_machine()
    time_machine.add_state("Unique", "true")

    # Create the breakroom table
    breakroom_table = required_object_builder.breakroom_table()
    carrot_object.update_receptacle(breakroom_table.name)

    # Success conditions
    conditions: list[StateCondition] = [
        # Pick up the carrot
        StateCondition(
            stateName="CarrotPickedUp",
            context=carrot_object.name,
            expression=StateExpression.from_expression(
                IsPickedUpExpression(target=carrot_object.name, value=True)
            ),
        ),
        # Ensure the machine is used on the target
        StateCondition(
            stateName="MachineUsedOnTarget",
            context=time_machine.name,
            expression=StateExpression.from_expression(
                AndExpression.from_expressions(
                    IsToggledOnExpression(target=time_machine.name, value=True),
                    ContainsExpression(target=time_machine.name, contains=carrot_object.name),
                )
            ),
        ),
        # Close the time machine after picking up the object
        StateCondition(
            stateName="TimeMachineClosed",
            context=time_machine.name,
            expression=StateExpression.from_expression(
                AndExpression.from_expressions(
                    IsOpenExpression(target=time_machine.name, value=False),
                    NotExpression(
                        expression=StateExpression.from_expression(
                            IsFullOfItemsExpression(target=time_machine.name, value=True)
                        )
                    ),
                )
            ),
        ),
    ]
    goals = [
        *[TaskGoal.from_state_condition(condition) for condition in conditions],
        # Separately, create the task goal that makes sure the output object is picked up after conversion
        TaskGoal.from_object_goal_states(
            [ObjectGoalState.from_parts(output_object.name.with_asterisk, "isPickedUp", "true")]
        ),
    ]

    # Create mission
    def create_mission() -> ChallengeBuilderOutput:
        return ChallengeBuilderOutput(
            start_room="BreakRoom",
            required_objects={
                time_machine.name: time_machine,
                carrot_object.name: carrot_object,
                breakroom_table.name: breakroom_table,
                output_object.name: output_object,
            },
            state_conditions=conditions,
            task_goals=goals,
            plan=[
                "go to the time machine",
                "open the time machine",
                f"put the {carrot_object.readable_name} in the time machine",
                "close the time machine",
                "turn on the time machine",
                "open the time machine",
                f"pick up the {converted_object.readable_name} from the time machine",
                "close the time machine",
            ],
            preparation_plan=["go to the breakroom", f"pick up the {carrot_object.readable_name}"],
        )

    def create_mission_with_door_open() -> ChallengeBuilderOutput:
        builder_output = create_mission()
        # Open the time machine
        builder_output.required_objects[time_machine.name].add_state("isOpen", "true")
        # Change the plans
        builder_output.plan = [
            "go to the time machine",
            f"put the {carrot_object.readable_name} in the time machine",
            "close the time machine",
            "turn on the time machine",
            "open the time machine",
            f"pick up the {converted_object.readable_name} from the time machine",
            "close the time machine",
        ]
        return builder_output

    # Register versions of the challenges without color variants
    high_level_key = HighLevelKey(
        action="interact",
        interaction_object=time_machine.object_id,
        target_object=carrot_object.object_id,
        converted_object=converted_object.object_id,
    )

    ChallengeBuilder.register(high_level_key)(create_mission)
    ChallengeBuilder.register(high_level_key)(create_mission_with_door_open)

    # Register versions of the challenges with color variants
    if with_color_variants:
        for color in get_args(ColorChangerObjectColor):
            colored_target_object_kwargs = {
                "required_objects": {
                    carrot_object.name: {"colors": [color]},
                }
            }

            high_level_key = HighLevelKey(
                action="interact",
                interaction_object=time_machine.object_id,
                target_object=carrot_object.object_id,
                target_object_color=color,
                converted_object=converted_object.object_id,
            )
            # Register the challenge builder with the modifications
            ChallengeBuilder.register_with_modifiers(high_level_key, colored_target_object_kwargs)(
                create_mission
            )
            ChallengeBuilder.register_with_modifiers(high_level_key, colored_target_object_kwargs)(
                create_mission_with_door_open
            )


def register_repair_broken_things() -> None:
    """Register challenges to repair broken things."""
    object_instance_ids = [
        ObjectInstanceId.parse("Bowl_01_1"),
        ObjectInstanceId.parse("FoodPlate_01_1"),
    ]

    for object_instance_id in object_instance_ids:
        create_operate_time_machine_challenges(
            target_object=RequiredObject(
                name=object_instance_id,
                state=[RequiredObjectState.from_parts("isBroken", "true")],
            ),
            converted_object=object_instance_id,
            additional_conditions_for_converted_object=[
                IsBrokenExpression(target=object_instance_id, value=False)
            ],
            with_color_variants=True,
        )


def register_repair_carrots() -> None:
    """Register challenges to repair carrots."""
    converted_object_instance_ids = [
        ObjectInstanceId.parse("Apple_1"),
        ObjectInstanceId.parse("Banana_01_1"),
        ObjectInstanceId.parse("BananaBunch_01_1"),
        ObjectInstanceId.parse("BreadLoaf_1"),
        ObjectInstanceId.parse("BreadSlice_01_1"),
        ObjectInstanceId.parse("Bowl_01_1"),
        ObjectInstanceId.parse("Burger_04_1"),
        ObjectInstanceId.parse("Cake_02_1"),
        ObjectInstanceId.parse("CakeSlice_02_1"),
        ObjectInstanceId.parse("CandyBar_01_1"),
        ObjectInstanceId.parse("CanSodaNew_01_1"),
        ObjectInstanceId.parse("CanSodaNew_Crushed_01_1"),
        ObjectInstanceId.parse("CanSodaNew_Open_01_1"),
        ObjectInstanceId.parse("CoffeeBeans_01_1"),
        ObjectInstanceId.parse("CoffeeMug_Boss_1"),
        ObjectInstanceId.parse("CoffeeMug_Yellow_1"),
        ObjectInstanceId.parse("Donut_01_1"),
        ObjectInstanceId.parse("FoodPlate_01_1"),
        ObjectInstanceId.parse("Fork_01_1"),
        ObjectInstanceId.parse("Jar_Jam_01_1"),
        ObjectInstanceId.parse("Jar_PeanutButter_01_1"),
        ObjectInstanceId.parse("Knife_01_1"),
        ObjectInstanceId.parse("PaperCup_01_1"),
        ObjectInstanceId.parse("PaperCup_Crushed_01_1"),
        ObjectInstanceId.parse("PBJ_Sandwich_1"),
        ObjectInstanceId.parse("PieFruitSlice_01_1"),
        ObjectInstanceId.parse("PieFruit_01_1"),
        ObjectInstanceId.parse("SandwichHalf_01_1"),
        ObjectInstanceId.parse("Spoon_01_1"),
        ObjectInstanceId.parse("Toast_01_1"),
        ObjectInstanceId.parse("Toast_02_1"),
        ObjectInstanceId.parse("Toast_03_1"),
        ObjectInstanceId.parse("Toast_04_1"),
        ObjectInstanceId.parse("Toast_04_Jam_1"),
        ObjectInstanceId.parse("Toast_04_PBJ_1"),
    ]

    for converted_object in converted_object_instance_ids:
        create_operate_time_machine_with_carrot(converted_object, with_color_variants=True)
