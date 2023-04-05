from typing import Optional

import typer
from loguru import logger

from simbot_offline_inference.commands import run_background_services, run_evaluation
from simbot_offline_inference.prepare_trajectory_data import process_their_trajectory_data
from simbot_offline_inference.settings import Settings


app = typer.Typer(name="Run inference offline.", no_args_is_help=True, add_completion=False)


app.command(rich_help_panel="Run")(run_background_services)


@app.command(rich_help_panel="Evaluation")
def run_evaluation_on_t1(start_index: int = 0, num_instances: Optional[int] = None) -> None:
    """Run the evaluation on the T1 test set."""
    settings = Settings()
    trajectory_data_path = settings.trajectory_dir.joinpath("valid.json")

    logger.info(f"Loading test data from {trajectory_data_path}")
    instances = process_their_trajectory_data(trajectory_data_path)

    run_evaluation(
        instances, session_id_prefix="T1", start_index=start_index, num_instances=num_instances
    )


@app.command(rich_help_panel="Evaluation")
def run_evaluation_on_t2(start_index: int = 0, num_instances: Optional[int] = None) -> None:
    """Run the evaluation on the T2 test set."""
    settings = Settings()
    trajectory_data_path = settings.trajectory_dir.joinpath("T2_valid.json")

    logger.info(f"Loading test data from {trajectory_data_path}")
    instances = process_their_trajectory_data(trajectory_data_path)

    run_evaluation(
        instances, session_id_prefix="T2", start_index=start_index, num_instances=num_instances
    )


if __name__ == "__main__":
    app()
