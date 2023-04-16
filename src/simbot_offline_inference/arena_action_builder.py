import random
from functools import partial
from typing import Any, Literal

from convert_case import title_case


ArenaAction = dict[str, Any]


class ArenaActionBuilder:
    """Generate actions for the Arena."""

    def random_navigation(self) -> ArenaAction:
        """Return a random action."""
        methods = [
            partial(self.rotate, direction="left"),
            partial(self.rotate, direction="right"),
            partial(self.move, direction="backward"),
            partial(self.move, direction="forward"),
            partial(self.look, direction="up"),
            partial(self.look, direction="down"),
        ]

        return random.choice(methods)(magnitude=random.randint(0, 360))  # noqa: WPS432

    def get_language_instruction_from_action(self, action: ArenaAction) -> str:
        """Return a language instruction from an action."""
        switcher = {
            "Rotate": f"Rotate {action['rotation']['direction']}",
            "Move": f"Move {action['move']['direction']}",
            "Look": f"Look {action['look']['direction']}",
        }
        try:
            return switcher[action["type"]]
        except KeyError:
            return "Rotate right"

    def dummy_action(self) -> ArenaAction:
        """Create a dummy action."""
        return self.rotate("right", 0)

    def rotate(self, direction: Literal["left", "right"], magnitude: int = 45) -> ArenaAction:
        """Create a rotate action."""
        # Make sure the magnitude is in the range [0, 360)
        magnitude = magnitude % 360  # noqa: WPS432

        return {
            "id": "1",
            "type": "Rotate",
            "rotation": {
                "direction": title_case(direction),
                "magnitude": magnitude,
            },
        }

    def move(self, direction: Literal["forward", "backward"], magnitude: int = 1) -> ArenaAction:
        """Create a move action."""
        # Force the magnitude to be 1
        magnitude = 1

        return {
            "id": "1",
            "type": "Move",
            "move": {
                "direction": title_case(direction),
                "magnitude": magnitude,
            },
        }

    def look(self, direction: Literal["up", "down"], magnitude: int = 30) -> ArenaAction:
        """Create a look action."""
        magnitude = magnitude % 60
        return {
            "id": "1",
            "type": "Look",
            "look": {
                "direction": title_case(direction),
                "magnitude": magnitude,
            },
        }

    def viewpoint(self, viewpoint: str) -> ArenaAction:
        """Go to a viewpoint."""
        return {
            "id": "1",
            "type": "Goto",
            "goto": {
                "object": {
                    "goToPoint": viewpoint,
                },
            },
        }
