from fastapi import Depends

from app.models.system import ServiceInfo
from app.repositories.system_repository import SystemRepository


class SystemService:
    def __init__(
        self, system_repository: SystemRepository = Depends()
    ) -> None:
        self.system_repository = system_repository

    def get_service_info(self) -> ServiceInfo:
        return self.system_repository.get_service_info()
