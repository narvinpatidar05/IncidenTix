"""Incident domain models."""

from datetime import datetime
from typing import Literal

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


class Findings(BaseModel):
    """Structured output of an investigation. Matches submit_findings tool args."""

    root_cause: str
    evidence: list[str] = Field(min_length=1)
    confidence: Literal["high", "medium", "low"]
    suggested_fix: str
