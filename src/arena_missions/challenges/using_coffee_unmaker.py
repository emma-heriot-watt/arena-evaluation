from typing import get_args

from arena_missions.builders import ChallengeBuilder, ChallengeBuilderOutput, RequiredObjectBuilder
from arena_missions.constants.arena import ColorChangerObjectColor
from arena_missions.structures import (
    AndExpression,
    HighLevelKey,
    IsFilledWithExpression,
    IsPickedUpExpression,
    IsToggledOnExpression,
    NotExpression,
    ObjectInstanceId,
    RequiredObject,
    StateCondition,
    StateExpression,
    TaskGoal,
)


def convert_coffee_from_pot_to_beans() -> ChallengeBuilderOutput:
    """Convert coffee back to beans with the coffee unmaker."""
    required_objects_builder = RequiredObjectBuilder()

    # Remove existing beans from the scene
    coffee_beans = RequiredObject(name=ObjectInstanceId.parse("CoffeeBeans_01_1"))
    coffee_beans.update_state("Blacklist", "true")

    # Coffee unmaker
    coffee_unmaker = RequiredObject(name=ObjectInstanceId.parse("CoffeeUnMaker_01_1"))

    # Create the coffee pot
    coffee_pot = required_objects_builder.coffee_pot(fill_with="Coffee")

    conditions = [
        # Pick up the coffee pot
        StateCondition(
            stateName="HoldingCoffeePot",
            context=coffee_pot.name,
            expression=StateExpression.from_expression(
                IsPickedUpExpression(target=coffee_pot.name, value=True)
            ),
        ),
        # Fill the coffee unmaker with coffee, that happens to be from the coffee pot
        StateCondition(
            stateName="CoffeeUnMakerFilledWithCoffee",
            context=coffee_unmaker.name,
            expression=StateExpression.from_expression(
                AndExpression.from_expressions(
                    IsFilledWithExpression(target=coffee_unmaker.name, fluid="Coffee"),
                    NotExpression(
                        expression=StateExpression.from_expression(
                            IsFilledWithExpression(target=coffee_pot.name, fluid="Coffee")
                        )
                    ),
                )
            ),
        ),
        # Turn on the coffee unmaker
        StateCondition(
            stateName="CoffeeUnMakerOn",
            context=coffee_unmaker.name,
            expression=StateExpression.from_expression(
                IsToggledOnExpression(target=coffee_unmaker.name, value=True)
            ),
        ),
    ]

    goals = [TaskGoal.from_state_condition(condition) for condition in conditions]

    return ChallengeBuilderOutput(
        start_room="BreakRoom",
        required_objects={
            coffee_pot.name: coffee_pot,
            coffee_unmaker.name: coffee_unmaker,
            coffee_beans.name: coffee_beans,
        },
        task_goals=goals,
        state_conditions=conditions,
        plan=[
            "go to the coffee unmaker",
            "pour the coffee unto the coffee unmaker",
            "toggle the coffee unmaker",
        ],
        preparation_plan=[
            f"find the {coffee_pot.readable_name}",
            f"pick up the {coffee_pot.readable_name}",
        ],
    )


def convert_coffee_from_target_object_to_beans(
    *, target_object_instance_id: ObjectInstanceId, with_color_variants: bool = True
) -> None:
    """Convert coffee back to beans with the coffee unmaker."""
    required_objects_builder = RequiredObjectBuilder()

    # Remove existing beans from the scene
    coffee_beans = RequiredObject(name=ObjectInstanceId.parse("CoffeeBeans_01_1"))
    coffee_beans.update_state("Blacklist", "true")

    # Coffee unmaker
    coffee_unmaker = RequiredObject(name=ObjectInstanceId.parse("CoffeeUnMaker_01_1"))

    # Create the target object
    target_object = RequiredObject(name=target_object_instance_id)
    target_object.update_state("isFilled", "Coffee")
    target_object.update_state("isHot", "true")

    # Create the breakroom table
    breakroom_table = required_objects_builder.breakroom_table()

    # Put the target object on the breakroom table
    target_object.update_receptacle(breakroom_table.name)

    conditions = [
        # Pick up the coffee pot
        StateCondition(
            stateName="HoldingMug",
            context=target_object.name,
            expression=StateExpression.from_expression(
                IsPickedUpExpression(target=target_object.name, value=True)
            ),
        ),
        # Fill the coffee unmaker with coffee, that happens to be from the coffee pot
        StateCondition(
            stateName="CoffeeUnMakerFilledWithCoffee",
            context=coffee_unmaker.name,
            expression=StateExpression.from_expression(
                AndExpression.from_expressions(
                    IsFilledWithExpression(target=coffee_unmaker.name, fluid="Coffee"),
                    NotExpression(
                        expression=StateExpression.from_expression(
                            IsFilledWithExpression(target=target_object.name, fluid="Coffee")
                        )
                    ),
                )
            ),
        ),
        # Turn on the coffee unmaker
        StateCondition(
            stateName="CoffeeUnMakerOn",
            context=coffee_unmaker.name,
            expression=StateExpression.from_expression(
                IsToggledOnExpression(target=coffee_unmaker.name, value=True)
            ),
        ),
    ]

    goals = [TaskGoal.from_state_condition(condition) for condition in conditions]

    def create_mission() -> ChallengeBuilderOutput:
        return ChallengeBuilderOutput(
            start_room="BreakRoom",
            required_objects={
                breakroom_table.name: breakroom_table,
                target_object.name: target_object,
                coffee_unmaker.name: coffee_unmaker,
                coffee_beans.name: coffee_beans,
            },
            task_goals=goals,
            state_conditions=conditions,
            plan=[
                "go to the coffee unmaker",
                "pour the coffee unto the coffee unmaker",
                "toggle the coffee unmaker",
            ],
            preparation_plan=[
                f"find the {target_object.readable_name}",
                f"pick up the {target_object.readable_name}",
            ],
        )

    high_level_key = HighLevelKey(
        action="interact",
        interaction_object=coffee_unmaker.object_id,
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
                action="interact",
                interaction_object=coffee_unmaker.object_id,
                target_object=target_object.object_id,
                target_object_color=color,
            )

            # Register the challenge builder with the modifications
            ChallengeBuilder.register_with_modifiers(high_level_key, colored_target_object_kwargs)(
                create_mission
            )


def register_coffee_unmaker_challenges() -> None:
    """Register challenges with the coffee unmaker."""
    target_object_iterator = [
        (ObjectInstanceId.parse("Bowl_01_1"), True),
        (ObjectInstanceId.parse("CoffeePot_01_1"), True),
        (ObjectInstanceId.parse("CoffeeMug_Boss_1"), True),
        (ObjectInstanceId.parse("CoffeeMug_Yellow_1"), True),
    ]
    for target_object, with_color_variants in target_object_iterator:
        convert_coffee_from_target_object_to_beans(
            target_object_instance_id=target_object,
            with_color_variants=with_color_variants,
        )
