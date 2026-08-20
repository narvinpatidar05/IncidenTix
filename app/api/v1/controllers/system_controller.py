from fastapi import Depends

from app.models.system import ServiceInfo
from app.schemas.system import ServiceInfoResponse
from app.services.system_service import SystemService


class SystemController:
    def __init__(self, system_service: SystemService = Depends()) -> None:
        self.system_service = system_service

    def get_service_info(self) -> ServiceInfoResponse:
        result: ServiceInfo = self.system_service.get_service_info()
        return ServiceInfoResponse(
            service=result.service,
            status=result.status,
            environment=result.environment,
            version=result.version,
            api_v1_prefix=result.api_v1_prefix,
        )
