from collections.abc import Generator
from typing import Any, Callable, Literal, Union, cast, get_args
from typing_extensions import Self

from pydantic import BaseModel, Field, validator

from arena_missions.constants.arena import BooleanStr, FluidType, GoalStateExpressionKey
from arena_missions.structures.object_id import ObjectInstanceId
from arena_missions.structures.state_condition import StateCondition


TASK_GOAL_VISIBILITY = {  # noqa: WPS407
    "isHidden": False,
    "activationInteractable": "ALWAYS UNLOCKED",
    "stickyNoteIndex": 0,
}


ObjectGoalStateRelation = Literal[
    # "and" is not allowed. This is because "and" does not work the way you think it does.
    # "and",
    "or",
]

GoalStateExpressionValue = Union[BooleanStr, ObjectInstanceId, FluidType]


class ObjectGoalStateExpression(str):  # noqa: WPS600
    """A goal object state value."""

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[..., Self], None, None]:
        """Return a generator of validators for this type."""
        yield cls.validate

    @classmethod
    def parse(cls, v: Any) -> Self:
        """Parse the input."""
        return cls.validate(v)

    @classmethod
    def validate(cls, v: Any) -> Self:  # noqa: WPS231
        """Validate the object goal state expression."""
        if not isinstance(v, str):
            raise TypeError("Goal object state value must be a string")

        state_condition_key, state_condition_value = v.split("=")

        # Make sure the state condition key is a valid state
        # if state_condition_key not in get_args(GoalStateExpressionKey):
        #     raise ValueError(f"{state_condition_key} is not a valid state condition.")

        # If the state condition key is contains, then the value should be an ObjectInstanceId
        if state_condition_key == "Contains":
            ObjectInstanceId(state_condition_value)

        # If the state condition key is isFilled, then the value should be a LiquidType
        elif state_condition_key == "isFilled":
            if state_condition_value not in get_args(FluidType):
                raise ValueError(f"{state_condition_value} must be a valid liquid type.")

        # Otherwise, the value should be a boolean string
        elif state_condition_value not in get_args(BooleanStr):
            raise ValueError("Goal object state value must be true or false")

        return cls(v)

    @classmethod
    def from_parts(
        cls,
        state_condition_key: Union[str, GoalStateExpressionKey],
        state_condition_value: GoalStateExpressionValue,
    ) -> Self:
        """Create a goal object state value from its parts."""
        return cls.parse(f"{state_condition_key}={state_condition_value}")

    @property
    def state_condition_key(self) -> Union[str, GoalStateExpressionKey]:
        """Return the state condition key."""
        return self.split("=")[0]

    @property
    def state_condition_value(self) -> GoalStateExpressionValue:
        """Return the state condition value."""
        state_condition_value = self.split("=")[1]

        if self.state_condition_key == "Contains":
            return ObjectInstanceId.parse(state_condition_value)

        if self.state_condition_key == "isFilled":
            return cast(FluidType, state_condition_value)

        return cast(BooleanStr, state_condition_value)


class ObjectGoalState(BaseModel):
    """A goal object state."""

    __root__: dict[ObjectInstanceId, ObjectGoalStateExpression]

    def __len__(self) -> int:
        """Return the length of the root dict."""
        return len(self.__root__)

    @classmethod
    def from_parts(
        cls,
        object_instance_id: ObjectInstanceId,
        state_condition_key: Union[str, GoalStateExpressionKey],
        state_condition_value: GoalStateExpressionValue,
    ) -> Self:
        """Create a goal object state from its parts."""
        return cls(
            __root__={
                object_instance_id: ObjectGoalStateExpression.from_parts(
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
    def state_condition_key(self) -> Union[str, GoalStateExpressionKey]:
        """Return the state condition key."""
        return list(self.__root__.values())[0].state_condition_key

    @property
    def state_condition_value(self) -> GoalStateExpressionValue:
        """Return the state condition value."""
        return list(self.__root__.values())[0].state_condition_value


class TaskGoal(BaseModel):
    """Task goal within the Arena."""

    object_states: list[ObjectGoalState] = Field(..., unique_items=True, min_items=1)
    object_states_relation: ObjectGoalStateRelation = "or"

    # This will be automatically set later
    goal_id: int = 0

    # Unused/Ignored fields
    description: str = Field(default="")
    preconditions: list[Any] = Field(default_factory=list)
    visibility: dict[str, Any] = Field(default=TASK_GOAL_VISIBILITY)
    can_reset: bool = Field(default=False, alias="canReset")

    @classmethod
    def from_object_goal_states(cls, object_states: list[ObjectGoalState]) -> "TaskGoal":
        """Create the goal from the object states."""
        return cls(object_states=object_states)

    @classmethod
    def from_state_condition(cls, state_condition: StateCondition) -> "TaskGoal":
        """Create the goal from the state condition."""
        return cls.from_object_goal_states(
            [
                ObjectGoalState.from_parts(
                    state_condition.instance_id,
                    state_condition.state_name,
                    state_condition.state_value,
                )
            ]
        )

    @validator("object_states", each_item=True)
    @classmethod
    def ensure_each_state_has_only_one_key(cls, state: dict[str, str]) -> dict[str, str]:
        """Ensure that each state/location dict has only one key."""
        if len(state) != 1:
            raise ValueError("Each state must have only one key")
        return state
