from collections.abc import Generator, Mapping
from types import MappingProxyType
from typing import Any, Callable, Literal, Union, cast, get_args

from pydantic import BaseModel, Field, validator

from arena_missions.constants.arena import BooleanStr, GoalStateExpressionKey, LiquidType
from arena_missions.structures.object_id import ObjectInstanceId


TASK_GOAL_VISIBILITY = MappingProxyType(
    {
        "isHidden": False,
        "activationInteractable": "ALWAYS UNLOCKED",
        "stickyNoteIndex": 0,
    }
)


GoalStateExpressionValue = Union[BooleanStr, ObjectInstanceId, LiquidType]


class ObjectGoalStateExpression(str):  # noqa: WPS600
    """A goal object state value."""

    @classmethod
    def __get_validators__(
        cls,
    ) -> Generator[Callable[..., "ObjectGoalStateExpression"], None, None]:
        """Return a generator of validators for this type."""
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> "ObjectGoalStateExpression":  # noqa: WPS231, WPS238
        """Validate the object goal state expression."""
        if not isinstance(v, str):
            raise TypeError("Goal object state value must be a string")

        state_condition_key, state_condition_value = v.split("=")

        # Make sure the state condition key is a valid state
        if state_condition_key not in get_args(GoalStateExpressionKey):
            raise ValueError(f"{state_condition_key} is not a valid state condition.")

        # If the state condition key is contains, then the value should be an ObjectInstanceId
        if state_condition_key == "Contains":
            ObjectInstanceId(state_condition_value)

        # If the state condition key is isFilled, then the value should be a LiquidType
        elif state_condition_key == "isFilled":
            if state_condition_value not in get_args(LiquidType):
                raise ValueError(f"{state_condition_value} must be a valid liquid type.")

        # Otherwise, the value should be a boolean string
        else:
            if v not in get_args(BooleanStr):  # noqa: WPS513
                raise ValueError("Goal object state value must be true or false")

        return cls(v)

    @classmethod
    def from_parts(
        cls,
        state_condition_key: GoalStateExpressionKey,
        state_condition_value: GoalStateExpressionValue,
    ) -> "ObjectGoalStateExpression":
        """Create a goal object state value from its parts."""
        return cls(f"{state_condition_key}={state_condition_value}")

    def __repr__(self) -> str:
        """Return a string representation of the goal object state value."""
        return f"ObjectGoalStateExpression({super().__repr__()})"

    @property
    def state_condition_key(self) -> GoalStateExpressionKey:
        """Return the state condition key."""
        return cast(GoalStateExpressionKey, self.split("=")[0])

    @property
    def state_condition_value(self) -> GoalStateExpressionValue:
        """Return the state condition value."""
        state_condition_value = self.split("=")[1]

        if self.state_condition_key == "Contains":
            return ObjectInstanceId(state_condition_value)

        if self.state_condition_key == "isFilled":
            return cast(LiquidType, state_condition_value)

        return cast(BooleanStr, state_condition_value)


class ObjectGoalState(BaseModel):
    """A goal object state."""

    __root__: dict[ObjectInstanceId, ObjectGoalStateExpression]

    @classmethod
    def from_parts(
        cls,
        object_id: ObjectInstanceId,
        state_condition_key: GoalStateExpressionKey,
        state_condition_value: GoalStateExpressionValue,
    ) -> "ObjectGoalState":
        """Create a goal object state from its parts."""
        return cls.parse_obj(
            {
                object_id: ObjectGoalStateExpression.from_parts(
                    state_condition_key, state_condition_value
                )
            }
        )

    @validator("__root__")
    @classmethod
    def ensure_only_one_key(
        cls, root: dict[ObjectInstanceId, ObjectGoalStateExpression]
    ) -> dict[ObjectInstanceId, ObjectGoalStateExpression]:
        """Ensure that the root dict has only one key."""
        if len(root) != 1:
            raise ValueError("State must have only one key")
        return root

    @property
    def object_instance_id(self) -> ObjectInstanceId:
        """Return the object instance id."""
        return list(self.__root__.keys())[0]

    @property
    def state_condition_key(self) -> GoalStateExpressionKey:
        """Return the state condition key."""
        return list(self.__root__.values())[0].state_condition_key

    @property
    def state_condition_value(self) -> GoalStateExpressionValue:
        """Return the state condition value."""
        return list(self.__root__.values())[0].state_condition_value


ObjectGoalStateRelation = Literal["and", "or"]


class TaskGoal(BaseModel):
    """Task goal within the Arena."""

    object_states: list[ObjectGoalState] = Field(..., unique_items=True, min_items=1)
    object_states_relation: ObjectGoalStateRelation

    # This will be automatically set later
    goal_id: int = 0

    # Unused/Ignored fields
    description: str = Field(default="")
    preconditions: list[Any] = Field(default_factory=list, const=True)
    visibility: Mapping[str, Any] = Field(default=TASK_GOAL_VISIBILITY, const=True)
    can_reset: bool = Field(default=False, alias="canReset", const=True)

    @classmethod
    def from_object_goal_states(
        cls, object_states: list[ObjectGoalState], relation: ObjectGoalStateRelation
    ) -> "TaskGoal":
        """Create the goal from the object states."""
        return cls(object_states=object_states, object_states_relation=relation)

    @validator("object_states", each_item=True)
    @classmethod
    def ensure_each_state_has_only_one_key(cls, state: dict[str, str]) -> dict[str, str]:
        """Ensure that each state/location dict has only one key."""
        if len(state) != 1:
            raise ValueError("Each state must have only one key")
        return state