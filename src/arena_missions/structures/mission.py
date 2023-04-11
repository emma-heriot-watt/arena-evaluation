from datetime import datetime
from typing import Optional

import shortuuid
from pydantic import BaseModel

from arena_missions.structures.cdf import CDF
from arena_missions.structures.high_level_key import HighLevelKey


class MissionTrajectory(BaseModel):
    """Single trajectory for a given mission."""

    high_level_key: str
    utterances: list[str]
    cdf: CDF

    # Used by T1/T2 data
    mission_group: Optional[str] = None

    def create_session_id(self, prefix: str, *, include_randomness: bool = True) -> str:
        """Create a session ID for the trajectory."""
        safe_high_level_key = self.high_level_key.replace("=", "--").replace("#", "_").lstrip("_")

        now = datetime.now()
        date_chunk = f"{now.year:02d}{now.month:02d}{now.day:02d}"
        randomness = f"-{shortuuid.uuid()[:5]}" if include_randomness else ""

        return prefix + f".{date_chunk}/{safe_high_level_key}{randomness}".lower()


class Mission(BaseModel):
    """Single mission for the Arena.."""

    high_level_key: HighLevelKey
    plans: list[list[str]]
    cdf: CDF

    # Used by T1/T2 data
    mission_group: Optional[str] = None

    def convert_to_single_trajectory(self) -> list[MissionTrajectory]:
        """Convert the challenge to a list of single trajectories."""
        trajectories: list[MissionTrajectory] = []

        for plan in self.plans:
            trajectories.append(
                MissionTrajectory(
                    high_level_key=self.high_level_key.key,
                    utterances=plan,
                    cdf=self.cdf,
                    mission_group=self.mission_group,
                )
            )

        return trajectories
