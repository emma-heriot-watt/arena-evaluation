from pathlib import Path

from loguru import logger
from rich import box, print as rich_print
from rich.columns import Columns
from rich.panel import Panel
from rich.table import Table

from arena_missions.builders import ChallengeBuilder
from arena_missions.builders.mission_builder import MissionBuilder
from arena_missions.builders.required_objects_builder import RequiredObjectBuilder
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


def validate_generated_missions() -> None:
    """Validate all missions from the `MissionBuilder`."""
    settings = Settings()
    settings.put_settings_in_environment()
    settings.prepare_file_system()

    setup_rich_logging()

    missions = MissionBuilder(ChallengeBuilder(), RequiredObjectBuilder()).generate_all_missions()
    cdfs = [
        CDFValidationInstance(cdf=mission.cdf, path=mission.high_level_key.key)
        for mission in missions
    ]

    arena_orchestrator = ArenaOrchestrator()
    challenge_validator = ChallengeValidator(arena_orchestrator)

    logger.info("Starting validation")
    challenge_validator.validate_cdfs(cdfs)

    logger.info("Done.")


def print_high_level_keys() -> None:
    """Print all the high level keys from the registered challenge builder."""
    keys = sorted([str(key) for key in ChallengeBuilder.list_available()])
    columns = Columns(keys)
    panel = Panel(
        columns,
        title="Registered high-level keys",
        border_style="green",
        subtitle=f"Total: {len(keys)}",
    )
    rich_print(panel)


def print_challenges_per_high_level_key() -> None:
    """Print the challenges that exist per high-level key."""
    table = Table(box=box.ROUNDED, style="yellow", highlight=True)
    table.add_column("High-level key")
    table.add_column("Num. challenges")

    for key, challenge_count in ChallengeBuilder.count_available_functions_per_key().items():
        table.add_row(str(key), str(challenge_count))

    rich_print(table)
