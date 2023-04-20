from typing import get_args

from arena_missions.builders import ChallengeBuilder, ChallengeBuilderOutput, RequiredObjectBuilder
from arena_missions.constants.arena import ColorChangerObjectColor
from arena_missions.structures import (
    ColorMetaDataChangeExpression,
    ContainsExpression,
    HighLevelKey,
    IsPickedUpExpression,
    ObjectInstanceId,
    RequiredObject,
    StateCondition,
    StateExpression,
    TaskGoal,
)


def create_change_object_color_challenge(
    target_object_instance_id: ObjectInstanceId,
    converted_object_color: ColorChangerObjectColor,
) -> None:
    """Generate challenes to transform an object's color using the color changer."""
    # Create the target object
    required_objects_builder = RequiredObjectBuilder()

    receptacle = required_objects_builder.breakroom_table()
    color_changer = required_objects_builder.color_changer()

    target_object = RequiredObject(name=target_object_instance_id)
    target_object.add_state("Unique", "true")

    # Put it in the container
    target_object.update_receptacle(receptacle.name)

    conditions = [
        # Ensure the object is picked up from the receptacle
        StateCondition(
            stateName="PickedUpFromReceptacle",
            context=target_object.name,
            expression=StateExpression.from_expression(
                IsPickedUpExpression(target=target_object.name, value=True)
            ),
        ),
        StateCondition(
            stateName="OnColorChanger",
            context=color_changer.name,
            expression=StateExpression.from_expression(
                ContainsExpression(target=color_changer.name, contains=target_object.name)
            ),
        ),
        StateCondition(
            stateName="ChangedColor",
            context=target_object.name,
            expression=StateExpression.from_expression(
                ColorMetaDataChangeExpression(
                    target=target_object.name, colorvalue=converted_object_color
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
                receptacle.name: receptacle,
                target_object.name: target_object,
                color_changer.name: color_changer,
            },
            task_goals=goals,
            state_conditions=conditions,
            plan=[
                f"go to the {color_changer.readable_name}",
                f"place the {target_object.readable_name} in the {color_changer.readable_name}",
                f"press the {converted_object_color} button",
            ],
            preparation_plan=[
                f"go to the {receptacle.readable_name}",
                f"pick up the {target_object_instance_id.readable_name}",
            ],
        )

    high_level_key = HighLevelKey(
        action="interact",
        target_object=target_object_instance_id.object_id,
        converted_object_color=converted_object_color,
        interaction_object=color_changer.object_id,
    )

    ChallengeBuilder.register(high_level_key)(create_mission)

    # Register versions of the challenges with color variants
    for start_color in get_args(ColorChangerObjectColor):
        colored_target_object_kwargs = {
            "required_objects": {
                target_object.name: {"colors": [start_color]},
            }
        }

        high_level_key = HighLevelKey(
            action="interact",
            interaction_object=color_changer.object_id,
            target_object=target_object.object_id,
            target_object_color=start_color,
            converted_object_color=converted_object_color,
        )

        ChallengeBuilder.register_with_modifiers(high_level_key, colored_target_object_kwargs)(
            create_mission
        )


def register_color_changer_challenges() -> None:
    """Register challenges to change object color using the color changer."""
    target_object_iterator = [
        ObjectInstanceId.parse("Apple_1"),
        ObjectInstanceId.parse("Bowl_01_1"),
        ObjectInstanceId.parse("Carrot_01_1"),
        ObjectInstanceId.parse("CoffeeMug_Boss_1"),
        ObjectInstanceId.parse("CoffeeMug_Yellow_1"),
        ObjectInstanceId.parse("DeskFan_Broken_01_1"),
        ObjectInstanceId.parse("DeskFan_New_01_1"),
        ObjectInstanceId.parse("Donut_01_1"),
        ObjectInstanceId.parse("FoodPlate_01_1"),
        ObjectInstanceId.parse("Pear_01_1"),
    ]

    color_changer_colors = get_args(ColorChangerObjectColor)

    for target_object in target_object_iterator:
        for object_color in color_changer_colors:
            create_change_object_color_challenge(target_object, object_color)
