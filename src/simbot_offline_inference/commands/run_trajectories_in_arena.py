from loguru import logger

from arena_missions.structures import MissionTrajectory
from emma_common.logging import setup_rich_logging
from simbot_offline_inference.arena_evaluator import SimBotArenaEvaluator
from simbot_offline_inference.inference_controller import SimBotInferenceController
from simbot_offline_inference.metrics import SimBotEvaluationMetrics
from simbot_offline_inference.orchestrators import ArenaOrchestrator, ExperienceHubOrchestrator
from simbot_offline_inference.settings import Settings


def run_trajectories_in_arena(
    instances: list[MissionTrajectory],
    session_id_prefix: str,
    *,
    enable_randomness_in_session_id: bool = False,
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
        settings.evaluation_output_dir, settings.metrics_file, settings.s3_evaluation_output_dir
    )
    evaluator = SimBotArenaEvaluator(
        inference_controller,
        evaluation_metrics,
        session_id_prefix=session_id_prefix,
        enable_randomness_in_session_id=enable_randomness_in_session_id,
    )

    logger.info(f"Running evaluation for {len(instances)} instances...")
    evaluator.run_evaluation(instances)

    logger.info("Done!")