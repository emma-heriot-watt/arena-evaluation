from rich.live import Live
from rich.progress import BarColumn, MofNCompleteColumn, Progress, TimeElapsedColumn


class ArenaEvaluatorProgressTracker:
    """Create Rich progress bars to track evaluation progress."""

    def __init__(self) -> None:
        self.progress = Progress(
            "{task.description}",
            BarColumn(bar_width=None),
            MofNCompleteColumn(),
            TimeElapsedColumn(),
            expand=True,
        )

        self._overall_trajectory_task = self.progress.add_task(
            description="Overall progress", start=False, total=None
        )
        self._current_trajectory_task = self.progress.add_task(
            description="Current progress", start=False, total=None, visible=False
        )

    def start_new_evaluation(self, total_trajectories: int) -> None:
        """Start a new evaluation."""
        self.progress.update(self._overall_trajectory_task, total=total_trajectories)
        self.progress.start_task(self._overall_trajectory_task)

    def start_new_session(self, session_id: str, num_utterances: int = 1) -> None:
        """Reset the trajectory progress section for the new trajectory."""
        self.progress.reset(
            self._current_trajectory_task, start=False, total=num_utterances, visible=True
        )
        self.progress.update(self._current_trajectory_task, description=f"Running {session_id}")

    def sent_utterance(self) -> None:
        """Update trajectory progress when sending an utterance."""
        if not self.progress.tasks[self._current_trajectory_task].started:
            self.progress.start_task(self._current_trajectory_task)
        self.progress.advance(self._current_trajectory_task)

    def finish_trajectory(self) -> None:
        """Finish the trajectory progress."""
        self.progress.stop_task(self._current_trajectory_task)
        self.progress.advance(self._overall_trajectory_task)

    def display(self) -> Live:
        """Display the progress tracker."""
        return Live(self.progress)
