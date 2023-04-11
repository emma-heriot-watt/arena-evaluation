from collections.abc import Generator
from typing import Any, Callable, cast, get_args
from typing_extensions import Self

from arena_missions.constants.arena import ObjectIds, load_object_id_to_readable_name_map


def convert_object_instance_id_to_object_id(object_instance: str) -> str:
    """Convert object instance to object id.

    We need to remove everything after the last "_".
    """
    return object_instance[::-1].split("_", 1)[1][::-1]


class ObjectId(str):  # noqa: WPS600
    """An object ID in the Arena."""

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[..., Self], None, None]:
        """Return a generator of validators for this type."""
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> Self:
        """Validate the object ID."""
        if not isinstance(v, str):
            raise TypeError("Object ID must be a string")

        # Make sure the ID is one of the literals
        if v not in get_args(ObjectIds):
            raise ValueError("Object ID is not valid and does not exist in the Arena.")

        return cls(v)

    def __repr__(self) -> str:
        """Return a string representation of the object ID."""
        return f"ObjectId({super().__repr__()})"

    @classmethod
    def parse(cls, v: Any) -> Self:
        """Parse the input."""
        return cls.validate(v)

    @property
    def readable_name(self) -> str:
        """Return the readable name of the object."""
        return load_object_id_to_readable_name_map()[cast(ObjectIds, self)]


class ObjectInstanceId(str):  # noqa: WPS600
    """An object instance ID in the Arena."""

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[..., Self], None, None]:
        """Return a generator of validators for this type."""
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> Self:
        """Validate the object instance ID."""
        if not isinstance(v, str):
            raise TypeError("Object instance ID must be a string")

        # Make sure it has an object ID in it
        ObjectId.parse(convert_object_instance_id_to_object_id(v))

        # Make sure the instance number is an integer
        instance_number = v.split("_")[-1]

        # Make sure the instance number does not have any leading 0s
        if instance_number.startswith("0"):
            raise ValueError("Object instance ID cannot have leading 0s")

        if not instance_number.isdigit():
            raise ValueError("Object instance ID end with a digit")

        return cls(v)

    def __repr__(self) -> str:
        """Return a string representation of the object instance ID."""
        return f"ObjectInstanceId({super().__repr__()})"

    @classmethod
    def parse(cls, v: Any) -> Self:
        """Parse the input."""
        return cls.validate(v)

    @property
    def object_id(self) -> ObjectId:
        """Return the object ID of the object instance."""
        return ObjectId(convert_object_instance_id_to_object_id(self))

    @property
    def readable_name(self) -> str:
        """Return the readable name of the object instance."""
        return self.object_id.readable_name
