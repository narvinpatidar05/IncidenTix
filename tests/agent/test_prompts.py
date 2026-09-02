"""Tests for build_system_prompt."""

from datetime import UTC, datetime

from incidentix.agent.prompts import build_system_prompt
from incidentix.incident.models import Incident

_INCIDENT = Incident(
    id="inc-001",
    service="payment-api",
    alert_name="HighErrorRate",
    severity="critical",
    raw_payload={"status": "firing", "value": 0.42},
    created_at=datetime(2026, 9, 2, 10, 0, tzinfo=UTC),
)


def test_build_system_prompt_includes_persona() -> None:
    prompt = build_system_prompt(_INCIDENT)
    assert isinstance(prompt, str)
    assert "SRE incident investigator" in prompt


def test_build_system_prompt_includes_incident_fields() -> None:
    prompt = build_system_prompt(_INCIDENT)
    assert "payment-api" in prompt
    assert "HighErrorRate" in prompt
    assert "critical" in prompt
    assert "firing" in prompt
    assert "0.42" in prompt


def test_build_system_prompt_empty_payload_is_valid_json() -> None:
    incident = _INCIDENT.model_copy(update={"raw_payload": {}})
    prompt = build_system_prompt(incident)
    assert "{}" in prompt
