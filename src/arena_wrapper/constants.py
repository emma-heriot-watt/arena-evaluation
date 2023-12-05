########################################################################################################################
# The list of object classes that are allowed to use for simbot challenge. Following classes can be used with
# OBJECT_CLASS as ObjectOutputType.

OBJECT_CLASS_ALLOW_LIST = ["stickynote"]
########################################################################################################################
# Action space

NAVIGATIONAL_ACTIONS = ["Goto", "Move", "Rotate", "Look"]
OBJECT_INTERACTION_ACTIONS = [
    "Pickup",
    "Open",
    "Close",
    "Break",
    "Scan",
    "Examine",
    "Place",
    "Pour",
    "Toggle",
    "Fill",
    "Clean",
]
ACTIONS_REQUIRING_MASK = [
    "Pickup",
    "Open",
    "Close",
    "Break",
    "Scan",
    "Examine",
    "Place",
    "Pour",
    "Toggle",
    "Fill",
    "Clean",
    "Goto",
]
########################################################################################################################
