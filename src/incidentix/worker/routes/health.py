"""Cloud Run liveness endpoint."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    """Return liveness status."""
    return {"status": "ok"}
