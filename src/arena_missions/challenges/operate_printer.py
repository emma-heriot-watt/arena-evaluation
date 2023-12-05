from typing import get_args

from arena_missions.builders import ChallengeBuilder, ChallengeBuilderOutput, RequiredObjectBuilder
from arena_missions.constants.arena import OfficeLayout
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


def create_operate_printer_challenges(
    printer_cartridge: RequiredObject,
    printer_spawned_object: ObjectInstanceId,
    office_layout: OfficeLayout,
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

    # Ensure the robotic arm is out the way
    robotic_arm = required_object_builder.robotic_arm()

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
            stateName="PrinterUsed",
            context=printer.name,
            expression=StateExpression.from_expression(
                AndExpression.from_expressions(
                    ContainsExpression(
                        target=printer.name, contains=printer_spawned_object.with_asterisk
                    ),
                    ContainsExpression(
                        target=printer.name, contains=printer_cartridge.name.with_asterisk
                    ),
                )
            ),
        ),
    ]

    goals = [TaskGoal.from_state_condition(condition) for condition in conditions]

    # Create mission
    def create_mission() -> ChallengeBuilderOutput:
        return ChallengeBuilderOutput(
            start_room="Lab1",
            office_layout=office_layout,
            required_objects={
                printer.name: printer,
                printer_cartridge.name: printer_cartridge,
                breakroom_table.name: breakroom_table,
                robotic_arm.name: robotic_arm,
            },
            state_conditions=conditions,
            task_goals=goals,
            plan=[
                "find the printer",
                f"put the {printer_cartridge.readable_name} in the printer",
                "turn on the printer",
            ],
            preparation_plan=[
                "go to the breakroom",
                f"pick up the {printer_cartridge.readable_name}",
                "go to the robotics lab",
            ],
        )

    # Register versions of the challenges without color variants
    high_level_key = HighLevelKey(
        action="interact",
        interaction_object=printer.object_id,
        target_object=printer_cartridge.object_id,
        converted_object=printer_spawned_object.object_id,
    )

    ChallengeBuilder.register(high_level_key)(create_mission)


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
    for office_layout in get_args(OfficeLayout):
        for object_instance_id, converted_object_id in object_instance_ids:
            create_operate_printer_challenges(
                printer_cartridge=RequiredObject(name=object_instance_id),
                printer_spawned_object=converted_object_id,
                office_layout=office_layout,
            )
