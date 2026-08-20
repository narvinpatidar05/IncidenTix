from fastapi import Depends

from app.models.health import HealthCheck
from app.schemas.health import HealthResponse
from app.services.health_service import HealthService


class HealthController:
    def __init__(self, health_service: HealthService = Depends()) -> None:
        self.health_service = health_service

    def get_health(self) -> HealthResponse:
        result: HealthCheck = self.health_service.get_health()
        return HealthResponse(
            status=result.status,
            service=result.service,
            environment=result.environment,
            version=result.version,
        )
