from pathlib import Path
from typing import Any, NamedTuple

from loguru import logger
from rich.progress import track

from simbot_offline_inference.orchestrators import ArenaOrchestrator


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
        failed_cdfs: list[CDFValidationInstance] = []

        with self._arena_orchestrator:
            for instance in track(cdfs, description="Validating CDFs"):
                try:
                    self._validate_single_cdf(instance.cdf)
                except InvalidCDFException:
                    logger.error(f"Failed to validate CDF: {instance.path}")
                    failed_cdfs.append(instance)

        if failed_cdfs:
            logger.error(f"{len(failed_cdfs)} CDFs are invalid")
            return False

        return True

    def _validate_single_cdf(self, cdf: dict[str, Any]) -> None:
        """Validate a single CDF with the Arena."""
        self._arena_orchestrator.send_cdf_to_arena(cdf)

        if not self._check_unity_log_for_exceptions():
            raise InvalidCDFException(cdf, "Unity log contains exceptions")

        self._arena_orchestrator.send_dummy_actions_to_arena()

        if not self._check_unity_log_for_exceptions():
            raise InvalidCDFException(cdf, "Unity log contains exceptions")

    def _check_unity_log_for_exceptions(self) -> bool:
        """Check the Unity log for any exceptions."""
        raise NotImplementedError
