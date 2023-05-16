import json
from collections.abc import Iterator
from enum import Enum
from pathlib import Path
from typing import Optional
from uuid import uuid4

from loguru import logger
from rich.progress import track

from arena_missions.structures import MissionTrajectory
from simbot_offline_inference.commands.run_trajectories_in_arena import run_trajectories_in_arena
from simbot_offline_inference.metrics import MissionGroup, WandBEvaluationCallback
from simbot_offline_inference.settings import Settings


class EvaluationType(Enum):
    """Types of evaluation datasets."""

    t1 = "T1"
    t2 = "T2"


def extract_mission_group_from_description(mission_desc: str) -> Optional[MissionGroup]:
    """Extract the group from the mission description."""
    switcher: dict[str, MissionGroup] = {
        "Break_Object": "breakObject",
        "Clean_and_Deliver": "clean&deliver",
        "Color_and_Deliver": "color&deliver",
        "Fill_and_Deliver": "fill&deliver",
        "Freeze_and_Deliver": "freeze&deliver",
        "Heat_and_Deliver": "heat&deliver",
        "Insert_in_Device": "insertInDevice",
        "Pickup_and_Deliver": "pickup&deliver",
        "Pour_into_Container": "pourContainer",
        "Repair_and_Deliver": "repair&deliver",
        "Scan_Object": "scanObject",
        "Toggle_": "toggleDevice",
    }

    for mission_group, mission_group_name in switcher.items():
        if mission_group.lower() in mission_desc.lower():
            return mission_group_name

    return None


def process_their_trajectory_data(
    in_file: Path, session_id_prefix: str
) -> list[MissionTrajectory]:
    """Process the trajectory data from their evaluation sets."""
    task_data = json.loads(in_file.read_bytes())

    test_instances: list[MissionTrajectory] = []

    iterator = track(
        task_data.items(), description="Processing their trajectory data to our format"
    )

    for task_description, task in iterator:
        for annotation_idx, annotation in enumerate(task["human_annotations"]):
            utterances: Iterator[str] = (
                instruction["instruction"] for instruction in annotation["instructions"]
            )
            utterances = (utterance for utterance in utterances if "_" not in utterance)
            utterances = (utterance.lower() for utterance in utterances)

            test_instance = MissionTrajectory(
                mission_group=extract_mission_group_from_description(task_description),
                mission_id=f"{task_description}_{annotation_idx}",
                session_id=f"{session_id_prefix}_{str(uuid4())}",
                cdf=task["CDF"],
                utterances=list(utterances),
                randomise_start_position=False,
            )

            test_instances.append(test_instance)

    return test_instances


def run_their_evaluation(
    evaluation_type: EvaluationType, wandb_project: str = "alexa-arena-evaluation"
) -> None:
    """Run the evaluation on the test set."""
    settings = Settings()

    trajectory_data_per_evaluation_type: dict[EvaluationType, Path] = {
        EvaluationType.t1: settings.trajectory_dir.joinpath("valid.json"),
        EvaluationType.t2: settings.trajectory_dir.joinpath("test.json"),
    }
    trajectory_data_path = trajectory_data_per_evaluation_type[evaluation_type]

    logger.info(f"Loading test data from {trajectory_data_path}")
    instances = process_their_trajectory_data(
        trajectory_data_path, session_id_prefix=evaluation_type.value
    )

    run_trajectories_in_arena(
        instances,
        wandb_callback=WandBEvaluationCallback(
            project=wandb_project,
            entity=settings.wandb_entity,
            group=evaluation_type.value,
            mission_trajectory_dir=settings.missions_dir,
            mission_trajectory_outputs_dir=settings.evaluation_output_dir,
            unity_logs=settings.unity_log_path,
        ),
    )
