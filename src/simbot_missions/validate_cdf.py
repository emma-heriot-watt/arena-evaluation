from pathlib import Path
from typing import Any

from loguru import logger

from simbot_offline_inference.controller import SimBotInferenceController


class InvalidCDFException(Exception):
    """Exception for when an invalid CDF is found."""

    def __init__(self, cdf: Any, *args: Any) -> None:
        logger.error(f"CDF: {cdf}")
        super().__init__(*args)


class ChallengeValidator:
    """Validate the CDF file in the Arena.

    The only way to validate the CDF file is to submit it to the Arena and see if there are any
    errors.

    It's annoying, but it's the only way, and this should hopefully automate that entire process.
    """

    def __init__(
        self, inference_controller: SimBotInferenceController, unity_log_path: Path
    ) -> None:
        self._inference_controller = inference_controller
        self._unity_log_path = unity_log_path

    def validate_cdfs(self, cdfs: list[dict[str, Any]]) -> bool:
        """Validate the CDFs with the Arena."""
        with self._inference_controller:
            for cdf in cdfs:
                try:
                    self.validate_single_cdf(cdf)
                except InvalidCDFException:
                    logger.exception("CDF validation failed")
                    return False

        return True

    def validate_single_cdf(self, cdf: dict[str, Any]) -> None:
        """Validate a single CDF with the Arena."""
        with self._inference_controller:
            self._inference_controller.send_cdf_to_arena(cdf)

            if not self._check_unity_log_for_exceptions():
                raise InvalidCDFException(cdf, "Unity log contains exceptions")

            self._inference_controller.send_dummy_actions_to_arena()

            if not self._check_unity_log_for_exceptions():
                raise InvalidCDFException(cdf, "Unity log contains exceptions")

    def _check_unity_log_for_exceptions(self) -> bool:
        """Check the Unity log for any exceptions."""
        raise NotImplementedError
