from typing import Literal, Optional, get_args

from arena_missions.builders import ChallengeBuilder, ChallengeBuilderOutput, RequiredObjectBuilder
from arena_missions.constants.arena import ColorChangerObjectColor, OfficeLayout
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


def create_fill_object_in_sink(
    object_instance_id: ObjectInstanceId,
    room: Literal["BreakRoom", "Warehouse"],
    office_layout: Optional[OfficeLayout] = None,
    *,
    with_color_variants: bool = False,
) -> None:
    """Fill an object in a sink."""
    required_object_builder = RequiredObjectBuilder()

    sink = RequiredObject(
        name=ObjectInstanceId.parse("KitchenCounterSink_01_1"), roomLocation=[room]
    )

    # Create object
    target_object = RequiredObject(name=object_instance_id)
    target_object.add_state("Unique", "true")

    # Create the breakroom table
    breakroom_table = required_object_builder.breakroom_table()

    # Put the target object on the table
    target_object.update_receptacle(breakroom_table.name)

    conditions = [
        # Fill the object with water
        StateCondition(
            stateName="FilledObjectWithWater",
            context=target_object.name,
            expression=StateExpression.from_expression(
                IsFilledWithExpression(target=target_object.name, fluid="Water")
            ),
        ),
        # Drain the sink
        StateCondition(
            stateName="DrainedSink",
            context=sink.name,
            expression=StateExpression.from_expression(
                AndExpression.from_expressions(
                    IsToggledOnExpression(target=sink.name, value=False),
                    NotExpression(
                        expression=StateExpression.from_expression(
                            IsFilledWithExpression(target=sink.name, fluid="Water")
                        )
                    ),
                )
            ),
        ),
    ]

    def fill_from_off_sink() -> ChallengeBuilderOutput:
        prep_condition = StateCondition(
            stateName="HoldingUnfilledObject",
            context=target_object.name,
            expression=StateExpression.from_expression(
                IsPickedUpExpression(target=target_object.name, value=True)
            ),
        )
        mission_conditions = [prep_condition, *conditions]

        return ChallengeBuilderOutput(
            start_room=room,
            office_layout=office_layout,
            required_objects={
                sink.name: sink,
                target_object.name: target_object,
                breakroom_table.name: breakroom_table,
            },
            state_conditions=mission_conditions,
            task_goals=[
                TaskGoal.from_state_condition(condition) for condition in mission_conditions
            ],
            plan=[
                "go to the sink",
                "toggle the sink",
                f"fill the {object_instance_id.readable_name} in the sink",
                "toggle the sink",
            ],
            preparation_plan=[
                "go to the breakroom table",
                f"pick up the {object_instance_id.readable_name}",
            ],
        )

    def fill_from_on_sink() -> ChallengeBuilderOutput:
        prep_condition = StateCondition(
            stateName="HoldingUnfilledObjectWithSinkOn",
            context=sink.name,
            expression=StateExpression.from_expression(
                AndExpression.from_expressions(
                    IsPickedUpExpression(target=target_object.name, value=True),
                    IsToggledOnExpression(target=sink.name, value=True),
                    NotExpression(
                        expression=StateExpression.from_expression(
                            IsFilledWithExpression(target=target_object.name, fluid="Water")
                        )
                    ),
                )
            ),
        )
        mission_conditions = [prep_condition, *conditions]

        builder_output = fill_from_off_sink()
        builder_output.state_conditions = mission_conditions
        builder_output.task_goals = [
            TaskGoal.from_state_condition(condition) for condition in mission_conditions
        ]
        builder_output.plan = [
            "go to the sink",
            f"fill the {object_instance_id.readable_name} in the sink",
            "toggle the sink",
        ]
        builder_output.preparation_plan = [
            "find the sink",
            "toggle the sink",
            "go to the breakroom table",
            "pick up the plate",
        ]
        return builder_output

    high_level_key = HighLevelKey(
        action="fill",
        interaction_object=sink.object_id,
        target_object=target_object.object_id,
    )

    ChallengeBuilder.register(high_level_key)(fill_from_off_sink)
    ChallengeBuilder.register(high_level_key)(fill_from_on_sink)

    # Register versions of the challenges with color variants
    if with_color_variants:
        for color in get_args(ColorChangerObjectColor):
            colored_target_object_kwargs = {
                "required_objects": {
                    target_object.name: {"colors": [color]},
                }
            }

            high_level_key = HighLevelKey(
                action="fill",
                interaction_object=sink.object_id,
                target_object=target_object.object_id,
                target_object_color=color,
            )
            # Register the challenge builder with the modifications
            ChallengeBuilder.register_with_modifiers(high_level_key, colored_target_object_kwargs)(
                fill_from_off_sink
            )
            ChallengeBuilder.register_with_modifiers(high_level_key, colored_target_object_kwargs)(
                fill_from_on_sink
            )


def register_fill_objects_in_sink(enable_color_variants: bool = True) -> None:
    """Register challenges about filling an object in sink challenges."""
    object_iterator = [
        (ObjectInstanceId.parse("Bowl_01_1"), True),
        (ObjectInstanceId.parse("CoffeeMug_Boss_1"), True),
        (ObjectInstanceId.parse("CoffeeMug_Yellow_1"), True),
        (ObjectInstanceId.parse("CoffeePot_01_1"), False),
    ]

    for layout in get_args(OfficeLayout):
        for object_instance_id, with_color_variants in object_iterator:
            create_fill_object_in_sink(
                object_instance_id,
                room="BreakRoom",
                office_layout=layout,
                with_color_variants=enable_color_variants & with_color_variants,
            )
            create_fill_object_in_sink(
                object_instance_id,
                room="Warehouse",
                office_layout=layout,
                with_color_variants=enable_color_variants & with_color_variants,
            )
