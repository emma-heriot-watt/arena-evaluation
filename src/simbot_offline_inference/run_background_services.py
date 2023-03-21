from loguru import logger

from emma_experience_hub.commands.simbot.cli import (
    SERVICE_REGISTRY_PATH,
    SERVICES_COMPOSE_PATH,
    SERVICES_STAGING_COMPOSE_PATH,
    run_background_services,
)
from simbot_offline_inference.settings import Settings


if __name__ == "__main__":
    logger.debug("Starting background services for the experience hub...")
    settings = Settings()
    run_background_services(
        service_registry_path=settings.experience_hub_dir.joinpath(SERVICE_REGISTRY_PATH),
        services_docker_compose_path=settings.experience_hub_dir.joinpath(SERVICES_COMPOSE_PATH),
        staging_services_docker_compose_path=settings.experience_hub_dir.joinpath(
            SERVICES_STAGING_COMPOSE_PATH
        ),
        model_storage_dir=settings.models_dir,
        download_models=True,
        force_download=False,
        run_in_background=False,
        enable_observability=False,
        is_production=False,
    )
