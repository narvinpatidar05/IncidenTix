from app.core.config import get_settings
from app.models.system import ServiceInfo


class SystemRepository:
    def get_service_info(self) -> ServiceInfo:
        settings = get_settings()
        return ServiceInfo(
            service=settings.app_name,
            status="ok",
            environment=settings.app_env,
            version=settings.app_version,
            api_v1_prefix=settings.api_v1_prefix,
        )
