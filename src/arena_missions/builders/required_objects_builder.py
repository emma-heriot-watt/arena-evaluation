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

    def default_objects(self) -> list[RequiredObject]:
        """Generate all default objects for the arena."""
        return [
            *self.doors(),
            *self.light_switches(),
            *self.broken_cords(),
            *self.fuse_boxes(),
            *self.computer_monitors(),
        ]

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
            state=[RequiredObjectState.from_parts("isOpen", "true" if is_open else "false")],
            roomLocation=[room],
        )

    def freezer(self, *, room: OfficeRoom = "BreakRoom", is_open: bool = False) -> RequiredObject:
        """Generate the freezer for the arena."""
        return RequiredObject(
            name=ObjectInstanceId.parse("FridgeUpper_02_1"),
            state=[RequiredObjectState.from_parts("isOpen", "true" if is_open else "false")],
            roomLocation=[room],
        )

    def time_machine(self, *, room: OfficeRoom = "BreakRoom") -> RequiredObject:
        """Generate the time machine for the arena."""
        return RequiredObject(
            name=ObjectInstanceId.parse("YesterdayMachine_01_1"), roomLocation=[room]
        )

    def robotic_arm(self, *, is_arm_lifted: bool = True) -> RequiredObject:
        """Generate the robotic arm for the arena."""
        return RequiredObject(
            name=ObjectInstanceId.parse("RoboticArm_01_1"),
            state=[
                RequiredObjectState.from_parts("isToggledOn", "true" if is_arm_lifted else "false")
            ],
        )
