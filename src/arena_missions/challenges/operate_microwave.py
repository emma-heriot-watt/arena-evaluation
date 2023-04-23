from typing import get_args

from arena_missions.builders import ChallengeBuilder, ChallengeBuilderOutput, RequiredObjectBuilder
from arena_missions.constants.arena import ColorChangerObjectColor
from arena_missions.structures import (
    AndExpression,
    ContainsExpression,
    HighLevelKey,
    IsBrokenExpression,
    IsHotExpression,
    IsOpenExpression,
    IsPickedUpExpression,
    IsToggledOnExpression,
    ObjectId,
    ObjectInstanceId,
    RequiredObject,
    StateCondition,
    StateExpression,
    TaskGoal,
)


def create_heat_with_microwave_challenges(
    target_object: RequiredObject,
    converted_object: ObjectId,
    with_color_variants: bool = False,
) -> None:
    """Register challeneges."""
    required_object_builder = RequiredObjectBuilder()

    # Make the target object unique
    target_object.add_state("Unique", "true")

    # Create the microwave
    microwave = required_object_builder.microwave()
    microwave.add_state("Unique", "true")

    # Create the breakroom table
    breakroom_table = required_object_builder.breakroom_table()
    target_object.update_receptacle(breakroom_table.name)

    # Success conditions
    conditions = [
        # Pick up an object that is not hot
        StateCondition(
            stateName="OriginalPickedUp",
            context=target_object.name,
            expression=StateExpression.from_expression(
                AndExpression.from_expressions(
                    IsPickedUpExpression(target=target_object.name, value=True),
                    IsHotExpression(target=target_object.name, value=False),
                )
            ),
        ),
        # Ensure the machine is used on the target
        StateCondition(
            stateName="MachineUsedOnTarget",
            context=microwave.name,
            expression=StateExpression.from_expression(
                AndExpression.from_expressions(
                    IsToggledOnExpression(target=microwave.name, value=True),
                    ContainsExpression(target=microwave.name, contains=target_object.name),
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
                    IsHotExpression(target=target_object.name, value=True),
                )
            ),
        ),
    ]

    # Create mission
    def create_mission() -> ChallengeBuilderOutput:
        return ChallengeBuilderOutput(
            start_room="BreakRoom",
            required_objects={
                microwave.name: microwave,
                target_object.name: target_object,
                breakroom_table.name: breakroom_table,
            },
            state_conditions=conditions,
            task_goals=[TaskGoal.from_state_condition(condition) for condition in conditions],
            plan=[
                "go to the microwave",
                "open the microwave",
                f"put the {target_object.readable_name} in the microwave",
                "close the microwave",
                "turn on the microwave",
                "open the microwave",
                f"pick up the {converted_object.readable_name} from the microwave",
                "close the microwave",
            ],
            preparation_plan=[
                "go to the breakroom table",
                f"pick up the {target_object.readable_name}",
            ],
        )

    def create_mission_with_door_open() -> ChallengeBuilderOutput:
        builder_output = create_mission()
        # Open the microwave
        builder_output.required_objects[microwave.name].add_state("isOpen", "true")
        # Change the plans
        builder_output.plan = [
            "go to the microwave",
            f"put the {target_object.readable_name} in the microwave",
            "close the microwave",
            "turn on the microwave",
            "open the microwave",
            f"pick up the {converted_object.readable_name} from the microwave",
            "close the microwave",
        ]
        return builder_output

    # Register versions of the challenges without color variants
    high_level_key = HighLevelKey(
        action="interact",
        interaction_object=microwave.object_id,
        target_object=target_object.object_id,
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
                interaction_object=microwave.object_id,
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


def create_break_with_microwave_challenges(
    target_object: RequiredObject,
    converted_object: ObjectId,
    with_color_variants: bool = False,
) -> None:
    """Register challeneges."""
    required_object_builder = RequiredObjectBuilder()

    # Make the target object unique
    target_object.add_state("Unique", "true")

    # Create the microwave
    microwave = required_object_builder.microwave()
    microwave.add_state("Unique", "true")

    # Create the breakroom table
    breakroom_table = required_object_builder.breakroom_table()
    target_object.update_receptacle(breakroom_table.name)

    # Success conditions
    conditions = [
        # Pick up an object that is not hot
        StateCondition(
            stateName="OriginalPickedUp",
            context=target_object.name,
            expression=StateExpression.from_expression(
                AndExpression.from_expressions(
                    IsPickedUpExpression(target=target_object.name, value=True),
                    IsBrokenExpression(target=target_object.name, value=False),
                )
            ),
        ),
        # Ensure the machine is used on the target
        StateCondition(
            stateName="MachineUsedOnTarget",
            context=microwave.name,
            expression=StateExpression.from_expression(
                AndExpression.from_expressions(
                    IsToggledOnExpression(target=microwave.name, value=True),
                    ContainsExpression(target=microwave.name, contains=target_object.name),
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
                    IsBrokenExpression(target=target_object.name, value=True),
                )
            ),
        ),
    ]

    # Create mission
    def create_mission() -> ChallengeBuilderOutput:
        return ChallengeBuilderOutput(
            start_room="BreakRoom",
            required_objects={
                microwave.name: microwave,
                target_object.name: target_object,
                breakroom_table.name: breakroom_table,
            },
            state_conditions=conditions,
            task_goals=[TaskGoal.from_state_condition(condition) for condition in conditions],
            plan=[
                "go to the microwave",
                "open the microwave",
                f"put the {target_object.readable_name} in the microwave",
                "close the microwave",
                "turn on the microwave",
                "open the microwave",
                f"pick up the {converted_object.readable_name} from the microwave",
                "close the microwave",
            ],
            preparation_plan=[
                "go to the breakroom table",
                f"pick up the {target_object.readable_name}",
            ],
        )

    def create_mission_with_door_open() -> ChallengeBuilderOutput:
        builder_output = create_mission()
        # Open the microwave
        builder_output.required_objects[microwave.name].add_state("isOpen", "true")
        # Change the plans
        builder_output.plan = [
            "go to the microwave",
            f"put the {target_object.readable_name} in the microwave",
            "close the microwave",
            "turn on the microwave",
            "open the microwave",
            f"pick up the {converted_object.readable_name} from the microwave",
            "close the microwave",
        ]
        return builder_output

    # Register versions of the challenges without color variants
    high_level_key = HighLevelKey(
        action="interact",
        interaction_object=microwave.object_id,
        target_object=target_object.object_id,
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
                interaction_object=microwave.object_id,
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


def register_heat_things(enable_color_variants: bool = True) -> None:
    """Register challenges to heat different things."""
    heatable_target_object_iterator = [
        (ObjectInstanceId.parse("Apple_1"), True),
        (ObjectInstanceId.parse("AppleSlice_01_1"), False),
        (ObjectInstanceId.parse("Banana_01_1"), False),
        (ObjectInstanceId.parse("BananaBunch_01_1"), False),
        (ObjectInstanceId.parse("BreadLoaf_1"), False),
        (ObjectInstanceId.parse("BreadSlice_01_1"), False),
        (ObjectInstanceId.parse("Bowl_01_1"), True),
        (ObjectInstanceId.parse("Burger_04_1"), False),
        (ObjectInstanceId.parse("Cake_02_1"), True),
        (ObjectInstanceId.parse("CandyBar_01_1"), False),
        (ObjectInstanceId.parse("CanSodaNew_01_1"), False),
        (ObjectInstanceId.parse("Carrot_01_1"), True),
        (ObjectInstanceId.parse("CoffeeMug_Boss_1"), True),
        (ObjectInstanceId.parse("CoffeeMug_Yellow_1"), True),
        (ObjectInstanceId.parse("CoffeePot_01_1"), False),
        (ObjectInstanceId.parse("Donut_01_1"), True),
        (ObjectInstanceId.parse("FoodPlate_01_1"), True),
        (ObjectInstanceId.parse("Jar_Jam_01_1"), False),
        (ObjectInstanceId.parse("Jar_PeanutButter_01_1"), False),
        (ObjectInstanceId.parse("PBJ_Sandwich_1"), False),
        (ObjectInstanceId.parse("Pear_01_1"), True),
        (ObjectInstanceId.parse("PieFruitSlice_01_1"), False),
        (ObjectInstanceId.parse("PieFruit_01_1"), False),
        (ObjectInstanceId.parse("SandwichHalf_01_1"), False),
        (ObjectInstanceId.parse("Toast_01_1"), False),
        (ObjectInstanceId.parse("Toast_02_1"), False),
        (ObjectInstanceId.parse("Toast_03_1"), False),
        (ObjectInstanceId.parse("Toast_04_1"), False),
        (ObjectInstanceId.parse("Toast_04_Jam_1"), False),
        (ObjectInstanceId.parse("Toast_04_PBJ_1"), False),
    ]

    for heatable_target_object, heatable_with_color_variants in heatable_target_object_iterator:
        create_heat_with_microwave_challenges(
            target_object=RequiredObject(
                name=heatable_target_object,
            ),
            converted_object=heatable_target_object.object_id,
            with_color_variants=heatable_with_color_variants,
        )

    breakable_target_object_iterator = [
        (ObjectInstanceId.parse("Floppy_AntiVirus_1"), False),
        (ObjectInstanceId.parse("Floppy_Virus_1"), False),
    ]
    for breakable_target_object, breakable_with_color_variants in breakable_target_object_iterator:
        create_break_with_microwave_challenges(
            target_object=RequiredObject(
                name=breakable_target_object,
            ),
            converted_object=breakable_target_object.object_id,
            with_color_variants=enable_color_variants & breakable_with_color_variants,
        )
