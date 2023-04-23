from typing import Literal, Optional

from arena_missions.constants.arena import OfficeRoom
from arena_missions.structures import ObjectInstanceId, RequiredObject, RequiredObjectState


class RequiredObjectBuilder:
    """Simplify object building within the arena."""

    num_doors: int = 7
    num_light_switches: int = 8
    num_broken_cords: int = 3
    num_gray_fuse_boxes: int = 2
    num_red_fuse_boxes: int = 1
    num_computer_monitors: int = 5
    max_num_lab1_desks: int = 5
    max_num_lab2_desks: int = 3

    def default_objects(self) -> list[RequiredObject]:
        """Generate all default objects for the arena."""
        return [
            *self.doors(),
            *self.light_switches(),
            *self.broken_cords(),
            *self.fuse_boxes(),
            *self.computer_monitors(),
        ]

    def color_changer(self) -> RequiredObject:
        """Generate the color changer for the arena."""
        return RequiredObject.from_string("ColorChangerStation_1")

    def doors(self, *, is_open: bool = True) -> list[RequiredObject]:
        """Generate all 7 doors for the arena."""
        return [
            RequiredObject(
                name=ObjectInstanceId.parse(f"Door_01_{door_num}"),
                state=[RequiredObjectState.from_parts("isOpen", "true" if is_open else "false")],
            )
            for door_num in range(1, self.num_doors + 1)
        ]

    def light_switches(self) -> list[RequiredObject]:
        """Generate all 8 light switches for the arena."""
        return [
            RequiredObject(
                name=ObjectInstanceId.parse(f"LightSwitch_01_{switch_num}"),
            )
            for switch_num in range(1, self.num_light_switches + 1)
        ]

    def broken_cords(self, *, is_on: bool = False) -> list[RequiredObject]:
        """Generate all 3 broken cords for the arena."""
        return [
            RequiredObject(
                name=ObjectInstanceId.parse(f"Broken_Cord_01_{cord_num}"),
                state=[
                    RequiredObjectState.from_parts("isToggledOn", "true" if is_on else "false")
                ],
            )
            for cord_num in range(1, self.num_broken_cords + 1)
        ]

    def fuse_boxes(self) -> list[RequiredObject]:
        """Generate all fuse boxes for the arena."""
        gray_fuse_boxes = [
            RequiredObject(name=ObjectInstanceId.parse(f"FuseBox_01_{fuse_box_num}"))
            for fuse_box_num in range(1, self.num_gray_fuse_boxes + 1)
        ]
        red_fuse_boxes = [
            RequiredObject(name=ObjectInstanceId.parse(f"FuseBox_02_{fuse_box_num}"))
            for fuse_box_num in range(1, self.num_red_fuse_boxes + 1)
        ]
        return [*gray_fuse_boxes, *red_fuse_boxes]

    def computer_monitors(self) -> list[RequiredObject]:
        """Generate all computer monitors for the arena."""
        return [
            RequiredObject(name=ObjectInstanceId.parse(f"Computer_Monitor_01_{monitor_num}"))
            for monitor_num in range(1, self.num_computer_monitors + 1)
        ]

    def freeze_ray(self) -> RequiredObject:
        """Generate the freeze ray for the arena."""
        return RequiredObject(name=ObjectInstanceId.parse("FreezeRay_1"))

    def emotion_tester(self) -> RequiredObject:
        """Generate the emotion tester for the arena."""
        return RequiredObject(name=ObjectInstanceId.parse("TAMPrototypeHead_01_1"))

    def portal_generator(self) -> RequiredObject:
        """Generate the portal generator for the arena."""
        return RequiredObject(name=ObjectInstanceId.parse("PortalGenerator_10000"))

    def laser(self) -> RequiredObject:
        """Generate the laser for the arena."""
        return RequiredObject(name=ObjectInstanceId.parse("Laser_1"))

    def gravity_pad(self) -> RequiredObject:
        """Generate the gravity pad for the arena."""
        return RequiredObject(name=ObjectInstanceId.parse("GravityPad_1"))

    def fridge(self, *, room: OfficeRoom = "BreakRoom", is_open: bool = False) -> RequiredObject:
        """Generate the fridge for the arena."""
        return RequiredObject(
            name=ObjectInstanceId.parse("FridgeLower_02_1"),
            state=[
                RequiredObjectState.from_parts("isOpen", "true" if is_open else "false"),
                RequiredObjectState.from_parts("removeInitialContainedItems", "true"),
            ],
            roomLocation=[room],
        )

    def freezer(self, *, room: OfficeRoom = "BreakRoom", is_open: bool = False) -> RequiredObject:
        """Generate the freezer for the arena."""
        return RequiredObject(
            name=ObjectInstanceId.parse("FridgeUpper_02_1"),
            state=[
                RequiredObjectState.from_parts("isOpen", "true" if is_open else "false"),
                RequiredObjectState.from_parts("removeInitialContainedItems", "true"),
            ],
            roomLocation=[room],
        )

    def time_machine(self, *, room: OfficeRoom = "BreakRoom") -> RequiredObject:
        """Generate the time machine for the arena."""
        return RequiredObject(
            name=ObjectInstanceId.parse("YesterdayMachine_01_1"), roomLocation=[room]
        )

    def carrot_maker(self, *, room: OfficeRoom = "Lab2") -> RequiredObject:
        """Generate the carrot maker for the arena."""
        return RequiredObject(name=ObjectInstanceId.parse("EAC_Machine_1"), roomLocation=[room])

    def microwave(self, *, room: OfficeRoom = "BreakRoom") -> RequiredObject:
        """Generate the microwave for the arena."""
        return RequiredObject(
            name=ObjectInstanceId.parse("Microwave_01_1"),
            state=[
                RequiredObjectState.from_parts("removeInitialContainedItems", "true"),
            ],
            roomLocation=[room],
        )

    def robotic_arm(self, *, is_arm_lifted: bool = True) -> RequiredObject:
        """Generate the robotic arm for the arena."""
        return RequiredObject(
            name=ObjectInstanceId.parse("RoboticArm_01_1"),
            state=[
                RequiredObjectState.from_parts("isToggledOn", "true" if is_arm_lifted else "false")
            ],
        )

    def fork_lift(self, *, is_fork_lifted: bool = True) -> RequiredObject:
        """Generate the fork lift for the arena."""
        return RequiredObject(
            name=ObjectInstanceId.parse("ForkLift_1"),
            state=[
                RequiredObjectState.from_parts(
                    "isToggledOn", "true" if is_fork_lifted else "false"
                )
            ],
        )

    def coffee_pot(
        self, *, fill_with: Optional[Literal["Coffee", "Water"]] = None
    ) -> RequiredObject:
        """Generate the coffee pot for the arena."""
        coffee_pot = RequiredObject(
            name=ObjectInstanceId.parse("CoffeePot_01_1"), roomLocation=["BreakRoom"]
        )

        if fill_with == "Coffee":
            coffee_pot.update_state("isFilled", "Coffee")
            coffee_pot.update_state("isHot", "true")

        if fill_with == "Water":
            coffee_pot.update_state("isFilled", "Water")

        return coffee_pot

    def coffee_unmaker(self) -> RequiredObject:
        """Generate the coffee unmaker for the arena."""
        return RequiredObject(
            name=ObjectInstanceId.parse("CoffeeUnMaker_01_1"), roomLocation=["BreakRoom"]
        )

    def breakroom_table(self) -> RequiredObject:
        """Create the round table in the breakroom."""
        return RequiredObject(
            name=ObjectInstanceId.parse("TableRound_02_1"),
            state=[RequiredObjectState.from_parts("removeInitialContainedItems", "true")],
            roomLocation=["BreakRoom"],
        )

    def breakroom_countertop(self) -> RequiredObject:
        """Create the countertop in the breakroom."""
        return RequiredObject(
            name=ObjectInstanceId.parse("KitchenCounterTop_02_1"),
            state=[RequiredObjectState.from_parts("removeInitialContainedItems", "true")],
            roomLocation=["BreakRoom"],
        )

    def printer(self) -> RequiredObject:
        """Generate the printer for the arena."""
        return RequiredObject(name=ObjectInstanceId.parse("Printer_3D_1"))

    def main_office_desks(self) -> list[RequiredObject]:
        """Returns office desks in main office."""
        desk_names = [
            "AP_Prop_Desk_Blue",
            "AP_Prop_Desk_Green",
            "AP_Prop_Desk_Red",
        ]

        desk_objects = []

        for desk_name in desk_names:
            desk_objects.append(
                RequiredObject(
                    name=ObjectInstanceId.parse(f"{desk_name}_1"),
                    state=[RequiredObjectState.from_parts("removeInitialContainedItems", "true")],
                    roomLocation=["MainOffice"],
                )
            )

        return desk_objects

    def reception_desk(self) -> RequiredObject:
        """Returns the reception desk in the reception."""
        return RequiredObject(
            name=ObjectInstanceId.parse("ReceptionDesk_1"),
            state=[RequiredObjectState.from_parts("removeInitialContainedItems", "true")],
            roomLocation=["Reception"],
        )

    def manager_desk(self) -> RequiredObject:
        """Returns the manager desk in the small office."""
        return RequiredObject(
            name=ObjectInstanceId.parse("ManagerDesk_1"),
            state=[RequiredObjectState.from_parts("removeInitialContainedItems", "true")],
            roomLocation=["SmallOffice"],
        )

    def warehouse_cabinet(self) -> RequiredObject:
        """Returns the warehouse cabinet."""
        return RequiredObject(
            name=ObjectInstanceId.parse("KitchenCabinet_02_1"), roomLocation=["Warehouse"]
        )

    def warehouse_metal_table(self) -> RequiredObject:
        """Returns the warehouse metal table."""
        return RequiredObject(
            name=ObjectInstanceId.parse("Table_Metal_01_1"), roomLocation=["Warehouse"]
        )

    def warehouse_wooden_table(self) -> RequiredObject:
        """Returns the warehouse wooden table."""
        return RequiredObject(
            name=ObjectInstanceId.parse("SM_Prop_Table_02_1"), roomLocation=["Warehouse"]
        )

    def lab1_desks(self) -> list[RequiredObject]:
        """Returns desks in the Lab1."""
        desk_format = "Desk_01_{instance_count}"

        desks = []

        for desk_idx in range(1, self.max_num_lab1_desks + 1):
            desk_id = ObjectInstanceId.parse(desk_format.format(instance_count=desk_idx))
            desk = RequiredObject(name=desk_id)
            desk.add_state("Unique", "true")
            desk.update_room("Lab1")
            desks.append(desk)

        return desks

    def lab2_desks(self) -> list[RequiredObject]:
        """Returns desks in the Lab2."""
        desk_format = "Desk_01_{instance_count}"

        desks = []

        for desk_idx in range(1, self.max_num_lab2_desks + 1):
            desk_id = ObjectInstanceId.parse(desk_format.format(instance_count=desk_idx))
            desk = RequiredObject(name=desk_id)
            desk.add_state("Unique", "true")
            desk.update_room("Lab2")
            desks.append(desk)

        return desks
