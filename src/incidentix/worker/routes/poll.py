"""Poll endpoint placeholder."""

from fastapi import APIRouter

router = APIRouter()


@router.post("/poll")
def poll() -> dict[str, str]:
    """Return a placeholder until job picking is implemented."""
    return {"status": "not implemented yet"}
