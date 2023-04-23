from typing import Any, Optional, get_args

from arena_missions.builders import ChallengeBuilder, ChallengeBuilderOutput, RequiredObjectBuilder
from arena_missions.constants.arena import ColorChangerObjectColor, ObjectColor
from arena_missions.structures import (
    AndExpression,
    ContainsExpression,
    HighLevelKey,
    IsOpenExpression,
    IsPickedUpExpression,
    ObjectId,
    ObjectInstanceId,
    RequiredObject,
    StateCondition,
    StateExpression,
    TaskGoal,
)


def get_color_from_id(object_id: ObjectId) -> Optional[ObjectColor]:
    """Extracts the color from the object id."""
    if "green" in object_id.lower():
        return "Green"

    if "blue" in object_id.lower():
        return "Blue"

    if "red" in object_id.lower():
        return "Red"

    return None


def create_place_plate_stack_challenge(
    target_object_instance_id: ObjectInstanceId,
    container: RequiredObject,
    *,
    with_stacked_object_color_variants: bool = False,
) -> None:
    """Generate challenges to pick up objects from containers."""
    required_object_builder = RequiredObjectBuilder()
    # Create the target object
    target_object = RequiredObject(name=target_object_instance_id)
    target_object.add_state("Unique", "true")

    # Create the plate
    plate = RequiredObject(name=ObjectInstanceId.parse("FoodPlate_01_1"))
    plate.add_state("Unique", "true")
    plate.add_state("isDirty", "false")
    plate.add_state("isEmpty", "true")

    # Create the breakroom table
    breakroom_table = required_object_builder.breakroom_table()

    # Put the target object on the table
    target_object.update_receptacle(breakroom_table.name)

    # Put plate in the container
    plate.update_receptacle(container.name)

    conditions = [
        # [PREP] Ensure the item is picked up
        StateCondition(
            stateName="ObjectPickedUp",
            context=target_object.name,
            expression=StateExpression.from_expression(
                IsPickedUpExpression(target=target_object.name, value=True),
            ),
        ),
        # Place object on the plate which is in the container while its open
        StateCondition(
            stateName="PlacedOnPlateInContainer",
            context=target_object.name,
            expression=StateExpression.from_expression(
                AndExpression.from_expressions(
                    IsOpenExpression(target=container.name, value=True),
                    ContainsExpression(target=container.name, contains=plate.name),
                    ContainsExpression(target=plate.name, contains=target_object.name),
                    IsPickedUpExpression(target=target_object.name, value=False),
                )
            ),
        ),
    ]

    goals = [TaskGoal.from_state_condition(condition) for condition in conditions]

    def create_mission() -> ChallengeBuilderOutput:
        """Create the mission."""
        if not container.room:
            raise ValueError(f"Receptacle {container.name} must have a room set")

        return ChallengeBuilderOutput(
            start_room=container.room,
            required_objects={
                container.name: container,
                target_object.name: target_object,
                plate.name: plate,
            },
            task_goals=goals,
            state_conditions=conditions,
            plan=[
                f"go to the {container.readable_name}",
                f"open the {container.readable_name}",
                f"put the {target_object_instance_id.readable_name} on the plate",
                f"close the {container.readable_name}",
            ],
            preparation_plan=[
                "go to the breakroom",
                f"pick up the {target_object.readable_name}",
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
            action="place",
            target_object=plate.object_id,
            target_object_color=plate_color,
            stacked_object=target_object.object_id,
            from_receptacle=container.object_id,
            from_receptacle_color=get_color_from_id(container.object_id),
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
                    action="place",
                    target_object=plate.object_id,
                    target_object_color=plate_color,
                    stacked_object=target_object.object_id,
                    stacked_object_color=target_color,
                    from_receptacle=container.object_id,
                    from_receptacle_color=get_color_from_id(container.object_id),
                    from_receptacle_is_container=False,
                )
                # Register the challenge builder with the modifications
                ChallengeBuilder.register_with_modifiers(
                    high_level_key, colored_target_object_kwargs
                )(create_mission)


def create_place_plate_on_gravity_pad_challenge(
    target_object_instance_id: ObjectInstanceId,
    gravity_pad: RequiredObject,
    *,
    with_color_variants: bool = False,
) -> None:
    """Generate challenges to pick up objects from containers."""
    required_object_builder = RequiredObjectBuilder()
    # Create the target object
    target_object = RequiredObject(name=target_object_instance_id)
    target_object.add_state("Unique", "true")

    # Create the plate
    plate = RequiredObject(name=ObjectInstanceId.parse("FoodPlate_01_1"))
    plate.add_state("Unique", "true")
    plate.add_state("isDirty", "false")
    plate.add_state("isEmpty", "true")

    # Create the breakroom table
    breakroom_table = required_object_builder.breakroom_table()

    # Put the target object on the breakroom table
    target_object.update_receptacle(breakroom_table.name)

    # Put plate in the gravity pad
    plate.update_receptacle(gravity_pad.name)

    conditions = [
        # [PREP] Ensure the item is picked up
        StateCondition(
            stateName="ObjectPickedUp",
            context=target_object.name,
            expression=StateExpression.from_expression(
                IsPickedUpExpression(target=target_object.name, value=True),
            ),
        ),
        # Place object on the plate which is in the container while its open
        StateCondition(
            stateName="PlacedOnPlateInContainer",
            context=target_object.name,
            expression=StateExpression.from_expression(
                AndExpression.from_expressions(
                    ContainsExpression(target=gravity_pad.name, contains=plate.name),
                    ContainsExpression(target=plate.name, contains=target_object.name),
                    IsPickedUpExpression(target=target_object.name, value=False),
                )
            ),
        ),
    ]

    goals = [TaskGoal.from_state_condition(condition) for condition in conditions]

    def create_mission() -> ChallengeBuilderOutput:
        """Create the mission."""
        return ChallengeBuilderOutput(
            start_room="Lab2",
            required_objects={
                gravity_pad.name: gravity_pad,
                target_object.name: target_object,
                breakroom_table.name: breakroom_table,
                plate.name: plate,
            },
            task_goals=goals,
            state_conditions=conditions,
            plan=[
                f"go to the {gravity_pad.readable_name}",
                f"put the {target_object.readable_name} on the plate",
            ],
            preparation_plan=[
                "go to the breakroom",
                f"pick up the {target_object.readable_name}",
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
            action="place",
            target_object=plate.object_id,
            target_object_color=plate_color,
            stacked_object=target_object.object_id,
            from_receptacle=gravity_pad.object_id,
            from_receptacle_is_container=False,
        )
        # Register the challenge builder with the modifications
        ChallengeBuilder.register_with_modifiers(high_level_key, colored_target_object_kwargs)(
            create_mission
        )

        if with_color_variants:
            for target_color in get_args(ColorChangerObjectColor):
                colored_target_object_kwargs["required_objects"].update(
                    {target_object.name: {"colors": [target_color]}}
                )
                high_level_key = HighLevelKey(
                    action="place",
                    target_object=plate.object_id,
                    target_object_color=plate_color,
                    stacked_object=target_object.object_id,
                    stacked_object_color=target_color,
                    from_receptacle=gravity_pad.object_id,
                    from_receptacle_is_container=False,
                )
                # Register the challenge builder with the modifications
                ChallengeBuilder.register_with_modifiers(
                    high_level_key, colored_target_object_kwargs
                )(create_mission)


def register_place_plate_stack_challenges(enable_color_variants: bool = True) -> None:
    """Register challenges to pick up and place objects in the fridge/freezer."""
    required_objects_builder = RequiredObjectBuilder()

    containers = [required_objects_builder.fridge(), required_objects_builder.freezer()]

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
        for container in containers:
            create_place_plate_stack_challenge(
                target_object,
                container,
                with_stacked_object_color_variants=enable_color_variants & with_color_variants,
            )


def register_place_bowl_stack_from_gravity_pad(enable_color_variants: bool = True) -> None:
    """Register challenges to pick up and place objects in the fridge/freezer."""
    required_objects_builder = RequiredObjectBuilder()

    create_place_plate_on_gravity_pad_challenge(
        ObjectInstanceId.parse("Bowl_01_1"),
        required_objects_builder.gravity_pad(),
        with_color_variants=enable_color_variants,
    )
