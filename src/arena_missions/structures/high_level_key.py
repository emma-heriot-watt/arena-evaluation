from typing import Literal, Optional

from convert_case import snake_case, title_case
from pydantic import BaseModel, validator

from arena_missions.constants.arena import ObjectColor


OperateAction = Literal[
    "3dprinter",
    "coffeemaker",
    "coffeeunmaker",
    "colorchanger",
    "embiggenator",
    "gravitypad",
    "microwave",
    "timemachine",
]
InstructionAction = Literal[
    "break",
    "clean",
    "close",
    "fill",
    "open",
    "pickup",
    "place",
    "pour",
    "scan",
    "toggle",
]


class HighLevelKey(BaseModel):
    """Structured form of the High-Level Key."""

    key: str

    action: Literal[InstructionAction, OperateAction]

    target_object: str
    target_object_color: Optional[ObjectColor] = None

    converted_object: Optional[str] = None
    converted_object_color: Optional[ObjectColor] = None

    from_receptacle: Optional[str] = None
    from_receptacle_color: Optional[ObjectColor] = None
    from_receptacle_is_container: bool = False

    to_receptacle: Optional[str] = None
    to_receptacle_color: Optional[ObjectColor] = None
    to_receptacle_is_container: bool = False

    def __str__(self) -> str:
        """Return the string representation of the high-level key."""
        return self.key

    @classmethod
    def from_string(cls, key_string: str) -> "HighLevelKey":
        """Create the high-level key from the string."""
        high_level_key_dict = {}

        # Split the key by the # character
        parts = key_string.split("#")

        for part in parts:
            # Split each part by the = character
            part_name, part_value = part.split("=")

            # Convert the key to snake_case
            part_name = snake_case(part_name)

            # If the part_name is going to hold a boolean and the value does not exist, set it to
            # True since it is a flag
            if part_name.endswith("is-container") and not part_value:
                part_value = "true"

            # Add it to the dictionary
            high_level_key_dict[part_name] = part_value

        # Parse it with pydantic
        return cls.parse_obj({**high_level_key_dict, "key": key_string})

    @validator(
        "target_object_color",
        "converted_object_color",
        "from_receptacle_color",
        "to_receptacle_color",
        pre=True,
    )
    @classmethod
    def format_color_string(cls, color: Optional[str]) -> Optional[str]:
        """Format the color to be in title case."""
        if color:
            color = title_case(color)
        return color
