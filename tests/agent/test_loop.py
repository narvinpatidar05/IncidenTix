"""Tests for the agentic investigation loop (no live Ollama)."""

from datetime import UTC, datetime

import pytest

from incidentix.agent.loop import InvestigationError, run_investigation
from incidentix.incident.models import Incident

_INCIDENT = Incident(
    id="inc-001",
    service="payment-api",
    alert_name="HighErrorRate",
    severity="critical",
    raw_payload={"status": "firing"},
    created_at=datetime(2026, 10, 2, tzinfo=UTC),
)

_FINDINGS_ARGS = {
    "root_cause": "DB pool exhaustion after payment-api timeouts",
    "evidence": ["Connection timeout to payment-api", "error rate spiked to 45"],
    "confidence": "medium",
    "suggested_fix": "Increase DB pool size and retry the downstream",
}


class _FakeClient:
    def __init__(self, responses: list[dict]) -> None:
        self._responses = list(responses)

    def run_with_tools(
        self, system_prompt: str, tools: list[dict], messages: list[dict]
    ) -> dict:
        assert system_prompt
        assert tools
        assert messages
        return self._responses.pop(0)


def test_run_investigation_returns_findings_after_logs() -> None:
    client = _FakeClient(
        [
            {
                "text": "checking logs",
                "tool_calls": [
                    {
                        "name": "get_logs",
                        "input": {
                            "service": "payment-api",
                            "query": "error",
                            "minutes_back": 60,
                        },
                    }
                ],
            },
            {
                "text": "done",
                "tool_calls": [{"name": "submit_findings", "input": _FINDINGS_ARGS}],
            },
        ]
    )
    findings = run_investigation(_INCIDENT, client)
    assert findings.root_cause == _FINDINGS_ARGS["root_cause"]
    assert findings.confidence == "medium"
    assert len(findings.evidence) >= 1


def test_run_investigation_get_logs_uses_mock_data() -> None:
    captured: list[str] = []

    class _CaptureClient(_FakeClient):
        def run_with_tools(self, system_prompt, tools, messages):
            for msg in messages:
                if msg.get("role") == "tool":
                    captured.append(msg["content"])
            return super().run_with_tools(system_prompt, tools, messages)

    client = _CaptureClient(
        [
            {
                "text": "",
                "tool_calls": [
                    {
                        "name": "get_logs",
                        "input": {
                            "service": "payment-api",
                            "query": "error",
                            "minutes_back": 30,
                        },
                    }
                ],
            },
            {
                "text": "",
                "tool_calls": [
                    {
                        "name": "get_metrics",
                        "input": {"query": "error_rate", "minutes_back": 30},
                    }
                ],
            },
            {
                "text": "",
                "tool_calls": [{"name": "submit_findings", "input": _FINDINGS_ARGS}],
            },
        ]
    )
    run_investigation(_INCIDENT, client)
    blob = "\n".join(captured)
    assert "Connection timeout to payment-api" in blob
    assert "error_rate" in blob


def test_run_investigation_stops_after_max_iterations() -> None:
    client = _FakeClient(
        [{"text": "still thinking", "tool_calls": []} for _ in range(6)]
    )
    with pytest.raises(InvestigationError, match="No submit_findings"):
        run_investigation(_INCIDENT, client)


def test_run_investigation_invalid_findings_then_retry() -> None:
    bad = {**_FINDINGS_ARGS, "evidence": []}
    client = _FakeClient(
        [
            {
                "text": "",
                "tool_calls": [{"name": "submit_findings", "input": bad}],
            },
            {
                "text": "",
                "tool_calls": [{"name": "submit_findings", "input": _FINDINGS_ARGS}],
            },
        ]
    )
    findings = run_investigation(_INCIDENT, client)
    assert findings.confidence == "medium"
