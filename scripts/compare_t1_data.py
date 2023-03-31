import itertools
import json
from pathlib import Path

from pydantic import BaseModel
from rich.pretty import pprint as rich_print
from rich.progress import track


TOTAL_COUNT = 1149


class SplitMetrics(BaseModel):
    """Model for each metrics.json that got saved."""

    games_available: int = TOTAL_COUNT
    games_played: int
    games_completed: int
    subgoals_completed: int
    total_subgoals: int
    mission_groups: set[str]
    games_played_per_mission_group: dict[str, int]
    games_completed_per_mission_group: dict[str, int]
    success_rate: float
    subgoal_completion_rate: float
    success_rate_per_mission: dict[str, float]


def average_actions(mission_dir: Path) -> None:
    """Get the average number of actions taken per mission."""
    num_actions = []
    files_to_check = list(mission_dir.iterdir())

    for mission_file in track(files_to_check):
        if mission_file.is_dir():
            continue

        with open(mission_file) as open_file:
            parsed_file = json.load(open_file)
            actions = parsed_file["predicted_actions"]
            num_actions.append(len(actions))

    rich_print(sum(num_actions) / len(num_actions))


def compare_data(data_dir: Path) -> None:
    """Run the numbers."""
    # Load all the data
    loaded_data: list[SplitMetrics] = []
    for data_file in data_dir.iterdir():
        if data_file.is_dir():
            continue
        loaded_data.append(SplitMetrics.parse_file(data_file))

    games_played = sum(data.games_played for data in loaded_data)
    games_completed = sum(data.games_completed for data in loaded_data)
    subgoals_completed = sum(data.subgoals_completed for data in loaded_data)
    total_subgoals = sum(data.total_subgoals for data in loaded_data)
    mission_groups = set(
        itertools.chain.from_iterable([data.mission_groups for data in loaded_data])
    )
    games_played_per_mission_group = {
        mission_group: sum(
            data.games_played_per_mission_group[mission_group]
            if mission_group in data.games_played_per_mission_group
            else 0
            for data in loaded_data
        )
        for mission_group in mission_groups
    }
    games_completed_per_mission_group = {
        mission_group: sum(
            data.games_completed_per_mission_group[mission_group]
            if mission_group in data.games_completed_per_mission_group
            else 0
            for data in loaded_data
        )
        for mission_group in mission_groups
    }
    merged_data = SplitMetrics(
        games_played=games_played,
        games_completed=games_completed,
        subgoals_completed=subgoals_completed,
        total_subgoals=total_subgoals,
        mission_groups=mission_groups,
        games_played_per_mission_group=games_played_per_mission_group,
        games_completed_per_mission_group=games_completed_per_mission_group,
        success_rate=games_completed / games_played,
        subgoal_completion_rate=subgoals_completed / total_subgoals,
        success_rate_per_mission={
            mission_group: games_completed_per_mission_group[mission_group]
            / games_played_per_mission_group[mission_group]
            for mission_group in mission_groups
        },
    )

    rich_print(merged_data)


if __name__ == "__main__":
    compare_data(Path("storage/metrics/"))
    average_actions(Path("storage/metrics/missions/"))
