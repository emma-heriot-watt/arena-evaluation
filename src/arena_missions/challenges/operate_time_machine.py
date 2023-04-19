from typing import get_args

from arena_missions.builders import ChallengeBuilder, ChallengeBuilderOutput, RequiredObjectBuilder
from arena_missions.constants.arena import ColorChangerObjectColor
from arena_missions.structures import (
    AndExpression,
    ContainsExpression,
    Expression,
    HighLevelKey,
    IsBrokenExpression,
    IsOpenExpression,
    IsPickedUpExpression,
    IsToggledOnExpression,
    ObjectId,
    ObjectInstanceId,
    RequiredObject,
    RequiredObjectState,
    StateCondition,
    StateExpression,
    TaskGoal,
)


def create_operate_time_machine_challenges(
    target_object: RequiredObject,
    converted_object: ObjectId,
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
                    IsOpenExpression(target=target_object.name, value=False),
                    IsPickedUpExpression(target=target_object.name, value=True),
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
            preparation_plan=["go to the breakroom table", f"pick up the {target_object.name}"],
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
        converted_object=converted_object,
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
                converted_object=converted_object,
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
            converted_object=object_instance_id.object_id,
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

    for converted_object_instance_id in converted_object_instance_ids:
        converted_object = converted_object_instance_id.object_id
        create_operate_time_machine_challenges(
            target_object=RequiredObject(
                name=ObjectInstanceId.parse("Carrot_01_1"), yesterdayState=converted_object
            ),
            converted_object=converted_object,
            additional_conditions_for_converted_object=[],
        )
