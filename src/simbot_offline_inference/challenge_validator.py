from contextlib import ExitStack
from pathlib import Path
from typing import Any, NamedTuple, Optional, Union

from loguru import logger
from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, MofNCompleteColumn, Progress, TimeElapsedColumn

from arena_missions.structures import CDF
from simbot_offline_inference.orchestrators import ArenaOrchestrator


UNITY_FAILURES = {  # noqa: WPS407
    "UNABLE_TO_SPAWN_OBJECTS": "The objects that were unable to spawn are",
    "DUPLICATE_KEYS_IN_CDF": "ArgumentException: An item with the same key has already been added",
    "IMPROPER_OBJECT_REFERENCE": "Object reference not set to an instance of an object",
}


class InvalidCDFException(Exception):
    """Exception for when an invalid CDF is found."""

    def __init__(self, cdf: Any, *args: Any) -> None:
        logger.error(f"CDF: {cdf}")
        super().__init__(*args)


class CDFValidationInstance(NamedTuple):
    """A CDF validation instance."""

    cdf: CDF
    path: Union[Path, str]


class ChallengeValidator:
    """Validate the CDF file in the Arena.

    The only way to validate the CDF file is to submit it to the Arena and see if there are any
    errors.

    It's annoying, but it's the only way, and this should hopefully automate that entire process.
    """

    def __init__(
        self,
        arena_orchestrator: ArenaOrchestrator,
        *,
        send_dummy_actions_after_cdf_load: bool = False,
    ) -> None:
        self._arena_orchestrator = arena_orchestrator
        self._send_dummy_actions_after_cdf_load = send_dummy_actions_after_cdf_load

        self.progress = Progress(
            "{task.description}",
            BarColumn(bar_width=None),
            MofNCompleteColumn(),
            TimeElapsedColumn(),
            expand=True,
        )

    def validate_cdfs(self, cdfs: list[CDFValidationInstance]) -> bool:
        """Validate the CDFs with the Arena."""
        task_id = self.progress.add_task("Validating CDFs", total=len(cdfs))

        # Create the context managers
        context_manager_stack = ExitStack()
        context_manager_stack.enter_context(self._display_progress())
        context_manager_stack.enter_context(self._arena_orchestrator)

        with context_manager_stack:
            for instance in cdfs:
                try:
                    self._validate_single_cdf(instance.cdf)
                except InvalidCDFException:
                    logger.error(f"Failed to validate CDF: {instance.path}")
                    return False

                self.progress.advance(task_id)

        return True

    def _validate_single_cdf(self, cdf: CDF) -> None:
        """Validate a single CDF with the Arena."""
        self._arena_orchestrator.send_cdf_to_arena(cdf.dict(by_alias=True))

        if self._send_dummy_actions_after_cdf_load:
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

    def _display_progress(self) -> Live:
        """Display the progress bar."""
        return Live(Panel(self.progress, padding=(1, 4), border_style="yellow"))
