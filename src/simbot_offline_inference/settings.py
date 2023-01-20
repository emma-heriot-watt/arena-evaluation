import os
from pathlib import Path

from pydantic import BaseSettings, FilePath


class Settings(BaseSettings):
    # Paths
    storage_dir: Path = Path("storage/")
    models_dir: Path = storage_dir.joinpath("models/")
    auxiliary_metadata_dir: Path = storage_dir.joinpath("auxiliary_metadata/")
    feature_cache_dir: Path = storage_dir.joinpath("features/")
    trajectory_dir: Path = storage_dir.joinpath("data/", "trajectory-data/")
    experience_hub_dir: Path = storage_dir.joinpath("experience-hub/")

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
        directories = [
            self.storage_dir,
            self.auxiliary_metadata_dir,
            self.feature_cache_dir,
            self.trajectory_dir,
            self.models_dir,
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
