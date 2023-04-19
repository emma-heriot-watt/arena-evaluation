from typing import Literal, Optional
from typing_extensions import Self

from convert_case import kebab_case, snake_case, title_case
from pydantic import BaseModel, validator

from arena_missions.constants.arena import ObjectColor
from arena_missions.structures.object_id import ObjectId


InstructionAction = Literal[
    "break",
    "clean",
    "close",
    "fill",
    "interact",
    "open",
    "pickup",
    "place",
    "pour",
    "scan",
    "toggle",
    "change_color",
]


class HighLevelKey(BaseModel, validate_assignment=True, frozen=True, extra="forbid"):
    """Structured form of the High-Level Key."""

    action: InstructionAction

    target_object: ObjectId
    target_object_color: Optional[ObjectColor] = None

    interaction_object: Optional[ObjectId] = None
    interaction_object_color: Optional[ObjectColor] = None

    converted_object: Optional[ObjectId] = None
    converted_object_color: Optional[ObjectColor] = None

    from_receptacle: Optional[ObjectId] = None
    from_receptacle_color: Optional[ObjectColor] = None
    from_receptacle_is_container: bool = False

    to_receptacle: Optional[ObjectId] = None
    to_receptacle_color: Optional[ObjectColor] = None
    to_receptacle_is_container: bool = False

    def __str__(self) -> str:
        """Return the string representation of the high-level key."""
        return self.key

    @classmethod
    def from_string(cls, key_string: str) -> Self:
        """Create the high-level key from the string."""
        high_level_key_dict = {}

        # Split the key by the # character
        parts = [part for part in key_string.split("#") if part]

        for part in parts:
            # Split each part by the = character
            split_part = part.split("=")

            # Convert the key to snake_case
            part_name = split_part[0]
            part_name = snake_case(part_name)

            # If the part_name is going to hold a boolean and the value does not exist, set it to
            # True since it is a flag
            if part_name.endswith("is_container") and len(split_part) == 1:
                part_value = "true"
            # Otherwise, set it to the 2nd part of the split
            elif len(split_part) == 2:
                part_value = split_part[1]
            # Otherwise, raise an error
            else:
                raise ValueError(f"Each split part should contain 2 pieces, received {part}")

            # Add it to the dictionary
            high_level_key_dict[part_name] = part_value

        # Parse it with pydantic
        return cls.parse_obj(high_level_key_dict)

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

    @property
    def key(self) -> str:
        """Get the high-level key as a string."""
        parts: list[str] = []

        for part_name, part_value in self.dict().items():
            if part_value:
                part_name = kebab_case(part_name)
                if isinstance(part_value, bool):
                    parts.append(f"#{part_name}")
                else:
                    parts.append(f"#{part_name}={part_value}")

        return "".join(parts)
