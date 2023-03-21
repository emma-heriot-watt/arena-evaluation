from collections import Counter
from typing import Literal, Optional


def calculate_subgoal_completion_rate(subgoal_completion_status: list[Literal[0, 1]]) -> float:
    """Calculate the subgoal completion rate for the given set of subgoals."""
    try:
        return sum(subgoal_completion_status) / len(subgoal_completion_status)
    except ZeroDivisionError:
        return 0


class SimBotEvaluationMetrics:
    """Store and calculate metrics for the evaluation."""

    def __init__(self) -> None:
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

        for mission_group in self.mission_groups:
            try:
                output[mission_group] = (
                    self.games_completed_per_mission_group[mission_group]
                    / self.games_played_per_mission_group[mission_group]
                )
            except (KeyError, ZeroDivisionError):
                output[mission_group] = 0

        return output

    def add_mission_metrics(
        self,
        mission_group: Optional[str],
        is_mission_completed: bool,
        subgoal_completion_status: list[Literal[0, 1]],
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
