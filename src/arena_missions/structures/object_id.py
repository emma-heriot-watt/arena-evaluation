from pydantic import BaseModel, validator

from arena_missions.constants.arena import ObjectIds


def convert_object_instance_id_to_object_id(object_instance: str) -> str:
    """Convert object instance to object id.

    We need to remove everything after the last "_".
    """
    return object_instance[::-1].split("_", 1)[1][::-1]


class ObjectId(BaseModel, frozen=True):
    """An object ID in the Arena.

    This can be created quickly with `ObjectId.parse_obj("object_id")`.
    """

    __root__: ObjectIds

    def __str__(self) -> str:
        """Return the string representation of the object ID."""
        return str(self.__root__)


class ObjectInstanceId(BaseModel, frozen=True):
    """An object instance ID in the Arena."""

    __root__: str

    def __str__(self) -> str:
        """Return the string representation of the object instance ID."""
        return str(self.__root__)

    @validator("__root__")
    @classmethod
    def ensure_object_id_aspect_is_valid(cls, object_instance_id: str) -> str:
        """Ensure the ID starts with a valid ObjectID."""
        ObjectId.parse_obj(convert_object_instance_id_to_object_id(object_instance_id))
        return object_instance_id

    @validator("__root__")
    @classmethod
    def ensure_instance_number_is_valid(cls, object_instance_id: str) -> str:
        """Ensure the instance number is valid."""
        instance_number = object_instance_id.split("_")[-1]

        # Make sure the instance number does not have any leading 0s
        if instance_number.startswith("0"):
            raise ValueError("Object instance ID cannot have leading 0s")

        # Make sure the instance number is a
        if not instance_number.isdigit():
            raise ValueError("Object instance ID ends with a digit")

        return object_instance_id

    @property
    def object_id(self) -> ObjectId:
        """Return the object ID of the object instance."""
        return ObjectId.parse_obj(convert_object_instance_id_to_object_id(self.__root__))
