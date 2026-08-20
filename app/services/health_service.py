from fastapi import Depends

from app.models.health import HealthCheck
from app.repositories.health_repository import HealthRepository


class HealthService:
    def __init__(
        self, health_repository: HealthRepository = Depends()
    ) -> None:
        self.health_repository = health_repository

    def get_health(self) -> HealthCheck:
        return self.health_repository.get_health_check()
