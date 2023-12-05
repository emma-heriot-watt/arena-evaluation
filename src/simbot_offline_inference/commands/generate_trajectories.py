import random
from pathlib import Path

from loguru import logger

from arena_missions.builders import ChallengeBuilder, MissionBuilder, RequiredObjectBuilder
from arena_missions.structures import MissionTrajectory
from simbot_offline_inference.commands.run_trajectories_in_arena import run_trajectories_in_arena
from simbot_offline_inference.metrics import WandBTrajectoryGenerationCallback
from simbot_offline_inference.settings import Settings


def _get_default_mission_dir() -> Path:
    """Return the default mission dir."""
    return Settings().missions_dir


def generate_trajectories(
    output_dir: Path = _get_default_mission_dir(),  # noqa: WPS404
    *,
    session_id_prefix: str = "T",
    enable_randomisation_in_session_id: bool = True,
) -> None:
    """Generate trajectories from the missions."""
    settings = Settings()
    settings.put_settings_in_environment()
    settings.prepare_file_system()
    output_dir.mkdir(parents=True, exist_ok=True)

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
        output_path = output_dir.joinpath(f"{trajectory.session_id}.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(trajectory.json(by_alias=True))

        # Update the list of saved trajectories to keep a separate track
        saved_trajectories_paths.add(output_path)

    logger.info(f"Saved {len(saved_trajectories_paths)} trajectories to disk.")


def run_trajectories(
    trajectories_dir: Path,
    wandb_group_name: str,
    wandb_project: str = "arena-high-level-trajectories",
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

    wandb_callback = WandBTrajectoryGenerationCallback(
        project=wandb_project,
        entity=settings.wandb_entity,
        group=wandb_group_name,
        mission_trajectory_dir=settings.missions_dir,
        mission_trajectory_outputs_dir=settings.evaluation_output_dir,
        unity_logs=settings.unity_log_path,
    )

    run_trajectories_in_arena(trajectories, wandb_callback=wandb_callback)
