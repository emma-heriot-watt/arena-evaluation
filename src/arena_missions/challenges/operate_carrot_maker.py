from typing import get_args

from arena_missions.builders import ChallengeBuilder, ChallengeBuilderOutput, RequiredObjectBuilder
from arena_missions.constants.arena import ColorChangerObjectColor
from arena_missions.structures import (
    AndExpression,
    ContainsExpression,
    HighLevelKey,
    IsPickedUpExpression,
    IsToggledOnExpression,
    ObjectInstanceId,
    RequiredObject,
    StateCondition,
    StateExpression,
    TaskGoal,
)


def create_operate_carrot_maker_challenges(
    target_object: RequiredObject,
    with_color_variants: bool = False,
) -> None:
    """Register challeneges."""
    required_object_builder = RequiredObjectBuilder()

    # Make the target object unique
    target_object.add_state("Unique", "true")

    # Create the carrot maker
    carrot_maker = required_object_builder.carrot_maker()
    carrot_maker.add_state("Unique", "true")

    # Create the breakroom table
    breakroom_table = required_object_builder.breakroom_table()
    target_object.update_receptacle(breakroom_table.name)
    spawned_carrot = ObjectInstanceId.parse(f"{carrot_maker.object_id}_Spawned_Carrot_01_1")

    # Success conditions
    conditions = [
        # The target object is picked up
        StateCondition(
            stateName="OriginalPickedUp",
            context=target_object.name,
            expression=StateExpression.from_expression(
                AndExpression.from_expressions(
                    IsPickedUpExpression(target=target_object.name, value=True),
                )
            ),
        ),
        # The target object is placed on the carrot machine
        StateCondition(
            stateName="MachineContainsTarget",
            context=carrot_maker.name,
            expression=StateExpression.from_expression(
                AndExpression.from_expressions(
                    ContainsExpression(target=carrot_maker.name, contains=target_object.name)
                )
            ),
        ),
        # Ensure the machine is used on the target
        StateCondition(
            stateName="MachineUsedOnTarget",
            context=carrot_maker.name,
            expression=StateExpression.from_expression(
                AndExpression.from_expressions(
                    IsToggledOnExpression(target=carrot_maker.name, value=True),
                )
            ),
        ),
    ]

    # Create mission
    def create_mission() -> ChallengeBuilderOutput:
        return ChallengeBuilderOutput(
            start_room="Lab2",
            required_objects={
                carrot_maker.name: carrot_maker,
                target_object.name: target_object,
                breakroom_table.name: breakroom_table,
            },
            state_conditions=conditions,
            task_goals=[TaskGoal.from_state_condition(condition) for condition in conditions],
            plan=[
                "go to the carrot maker",
                f"put the {target_object.readable_name} on the carrot maker",
                "toggle the carrot maker",
            ],
            preparation_plan=[
                "go to the breakroom",
                f"pick up the {target_object.readable_name}",
                "go to the quantum lab",
            ],
        )

    # Register versions of the challenges
    high_level_key = HighLevelKey(
        action="interact",
        interaction_object=carrot_maker.object_id,
        target_object=target_object.object_id,
        converted_object=spawned_carrot.object_id,
    )

    ChallengeBuilder.register(high_level_key)(create_mission)
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
                interaction_object=carrot_maker.object_id,
                target_object=target_object.object_id,
                target_object_color=color,
                converted_object=spawned_carrot.object_id,
            )
            # Register the challenge builder with the modifications
            ChallengeBuilder.register_with_modifiers(high_level_key, colored_target_object_kwargs)(
                create_mission
            )


def register_carrot_maker_challenges() -> None:
    """Register challenges with the carrot maker."""
    target_object_iterator = [
        (ObjectInstanceId.parse("Apple_1"), True),
        (ObjectInstanceId.parse("Banana_01_1"), False),
        (ObjectInstanceId.parse("BananaBunch_01_1"), False),
        (ObjectInstanceId.parse("BreadLoaf_1"), False),
        (ObjectInstanceId.parse("BreadSlice_01_1"), False),
        (ObjectInstanceId.parse("Bowl_01_1"), True),
        (ObjectInstanceId.parse("Burger_04_1"), False),
        (ObjectInstanceId.parse("Cake_02_1"), True),
        (ObjectInstanceId.parse("CakeSlice_02_1"), False),
        (ObjectInstanceId.parse("CandyBar_01_1"), False),
        (ObjectInstanceId.parse("CanSodaNew_01_1"), False),
        (ObjectInstanceId.parse("CanSodaNew_Crushed_01_1"), False),
        (ObjectInstanceId.parse("CanSodaNew_Open_01_1"), False),
        (ObjectInstanceId.parse("CoffeeBeans_01_1"), False),
        (ObjectInstanceId.parse("CoffeeMug_Boss_1"), False),
        (ObjectInstanceId.parse("CoffeeMug_Yellow_1"), True),
        (ObjectInstanceId.parse("Donut_01_1"), True),
        (ObjectInstanceId.parse("FoodPlate_01_1"), True),
        (ObjectInstanceId.parse("Fork_01_1"), False),
        (ObjectInstanceId.parse("Jar_Jam_01_1"), False),
        (ObjectInstanceId.parse("Jar_PeanutButter_01_1"), False),
        (ObjectInstanceId.parse("Knife_01_1"), False),
        (ObjectInstanceId.parse("PaperCup_01_1"), False),
        (ObjectInstanceId.parse("PaperCup_Crushed_01_1"), False),
        (ObjectInstanceId.parse("PBJ_Sandwich_1"), False),
        (ObjectInstanceId.parse("PieFruitSlice_01_1"), False),
        (ObjectInstanceId.parse("PieFruit_01_1"), False),
        (ObjectInstanceId.parse("SandwichHalf_01_1"), False),
        (ObjectInstanceId.parse("Spoon_01_1"), False),
        (ObjectInstanceId.parse("Toast_01_1"), False),
        (ObjectInstanceId.parse("Toast_02_1"), False),
        (ObjectInstanceId.parse("Toast_03_1"), False),
        (ObjectInstanceId.parse("Toast_04_1"), False),
        (ObjectInstanceId.parse("Toast_04_Jam_1"), False),
        (ObjectInstanceId.parse("Toast_04_PBJ_1"), False),
    ]

    for target_object, with_color_variants in target_object_iterator:
        create_operate_carrot_maker_challenges(
            target_object=RequiredObject(
                name=target_object,
            ),
            with_color_variants=with_color_variants,
        )
