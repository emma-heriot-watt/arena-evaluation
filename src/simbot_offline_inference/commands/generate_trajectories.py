import random
from pathlib import Path

from loguru import logger

from arena_missions.builders import ChallengeBuilder, MissionBuilder, RequiredObjectBuilder
from arena_missions.structures import MissionTrajectory
from simbot_offline_inference.commands.run_trajectories_in_arena import run_trajectories_in_arena
from simbot_offline_inference.settings import Settings


def generate_trajectories(
    *, session_id_prefix: str = "T", enable_randomisation_in_session_id: bool = True
) -> None:
    """Generate trajectories from the missions."""
    settings = Settings()
    settings.put_settings_in_environment()
    settings.prepare_file_system()

    logger.info("Loading missions...")
    missions = list(
        MissionBuilder(ChallengeBuilder(), RequiredObjectBuilder()).generate_all_missions()
    )
    logger.info(f"Loaded {len(missions)} missions")

    trajectories = [
        mission.convert_to_trajectory(
            session_id_prefix, include_randomness=enable_randomisation_in_session_id
        )
        for mission in missions
    ]

    logger.info(f"Loaded {len(trajectories)} separate trajectories.")

    saved_trajectories_paths = set()

    for trajectory in trajectories:
        output_path = settings.missions_dir.joinpath(f"{trajectory.session_id}.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(trajectory.json(by_alias=True))

        # Update the list of saved trajectories to keep a separate track
        saved_trajectories_paths.add(output_path)

    logger.info(f"Saved {len(saved_trajectories_paths)} trajectories to disk.")


def run_trajectories(
    trajectories_dir: Path,
    *,
    randomise_order: bool = False,
) -> None:
    """Run trajectories from disk."""
    if not trajectories_dir.is_dir():
        raise NotADirectoryError("The given path is not a directory.")

    settings = Settings()
    settings.put_settings_in_environment()
    settings.prepare_file_system()

    trajectories = [
        MissionTrajectory.parse_file(trajectory_file)
        for trajectory_file in trajectories_dir.rglob("*.json")
    ]

    logger.info(f"Loaded {len(trajectories)} separate trajectories.")

    if randomise_order:
        random.shuffle(trajectories)

    run_trajectories_in_arena(trajectories)
