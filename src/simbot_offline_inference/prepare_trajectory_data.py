"""Process the trajectory data for inference.

This script processes the trajectory data for inference on the offline arena.
"""
import json
from pathlib import Path
from typing import Any, TypedDict

import numpy as np


DATA_ROOT_DIR = Path("storage/data/")
TRAJECTORY_ROOT_DIR = DATA_ROOT_DIR.joinpath("trajectory-data/")


class SimBotTestInstance(TypedDict):
    """Inferface for the test data."""

    test_number: int
    mission_id: str
    mission_cdf: Any
    utterances: list[str]


def process_file(in_file: Path, out_file: Path) -> None:
    """Process a file."""
    with open(in_file) as input_file:
        data = json.load(input_file)

    nlg_commands: list[SimBotTestInstance] = []
    ind_cnt = 1

    for task_descr, task in data.items():
        human_annotations = task["human_annotations"]
        for annotation in human_annotations:
            di_item = SimBotTestInstance(
                test_number=ind_cnt,
                mission_id=task_descr,
                mission_cdf=task["CDF"],
                utterances=[],
            )
            ind_cnt += 1

            instructions = annotation["instructions"]
            for instruction in instructions:
                text_inst = instruction["instruction"].lower()
                if (
                    "_" in text_inst
                ):  # To get rid of occurences which have object IDs instead ofobjects
                    continue
                di_item["utterances"].append(text_inst)

            nlg_commands.append(di_item)

    np.save(out_file, nlg_commands)


def process_all_trajectory_data(trajectory_root: Path = TRAJECTORY_ROOT_DIR) -> None:
    """Process all the trajectory data into the numpy files."""
    process_file(
        trajectory_root.joinpath("valid.json"),
        trajectory_root.joinpath("nlg_commands_val.npy"),
    )
    process_file(
        trajectory_root.joinpath("train.json"),
        trajectory_root.joinpath("nlg_commands_train.npy"),
    )
    process_file(
        trajectory_root.joinpath("T2_valid.json"),
        trajectory_root.joinpath("nlg_commands_T2.npy"),
    )


if __name__ == "__main__":
    process_all_trajectory_data()
