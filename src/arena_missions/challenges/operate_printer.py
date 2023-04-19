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


def create_operate_printer_challenges(
    printer_cartridge: RequiredObject,
    converted_object: ObjectInstanceId,
    with_color_variants: bool = False,
) -> None:
    """Register challenges."""
    required_object_builder = RequiredObjectBuilder()

    # Make the target object unique
    printer_cartridge.add_state("Unique", "true")

    # Create the time machine
    printer = required_object_builder.printer()
    printer.add_state("Unique", "true")

    # Create the breakroom table
    breakroom_table = required_object_builder.breakroom_table()
    printer_cartridge.update_receptacle(breakroom_table.name)

    # Success conditions
    conditions = [
        # Pick up the target object
        StateCondition(
            stateName="TargetPickedUp",
            context=printer_cartridge.name,
            expression=StateExpression.from_expression(
                AndExpression.from_expressions(
                    IsPickedUpExpression(target=printer_cartridge.name, value=True),
                )
            ),
        ),
        # Ensure the machine is used on the target
        StateCondition(
            stateName="MachineUsedOnTarget",
            context=printer.name,
            expression=StateExpression.from_expression(
                AndExpression.from_expressions(
                    IsToggledOnExpression(target=printer.name, value=True),
                    ContainsExpression(target=printer.name, contains=printer_cartridge.name),
                )
            ),
        ),
        # Pick up the converted object
        StateCondition(
            stateName="ConvertedPickedUp",
            context=printer_cartridge.name,
            expression=StateExpression.from_expression(
                AndExpression.from_expressions(
                    IsPickedUpExpression(target=converted_object, value=True),
                )
            ),
        ),
    ]

    # Create mission
    def create_mission() -> ChallengeBuilderOutput:
        return ChallengeBuilderOutput(
            start_room="Lab1",
            required_objects={
                printer.name: printer,
                printer_cartridge.name: printer_cartridge,
                breakroom_table.name: breakroom_table,
            },
            state_conditions=conditions,
            task_goals=[TaskGoal.from_state_condition(condition) for condition in conditions],
            plan=[
                "go printer",
                f"put the {printer_cartridge.readable_name} in the printer",
                "turn on the printer",
                f"pick up the {converted_object.readable_name}",
            ],
            preparation_plan=[
                "go to the breakroom table",
                f"pick up the {printer_cartridge.readable_name}",
                "go to the robotics lab",
            ],
        )

    # Register versions of the challenges without color variants
    high_level_key = HighLevelKey(
        action="interact",
        interaction_object=printer.object_id,
        target_object=printer_cartridge.object_id,
        converted_object=converted_object.object_id,
    )

    ChallengeBuilder.register(high_level_key)(create_mission)

    # Register versions of the challenges with color variants
    if with_color_variants:
        for color in get_args(ColorChangerObjectColor):
            colored_target_object_kwargs = {
                "required_objects": {
                    printer_cartridge.name: {"colors": [color]},
                }
            }
            high_level_key = HighLevelKey(
                action="interact",
                interaction_object=printer.object_id,
                target_object=printer_cartridge.object_id,
                target_object_color=color,
                converted_object=converted_object.object_id,
            )
            # Register the challenge builder with the modifications
            ChallengeBuilder.register_with_modifiers(high_level_key, colored_target_object_kwargs)(
                create_mission
            )


def register_print_things() -> None:
    """Register challenges to print things using the 3D printer."""
    object_instance_ids = [
        (
            ObjectInstanceId.parse("Printer_Cartridge_Figure_1"),
            ObjectInstanceId.parse("Printer_3D_1_Spawned_ActionFigure_1"),
        ),
        (
            ObjectInstanceId.parse("Printer_Cartridge_Hammer_1"),
            ObjectInstanceId.parse("Printer_3D_1_Spawned_Hammer_1"),
        ),
        (
            ObjectInstanceId.parse("Printer_Cartridge_Lever_1"),
            ObjectInstanceId.parse("Printer_3D_1_Spawned_FuseBox_01_Lever_1"),
        ),
        (
            ObjectInstanceId.parse("Printer_Cartridge_Mug_1"),
            ObjectInstanceId.parse("Printer_3D_1_Spawned_CoffeeMug_Yellow_1"),
        ),
    ]

    for object_instance_id, converted_object_id in object_instance_ids:
        create_operate_printer_challenges(
            printer_cartridge=RequiredObject(name=object_instance_id),
            converted_object=converted_object_id,
            with_color_variants=False,
        )
