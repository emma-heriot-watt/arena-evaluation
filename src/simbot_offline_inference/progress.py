# Things to track:
# [ ] Number of trajectories that completed / total trajectories
# [ ] Current mission name
# [ ] Unity instance status (running, checking X/250)
# [ ] Trajectory phase:
#       Loading CDF (spinning)
#       Sending dummy actions (X/10)
#       Sending utterance (X/Y)

from rich.columns import Columns
from rich.console import Group
from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, MofNCompleteColumn, Progress, TimeElapsedColumn
from rich.text import Text


class ArenaEvaluatorProgressTracker:
    def __init__(self) -> None:
        self.progress = Progress(
            "{task.description}",
            BarColumn(bar_width=None),
            MofNCompleteColumn(),
            TimeElapsedColumn(),
            expand=True,
        )

        self._trajectory_count_task = self.progress.add_task(
            description="Running trajectories",
            start=False,
        )

        self._unity_status_task = self.progress.add_task(
            description="Check unity is running",
            start=False,
            total=1,
            visible=False,
        )

        self._trajectory_progress = Progress(
            "{task.description}", BarColumn(bar_width=None), MofNCompleteColumn(), expand=True
        )
        self._loading_cdf_task = self._trajectory_progress.add_task(
            description="Loading CDF",
            total=10,
            start=False,
            visible=False,
        )
        self._sent_utterance_task = self._trajectory_progress.add_task(
            description="Sending utterances", start=False
        )

        self._current_mission_name: str = ""
        self._completed_mission_names: list[str] = []

    def start_new_evaluation(self, total_trajectories: int) -> None:
        """Start a new evaluation."""
        self.progress.update(self._trajectory_count_task, total=total_trajectories)
        self.progress.start_task(self._trajectory_count_task)

    def start_unity_check(self, total: int) -> None:
        """Start the Unity instance check progress."""
        self.progress.start_task(self._unity_status_task)
        self.progress.update(
            self._unity_status_task, total=total, description="Checking Unity instance"
        )

    def sent_another_unity_check(self) -> None:
        """Update progress when sending another check for the Unity instance."""
        self.progress.advance(self._unity_status_task)

    def finish_unity_check(self) -> None:
        """Finish the Unity instance check progress."""
        self.progress.stop_task(self._unity_status_task)
        self.progress.update(
            self._unity_status_task,
            description="Unity instance is running",
            completed=self.progress.tasks[self._unity_status_task].completed,
        )

    def start_new_trajectory(
        self, mission_name: str, max_num_dummy_actions: int = 10, num_utterances: int = 1
    ) -> None:
        """Reset the trajectory progress section for the new trajectory."""
        self._current_mission_name = mission_name
        self._trajectory_progress.reset(
            self._loading_cdf_task, total=max_num_dummy_actions, start=False
        )
        self._trajectory_progress.reset(
            self._sent_utterance_task, total=num_utterances, start=False
        )

    def loading_cdf(self) -> None:
        """Update trajectory progress when loading the CDF in the arena."""
        self._trajectory_progress.start_task(self._loading_cdf_task)

    def sent_dummy_actions(self, count: int = 1) -> None:
        """Update trajectory progress when sending dummy actions."""
        self._trajectory_progress.advance(self._loading_cdf_task, count)

    def arena_ready_for_utterance(self) -> None:
        """Update trajectory progress when the arena is ready for an utterance."""
        self._trajectory_progress.update(
            self._loading_cdf_task,
            total=self._trajectory_progress.tasks[self._loading_cdf_task].completed,
        )
        self._trajectory_progress.stop_task(self._loading_cdf_task)

        self._trajectory_progress.start_task(self._sent_utterance_task)

    def sent_utterance(self, count: int = 1) -> None:
        """Update trajectory progress when sending an utterance."""
        # If the loading CDF task is still running, stop it
        self._trajectory_progress.advance(self._sent_utterance_task, count)

    def finish_trajectory(self) -> None:
        """Finish the trajectory progress section."""
        self._trajectory_progress.stop_task(self._sent_utterance_task)
        self.progress.advance(self._trajectory_count_task)
        self._completed_mission_names.append(self._current_mission_name)

    def display(self) -> Live:
        """Display the progress tracker."""
        return Live(self._create_display())

    def _create_display(self) -> Panel:
        all_completed_missions = [
            Text(mission_name) for mission_name in sorted(set(self._completed_mission_names))
        ]

        table_of_completed = Columns(all_completed_missions, equal=True, expand=True)

        return Panel(
            Group(
                self.progress,
                self._trajectory_progress,
                Panel(
                    table_of_completed,
                    title="Completed missions",
                    border_style="green",
                ),
            ),
            title="Progress",
            border_style="yellow",
            padding=(1, 5),
        )
