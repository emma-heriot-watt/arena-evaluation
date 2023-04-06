from pathlib import Path

import orjson
from loguru import logger
from rich.progress import track

from emma_common.logging import setup_rich_logging
from simbot_missions.challenge_validator import CDFValidationInstance, ChallengeValidator
from simbot_offline_inference.orchestrators import ArenaOrchestrator


def load_cdfs(directory: Path) -> list[CDFValidationInstance]:
    """Load CDFs from the given trajectory."""
    cdfs: list[CDFValidationInstance] = []

    files_to_load = list(directory.rglob("*.json"))

    for cdf_file in track(files_to_load, description="Loading CDFs"):
        cdf = orjson.loads(cdf_file.read_bytes())
        cdfs.append(CDFValidationInstance(cdf=cdf, path=cdf_file))

    return cdfs


def validate_cdfs(directory: Path) -> None:
    """Validate the CDFs in the directory."""
    setup_rich_logging()

    cdfs = load_cdfs(directory)

    arena_orchestrator = ArenaOrchestrator()
    challenge_validator = ChallengeValidator(arena_orchestrator)

    logger.info("Starting validation")
    challenge_validator.validate_cdfs(cdfs)

    logger.info("Done.")
