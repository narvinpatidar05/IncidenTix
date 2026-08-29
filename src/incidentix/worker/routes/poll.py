"""Pick the next mock issue."""

import logging

from fastapi import APIRouter

from incidentix.incident.loader import IncidentLoadError, pick_next_issue

router = APIRouter()
logger = logging.getLogger(__name__)


def pick_and_log() -> dict[str, str]:
    """Pick the next mock issue and log it. Never raises to the caller."""
    try:
        incident = pick_next_issue()
    except IncidentLoadError:
        logger.exception("Failed to load mock issue")
        return {"status": "error"}

    if incident is None:
        logger.info("No mock issues found")
        return {"status": "no issues found"}

    logger.info(
        "Picked issue id=%s service=%s alert_name=%s",
        incident.id,
        incident.service,
        incident.alert_name,
    )
    return {
        "status": "picked",
        "id": incident.id,
        "service": incident.service,
        "alert_name": incident.alert_name,
    }


@router.post("/poll")
def poll() -> dict[str, str]:
    """Pick the next mock issue and log it."""
    return pick_and_log()
