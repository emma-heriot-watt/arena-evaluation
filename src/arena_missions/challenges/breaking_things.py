import random
from typing import get_args

from arena_missions.builders import ChallengeBuilder, ChallengeBuilderOutput, RequiredObjectBuilder
from arena_missions.constants.arena import ColorChangerObjectColor
from arena_missions.structures import (
    AndExpression,
    ContainsExpression,
    HighLevelKey,
    IsBrokenExpression,
    IsPickedUpExpression,
    ObjectInstanceId,
    RequiredObject,
    StateCondition,
    StateExpression,
    TaskGoal,
)


def create_break_object_challenges(
    object_instance_id: ObjectInstanceId,
    receptacle: RequiredObject,
    breakroom_table: RequiredObject,
    *,
    with_color_variants: bool = False,
) -> None:
    """Register challenges."""
    required_object_builder = RequiredObjectBuilder()

    # Turn the fork lift on
    fork_lift = required_object_builder.fork_lift()
    # Turn the robotic arm on
    robotic_arm = required_object_builder.robotic_arm()

    # Make the target object unique
    target_object = RequiredObject(name=object_instance_id)
    target_object.add_state("Unique", "true")

    # Create the breakroom table
    target_object.update_receptacle(receptacle.name)

    # Ensure the hammer is on the table
    hammer = RequiredObject(name=ObjectInstanceId.parse("Hammer_1"))
    hammer.add_state("Unique", "true")
    hammer.update_receptacle(breakroom_table.name)

    # Success conditions
    conditions = [
        # Pick up the target object
        StateCondition(
            stateName="HammerPickedUp",
            context=hammer.name,
            expression=StateExpression.from_expression(
                AndExpression.from_expressions(
                    IsPickedUpExpression(target=hammer.name, value=True),
                    ContainsExpression(target=receptacle.name, contains=target_object.name),
                ),
            ),
        ),
        # Ensure the target object is broken
        StateCondition(
            stateName="TargetObjectBroken",
            context=target_object.name,
            expression=StateExpression.from_expression(
                IsBrokenExpression(target=target_object.name, value=True)
            ),
        ),
    ]

    goals = [TaskGoal.from_state_condition(condition) for condition in conditions]

    # Create mission
    def create_mission() -> ChallengeBuilderOutput:
        if not receptacle.room:
            raise ValueError(f"Receptacle {receptacle.name} must have a room set")

        return ChallengeBuilderOutput(
            start_room=receptacle.room,
            required_objects={
                breakroom_table.name: breakroom_table,
                receptacle.name: receptacle,
                target_object.name: target_object,
                hammer.name: hammer,
                robotic_arm.name: robotic_arm,
                fork_lift.name: fork_lift,
            },
            state_conditions=conditions,
            task_goals=goals,
            plan=[
                f"find the {target_object.readable_name}",
                f"break the {target_object.readable_name} with the hammer",
            ],
            preparation_plan=[
                "go to the breakroom",
                f"find the {hammer.readable_name}",
                f"pick up the {hammer.readable_name}",
            ],
        )

    # Register versions of the challenges without color variants
    high_level_key = HighLevelKey(
        action="break",
        target_object=target_object.object_id,
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
                action="break", target_object=target_object.object_id, target_object_color=color
            )
            # Register the challenge builder with the modifications
            ChallengeBuilder.register_with_modifiers(high_level_key, colored_target_object_kwargs)(
                create_mission
            )


def register_breaking_things_challenges(enable_color_variants: bool = True) -> None:
    """Register challenges to break things with the hammer."""
    required_object_builder = RequiredObjectBuilder()

    breakable_object_ids = [
        (ObjectInstanceId.parse("Bowl_01_1"), True),
        (ObjectInstanceId.parse("CoffeeMug_Boss_1"), True),
        (ObjectInstanceId.parse("CoffeeMug_Yellow_1"), True),
        (ObjectInstanceId.parse("Floppy_Virus_1"), False),
        (ObjectInstanceId.parse("FoodPlate_01_1"), True),
        (ObjectInstanceId.parse("Record_01_1"), False),
        (ObjectInstanceId.parse("Trophy01_1"), False),
    ]

    breakroom_table = required_object_builder.breakroom_table()

    receptacles = [
        required_object_builder.breakroom_countertop(),
        breakroom_table,
        *required_object_builder.main_office_desks(),
        required_object_builder.warehouse_cabinet(),
        required_object_builder.warehouse_metal_table(),
        required_object_builder.warehouse_wooden_table(),
        required_object_builder.reception_desk(),
        required_object_builder.manager_desk(),
    ]

    for target_object_id, with_color_variants in breakable_object_ids:
        for receptacle in receptacles:
            create_break_object_challenges(
                target_object_id,
                receptacle,
                breakroom_table,
                with_color_variants=enable_color_variants & with_color_variants,
            )


