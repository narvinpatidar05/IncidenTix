from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_v1_router
from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.system import router as system_router
from app.core.config import get_settings
from app.core.exception_handlers import register_exception_handlers
from app.core.lifespan import lifespan
from app.core.logging import setup_logging


def create_app() -> FastAPI:
    settings = get_settings()
    setup_logging()

    application = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
    )

    allow_wildcard = settings.cors_origins == ["*"]
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=not allow_wildcard,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(application)

    # Unversioned probes for Cloud Run / load balancers.
    application.include_router(health_router, tags=["Health"])
    application.include_router(system_router, tags=["System"])
    application.include_router(api_v1_router, prefix=settings.api_v1_prefix)

    return application


app = create_app()
