from typing import get_args

from arena_missions.builders import ChallengeBuilder, ChallengeBuilderOutput, RequiredObjectBuilder
from arena_missions.constants.arena import ColorChangerObjectColor
from arena_missions.structures import (
    AndExpression,
    ContainsExpression,
    HighLevelKey,
    IsFullOfItemsExpression,
    IsOpenExpression,
    IsPickedUpExpression,
    NotExpression,
    ObjectGoalState,
    ObjectInstanceId,
    RequiredObject,
    StateCondition,
    StateExpression,
    TaskGoal,
)


def create_pick_up_from_container_challenge(
    target_object_instance_id: ObjectInstanceId,
    container: RequiredObject,
    *,
    with_color_variants: bool = False,
) -> None:
    """Generate challegnes to pick up objects from containers."""
    # Create the target object
    target_object = RequiredObject(name=target_object_instance_id)
    target_object.add_state("Unique", "true")

    # Put it in the container
    target_object.update_receptacle(container.name)

    conditions = [
        # Ensure the object is picked up from the container
        StateCondition(
            stateName="PickedUpFromContainer",
            context=target_object.name,
            expression=StateExpression.from_expression(
                AndExpression.from_expressions(
                    IsPickedUpExpression(target=target_object.name, value=True),
                    IsOpenExpression(target=container.name, value=True),
                )
            ),
        ),
        StateCondition(
            stateName="ClosedContainer",
            context=container.name,
            expression=StateExpression.from_expression(
                AndExpression.from_expressions(
                    IsOpenExpression(target=container.name, value=False),
                    NotExpression(
                        expression=StateExpression.from_expression(
                            ContainsExpression(target=container.name, contains=target_object.name)
                        )
                    ),
                )
            ),
        ),
    ]

    goals = [
        # Ensure the object starts within the container at the start of the mission
        TaskGoal.from_object_goal_states(
            [ObjectGoalState.from_parts(container.name, "Contains", target_object.name)]
        ),
        *[TaskGoal.from_state_condition(condition) for condition in conditions],
    ]

    def create_mission() -> ChallengeBuilderOutput:
        """Create the mission."""
        if not container.room:
            raise ValueError(f"Container {container.name} must have a room set")

        return ChallengeBuilderOutput(
            start_room=container.room,
            required_objects={
                container.name: container,
                target_object.name: target_object,
            },
            task_goals=goals,
            state_conditions=conditions,
            plan=[
                f"find the {container.readable_name}",
                f"open the {container.readable_name}",
                f"pick up the {target_object_instance_id.readable_name}",
                f"close the {container.readable_name}",
            ],
        )

    def create_mission_with_container_open() -> ChallengeBuilderOutput:
        builder_output = create_mission()
        # Open the time machine
        builder_output.required_objects[container.name].add_state("isOpen", "true")
        # Change the plans
        builder_output.plan = [
            f"find the {container.readable_name}",
            f"pick up the {target_object_instance_id.readable_name}",
            f"close the {container.readable_name}",
        ]
        return builder_output

    high_level_key = HighLevelKey(
        action="pickup",
        target_object=target_object_instance_id.object_id,
        from_receptacle=container.object_id,
        from_receptacle_is_container=True,
    )

    ChallengeBuilder.register(high_level_key)(create_mission)
    ChallengeBuilder.register(high_level_key)(create_mission_with_container_open)

    # Register versions of the challenges with color variants
    if with_color_variants:
        for color in get_args(ColorChangerObjectColor):
            colored_target_object_kwargs = {
                "required_objects": {
                    target_object.name: {"colors": [color]},
                }
            }
            high_level_key = HighLevelKey(
                action="pickup",
                target_object=target_object_instance_id.object_id,
                target_object_color=color,
                from_receptacle=container.object_id,
                from_receptacle_is_container=True,
            )
            # Register the challenge builder with the modifications
            ChallengeBuilder.register_with_modifiers(high_level_key, colored_target_object_kwargs)(
                create_mission
            )
            ChallengeBuilder.register_with_modifiers(high_level_key, colored_target_object_kwargs)(
                create_mission_with_container_open
            )