def create_break_object_on_desks_challenges(
    object_instance_id: ObjectInstanceId,
    desks: list[RequiredObject],
    breakroom_table: RequiredObject,
    *,
    with_color_variants: bool = False,
) -> None:
    """Register challenges."""
    target_desk = random.choice(desks)
    required_object_builder = RequiredObjectBuilder()

    # Turn the fork lift on
    fork_lift = required_object_builder.fork_lift()
    # Turn the robotic arm on
    robotic_arm = required_object_builder.robotic_arm()

    # Make the target object unique
    target_object = RequiredObject(name=object_instance_id)
    target_object.add_state("Unique", "true")

    target_object.update_receptacle(target_desk.name)

    # Ensure the hammer is on the table
    hammer = RequiredObject(name=ObjectInstanceId.parse("Hammer_1"))
    hammer.add_state("Unique", "true")
    hammer.update_receptacle(breakroom_table.name)

    # Success conditions
    conditions = [
        # Pick up the target object
        StateCondition(
            stateName="HammerPickedUp",
            context=hammer.name,
            expression=StateExpression.from_expression(
                AndExpression.from_expressions(
                    IsPickedUpExpression(target=hammer.name, value=True),
                    ContainsExpression(target=target_desk.name, contains=target_object.name),
                ),
            ),
        ),
        # Ensure the target object is broken
        StateCondition(
            stateName="TargetObjectBroken",
            context=target_object.name,
            expression=StateExpression.from_expression(
                IsBrokenExpression(target=target_object.name, value=True)
            ),
        ),
    ]

    goals = [TaskGoal.from_state_condition(condition) for condition in conditions]

    # Create mission
    def create_mission() -> ChallengeBuilderOutput:
        if not target_desk.room:
            raise ValueError(f"Target desk {target_desk.name} must have a room set")

        return ChallengeBuilderOutput(
            start_room=target_desk.room,
            required_objects={
                breakroom_table.name: breakroom_table,
                **{desk.name: desk for desk in desks},
                target_object.name: target_object,
                hammer.name: hammer,
                robotic_arm.name: robotic_arm,
                fork_lift.name: fork_lift,
            },
            state_conditions=conditions,
            task_goals=goals,
            plan=[
                f"find the {target_object.readable_name}",
                f"break the {target_object.readable_name} with the hammer",
            ],
            preparation_plan=[
                "go to the breakroom",
                f"find the {hammer.readable_name}",
                f"pick up the {hammer.readable_name}",
            ],
        )

    # Register versions of the challenges without color variants
    high_level_key = HighLevelKey(
        action="break",
        target_object=target_object.object_id,
        from_receptacle=breakroom_table.object_id,
        from_receptacle_is_container=False,
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
                action="break",
                target_object=target_object.object_id,
                target_object_color=color,
                from_receptacle=breakroom_table.object_id,
                from_receptacle_is_container=False,
            )
            # Register the challenge builder with the modifications
            ChallengeBuilder.register_with_modifiers(high_level_key, colored_target_object_kwargs)(
                create_mission
            )


def register_breaking_things_on_desks_challenges(enable_color_variants: bool = True) -> None:
    """Register challenges to break things with the hammer."""
    required_object_builder = RequiredObjectBuilder()

    breakable_object_ids = [
        (ObjectInstanceId.parse("Bowl_01_1"), True),
        (ObjectInstanceId.parse("CoffeeMug_Boss_1"), True),
        (ObjectInstanceId.parse("CoffeeMug_Yellow_1"), True),
        (ObjectInstanceId.parse("Floppy_Virus_1"), False),
        (ObjectInstanceId.parse("FoodPlate_01_1"), True),
        (ObjectInstanceId.parse("Record_01_1"), False),
        (ObjectInstanceId.parse("Trophy01_1"), False),
    ]

    breakroom_table = required_object_builder.breakroom_table()

    all_desks = [required_object_builder.lab1_desks(), required_object_builder.lab2_desks()]

    for target_object_id, with_color_variants in breakable_object_ids:
        for desks in all_desks:
            create_break_object_on_desks_challenges(
                target_object_id,
                desks,
                breakroom_table,
                with_color_variants=enable_color_variants & with_color_variants,
            )
