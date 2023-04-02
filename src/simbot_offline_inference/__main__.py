from enum import Enum
from pathlib import Path
from typing import Optional

import numpy as np
import typer
from loguru import logger

from emma_common.logging import setup_rich_logging
from emma_experience_hub.commands.simbot.cli import (
    OBSERVABILITY_COMPOSE_PATH,
    SERVICE_REGISTRY_PATH,
    SERVICES_COMPOSE_PATH,
    SERVICES_PROD_COMPOSE_PATH,
    SERVICES_STAGING_COMPOSE_PATH,
    run_background_services as run_exp_hub_background_services,
)
from simbot_offline_inference.controller import SimBotInferenceController
from simbot_offline_inference.evaluator import SimBotArenaEvaluator
from simbot_offline_inference.metrics import SimBotEvaluationMetrics
from simbot_offline_inference.orchestrators import ArenaOrchestrator, ExperienceHubOrchestrator
from simbot_offline_inference.prepare_trajectory_data import process_trajectory_data
from simbot_offline_inference.settings import Settings
from simbot_offline_inference.web_backend import SimBotWebBackendApp


app = typer.Typer(name="Run inference offline.", no_args_is_help=True, add_completion=False)


class EvaluationType(Enum):
    """The type of evaluation to run."""

    t1 = "T1"
    t2 = "T2"


def get_processed_trajectory_data(evaluation_type: EvaluationType) -> Path:
    """Get the path to the processed trajectory data for the given evaluation type."""
    settings = Settings()

    evaluation_type_to_trajectory_data_path = {
        EvaluationType.t1: settings.trajectory_dir.joinpath("nlg_commands_val.npy"),
        EvaluationType.t2: settings.trajectory_dir.joinpath("nlg_commands_T2.npy"),
    }

    return evaluation_type_to_trajectory_data_path[evaluation_type]


@app.command(rich_help_panel="Preparation")
def prepare_trajectory_data(evaluation_type: EvaluationType) -> None:
    """Prepare all the trajectory data for the evaluation."""
    settings = Settings()

    if evaluation_type == EvaluationType.t1:
        process_trajectory_data(
            settings.trajectory_dir.joinpath("valid.json"),
            settings.trajectory_dir.joinpath("nlg_commands_val.npy"),
        )

    if evaluation_type == EvaluationType.t2:
        process_trajectory_data(
            settings.trajectory_dir.joinpath("T2_valid.json"),
            settings.trajectory_dir.joinpath("nlg_commands_T2.npy"),
        )

    logger.info("Done!")


@app.command(rich_help_panel="Run")
def run_background_services() -> None:
    """Run the background services for the Experience Hub."""
    settings = Settings()

    run_exp_hub_background_services(
        service_registry_path=settings.experience_hub_dir.joinpath(SERVICE_REGISTRY_PATH),
        services_docker_compose_path=settings.experience_hub_dir.joinpath(SERVICES_COMPOSE_PATH),
        staging_services_docker_compose_path=settings.experience_hub_dir.joinpath(
            SERVICES_STAGING_COMPOSE_PATH
        ),
        production_services_docker_compose_path=settings.experience_hub_dir.joinpath(
            SERVICES_PROD_COMPOSE_PATH
        ),
        observability_services_docker_compose_path=settings.experience_hub_dir.joinpath(
            OBSERVABILITY_COMPOSE_PATH
        ),
        model_storage_dir=settings.models_dir,
        download_models=True,
        force_download=False,
        run_in_background=False,
        enable_observability=False,
        is_production=False,
    )


@app.command(rich_help_panel="Run")
def run_evaluation(
    evaluation_type: EvaluationType, start_index: int, num_instances: Optional[int] = None
) -> None:
    """Run the evaluation."""
    processed_trajectory_data = get_processed_trajectory_data(evaluation_type)
    setup_rich_logging()

    settings = Settings()
    settings.put_settings_in_environment()
    settings.prepare_file_system()

    logger.debug(f"Loaded settings: {settings}")

    logger.info("Preparing orchestrators and evaluators")
    arena_orchestrator = ArenaOrchestrator()
    experience_hub_orchestrator = ExperienceHubOrchestrator(
        healthcheck_endpoint=f"{settings.base_endpoint}/healthcheck",
        predict_endpoint=f"{settings.base_endpoint}/v1/predict",
        auxiliary_metadata_dir=settings.auxiliary_metadata_dir,
        auxiliary_metadata_cache_dir=settings.auxiliary_metadata_cache_dir,
        cached_extracted_features_dir=settings.feature_cache_dir,
        experience_hub_dir=settings.experience_hub_dir,
        model_storage_dir=settings.models_dir,
    )
    inference_controller = SimBotInferenceController(
        arena_orchestrator, experience_hub_orchestrator
    )
    evaluation_metrics = SimBotEvaluationMetrics(
        settings.evaluation_output_dir, settings.metrics_file
    )
    evaluator = SimBotArenaEvaluator(
        inference_controller, evaluation_metrics, session_id_prefix=evaluation_type.value
    )

    logger.info(f"Loading test data from {processed_trajectory_data}")
    test_data = np.load(processed_trajectory_data, allow_pickle=True)
    logger.debug(f"Loaded {len(test_data)} instances to evaluate")

    if num_instances is not None:
        end_index = start_index + num_instances
        test_data = test_data[start_index:end_index]
        logger.info(f"Running {len(test_data)} instance from subset [{start_index}:{end_index}]")

    logger.info("Running evaluation on test data...")
    evaluator.run_evaluation(test_data)

    logger.info("Done!")


@app.command(rich_help_panel="Run")
def run_web_backend() -> None:
    """Run the backend for the web tool."""
    settings = Settings()
    settings.put_settings_in_environment()
    settings.prepare_file_system()

    logger.debug(f"Loaded settings: {settings}")

    logger.info("Preparing orchestrators and evaluators")
    arena_orchestrator = ArenaOrchestrator()
    experience_hub_orchestrator = ExperienceHubOrchestrator(
        healthcheck_endpoint=f"{settings.base_endpoint}/healthcheck",
        predict_endpoint=f"{settings.base_endpoint}/v1/predict",
        auxiliary_metadata_dir=settings.auxiliary_metadata_dir,
        auxiliary_metadata_cache_dir=settings.auxiliary_metadata_cache_dir,
        cached_extracted_features_dir=settings.feature_cache_dir,
        experience_hub_dir=settings.experience_hub_dir,
        model_storage_dir=settings.models_dir,
    )
    inference_controller = SimBotInferenceController(
        arena_orchestrator, experience_hub_orchestrator
    )
    backend_app = SimBotWebBackendApp(inference_controller, settings.cdf_dir)
    backend_app.run()


if __name__ == "__main__":
    app()
