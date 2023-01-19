import os
from pathlib import Path

from pydantic import BaseSettings, DirectoryPath, FilePath


class Settings(BaseSettings):
    # Paths
    storage_dir: DirectoryPath = Path("storage/")
    auxiliary_metadata_dir: DirectoryPath = storage_dir.joinpath("auxiliary_metadata/")
    feature_cache_dir: DirectoryPath = storage_dir.joinpath("features/")
    trajectory_dir: DirectoryPath = storage_dir.joinpath("data/", "trajectory-data/")

    # Experience hub
    base_endpoint: str = "http://0.0.0.0:5000"

    # Unity
    platform: str = "Linux"
    arena_path: FilePath = storage_dir.joinpath("arena", platform, "SimbotChallenge.x86_64")
    unity_log_path: Path = storage_dir.joinpath("logs", "unity_logs.log")
    display: int = 1

    def put_settings_in_environment(self) -> None:
        """Put settings in the environment variables."""
        for key, value in self:
            os.environ[key.upper()] = str(value)

    def create_directories(self) -> None:
        """Create directories that need creating if they don't exist already."""
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.auxiliary_metadata_dir.mkdir(parents=True, exist_ok=True)
        self.feature_cache_dir.mkdir(parents=True, exist_ok=True)
        self.trajectory_dir.mkdir(parents=True, exist_ok=True)
