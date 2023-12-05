import itertools
from collections.abc import Iterator
from typing import Any, Optional, get_args

from arena_missions.builders import (
    ChallengeBuilder,
    ChallengeBuilderFunction,
    ChallengeBuilderOutput,
    RequiredObjectBuilder,
)
from arena_missions.constants.arena import ColorChangerObjectColor
from arena_missions.structures import (
    AndExpression,
    ContainsExpression,
    HighLevelKey,
    IsPickedUpExpression,
    ObjectInstanceId,
    RequiredObject,
    StateCondition,
    StateExpression,
    TaskGoal,
)


def create_ambiguous_pickup_challenge(  # noqa: WPS231
    target_object_idx: int, available_objects: list[RequiredObject], receptacle: RequiredObject
) -> None:
    """Generate challenges to pick up objects from other ambiguous objects."""
    target_object = available_objects[target_object_idx]

    conditions = [
        # [PREP] Ensure all the objects are proper
        StateCondition(
            stateName="AllObjectsAreProper",
            context=receptacle.object_instance_id,
            expression=StateExpression.from_expression(
                AndExpression.from_expressions(
                    *[
                        ContainsExpression(
                            target=receptacle.object_instance_id,
                            contains=curr_object.object_instance_id,
                        )
                        for curr_object in available_objects
                    ]
                )
            ),
        ),
        # Ensure we pick up the target object
        StateCondition(
            stateName="PickedUpTargetObject",
            context=target_object.object_instance_id,
            expression=StateExpression.from_expression(
                IsPickedUpExpression(target=target_object.object_instance_id, value=True),
            ),
        ),
    ]

    goals = [TaskGoal.from_state_condition(condition) for condition in conditions]

    def create_mission_func_with_color(
        target_color: Optional[ColorChangerObjectColor],
    ) -> ChallengeBuilderFunction:
        plan = (
            f"pick up the {target_color} {target_object.readable_name}"
            if target_color
            else f"pick up the white {target_object.readable_name}"
        )

        def _create_mission() -> ChallengeBuilderOutput:
            """Create the mission."""
            if not receptacle.room:
                raise ValueError(f"Receptacle {receptacle.name} must have a room set")

            return ChallengeBuilderOutput(
                start_room=receptacle.room,
                required_objects={
                    receptacle.name: receptacle,
                    **{curr_object.name: curr_object for curr_object in available_objects},
                },
                task_goals=goals,
                state_conditions=conditions,
                plan=[plan],
            )

        return _create_mission

    object_colors = [None, *get_args(ColorChangerObjectColor)]
    object_color_permutations: Iterator[tuple[Any, ...]] = itertools.permutations(object_colors)

    for color_permutation in object_color_permutations:
        colored_target_object_kwargs: dict[str, Any] = {"required_objects": {}}

        for curr_object, color in zip(available_objects, color_permutation):
            if color is not None:
                colored_target_object_kwargs["required_objects"].update(
                    {curr_object.name: {"colors": [color]}}
                )
        target_color: Optional[ColorChangerObjectColor] = color_permutation[target_object_idx]

        high_level_key = HighLevelKey(
            action="pickup",
            target_object=target_object.object_id,
            target_object_color=target_color,
            target_object_is_ambiguous=True,
            from_receptacle=receptacle.object_id,
            from_receptacle_is_container=False,
        )

        # Register the challenge builder with the modifications
        create_mission: ChallengeBuilderFunction = create_mission_func_with_color(target_color)
        ChallengeBuilder.register_with_modifiers(high_level_key, colored_target_object_kwargs)(
            create_mission
        )


def register_ambiguous_pickup_challenges(max_num_distractors: int = 2) -> None:
    """Register challenges to pick up a target object among distractors objects."""
    required_objects_builder = RequiredObjectBuilder()

    receptacles = [
        required_objects_builder.breakroom_table(),
        required_objects_builder.breakroom_countertop(),
    ]

    # include only the objects that allow color changes
    target_object_iterator = [
        "Apple_{instance_count}",
        "Cake_02_{instance_count}",
        "Carrot_01_{instance_count}",
        "Donut_01_{instance_count}",
        "Pear_01_{instance_count}",
        "CoffeeMug_Yellow_{instance_count}",
        "CoffeeMug_Boss_{instance_count}",
        "Bowl_01_{instance_count}",
        "FoodPlate_01_{instance_count}",
        "DeskFan_New_01_{instance_count}",
    ]

    for target_object_template in target_object_iterator:
        for receptacle in receptacles:
            available_objects: list[RequiredObject] = []
            for idx in range(1, max_num_distractors + 1):
                curr_object = RequiredObject(
                    name=ObjectInstanceId.parse(
                        target_object_template.format(instance_count=idx + 1)
                    )
                )
                curr_object.update_receptacle(receptacle.name)
                available_objects.append(curr_object)

            for target_object_idx, _ in enumerate(available_objects):
                create_ambiguous_pickup_challenge(target_object_idx, available_objects, receptacle)
