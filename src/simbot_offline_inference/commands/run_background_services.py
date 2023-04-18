from emma_experience_hub.commands.simbot.cli import (
    run_background_services as run_exp_hub_background_services,
)
from simbot_offline_inference.settings import Settings


def run_background_services() -> None:
    """Run the background services for the Experience Hub."""
    settings = Settings()
    settings.put_settings_in_environment()

    run_exp_hub_background_services(
        model_storage_dir=settings.models_dir,
        force_download_models=False,
        run_in_background=False,
        observability=False,
        num_gpus=2,
        offline_evaluation=True,
    )
