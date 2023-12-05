from enum import Enum


# creating enumerations for object output types
class ObjectOutputType(str, Enum):
    OBJECT_CLASS = "OBJECT_CLASS"
    OBJECT_MASK = "OBJECT_MASK"
