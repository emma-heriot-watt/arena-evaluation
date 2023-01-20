import os
from pathlib import Path

from pydantic import BaseSettings, FilePath


class Settings(BaseSettings):
    """Settings to run the evaluation."""

    # Paths
    storage_dir: Path = Path("storage/")
    auxiliary_metadata_dir: Path = storage_dir.joinpath("auxiliary_metadata/")
    feature_cache_dir: Path = storage_dir.joinpath("features/")
    trajectory_dir: Path = storage_dir.joinpath("data/", "trajectory-data/")
    experience_hub_dir: Path = storage_dir.joinpath("experience-hub/")
    models_dir: Path = experience_hub_dir.joinpath("storage/models/")

    # Experience hub
    base_endpoint: str = "http://0.0.0.0:5522"
    simbot_port: int = 5522
    simbot_client_timeout: int = -1

    # Unity
    platform: str = "Linux"
    arena_path: FilePath = storage_dir.joinpath("arena", platform, "SimbotChallenge.x86_64")
    unity_log_path: Path = storage_dir.joinpath("logs", "unity_logs.log")
    display: int = 1

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
            self.feature_cache_dir,
            self.trajectory_dir,
            self.models_dir,
            self.unity_log_path.parent,
        ]
        for directory in directories_to_create:
            directory.mkdir(parents=True, exist_ok=True)

        # Create the unity logs path if it doesn't exist already
        self.unity_log_path.touch(exist_ok=True)
