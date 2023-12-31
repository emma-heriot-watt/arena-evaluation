from loguru import logger
from torchmetrics import MeanMetric

from arena_missions.structures import MissionTrajectory
from emma_common.logging import setup_rich_logging
from simbot_offline_inference.arena_evaluator import SimBotArenaEvaluator
from simbot_offline_inference.inference_controller import SimBotInferenceController
from simbot_offline_inference.metrics import EvaluationMetrics, WandBCallback
from simbot_offline_inference.orchestrators import ArenaOrchestrator, ExperienceHubOrchestrator
from simbot_offline_inference.settings import Settings


def run_trajectories_in_arena(
    instances: list[MissionTrajectory], *, wandb_callback: WandBCallback
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
    evaluation_metrics = EvaluationMetrics(
        settings.evaluation_output_dir,
        settings.evaluation_metrics_checkpoint,
        MeanMetric(),
        MeanMetric(),
    )

    evaluator = SimBotArenaEvaluator(
        inference_controller,
        evaluation_metrics,
        wandb_callback,
        enforce_successful_preparation=settings.enforce_successful_preparation,
        should_resume_previous_wandb_run=settings.should_resume_previous_wandb_run,
    )

    logger.info(f"Running evaluation for {len(instances)} instances...")
    evaluator.run_evaluation(instances)

    logger.info("Done!")
