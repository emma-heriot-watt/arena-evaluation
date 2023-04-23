from typing import Literal, Optional, get_args

from arena_missions.builders import ChallengeBuilder, ChallengeBuilderOutput, RequiredObjectBuilder
from arena_missions.constants.arena import ColorChangerObjectColor, OfficeLayout
from arena_missions.structures import (
    AndExpression,
    HighLevelKey,
    IsDirtyExpression,
    IsPickedUpExpression,
    IsToggledOnExpression,
    ObjectInstanceId,
    RequiredObject,
    StateCondition,
    StateExpression,
    TaskGoal,
)


def create_clean_dirty_plate_challenge(
    room: Literal["BreakRoom", "Warehouse"],
    office_layout: Optional[OfficeLayout] = None,
    *,
    with_color_variants: bool = False,
) -> None:
    """Clean a dirty plate."""
    required_object_builder = RequiredObjectBuilder()

    sink = RequiredObject(
        name=ObjectInstanceId.parse("KitchenCounterSink_01_1"), roomLocation=[room]
    )

    plate = RequiredObject(name=ObjectInstanceId.parse("FoodPlate_01_1"))
    plate.add_state("Unique", "true")
    plate.add_state("isDirty", "true")

    # Create the breakroom table
    breakroom_table = required_object_builder.breakroom_table()

    # Put the target object on the table
    plate.update_receptacle(breakroom_table.name)

    conditions = [
        # Holding a dirty plate
        StateCondition(
            stateName="HoldingDirtyPlate",
            context=sink.name,
            expression=StateExpression.from_expression(
                AndExpression.from_expressions(
                    IsDirtyExpression(target=plate.name, value=True),
                    IsPickedUpExpression(target=plate.name, value=True),
                )
            ),
        ),
        # Fill the sink before cleaning the plate
        StateCondition(
            stateName="FilledSinkBeforeCleaningPlate",
            context=sink.name,
            expression=StateExpression.from_expression(
                AndExpression.from_expressions(
                    IsToggledOnExpression(target=sink.name, value=True),
                    IsDirtyExpression(target=plate.name, value=True),
                )
            ),
        ),
        # Clean the plate
        StateCondition(
            stateName="CleanedPlate",
            context=sink.name,
            expression=StateExpression.from_expression(
                AndExpression.from_expressions(
                    IsToggledOnExpression(target=sink.name, value=True),
                    IsDirtyExpression(target=plate.name, value=False),
                )
            ),
        ),
        # Turn off the sink after cleaning the plate
        StateCondition(
            stateName="TurnedOffSinkAfterCleaningPlate",
            context=sink.name,
            expression=StateExpression.from_expression(
                AndExpression.from_expressions(
                    IsToggledOnExpression(target=sink.name, value=False),
                    IsDirtyExpression(target=plate.name, value=False),
                )
            ),
        ),
    ]

    def fill_sink_before_cleaning_plate() -> ChallengeBuilderOutput:
        """Fill the sink before cleaning the plate."""
        return ChallengeBuilderOutput(
            start_room=room,
            office_layout=office_layout,
            required_objects={
                sink.name: sink,
                plate.name: plate,
                breakroom_table.name: breakroom_table,
            },
            state_conditions=conditions,
            task_goals=[TaskGoal.from_state_condition(condition) for condition in conditions],
            plan=[
                "find the sink",
                "toggle the sink",
                "clean the plate in the sink",
                "toggle the sink",
            ],
            preparation_plan=[
                "go to the breakroom table",
                "pick up the plate",
            ],
        )

    def sink_already_filled_before_cleaning() -> ChallengeBuilderOutput:
        """Do not toggle the sink singce it's already filled."""
        builder_output = fill_sink_before_cleaning_plate()
        builder_output.required_objects[sink.name].update_state("isToggledOn", "true")
        builder_output.plan = [
            "find the sink",
            "clean the plate in the sink",
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
        action="clean",
        interaction_object=sink.object_id,
        target_object=plate.object_id,
    )

    ChallengeBuilder.register(high_level_key)(fill_sink_before_cleaning_plate)
    ChallengeBuilder.register(high_level_key)(sink_already_filled_before_cleaning)

    # Register versions of the challenges with color variants
    if with_color_variants:
        for color in get_args(ColorChangerObjectColor):
            colored_target_object_kwargs = {
                "required_objects": {
                    plate.name: {"colors": [color]},
                }
            }

            high_level_key = HighLevelKey(
                action="clean",
                interaction_object=sink.object_id,
                target_object=plate.object_id,
                target_object_color=color,
            )
            # Register the challenge builder with the modifications
            ChallengeBuilder.register_with_modifiers(high_level_key, colored_target_object_kwargs)(
                fill_sink_before_cleaning_plate
            )
            ChallengeBuilder.register_with_modifiers(high_level_key, colored_target_object_kwargs)(
                sink_already_filled_before_cleaning
            )


def register_clean_dirty_plates(enable_color_variants: bool = True) -> None:
    """Register all the the clean dirty plate challenges."""
    for layout in get_args(OfficeLayout):
        create_clean_dirty_plate_challenge(
            "BreakRoom", office_layout=layout, with_color_variants=enable_color_variants
        )
        create_clean_dirty_plate_challenge(
            "Warehouse", office_layout=layout, with_color_variants=enable_color_variants
        )
