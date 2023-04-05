from datetime import datetime
from typing import Optional

from loguru import logger

from emma_common.logging import setup_rich_logging
from simbot_offline_inference.arena_evaluator import SimBotArenaEvaluator
from simbot_offline_inference.inference_controller import SimBotInferenceController
from simbot_offline_inference.metrics import SimBotEvaluationMetrics
from simbot_offline_inference.orchestrators import ArenaOrchestrator, ExperienceHubOrchestrator
from simbot_offline_inference.prepare_trajectory_data import SimBotTestInstance
from simbot_offline_inference.settings import Settings


def append_date_to_session_id_prefix(prefix: str) -> str:
    """Append the date to the prefix."""
    now = datetime.now()
    date_chunk = f"{now.year:02d}{now.month:02d}{now.day:02d}"

    return f"{prefix}-{date_chunk}"


def run_evaluation(
    instances: list[SimBotTestInstance],
    session_id_prefix: str,
    start_index: int = 0,
    num_instances: Optional[int] = None,
) -> None:
    """Run the evaluation."""
    settings = Settings()
    settings.put_settings_in_environment()
    settings.prepare_file_system()

    setup_rich_logging()

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
        inference_controller,
        evaluation_metrics,
        session_id_prefix=append_date_to_session_id_prefix(session_id_prefix),
    )

    logger.debug(f"Loaded {len(instances)} instances to evaluate")
    if num_instances is not None:
        end_index = start_index + num_instances
        instances = instances[start_index:end_index]
        logger.info(f"Running {len(instances)} instance from subset [{start_index}:{end_index}]")

    logger.info("Running evaluation...")
    evaluator.run_evaluation(instances)

    logger.info("Done!")
