from pathlib import Path

import numpy as np
from loguru import logger

from emma_common.logging import setup_rich_logging
from simbot_offline_inference.evaluator import SimBotArenaEvaluator
from simbot_offline_inference.orchestrators import ArenaOrchestrator, ExperienceHubOrchestrator
from simbot_offline_inference.settings import Settings


def run_evaluation(processed_trajectory_data: Path) -> None:
    settings = Settings()
    settings.put_settings_in_environment()
    settings.create_directories()

    logger.debug("Loaded settings: {settings}")

    logger.info("Preparing orchestrators and evaluators")
    arena_orchestrator = ArenaOrchestrator()
    experience_hub_orchestrator = ExperienceHubOrchestrator(
        healthcheck_endpoint=f"{settings.base_endpoint}/healthcheck",
        predict_endpoint=f"{settings.base_endpoint}/v1/predict",
        auxiliary_metadata_dir=settings.auxiliary_metadata_dir,
        cached_extracted_features_dir=settings.feature_cache_dir,
        experience_hub_dir=settings.experience_hub_dir,
        session_id_prefix="T2",
    )
    evaluator = SimBotArenaEvaluator(arena_orchestrator, experience_hub_orchestrator)

    logger.info(f"Loading test data from {processed_trajectory_data}")
    test_data = np.load(processed_trajectory_data, allow_pickle=True)
    logger.debug(f"Loaded {len(test_data)} instances to evaluate")

    logger.info(f"Running evaluation on test data...")
    evaluator.run_evaluation(test_data)

    logger.info("Done!")


if __name__ == "__main__":
    settings = Settings()
    setup_rich_logging()
    run_evaluation(settings.trajectory_dir.joinpath("nlg_commands_T2.npy"))
