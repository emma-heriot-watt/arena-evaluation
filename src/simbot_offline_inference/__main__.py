import itertools
from pathlib import Path
from typing import Optional

import typer
from loguru import logger

from simbot_offline_inference.commands import (
    limit_instances_to_evaluate,
    run_background_services,
    run_evaluation,
    validate_cdfs,
)
from simbot_offline_inference.prepare_trajectory_data import process_their_trajectory_data
from simbot_offline_inference.settings import Settings
from simbot_offline_inference.structures import SimBotChallenge


app = typer.Typer(name="Run inference offline.", no_args_is_help=True, add_completion=False)


app.command(rich_help_panel="Run")(run_background_services)

app.command(rich_help_panel="Preparation")(validate_cdfs)


@app.command(rich_help_panel="Evaluation")
def run_evaluation_on_t1(start_index: int = 0, num_instances: Optional[int] = None) -> None:
    """Run the evaluation on the T1 test set."""
    settings = Settings()
    trajectory_data_path = settings.trajectory_dir.joinpath("valid.json")

    logger.info(f"Loading test data from {trajectory_data_path}")
    instances = process_their_trajectory_data(trajectory_data_path)

    if num_instances is not None:
        instances = limit_instances_to_evaluate(instances, num_instances, start_index)

    run_evaluation(instances, session_id_prefix="T1", upload_metrics_to_s3=True)


@app.command(rich_help_panel="Evaluation")
def run_evaluation_on_t2(start_index: int = 0, num_instances: Optional[int] = None) -> None:
    """Run the evaluation on the T2 test set."""
    settings = Settings()
    trajectory_data_path = settings.trajectory_dir.joinpath("T2_valid.json")

    logger.info(f"Loading test data from {trajectory_data_path}")
    instances = process_their_trajectory_data(trajectory_data_path)

    if num_instances is not None:
        instances = limit_instances_to_evaluate(instances, num_instances, start_index)

    run_evaluation(instances, session_id_prefix="T2", upload_metrics_to_s3=True)


@app.command(rich_help_panel="Generation")
def generate_trajectories(cdf_dir: Path) -> None:
    """Generate trajectories from the missions."""
    if not cdf_dir.is_dir():
        raise NotADirectoryError("The given path is not a directory.")

    settings = Settings()
    settings.put_settings_in_environment()
    settings.prepare_file_system()

    logger.info(f"Loading missions from {cdf_dir}")
    challenges = [SimBotChallenge.parse_file(cdf_file) for cdf_file in cdf_dir.rglob("*.json")]

    logger.info(f"Loaded {len(challenges)} missions.")

    trajectories = list(
        itertools.chain.from_iterable(
            [challenge.convert_to_single_trajectory() for challenge in challenges]
        )
    )

    logger.info(f"Loaded {len(trajectories)} separate trajectories.")

    run_evaluation(trajectories, session_id_prefix="T3")


if __name__ == "__main__":
    app()
