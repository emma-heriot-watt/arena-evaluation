import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Literal, Optional
from uuid import uuid1

from loguru import logger


def calculate_subgoal_completion_rate(subgoal_completion_status: list[Literal[0, 1]]) -> float:
    """Calculate the subgoal completion rate for the given set of subgoals."""
    try:
        return sum(subgoal_completion_status) / len(subgoal_completion_status)
    except ZeroDivisionError:
        return 0


class SimBotEvaluationMetrics:
    """Store and calculate metrics for the evaluation."""

    def __init__(self, evaluation_output_dir: Path, output_metrics_file: Path) -> None:
        self.output_path = evaluation_output_dir
        self.output_metrics_file = output_metrics_file

        self.games_played = 0
        self.games_completed = 0

        self.subgoals_completed = 0
        self.total_subgoals = 0

        self.mission_groups = []
        self.games_played_per_mission_group = Counter[str]()
        self.games_completed_per_mission_group = Counter[str]()

    @property
    def games_failed(self) -> int:
        """Get the total number of games where the agent failed outright."""
        return self.games_played - self.games_completed

    @property
    def overall_success_rate(self) -> float:
        """Calculate the overall success rate."""
        try:
            return self.games_completed / self.games_played
        except ZeroDivisionError:
            return 0

    @property
    def overall_subgoal_completion_rate(self) -> float:
        """Calculate the overall subgoal completion rate."""
        try:
            return self.subgoals_completed / self.total_subgoals
        except ZeroDivisionError:
            return 0

    @property
    def success_rate_per_mission_group(self) -> dict[str, float]:
        """Calculate the success rate per mission group."""
        output = {}

        for mission_group in set(self.mission_groups):
            try:
                output[mission_group] = (
                    self.games_completed_per_mission_group[mission_group]
                    / self.games_played_per_mission_group[mission_group]
                )
            except (KeyError, ZeroDivisionError):
                output[mission_group] = 0

        return output

    def has_mission_been_evaluated(self, mission_name: str) -> bool:
        """Check if the mission has already been evaluated."""
        return self.output_path.joinpath(f"{mission_name}.json").exists()

    def add_mission_metrics(
        self,
        mission_name: str,
        mission_group: Optional[str],
        is_mission_completed: bool,
        subgoal_completion_status: list[Literal[0, 1]],
        predicted_actions: list[dict[str, Any]],
        last_game_state: dict[str, Any],
    ) -> None:
        """Add metrics from a recently evaluated mission."""
        self.games_played += 1

        if is_mission_completed:
            self.games_completed += 1

        if mission_group:
            self.mission_groups.append(mission_group)
            self.games_played_per_mission_group.update([mission_group])

            if is_mission_completed:
                self.games_completed_per_mission_group.update([mission_group])

        self.total_subgoals += len(subgoal_completion_status)
        self.subgoals_completed += sum(subgoal_completion_status)

        predicted_actions = [{**action, "id": str(uuid1())} for action in predicted_actions]

        output_file = self.output_path.joinpath(f"{mission_name}.json")
        output_results = {
            "predicted_actions": predicted_actions,
            "last_game_state": last_game_state,
        }
        with open(output_file, "w") as file:
            json.dump(output_results, file)

        logger.info(f"Test #{self.games_played} over")
        logger.info(f"Mission completion status: {is_mission_completed}")
        logger.info(f"Subgoal completion status: {subgoal_completion_status}")
        logger.info(
            f"Subgoal completion rate for test: {calculate_subgoal_completion_rate(subgoal_completion_status)}"
        )
        logger.info(
            f"Current success rate per mission group: {self.success_rate_per_mission_group}"
        )

        self.log_overall_metrics()

    def log_overall_metrics(self) -> None:
        """Log the metrics to the CLI."""
        logger.info(f"Games played: {self.games_played}")
        logger.info(f"Overall success rate: {self.overall_success_rate}")
        logger.info(f"Overall subgoal completion rate: {self.overall_subgoal_completion_rate}")
        logger.info(f"Success rate per mission group: {self.success_rate_per_mission_group}")

        output = {
            "games_played": self.games_played,
            "games_completed": self.games_completed,
            "subgoals_completed": self.subgoals_completed,
            "total_subgoals": self.total_subgoals,
            "mission_groups": list(set(self.mission_groups)),
            "games_played_per_mission_group": self.games_played_per_mission_group,
            "games_completed_per_mission_group": self.games_completed_per_mission_group,
            "success_rate": self.overall_success_rate,
            "subgoal_completion_rate": self.overall_subgoal_completion_rate,
            "success_rate_per_mission": self.success_rate_per_mission_group,
        }

        with open(self.output_metrics_file, "w") as metrics_file:
            json.dump(output, metrics_file)

    def send_to_s3(self) -> None:
        logger.info("Uploading to S3")
        subprocess.run(
            f"aws s3 cp {str(self.output_path)} s3://emma-simbot/results/simbot-eval-ai/missions/ --recursive",
            shell=True,
            check=True,
        )
        subprocess.run(
            f"aws s3 cp {str(self.output_metrics_file)} s3://emma-simbot/results/simbot-eval-ai/metrics_{str(uuid1())}.json",
            shell=True,
            check=True,
        )
