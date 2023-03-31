"""Process the trajectory data for inference.

This script processes the trajectory data for inference on the offline arena.
"""
import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any, Optional, TypedDict

import numpy as np


DATA_ROOT_DIR = Path("storage/data/")
TRAJECTORY_ROOT_DIR = DATA_ROOT_DIR.joinpath("trajectory-data/")


class SimBotTestInstance(TypedDict):
    """Inferface for the test data."""

    test_number: int
    mission_id: str
    mission_group: Optional[str]
    mission_cdf: Any
    utterances: list[str]


def extract_mission_group_from_description(mission_desc: str) -> Optional[str]:
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


def process_trajectory_data(in_file: Path, out_file: Path) -> None:
    """Process a file."""
    task_data = json.loads(in_file.read_bytes())

    test_instances: list[SimBotTestInstance] = []

    for task_description, task in task_data.items():
        for annotation_idx, annotation in enumerate(task["human_annotations"]):
            utterances: Iterator[str] = (
                instruction["instruction"] for instruction in annotation["instructions"]
            )
            utterances = (utterance for utterance in utterances if "_" not in utterance)
            utterances = (utterance.lower() for utterance in utterances)

            test_instance = SimBotTestInstance(
                mission_group=extract_mission_group_from_description(task_description),
                test_number=len(test_instances) + 1,
                mission_id=f"{task_description}_{annotation_idx}",
                mission_cdf=task["CDF"],
                utterances=list(utterances),
            )

            test_instances.append(test_instance)

    np.save(out_file, test_instances)  # type: ignore[arg-type]


def process_all_trajectory_data(trajectory_root: Path = TRAJECTORY_ROOT_DIR) -> None:
    """Process all the trajectory data into the numpy files."""
    process_trajectory_data(
        trajectory_root.joinpath("valid.json"),
        trajectory_root.joinpath("nlg_commands_val.npy"),
    )
    # process_trajectory_data(
    #     trajectory_root.joinpath("train.json"),
    #     trajectory_root.joinpath("nlg_commands_train.npy"),
    # )
    process_trajectory_data(
        trajectory_root.joinpath("T2_valid.json"),
        trajectory_root.joinpath("nlg_commands_T2.npy"),
    )


if __name__ == "__main__":
    process_all_trajectory_data()
