from pathlib import Path
from typing import Any, Literal, Optional, get_args

import orjson
import torch
from torchmetrics import MeanMetric, SumMetric


MissionGroup = Literal[
    "breakObject",
    "clean&deliver",
    "color&deliver",
    "fill&deliver",
    "freeze&deliver",
    "heat&deliver",
    "insertInDevice",
    "pickup&deliver",
    "pourContainer",
    "repair&deliver",
    "scanObject",
    "toggleDevice",
]


class EvaluationMetrics:
    """Metrics for evaluating the agent's performance."""

    def __init__(
        self,
        evaluation_output_dir: Path,
        evaluation_metrics_checkpoint_path: Path,
        success_rate_metric: MeanMetric,
        subgoal_completion_rate_metric: MeanMetric,
        per_mission_group_success_rate: Optional[dict[str, MeanMetric]] = None,
    ) -> None:
        self._output_path = evaluation_output_dir
        self._evaluation_metrics_checkpoint_path = evaluation_metrics_checkpoint_path

        self.games_played = SumMetric()

        self.success_rate = success_rate_metric
        self.subgoal_completion_rate = subgoal_completion_rate_metric

        self.per_mission_group_success_rate = per_mission_group_success_rate or {
            mission_group: MeanMetric() for mission_group in get_args(MissionGroup)
        }

    def restore_checkpoint(self) -> "EvaluationMetrics":
        """Restore the evaluation metrics from the checkpoint."""
        if not self._evaluation_metrics_checkpoint_path.exists():
            raise FileNotFoundError(
                "Evaluation metrics checkpoint does not exist. Why are we resuming?"
            )

        return torch.load(self._evaluation_metrics_checkpoint_path)

    def save_checkpoint(self) -> None:
        """Create a checkpoint for the evaluation metrics."""
        torch.save(self, self._evaluation_metrics_checkpoint_path)

    def delete_checkpoint(self) -> None:
        """Delete the checkpoint for the evaluation metrics."""
        self._evaluation_metrics_checkpoint_path.unlink(missing_ok=True)

    def has_mission_been_evaluated(self, mission_id: str) -> bool:
        """Check if the mission has already been evaluated."""
        return self._output_path.joinpath(f"{mission_id}.json").exists()

    def update(
        self,
        mission_id: str,
        mission_group: Optional[str],
        is_mission_completed: bool,
        subgoal_completion_status: list[Literal[0, 1]],
        predicted_actions: list[dict[str, Any]],
        last_game_state: dict[str, Any],
        remaining_utterances: list[str],
    ) -> None:
        """Add metrics from a recently-evaluated mission."""
        self.games_played.update(1)
        self.success_rate.update(1 if is_mission_completed else 0)

        for subgoal_completion in subgoal_completion_status:
            self.subgoal_completion_rate.update(subgoal_completion)

        if mission_group:
            self.per_mission_group_success_rate[mission_group].update(
                1 if is_mission_completed else 0
            )

        self._save_mission_results(
            mission_id, predicted_actions, last_game_state, remaining_utterances
        )

    def _save_mission_results(
        self,
        mission_id: str,
        predicted_actions: list[dict[str, Any]],
        last_game_state: dict[str, Any],
        remaining_utterances: list[str],
    ) -> None:
        """Save the mission results to a file.

        This is what gets uploaded to Eval.AI.
        """
        output_results = {
            "predicted_actions": predicted_actions,
            "last_game_state": last_game_state,
            "remaining_utterances": remaining_utterances,
        }

        # Write the results to a file
        output_file = self._output_path.joinpath(f"{mission_id}.json")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_bytes(orjson.dumps(output_results))
