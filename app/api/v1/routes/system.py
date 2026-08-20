from fastapi import APIRouter, Depends, status

from app.api.v1.controllers.system_controller import SystemController
from app.core.constants import ROOT_PATH
from app.schemas.system import ServiceInfoResponse

router = APIRouter()


@router.get(
    ROOT_PATH,
    response_model=ServiceInfoResponse,
    status_code=status.HTTP_200_OK,
    summary="Service info",
)
def get_service_info(
    controller: SystemController = Depends(),
) -> ServiceInfoResponse:
    return controller.get_service_info()
