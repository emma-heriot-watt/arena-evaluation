import itertools
from enum import Enum
from pathlib import Path
from typing import Optional

from loguru import logger

from arena_missions.builders import ChallengeBuilder, MissionBuilder, RequiredObjectBuilder
from arena_missions.structures import Mission
from simbot_offline_inference.commands.run_trajectories_in_arena import run_trajectories_in_arena
from simbot_offline_inference.settings import Settings


class TrajectoryGenerationType(Enum):
    """Types of trajectory generation."""

    from_directory = "from_directory"
    from_mission_builder = "from_mission_builder"


def generate_trajectories_from_directory(
    cdf_dir: Path, enable_randomness_in_session_id: bool = False
) -> None:
    """Generate trajectories from the missions."""
    if not cdf_dir.is_dir():
        raise NotADirectoryError("The given path is not a directory.")

    settings = Settings()
    settings.put_settings_in_environment()
    settings.prepare_file_system()

    logger.info(f"Loading missions from {cdf_dir}")
    challenges = [Mission.parse_file(cdf_file) for cdf_file in cdf_dir.rglob("*.json")]

    logger.info(f"Loaded {len(challenges)} missions.")

    trajectories = list(
        itertools.chain.from_iterable(
            [challenge.convert_to_single_trajectory() for challenge in challenges]
        )
    )

    logger.info(f"Loaded {len(trajectories)} separate trajectories.")

    run_trajectories_in_arena(
        trajectories,
        session_id_prefix="T",
        enable_randomness_in_session_id=enable_randomness_in_session_id,
    )


def generate_trajectories_from_mission_builder(
    enable_randomness_in_session_id: bool = False,
) -> None:
    """Generate trajectories from auto-generated missions."""
    settings = Settings()
    settings.put_settings_in_environment()
    settings.prepare_file_system()

    logger.info("Loading missions")
    missions = list(
        MissionBuilder(ChallengeBuilder(), RequiredObjectBuilder()).generate_all_missions()
    )
    logger.info(f"Loaded {len(missions)} missions")

    trajectories = list(
        itertools.chain.from_iterable(
            [mission.convert_to_single_trajectory() for mission in missions]
        )
    )

    logger.info(f"Loaded {len(trajectories)} separate trajectories.")

    run_trajectories_in_arena(
        trajectories,
        session_id_prefix="T",
        enable_randomness_in_session_id=enable_randomness_in_session_id,
    )


def generate_trajectories(
    trajectory_generation_type: TrajectoryGenerationType,
    cdf_dir: Optional[Path] = None,
    enable_randomisation_in_session_id: bool = False,
) -> None:
    """Generate trajectories from the missions."""
    if trajectory_generation_type == TrajectoryGenerationType.from_directory:
        if cdf_dir is None:
            raise ValueError("The directory for the CDF files must be provided.")
        return generate_trajectories_from_directory(cdf_dir, enable_randomisation_in_session_id)

    if trajectory_generation_type == TrajectoryGenerationType.from_mission_builder:
        return generate_trajectories_from_mission_builder(enable_randomisation_in_session_id)

    raise ValueError("Unknown trajectory generation type.")
