from datetime import datetime
from typing import Any, Optional

import shortuuid
from pydantic import BaseModel


class MissionTrajectory(BaseModel):
    """Single trajectory for a given mission."""

    high_level_key: str
    utterances: list[str]
    cdf: dict[str, Any]

    # Used by T1/T2 data
    mission_group: Optional[str]

    def create_session_id(self, prefix: str, *, include_randomness: bool = True) -> str:
        """Create a session ID for the trajectory."""
        safe_high_level_key = self.high_level_key.replace("=", "--").replace("#", "_").lstrip("_")

        now = datetime.now()
        date_chunk = f"{now.year:02d}{now.month:02d}{now.day:02d}"
        randomness = f"-{shortuuid.uuid()[:5]}" if include_randomness else ""

        return f"{prefix}.{date_chunk}/{safe_high_level_key}{randomness}"