import os
from pathlib import Path
from typing import Union

from cloudpathlib import S3Path
from pydantic import BaseSettings, FilePath


class Settings(BaseSettings):
    """Settings to run the evaluation."""

    # Paths
    storage_dir: Path = Path("storage/")
    auxiliary_metadata_dir: Path = storage_dir.joinpath("auxiliary_metadata/")
    auxiliary_metadata_cache_dir: Path = storage_dir.joinpath("auxiliary_metadata_cache/")
    feature_cache_dir: Path = storage_dir.joinpath("features/")
    trajectory_dir: Path = storage_dir.joinpath("data/", "trajectory-data/")
    experience_hub_dir: Path = storage_dir.joinpath("experience-hub/")
    models_dir: Path = experience_hub_dir.joinpath("storage/models/")
    cdf_dir: Path = storage_dir.joinpath("cdfs/")
    metrics_file: Path = storage_dir.joinpath("metrics.json")

    evaluation_output_dir: Path = storage_dir.joinpath("action_outputs/")
    s3_evaluation_output_dir: S3Path = S3Path(
        "s3://emma-simbot/results/simbot-trajectories/missions/"
    )

    # Experience hub
    base_endpoint: str = "http://0.0.0.0:5522"
    simbot_port: int = 5522
    simbot_client_timeout: int = -1
    simbot_feature_flags__enable_offline_evaluation: bool = True  # noqa: WPS116, WPS118

    # Unity
    platform: str = "Linux"
    arena_path: FilePath = storage_dir.joinpath("arena", platform, "Arena.x86_64")
    unity_log_path: Path = storage_dir.joinpath("logs", "unity_logs.log")
    display: Union[str, int] = 1

    def put_settings_in_environment(self) -> None:
        """Put settings in the environment variables."""
        for env_name, env_var in self:
            os.environ[env_name.upper()] = str(env_var)

    def prepare_file_system(self) -> None:
        """Prepare the various directories and files on the machine."""
        # Create the necessary directories
        directories_to_create = [
            self.storage_dir,
            self.auxiliary_metadata_dir,
            self.auxiliary_metadata_cache_dir,
            self.feature_cache_dir,
            self.trajectory_dir,
            self.models_dir,
            self.unity_log_path.parent,
            self.evaluation_output_dir,
        ]
        for directory in directories_to_create:
            directory.mkdir(parents=True, exist_ok=True)

        # Create the unity logs path if it doesn't exist already
        self.unity_log_path.touch(exist_ok=True)
