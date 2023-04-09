from pathlib import Path

from loguru import logger

from arena_missions.structures import Mission
from emma_common.logging import setup_rich_logging
from simbot_offline_inference.challenge_validator import CDFValidationInstance, ChallengeValidator
from simbot_offline_inference.orchestrators import ArenaOrchestrator
from simbot_offline_inference.settings import Settings


def validate_cdfs(directory: Path) -> None:
    """Validate the CDFs in the directory."""
    settings = Settings()
    settings.put_settings_in_environment()
    settings.prepare_file_system()

    setup_rich_logging()

    files_to_load = list(directory.rglob("*.json"))
    logger.info(f"Found {len(files_to_load)} CDFs to validate.")

    cdfs = [
        CDFValidationInstance(cdf=Mission.parse_file(challenge_file).cdf, path=challenge_file)
        for challenge_file in files_to_load
    ]

    arena_orchestrator = ArenaOrchestrator()
    challenge_validator = ChallengeValidator(arena_orchestrator)

    logger.info("Starting validation")
    challenge_validator.validate_cdfs(cdfs)

    logger.info("Done.")
