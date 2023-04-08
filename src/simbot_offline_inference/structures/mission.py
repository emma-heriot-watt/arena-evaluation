from typing import Any, Optional

from pydantic import BaseModel

from simbot_offline_inference.structures.mission_trajectory import MissionTrajectory


class Mission(BaseModel):
    """Single challenge for the Arena.."""

    high_level_key: str
    plans: list[list[str]]
    cdf: dict[str, Any]

    # Used by T1/T2 data
    mission_group: Optional[str]

    def convert_to_single_trajectory(self) -> list[MissionTrajectory]:
        """Convert the challenge to a list of single trajectories."""
        trajectories: list[MissionTrajectory] = []

        for plan in self.plans:
            trajectories.append(
                MissionTrajectory(
                    high_level_key=self.high_level_key,
                    utterances=plan,
                    cdf=self.cdf,
                    mission_group=self.mission_group,
                )
            )

        return trajectories
