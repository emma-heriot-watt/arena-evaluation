from typing import Optional

from pydantic import BaseModel

from arena_missions.structures.cdf import CDF
from arena_missions.structures.high_level_key import HighLevelKey


class Mission(BaseModel):
    """Single mission for the Arena.."""

    high_level_key: HighLevelKey
    plans: list[list[str]]
    cdf: CDF

    # Used by T1/T2 data
    mission_group: Optional[str] = None
