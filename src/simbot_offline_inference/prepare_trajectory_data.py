"""Process the trajectory data for inference.

This script processes the trajectory data for inference on the offline arena.
"""
import json
from collections.abc import Iterator
from pathlib import Path
from typing import Optional

from rich.progress import track

from simbot_offline_inference.structures import SimBotTrajectory


def extract_mission_group_from_description(mission_desc: str) -> Optional[str]:  # noqa: WPS212
    """Extract the group from the mission description."""
    if "Break_Object".lower() in mission_desc.lower():
        return "breakObject"
    if "Clean_and_Deliver".lower() in mission_desc.lower():
        return "clean&deliver"
    if "Color_and_Deliver".lower() in mission_desc.lower():
        return "color&deliver"
    if "Fill_and_Deliver".lower() in mission_desc.lower():
        return "fill&deliver"
    if "Freeze_and_Deliver".lower() in mission_desc.lower():
        return "freeze&deliver"
    if "Heat_and_Deliver".lower() in mission_desc.lower():
        return "heat&deliver"
    if "Insert_in_Device".lower() in mission_desc.lower():
        return "insertInDevice"
    if "Pickup_and_Deliver".lower() in mission_desc.lower():
        return "pickup&deliver"
    if "Pour_into_Container".lower() in mission_desc.lower():
        return "pourContainer"
    if "Repair_and_Deliver".lower() in mission_desc.lower():
        return "repair&deliver"
    if "Scan_Object".lower() in mission_desc.lower():
        return "scanObject"
    if "Toggle_".lower() in mission_desc.lower():
        return "toggleDevice"

    return None


def process_their_trajectory_data(in_file: Path) -> list[SimBotTrajectory]:
    """Process the trajectory data from their evaluation sets."""
    task_data = json.loads(in_file.read_bytes())

    test_instances: list[SimBotTrajectory] = []

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

            test_instance = SimBotTrajectory(
                mission_group=extract_mission_group_from_description(task_description),
                high_level_key=f"{task_description}_{annotation_idx}",
                cdf=task["CDF"],
                utterances=list(utterances),
            )

            test_instances.append(test_instance)

    return test_instances
