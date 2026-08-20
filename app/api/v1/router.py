from fastapi import APIRouter

from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.system import router as system_router

api_v1_router = APIRouter()
api_v1_router.include_router(health_router, tags=["Health"])
api_v1_router.include_router(system_router, tags=["System"])
