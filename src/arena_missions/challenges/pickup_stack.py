from typing import Any, Optional, get_args

from arena_missions.builders import ChallengeBuilder, ChallengeBuilderOutput, RequiredObjectBuilder
from arena_missions.constants.arena import ColorChangerObjectColor, ObjectColor
from arena_missions.structures import (
    HighLevelKey,
    IsPickedUpExpression,
    ObjectInstanceId,
    RequiredObject,
    StateCondition,
    StateExpression,
    TaskGoal,
)
from arena_missions.structures.object_id import ObjectId


def get_color_from_id(object_id: ObjectId) -> Optional[ObjectColor]:
    """Extracts the color from the object id."""
    if "green" in object_id.lower():
        return "Green"

    if "blue" in object_id.lower():
        return "Blue"

    if "red" in object_id.lower():
        return "Red"

    return None


def create_plate_stack_challenge(
    target_object_instance_id: ObjectInstanceId,
    receptacle: RequiredObject,
    *,
    with_stacked_object_color_variants: bool = False,
) -> None:
    """Generate challenes to pick up objects from containers."""
    # Create the target object
    target_object = RequiredObject(name=target_object_instance_id)
    target_object.add_state("Unique", "true")

    # Create the plate
    plate = RequiredObject(name=ObjectInstanceId.parse("FoodPlate_01_1"))
    plate.add_state("Unique", "true")
    plate.add_state("isDirty", "false")

    # Put it in the container
    plate.update_receptacle(receptacle.name)
    target_object.update_receptacle(plate.name)

    conditions = [
        # Ensure we pick up the plate
        StateCondition(
            stateName="PickedUpPlate",
            context=plate.name,
            expression=StateExpression.from_expression(
                IsPickedUpExpression(target=plate.name, value=True),
            ),
        ),
    ]

    goals = [TaskGoal.from_state_condition(condition) for condition in conditions]

    def create_mission() -> ChallengeBuilderOutput:
        """Create the mission."""
        if not receptacle.room:
            raise ValueError(f"Receptacle {receptacle.name} must have a room set")

        return ChallengeBuilderOutput(
            start_room=receptacle.room,
            required_objects={
                receptacle.name: receptacle,
                target_object.name: target_object,
                plate.name: plate,
            },
            task_goals=goals,
            state_conditions=conditions,
            plan=[
                f"go to the {receptacle.readable_name}",
                "pick up the plate",
            ],
        )

    plate_colors = [None, *get_args(ColorChangerObjectColor)]

    for plate_color in plate_colors:
        colored_target_object_kwargs: dict[str, Any] = {"required_objects": {}}

        if plate_color is not None:
            colored_target_object_kwargs["required_objects"].update(
                {plate.name: {"colors": [plate_color]}}
            )
        high_level_key = HighLevelKey(
            action="pickup",
            target_object=plate.object_id,
            target_object_color=plate_color,
            stacked_object=target_object.object_id,
            from_receptacle=receptacle.object_id,
            from_receptacle_color=get_color_from_id(receptacle.object_id),
            from_receptacle_is_container=False,
        )
        # Register the challenge builder with the modifications
        ChallengeBuilder.register_with_modifiers(high_level_key, colored_target_object_kwargs)(
            create_mission
        )

        if with_stacked_object_color_variants:
            for target_color in get_args(ColorChangerObjectColor):
                colored_target_object_kwargs["required_objects"].update(
                    {target_object.name: {"colors": [target_color]}}
                )
                high_level_key = HighLevelKey(
                    action="pickup",
                    target_object=plate.object_id,
                    target_object_color=plate_color,
                    stacked_object=target_object.object_id,
                    stacked_object_color=target_color,
                    from_receptacle=receptacle.object_id,
                    from_receptacle_color=get_color_from_id(receptacle.object_id),
                    from_receptacle_is_container=False,
                )
                # Register the challenge builder with the modifications
                ChallengeBuilder.register_with_modifiers(
                    high_level_key, colored_target_object_kwargs
                )(create_mission)


def register_plate_stack_challenges() -> None:
    """Register challenges to pick up and place objects in the fridge."""
    required_objects_builder = RequiredObjectBuilder()

    receptacles = [
        required_objects_builder.breakroom_table(),
        required_objects_builder.breakroom_countertop(),
        *required_objects_builder.main_office_desks(),
    ]

    target_object_iterator = [
        (ObjectInstanceId.parse("Apple_1"), True),
        (ObjectInstanceId.parse("AppleSlice_01_1"), False),
        (ObjectInstanceId.parse("Banana_01_1"), False),
        (ObjectInstanceId.parse("BananaBunch_01_1"), False),
        (ObjectInstanceId.parse("BreadLoaf_1"), False),
        (ObjectInstanceId.parse("BreadSlice_01_1"), False),
        (ObjectInstanceId.parse("Burger_04_1"), False),
        (ObjectInstanceId.parse("Cake_02_1"), True),
        (ObjectInstanceId.parse("CakeSlice_02_1"), False),
        (ObjectInstanceId.parse("CandyBar_01_1"), False),
        (ObjectInstanceId.parse("Carrot_01_1"), True),
        (ObjectInstanceId.parse("Donut_01_1"), True),
        (ObjectInstanceId.parse("Fork_01_1"), False),
        (ObjectInstanceId.parse("Knife_01_1"), False),
        (ObjectInstanceId.parse("PBJ_Sandwich_1"), False),
        (ObjectInstanceId.parse("Pear_01_1"), True),
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
        for receptacle in receptacles:
            create_plate_stack_challenge(
                target_object, receptacle, with_stacked_object_color_variants=with_color_variants
            )