def create_place_in_container_challenge(
    target_object_instance_id: ObjectInstanceId,
    container: RequiredObject,
    *,
    with_color_variants: bool = False,
) -> None:
    """Generate challenges to pick up objects from containers."""
    required_object_builder = RequiredObjectBuilder()

    # Create the target object
    target_object = RequiredObject(name=target_object_instance_id)
    target_object.add_state("Unique", "true")

    # Create the breakroom table
    breakroom_table = required_object_builder.breakroom_table()

    # Put the target object on the table
    target_object.update_receptacle(breakroom_table.name)

    conditions = [
        # Ensure the container is not full of items at the start of the mission
        StateCondition(
            stateName="ContainerNotFull",
            context=target_object.name,
            expression=StateExpression.from_expression(
                AndExpression.from_expressions(
                    IsFullOfItemsExpression(target=container.name, value=False),
                    IsPickedUpExpression(target=target_object.name, value=True),
                )
            ),
        ),
        # Place it in the container while its open
        StateCondition(
            stateName="PlacedInContainer",
            context=target_object.name,
            expression=StateExpression.from_expression(
                AndExpression.from_expressions(
                    IsOpenExpression(target=container.name, value=True),
                    ContainsExpression(target=container.name, contains=target_object.name),
                    IsPickedUpExpression(target=target_object.name, value=False),
                )
            ),
        ),
        # Close the container with the object inside
        StateCondition(
            stateName="ClosedContainer",
            context=container.name,
            expression=StateExpression.from_expression(
                AndExpression.from_expressions(
                    IsOpenExpression(target=container.name, value=False),
                    ContainsExpression(target=container.name, contains=target_object.name),
                )
            ),
        ),
    ]

    goals = [TaskGoal.from_state_condition(condition) for condition in conditions]

    def create_mission() -> ChallengeBuilderOutput:
        """Create the mission."""
        if not container.room:
            raise ValueError(f"Container {container.name} must have a room set")

        return ChallengeBuilderOutput(
            start_room=container.room,
            required_objects={
                container.name: container,
                target_object.name: target_object,
                breakroom_table.name: breakroom_table,
            },
            task_goals=goals,
            state_conditions=conditions,
            plan=[
                f"find the {container.readable_name}",
                f"open the {container.readable_name}",
                f"put the {target_object_instance_id.readable_name} in the {container.readable_name}",
                f"close the {container.readable_name}",
            ],
            preparation_plan=[
                "go to the breakroom",
                f"pick up the {target_object.readable_name}",
            ],
        )

    def create_mission_with_container_open() -> ChallengeBuilderOutput:
        builder_output = create_mission()
        # Open the time machine
        builder_output.required_objects[container.name].add_state("isOpen", "true")
        # Change the plans
        builder_output.plan = [
            f"find the {container.readable_name}",
            f"put the {target_object_instance_id.readable_name} in the {container.readable_name}",
            f"close the {container.readable_name}",
        ]
        return builder_output

    high_level_key = HighLevelKey(
        action="place",
        target_object=target_object_instance_id.object_id,
        to_receptacle=container.object_id,
        to_receptacle_is_container=True,
    )

    ChallengeBuilder.register(high_level_key)(create_mission)
    ChallengeBuilder.register(high_level_key)(create_mission_with_container_open)

    # Register versions of the challenges with color variants
    if with_color_variants:
        for color in get_args(ColorChangerObjectColor):
            colored_target_object_kwargs = {
                "required_objects": {
                    target_object.name: {"colors": [color]},
                }
            }
            high_level_key = HighLevelKey(
                action="place",
                target_object=target_object_instance_id.object_id,
                target_object_color=color,
                to_receptacle=container.object_id,
                to_receptacle_is_container=True,
            )
            # Register the challenge builder with the modifications
            ChallengeBuilder.register_with_modifiers(high_level_key, colored_target_object_kwargs)(
                create_mission
            )
            ChallengeBuilder.register_with_modifiers(high_level_key, colored_target_object_kwargs)(
                create_mission_with_container_open
            )


