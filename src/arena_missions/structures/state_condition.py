from typing import Generic, Literal, TypeVar
from typing_extensions import Self

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

from arena_missions.constants.arena import FluidType, ObjectColor
from arena_missions.structures.object_id import ObjectInstanceId


T = TypeVar("T")

# Things that can be expressed as state conditions
ExpressionType = Literal[
    "CanBeSeen",
    "isFilledWith",
    "IsInRange",
    "isToggledOn",
    "isPickedUp",
    "isPowered",
    "isBroken",
    "isOpen",
    "isScanned",
    "isUsed",
    "isOverloaded",
    "isEmbiggenated",
    "isDirty",
    "isHot",
    "isCold",
    "OR",
    "AND",
    "NOT",
    "Contains",
    "DinoFed",
    "ColorMetaDataChange",
    "IsReceptacle",
    "isFullOfItems",
]


class Expression(BaseModel):
    """Expression within a state condition.

    This is the base class that all other expressions inherit from.
    """

    _key: ExpressionType

    @property
    def key(self) -> ExpressionType:
        """Get the key for the expression."""
        if not self._key:
            raise ValueError("Key should exist for the expression.")
        return self._key


class SimpleExpression(Expression):
    """Simple expression for a state condition.

    The target is the object instance that the expression is being applied to. The message can be
    always left blank.
    """

    target: ObjectInstanceId
    message: str = Field(default="", const=True)


class ValueExpression(GenericModel, Generic[T], SimpleExpression):
    """Expression that checks if an object has a specific value."""

    value: T  # noqa: WPS110


class BoolExpression(ValueExpression[bool]):
    """Expression that checks if some property is true or false."""

    value: bool  # noqa: WPS110


class IsInRangeExpression(ValueExpression[float]):
    """Expression that checks if the target object is within the range of the current object.

    This is different to `CanBeSeen` because it checks the distance between two objects, and not
    whether or not the target object is within a certain distance of the agent.
    """

    _key = "IsInRange"
    value: float  # noqa: WPS110


class ContainsExpression(SimpleExpression):
    """Expression that checks if an object contains another object.

    I have not seen the anchor point be used, so we can ignore that, just like we do for `message`.
    """

    _key: ExpressionType = "Contains"

    contains: ObjectInstanceId
    anchor_point: str = Field(default="", const=True, alias="anchorPoint")


class IsFilledWithExpression(SimpleExpression):
    """Expression that checks if an object is filled with a specific liquid."""

    _key: ExpressionType = "isFilledWith"

    fluid: FluidType


class CanBeSeenExpression(SimpleExpression):
    """Expression that checks if an object is within some distance of the agent."""

    _key: ExpressionType = "CanBeSeen"

    distance: float


class ColorMetaDataChangeExpression(SimpleExpression):
    """Expression that checks if an object has a specific color.

    This is useful for things like the Color Changer.
    """

    _key: ExpressionType = "ColorMetaDataChange"

    color: ObjectColor = Field(..., alias="colorvalue")


class DinoFedExpression(SimpleExpression):
    """Check if the Portal Generator has the "dinoFed' property set to True."""

    _key: ExpressionType = "DinoFed"

    target: ObjectInstanceId = Field(..., regex="^PortalGenerator.*")

    # Is this even a thing? I think so, but I don't see it in the source code?
    is_fed: bool = Field(..., alias="isFed")


class IsToggledOnExpression(BoolExpression):
    """Expression that checks if an object is toggled on."""

    _key: ExpressionType = "isToggledOn"


class IsPickedUpExpression(BoolExpression):
    """Checks if the target has been picked up."""

    _key: ExpressionType = "isPickedUp"


class IsPoweredExpression(BoolExpression):
    """Check if the target has been powered."""

    _key: ExpressionType = "isPowered"


class IsBrokenExpression(BoolExpression):
    """Check if the object is broken."""

    _key: ExpressionType = "isBroken"


class IsOpenExpression(BoolExpression):
    """Check if the object is open."""

    _key: ExpressionType = "isOpen"


class IsScannedExpression(BoolExpression):
    """Check if the object has been scanned."""

    _key: ExpressionType = "isScanned"


class IsUsedExpression(BoolExpression):
    """Check if the target has been used."""

    _key: ExpressionType = "isUsed"


class IsOverloadedExpression(BoolExpression):
    """Check if the target has been overloaded."""

    _key: ExpressionType = "isOverloaded"


class IsEmbiggenatedExpression(BoolExpression):
    """Check if the target has been embiggenated."""

    _key: ExpressionType = "isEmbiggenated"


class IsDirtyExpression(BoolExpression):
    """Check if the target is dirty."""

    _key: ExpressionType = "isDirty"


class IsHotExpression(BoolExpression):
    """Check if the target is hot."""

    _key: ExpressionType = "isHot"


class IsColdExpression(BoolExpression):
    """Check if the target is cold."""

    _key: ExpressionType = "isCold"


class IsReceptacleExpression(BoolExpression):
    """Check if the target is a receptacle."""

    _key: ExpressionType = "IsReceptacle"


class IsFullOfItemsExpression(BoolExpression):
    """Check if the target is full of items."""

    _key: ExpressionType = "isFullOfItems"


class StateExpression(BaseModel):
    """State expression."""

    __root__: dict[ExpressionType, Expression]

    @classmethod
    def from_expression(cls, expression: Expression) -> "StateExpression":
        """Create a state expression from a type and an expression."""
        return cls(__root__={expression.key: expression})


class NotExpression(Expression):
    """Expression that negates another expression."""

    _key: ExpressionType = "NOT"

    expression: StateExpression
    message: str = Field(default="", const=True)


class AggregateExpression(Expression):
    """Expression that combines other expressions."""

    expressions: list[StateExpression]

    @classmethod
    def from_expressions(cls, *expressions: Expression) -> Self:
        """Create the aggregate expression from expressions."""
        return cls(
            _key=cls._key,
            expressions=[
                StateExpression.from_expression(expression) for expression in expressions
            ],
        )


class AndExpression(AggregateExpression):
    """Expression that other expressions using the AND operator."""

    _key: ExpressionType = "AND"


class OrExpression(AggregateExpression):
    """Expression that other expressions using the OR operator."""

    _key: ExpressionType = "OR"


class StateCondition(BaseModel):
    """State condition."""

    expression: StateExpression
    state_name: str = Field(
        ..., description="Name of the expression", alias="stateName", regex="^[a-zA-Z]+$"
    )
    context: ObjectInstanceId = Field(..., description="Object Instance ID for the expression")

    @property
    def instance_id(self) -> ObjectInstanceId:
        """Get the instance ID of the object that this condition is for."""
        return self.context

    @property
    def state_value(self) -> Literal["true", "false"]:
        """Get the state value of the condition."""
        return "true"
