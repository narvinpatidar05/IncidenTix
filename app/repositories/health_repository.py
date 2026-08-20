from app.core.config import get_settings
from app.core.constants import HealthStatus
from app.models.health import HealthCheck


class HealthRepository:
    """Data access for health checks. Later this will ping Postgres / queue."""

    def get_health_check(self) -> HealthCheck:
        settings = get_settings()
        return HealthCheck(
            status=HealthStatus.HEALTHY,
            service=settings.app_name,
            environment=settings.app_env,
            version=settings.app_version,
        )
