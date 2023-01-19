from typing import Any

from loguru import logger

from arena_wrapper.enums.object_output_wrapper import ObjectOutputType
from simbot_offline_inference.orchestrators import ArenaOrchestrator, ExperienceHubOrchestrator
from simbot_offline_inference.prepare_trajectory_data import SimBotTestInstance


class SimBotArenaEvaluator:
    def __init__(
        self,
        arena_orchestrator: ArenaOrchestrator,
        experience_hub_orchestrator: ExperienceHubOrchestrator,
        object_output_type: ObjectOutputType = ObjectOutputType.OBJECT_MASK,
    ) -> None:
        self._arena_orchestrator = arena_orchestrator
        self._experience_hub_orchestrator = experience_hub_orchestrator

        self._object_output_type = object_output_type

    def train(self) -> None:
        raise NotImplementedError

    def predict(self) -> list[dict[str, Any]]:
        """Predict the actions to perform on the environment."""
        raise NotImplementedError

    def run_evaluation(self, test_data: list[SimBotTestInstance]) -> None:
        with self._arena_orchestrator, self._experience_hub_orchestrator:
            pass

        # TODO: Create progress tracker (Rich)

        # Make sure experience hub is ready
        self._experience_hub_orchestrator.healthcheck(1000, 1)

        # Run the evaluation

    def run_evaluation_step(self, test_data: SimBotTestInstance) -> None:
        """Run the evaluation on a single instance of the test data."""
        if not self._arena_orchestrator.launch_game(test_data["mission_cdf"]):
            raise AssertionError("Could not launch the game")

        if not self._experience_hub_orchestrator.healthcheck():
            raise AssertionError("The Experience Hub is not healthy.")

        for utterance in test_data["utterances"]:
            # Get the auxiliary metadata from the arena
            auxiliary_metadata = self._arena_orchestrator.get_reconstructed_metadata()

            # Get the next actions to take from the ExperienceHub
            actions = self._experience_hub_orchestrator.get_next_actions(
                test_data["test_number"], utterance, auxiliary_metadata
            )

            # Execute the actions on the arena environment
            return_val, error_code = self._arena_orchestrator.execute_action(
                actions, self._object_output_type, utterance
            )

            if not return_val:
                logger.error(f"Action coule not be completed for the utterance {utterance}")

        # TODO: Calculate results for the test

        raise NotImplementedError()
