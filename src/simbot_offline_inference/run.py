import os
from pathlib import Path

import numpy as np
from loguru import logger

from emma_common.logging import setup_rich_logging
from simbot_offline_inference.evaluator import SimBotArenaEvaluator
from simbot_offline_inference.orchestrators import ArenaOrchestrator, ExperienceHubOrchestrator
from simbot_offline_inference.prepare_trajectory_data import TRAJECTORY_ROOT_DIR


STORAGE_DIR = Path("storage/")

BASE_ENDPOINT = "http://0.0.0.0:5000"

AUXILIARY_METADATA_DIR = STORAGE_DIR.joinpath("auxiliary_metadata/")
AUXILIARY_METADATA_DIR.mkdir(parents=True, exist_ok=True)

FEATURE_CACHE_DIR = STORAGE_DIR.joinpath("features/")
FEATURE_CACHE_DIR.mkdir(parents=True, exist_ok=True)


def set_arena_env_vars() -> None:
    os.environ["PLATFORM"] = "Linux"
    os.environ["ARENA_PATH"] = str(
        STORAGE_DIR.joinpath("arena", "Linux", "SimbotChallenge.x86_64")
    )
    os.environ["UNITY_LOG_PATH"] = str(STORAGE_DIR.joinpath("logs", "unity_logs.log"))


def run_evaluation(processed_trajectory_data: Path) -> None:
    logger.info("Preparing orchestrators and evaluators")
    arena_orchestrator = ArenaOrchestrator()
    experience_hub_orchestrator = ExperienceHubOrchestrator(
        healthcheck_endpoint=f"{BASE_ENDPOINT}/healthcheck",
        predict_endpoint=f"{BASE_ENDPOINT}/v1/predict",
        auxiliary_metadata_dir=AUXILIARY_METADATA_DIR,
        cached_extracted_features_dir=FEATURE_CACHE_DIR,
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
    set_arena_env_vars()
    setup_rich_logging()
    run_evaluation(TRAJECTORY_ROOT_DIR.joinpath("nlg_commands_T2.npy"))
