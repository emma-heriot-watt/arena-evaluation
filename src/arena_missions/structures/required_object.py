from collections import ChainMap
from typing import Any, Literal, Optional, Union, get_args

from pydantic import BaseModel, Field, root_validator, validator

from arena_missions.constants.arena import (
    BooleanStr,
    LiquidType,
    ObjectColor,
    OfficeRoom,
    RequiredObjectStateName,
    SpawnRelation,
)
from arena_missions.structures.object_id import ObjectId, ObjectInstanceId


RequiredObjectStateValue = Union[BooleanStr, LiquidType]


class RequiredObjectState(BaseModel, validate_assignment=True):
    """Spawn state of a required object."""

    __root__: dict[RequiredObjectStateName, RequiredObjectStateValue]

    def __len__(self) -> int:
        """Get the length of the state."""
        return len(self.__root__)

    @classmethod
    def from_parts(
        cls, state_name: RequiredObjectStateName, state_value: RequiredObjectStateValue
    ) -> "RequiredObjectState":
        """Create a required object spawn state from parts."""
        return cls.parse_obj({state_name: state_value})

    @validator("__root__")
    @classmethod
    def ensure_only_one_key(
        cls, root: dict[RequiredObjectStateName, RequiredObjectStateValue]
    ) -> dict[RequiredObjectStateName, RequiredObjectStateValue]:
        """Ensure that there is only one key in the dictionary."""
        if len(root) != 1:
            raise ValueError("State must only have one key.")
        return root

    @validator("__root__")
    @classmethod
    def validate_state_value_for_key(
        cls, root: dict[RequiredObjectStateName, RequiredObjectStateValue]
    ) -> dict[RequiredObjectStateName, RequiredObjectStateValue]:
        """Validate the state value for the state key."""
        state_key, state_value = list(root.items())[0]

        if state_key == "isFilled":
            if state_value not in get_args(LiquidType):
                raise ValueError(f"{state_value} is not a valid liquid type.")

        elif state_value not in get_args(BooleanStr):
            raise ValueError(f"{state_value} is not a valid boolean string.")

        return root

    @property
    def name(self) -> RequiredObjectStateName:
        """Get the name of the state."""
        return list(self.__root__.keys())[0]

    @property
    def value(self) -> RequiredObjectStateValue:  # noqa: WPS110
        """Get the value of the state."""
        return list(self.__root__.values())[0]


class RequiredObject(BaseModel, validate_assignment=True):
    """Object within the Arena."""

    name: ObjectInstanceId
    state: list[RequiredObjectState] = Field(default_factory=list, unique_items=True)
    location: list[dict[ObjectInstanceId, SpawnRelation]] = Field(
        default_factory=list, unique_items=True, max_items=1
    )
    room_location: list[OfficeRoom] = Field(
        default_factory=list, max_items=1, alias="roomLocation"
    )
    colors: list[ObjectColor] = Field(default_factory=list, unique_items=True, max_items=1)

    # This is only used with the Carrot
    yesterday_state: Union[Literal[""], ObjectId] = Field(default="", alias="yesterdayState")

    # Unknown/Unused fields
    condition: dict[Any, Any] = Field(default_factory=dict)
    printing_object: str = Field(default="", alias="printingObject", const=True)
    associated_past_portals: list[Any] = Field(default_factory=list, alias="associatedPastPortals")
    associated_future_portals: list[Any] = Field(
        default_factory=list, alias="associatedFuturePortals"
    )
    current_portal: str = Field(default="", alias="currentPortal")
    dino_food: str = Field(default="", alias="dinoFood")

    @classmethod
    def from_string(cls, object_instance_id: str) -> "RequiredObject":
        """Instantiate a RequiredObject from the object instance ID."""
        return cls(name=ObjectInstanceId(object_instance_id))

    @validator("state", "location", each_item=True)
    @classmethod
    def ensure_each_state_has_only_one_key(cls, state: dict[str, str]) -> dict[str, str]:
        """Ensure that each state/location dict has only one key."""
        if len(state) != 1:
            raise ValueError("Each state must have only one key")
        return state

    @validator("yesterday_state")
    @classmethod
    def only_carrot_can_have_yesterday_state(
        cls, yesterday_state: str, values: dict[str, Any]  # noqa: WPS110
    ) -> str:
        """Only carrots can have yesterdayState."""
        if yesterday_state:
            if not values["name"].startswith("Carrot_01"):
                raise ValueError("Only Carrot can have yesterdayState")

        return yesterday_state

    @root_validator(pre=True)
    @classmethod
    def add_color_changed_state_if_colors(
        cls, values: dict[str, Any]  # noqa: WPS110
    ) -> dict[str, Any]:
        """Add colorChanged state if colors are present."""
        if "colors" in values and values["colors"]:
            merged_states = dict(ChainMap(*values["state"]))
            merged_states["isColorChanged"] = "true"
            values["state"] = [{k: v} for k, v in merged_states.items()]

        return values

    @property
    def receptacle(self) -> Optional[ObjectInstanceId]:
        """Return the receptacle this object is in."""
        if self.location:
            return list(self.location[0].keys())[0]
        return None

    @property
    def room(self) -> Optional[OfficeRoom]:
        """Return the room this object is in."""
        if self.room_location:
            return self.room_location[0]
        return None

    @property
    def color(self) -> Optional[ObjectColor]:
        """Return the color of this object."""
        if self.colors:
            return self.colors[0]
        return None

    def update_receptacle(self, receptacle: Optional[ObjectInstanceId]) -> None:
        """Set the receptacle this object is in."""
        if not receptacle:
            self.location.clear()
            return

        self.location.append({receptacle: "in"})

    def update_room(self, room: Optional[OfficeRoom]) -> None:
        """Set the room this object is in."""
        if not room:
            self.room_location.clear()
            return

        self.room_location[0] = room

    def update_color(self, color: Optional[ObjectColor]) -> None:
        """Set the color of this object."""
        if not color:
            self.colors.clear()
            return

        self.colors[0] = color

    def update_state(
        self, state_name: RequiredObjectStateName, state_value: Union[str, bool, None]
    ) -> None:
        """Update the state of this object."""
        # Remove the state from the list if it already exists
        self.state = [state for state in self.state if state.name != state_name]  # noqa: WPS601

        # Add the state to the list if it is not None
        if state_value is not None:
            self.state.append(
                RequiredObjectState.parse_obj({state_name: str(state_value).lower()})
            )

    def add_state(
        self, state_name: RequiredObjectStateName, state_value: Union[str, bool]
    ) -> None:
        """Add state to this object."""
        return self.update_state(state_name, state_value)

    def remove_state(self, state_name: RequiredObjectStateName) -> None:
        """Remove the state from this object."""
        return self.update_state(state_name, None)
