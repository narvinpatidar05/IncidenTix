"""Incident domain models."""

from datetime import datetime

from pydantic import BaseModel, Field


class Incident(BaseModel):
    """Input contract for an incoming alert.

    Downstream modules (agent loop, prompts, classification) consume this shape.
    """

    id: str
    service: str
    alert_name: str
    severity: str
    raw_payload: dict = Field(default_factory=dict)
    created_at: datetime