def register_objects_with_fridge_challenges(enable_color_variants: bool = True) -> None:
    """Register challenges to pick up and place objects in the fridge."""
    required_objects_builder = RequiredObjectBuilder()

    container = required_objects_builder.fridge()

    # Ensure each container is in the breakroom
    container.update_room("BreakRoom")

    target_object_iterator = [
        (ObjectInstanceId.parse("Apple_1"), True, True),
        (ObjectInstanceId.parse("AppleSlice_01_1"), False, False),
        (ObjectInstanceId.parse("Banana_01_1"), False, False),
        (ObjectInstanceId.parse("BananaBunch_01_1"), False, False),
        (ObjectInstanceId.parse("BreadLoaf_1"), False, False),
        (ObjectInstanceId.parse("BreadSlice_01_1"), False, False),
        (ObjectInstanceId.parse("Bowl_01_1"), True, True),
        (ObjectInstanceId.parse("Burger_04_1"), False, False),
        (ObjectInstanceId.parse("Cake_02_1"), True, True),
        (ObjectInstanceId.parse("CakeSlice_02_1"), False, False),
        (ObjectInstanceId.parse("CandyBar_01_1"), False, False),
        (ObjectInstanceId.parse("CanSodaNew_01_1"), False, False),
        (ObjectInstanceId.parse("CanSodaNew_Crushed_01_1"), False, False),
        (ObjectInstanceId.parse("CanSodaNew_Open_01_1"), False, False),
        (ObjectInstanceId.parse("Carrot_01_1"), True, True),
        (ObjectInstanceId.parse("Cereal_Box_01_1"), False, False),
        (ObjectInstanceId.parse("CoffeeBeans_01_1"), False, False),
        (ObjectInstanceId.parse("CoffeeCup_Open_Empty_02_1"), False, False),
        (ObjectInstanceId.parse("CoffeeMug_Boss_1"), True, True),
        (ObjectInstanceId.parse("CoffeeMug_Yellow_1"), True, True),
        (ObjectInstanceId.parse("Donut_01_1"), False, True),
        (ObjectInstanceId.parse("FoodPlate_01_1"), True, True),
        (ObjectInstanceId.parse("Fork_01_1"), False, False),
        (ObjectInstanceId.parse("Jar_Jam_01_1"), False, False),
        (ObjectInstanceId.parse("Jar_PeanutButter_01_1"), False, False),
        (ObjectInstanceId.parse("Knife_01_1"), False, False),
        (ObjectInstanceId.parse("MilkCarton_01_1"), False, False),
        (ObjectInstanceId.parse("PaperCup_01_1"), False, False),
        (ObjectInstanceId.parse("PaperCup_Crushed_01_1"), False, False),
        (ObjectInstanceId.parse("PBJ_Sandwich_1"), False, False),
        (ObjectInstanceId.parse("Pear_01_1"), True, True),
        (ObjectInstanceId.parse("PieFruitSlice_01_1"), False, False),
        (ObjectInstanceId.parse("PieFruit_01_1"), False, False),
        (ObjectInstanceId.parse("SandwichHalf_01_1"), False, False),
        (ObjectInstanceId.parse("Spoon_01_1"), False, False),
        (ObjectInstanceId.parse("Toast_01_1"), False, False),
        (ObjectInstanceId.parse("Toast_02_1"), False, False),
        (ObjectInstanceId.parse("Toast_03_1"), False, False),
        (ObjectInstanceId.parse("Toast_04_1"), False, False),
        (ObjectInstanceId.parse("Toast_04_Jam_1"), False, False),
        (ObjectInstanceId.parse("Toast_04_PBJ_1"), False, False),
    ]

    for target_object, pickup_color_variants, place_color_variants in target_object_iterator:
        create_pick_up_from_container_challenge(
            target_object,
            container,
            with_color_variants=pickup_color_variants & enable_color_variants,
        )
        create_place_in_container_challenge(
            target_object,
            container,
            with_color_variants=place_color_variants & enable_color_variants,
        )


