"""Worker FastAPI application entrypoint."""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .config import settings
from .routes import health, poll

logging.basicConfig(level=settings.log_level.upper())
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Log worker startup and shutdown."""
    logger.info("incidentix-worker starting")
    poll.pick_and_log()
    yield
    logger.info("incidentix-worker shutting down")


app = FastAPI(title="incidentix-worker", lifespan=lifespan)
app.include_router(health.router)
app.include_router(poll.router)
