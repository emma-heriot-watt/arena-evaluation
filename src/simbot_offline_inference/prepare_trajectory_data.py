"""Process the trajectory data for inference.

This script processes the trajectory data for inference on the offline arena.
"""
import json
from collections.abc import Iterator
from pathlib import Path
from typing import Optional

from rich.progress import track

from arena_missions.structures import MissionTrajectory


def extract_mission_group_from_description(mission_desc: str) -> Optional[str]:
    """Extract the group from the mission description."""
    switcher = {
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


def process_their_trajectory_data(in_file: Path) -> list[MissionTrajectory]:
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
                high_level_key=f"{task_description}_{annotation_idx}",
                cdf=task["CDF"],
                utterances=list(utterances),
            )

            test_instances.append(test_instance)

    return test_instances