def register_objects_with_freezer_challenges(enable_color_variants: bool = True) -> None:
    """Register challenges to pick up and place objects in the freezer."""
    required_objects_builder = RequiredObjectBuilder()

    container = required_objects_builder.freezer()

    # Ensure each container is in the breakroom
    container.update_room("BreakRoom")

    target_object_iterator = [
        (ObjectInstanceId.parse("Apple_1"), True, True),
        (ObjectInstanceId.parse("AppleSlice_01_1"), False, False),
        (ObjectInstanceId.parse("Banana_01_1"), False, False),
        (ObjectInstanceId.parse("BananaBunch_01_1"), False, False),
        (ObjectInstanceId.parse("BreadLoaf_1"), False, False),
        (ObjectInstanceId.parse("BreadSlice_01_1"), False, False),
        (ObjectInstanceId.parse("Bowl_01_1"), True, True),
        (ObjectInstanceId.parse("Burger_04_1"), False, False),
        (ObjectInstanceId.parse("Cake_02_1"), True, True),
        (ObjectInstanceId.parse("CakeSlice_02_1"), False, False),
        (ObjectInstanceId.parse("CandyBar_01_1"), False, False),
        (ObjectInstanceId.parse("CanSodaNew_01_1"), False, False),
        (ObjectInstanceId.parse("CanSodaNew_Crushed_01_1"), False, False),
        (ObjectInstanceId.parse("CanSodaNew_Open_01_1"), False, False),
        (ObjectInstanceId.parse("Carrot_01_1"), True, True),
        (ObjectInstanceId.parse("Cereal_Box_01_1"), False, False),
        (ObjectInstanceId.parse("CoffeeBeans_01_1"), False, False),
        (ObjectInstanceId.parse("CoffeeCup_Open_Empty_02_1"), False, False),
        (ObjectInstanceId.parse("CoffeeMug_Boss_1"), True, True),
        (ObjectInstanceId.parse("CoffeeMug_Yellow_1"), True, True),
        (ObjectInstanceId.parse("Donut_01_1"), False, True),
        (ObjectInstanceId.parse("FoodPlate_01_1"), True, True),
        (ObjectInstanceId.parse("Fork_01_1"), False, False),
        (ObjectInstanceId.parse("Jar_Jam_01_1"), False, False),
        (ObjectInstanceId.parse("Jar_PeanutButter_01_1"), False, False),
        (ObjectInstanceId.parse("Knife_01_1"), False, False),
        (ObjectInstanceId.parse("PaperCup_01_1"), False, False),
        (ObjectInstanceId.parse("PaperCup_Crushed_01_1"), False, False),
        (ObjectInstanceId.parse("PBJ_Sandwich_1"), False, False),
        (ObjectInstanceId.parse("Pear_01_1"), True, True),
        (ObjectInstanceId.parse("PieFruitSlice_01_1"), False, False),
        (ObjectInstanceId.parse("PieFruit_01_1"), False, False),
        (ObjectInstanceId.parse("SandwichHalf_01_1"), False, False),
        (ObjectInstanceId.parse("Spoon_01_1"), False, False),
        (ObjectInstanceId.parse("Toast_01_1"), False, False),
        (ObjectInstanceId.parse("Toast_02_1"), False, False),
        (ObjectInstanceId.parse("Toast_03_1"), False, False),
        (ObjectInstanceId.parse("Toast_04_1"), False, False),
        (ObjectInstanceId.parse("Toast_04_Jam_1"), False, False),
        (ObjectInstanceId.parse("Toast_04_PBJ_1"), False, False),
    ]
    for target_object, pickup_color_variants, place_color_variants in target_object_iterator:
        create_pick_up_from_container_challenge(
            target_object,
            container,
            with_color_variants=pickup_color_variants & enable_color_variants,
        )
        create_place_in_container_challenge(
            target_object,
            container,
            with_color_variants=place_color_variants & enable_color_variants,
        )


def register_warehouse_cabinet_challenges(enable_color_variants: bool = True) -> None:
    """Register challenges to pick up and place objects in the warehouse cabinet."""
    container = RequiredObject(
        name=ObjectInstanceId.parse("KitchenCabinet_02_1"), roomLocation=["Warehouse"]
    )

    target_object_iterator = [
        (ObjectInstanceId.parse("Apple_1"), True),
        (ObjectInstanceId.parse("AppleSlice_01_1"), False),
        (ObjectInstanceId.parse("Banana_01_1"), False),
        (ObjectInstanceId.parse("BananaBunch_01_1"), False),
        (ObjectInstanceId.parse("BreadLoaf_1"), False),
        (ObjectInstanceId.parse("BreadSlice_01_1"), False),
        (ObjectInstanceId.parse("Bowl_01_1"), True),
        (ObjectInstanceId.parse("Burger_04_1"), False),
        (ObjectInstanceId.parse("Cake_02_1"), True),
        (ObjectInstanceId.parse("CakeSlice_02_1"), False),
        (ObjectInstanceId.parse("CandyBar_01_1"), False),
        (ObjectInstanceId.parse("Carrot_01_1"), True),
        (ObjectInstanceId.parse("CanSodaNew_01_1"), False),
        (ObjectInstanceId.parse("CanSodaNew_Crushed_01_1"), False),
        (ObjectInstanceId.parse("CanSodaNew_Open_01_1"), False),
        (ObjectInstanceId.parse("CoffeeBeans_01_1"), False),
        (ObjectInstanceId.parse("CoffeeMug_Boss_1"), True),
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
        create_pick_up_from_container_challenge(
            target_object,
            container,
            with_color_variants=enable_color_variants & with_color_variants,
        )
        create_place_in_container_challenge(
            target_object,
            container,
            with_color_variants=enable_color_variants & with_color_variants,
        )
