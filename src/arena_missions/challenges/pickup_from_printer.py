from typing import get_args

from arena_missions.builders import ChallengeBuilder, ChallengeBuilderOutput, RequiredObjectBuilder
from arena_missions.constants.arena import OfficeLayout
from arena_missions.structures import (
    AndExpression,
    ContainsExpression,
    HighLevelKey,
    ObjectGoalState,
    ObjectInstanceId,
    RequiredObject,
    StateCondition,
    StateExpression,
    TaskGoal,
)


def create_pickup_from_printer_challenges(
    printer_cartridge: RequiredObject,
    printer_spawned_object_id: ObjectInstanceId,
    office_layout: OfficeLayout,
) -> None:
    """Register challenges."""
    required_object_builder = RequiredObjectBuilder()

    # Create the printer
    printer = required_object_builder.printer()

    # Make sure the cartridge is unique
    printer_cartridge.add_state("Unique", "true")

    # Ensure the robotic arm is out the way
    robotic_arm = required_object_builder.robotic_arm()

    # Create the breakroom table
    breakroom_table = required_object_builder.breakroom_table()
    printer_cartridge.update_receptacle(breakroom_table.name)

    # Success conditions
    conditions = [
        # [PREP] Ensure the machine is used on the target
        StateCondition(
            stateName="PrinterUsed",
            context=printer.name,
            expression=StateExpression.from_expression(
                AndExpression.from_expressions(
                    ContainsExpression(
                        target=printer.name, contains=printer_spawned_object_id.with_asterisk
                    ),
                    ContainsExpression(
                        target=printer.name, contains=printer_cartridge.name.with_asterisk
                    ),
                )
            ),
        ),
    ]

    goals = [
        *[TaskGoal.from_state_condition(condition) for condition in conditions],
        # Pick up the target object
        TaskGoal.from_object_goal_states(
            [
                ObjectGoalState.from_parts(
                    printer_spawned_object_id.with_asterisk, "isPickedUp", "true"
                )
            ]
        ),
    ]

    # Create mission
    def create_mission() -> ChallengeBuilderOutput:
        return ChallengeBuilderOutput(
            start_room="Lab1",
            office_layout=office_layout,
            required_objects={
                breakroom_table.name: breakroom_table,
                printer.name: printer,
                printer_cartridge.name: printer_cartridge,
                robotic_arm.name: robotic_arm,
            },
            state_conditions=conditions,
            task_goals=goals,
            plan=[
                f"pick up the {printer_spawned_object_id.readable_name} from the printer",
            ],
            preparation_plan=[
                "go to the breakroom",
                f"pick up the {printer_cartridge.readable_name}",
                "go to the robotics lab",
                "go to the printer",
                f"put the {printer_cartridge.readable_name} in the printer",
                "turn on the printer",
            ],
        )

    # Register versions of the challenges without color variants
    high_level_key = HighLevelKey(
        action="pickup",
        target_object=printer_spawned_object_id.object_id,
        from_receptacle=printer.object_id,
    )

    ChallengeBuilder.register(high_level_key)(create_mission)


def register_pickup_from_printer_challenges() -> None:
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
        for printer_cartridge_id, converted_object_id in object_instance_ids:
            create_pickup_from_printer_challenges(
                printer_cartridge=RequiredObject(name=printer_cartridge_id),
                printer_spawned_object_id=converted_object_id,
                office_layout=office_layout,
            )
