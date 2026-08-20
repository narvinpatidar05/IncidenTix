from fastapi import APIRouter, Depends, status

from app.api.v1.controllers.health_controller import HealthController
from app.core.constants import HEALTH_PATH
from app.schemas.health import HealthResponse

router = APIRouter()


@router.get(
    HEALTH_PATH,
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check",
)
def get_health(
    controller: HealthController = Depends(),
) -> HealthResponse:
    return controller.get_health()
