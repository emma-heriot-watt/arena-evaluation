from pathlib import Path
from typing import Any, NamedTuple, Optional

from loguru import logger
from rich.progress import track

from simbot_offline_inference.orchestrators import ArenaOrchestrator


UNITY_FAILURES = {
    "UNABLE_TO_SPAWN_OBJECTS": "The objects that were unable to spawn are",
    "DUPLICATE_KEYS_IN_CDF": "ArgumentException: An item with the same key has already been added",
}


class InvalidCDFException(Exception):
    """Exception for when an invalid CDF is found."""

    def __init__(self, cdf: Any, *args: Any) -> None:
        logger.error(f"CDF: {cdf}")
        super().__init__(*args)


class CDFValidationInstance(NamedTuple):
    """A CDF validation instance."""

    cdf: dict[str, Any]
    path: Path


class ChallengeValidator:
    """Validate the CDF file in the Arena.

    The only way to validate the CDF file is to submit it to the Arena and see if there are any
    errors.

    It's annoying, but it's the only way, and this should hopefully automate that entire process.
    """

    def __init__(self, arena_orchestrator: ArenaOrchestrator) -> None:
        self._arena_orchestrator = arena_orchestrator

    def validate_cdfs(self, cdfs: list[CDFValidationInstance]) -> bool:
        """Validate the CDFs with the Arena."""
        iterator = track(cdfs, description="Validating CDFs", total=len(cdfs))

        with self._arena_orchestrator:
            for instance in iterator:
                try:
                    self._validate_single_cdf(instance.cdf)
                except InvalidCDFException:
                    logger.error(f"Failed to validate CDF: {instance.path}")
                    return False

        return True

    def _validate_single_cdf(self, cdf: dict[str, Any]) -> None:
        """Validate a single CDF with the Arena."""
        self._arena_orchestrator.send_cdf_to_arena(cdf)
        self._arena_orchestrator.send_dummy_actions_to_arena()

        load_error = self._get_error_from_unity_log()
        if load_error is not None:
            raise InvalidCDFException(cdf, f"Unity log contains error: {load_error}")

    def _get_error_from_unity_log(self) -> Optional[str]:
        """Check the Unity log for any exceptions."""
        with open(self._arena_orchestrator.unity_log_path) as unity_log_file:
            for check_name, string_pattern in UNITY_FAILURES.items():
                if string_pattern in unity_log_file.read():
                    logger.error(check_name)
                    return check_name

        return None
