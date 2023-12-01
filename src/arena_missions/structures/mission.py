from datetime import datetime
from typing import Any, Optional, Union
from uuid import uuid4

import shortuuid
from pydantic import BaseModel, Field

from arena_missions.structures.cdf import CDF
from arena_missions.structures.high_level_key import HighLevelKey


class MissionTrajectory(BaseModel, smart_union=True):
    """Single trajectory for a given mission."""

    session_id: str
    utterances: list[str]

    # Preparation utterances which are not part of the mission.
    # These are given first to help setup the environment as needed.
    preparation_utterances: list[str] = Field(default_factory=list)

    high_level_key: Optional[HighLevelKey] = None

    # Challenge definition
    cdf: Union[CDF, dict[str, Any]]

    # Used by T1/T2 data
    mission_id: Optional[str] = None
    mission_group: Optional[str] = None

    randomise_start_position: bool = True

    @property
    def cdf_as_dict(self) -> dict[str, Any]:
        """Get the CDF as a dict."""
        if isinstance(self.cdf, dict):
            return self.cdf
        return self.cdf.dict(by_alias=True)

    def create_preparation_session_id(self, prefix: str = "T") -> str:
        """Create a session ID for the preparation utterances."""
        now = datetime.now()
        date_chunk = f"{now.year:02d}{now.month:02d}{now.day:02d}"
        return f"{prefix}.{date_chunk}/prep-{uuid4()}"


class Mission(BaseModel):
    """Single mission for the Arena.."""

    high_level_key: HighLevelKey
    plan: list[str]
    cdf: CDF

    # Preparation utterances which are not part of the mission.
    # These are given first to help setup the environment as needed.
    preparation_plan: list[str] = Field(default_factory=list)

    # Used by T1/T2 data
    mission_group: Optional[str] = None

    randomise_start_position: bool = True

    def convert_to_trajectory(
        self,
        session_id_prefix: str,
        *,
        include_randomness: bool = True,
        randomise_start_position: bool = True,
    ) -> MissionTrajectory:
        """Convert the challenge to a list of single trajectories."""
        return MissionTrajectory(
            high_level_key=self.high_level_key,
            session_id=self.create_session_id(
                session_id_prefix, include_randomness=include_randomness
            ),
            utterances=self.plan,
            preparation_utterances=self.preparation_plan,
            cdf=self.cdf,
            mission_group=self.mission_group,
            randomise_start_position=randomise_start_position,
        )

    def create_session_id(self, prefix: str, *, include_randomness: bool = True) -> str:
        """Create a session ID for the trajectory."""
        safe_high_level_key = (
            str(self.high_level_key).replace("=", "--").replace("#", "_").lstrip("_")
        )

        now = datetime.now()
        date_chunk = f"{now.year:02d}{now.month:02d}{now.day:02d}"
        randomness = f"-{shortuuid.uuid()[:5]}" if include_randomness else ""

        return f"{prefix}.{date_chunk}/{safe_high_level_key}{randomness}"
