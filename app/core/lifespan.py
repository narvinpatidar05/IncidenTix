from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    # Startup: DB pools, queue clients, etc. will be wired here later.
    yield
    # Shutdown: close connections here later.
