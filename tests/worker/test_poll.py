"""Tests for worker startup and POST /poll picking a mock issue."""

import json
import logging
from datetime import UTC, datetime
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from incidentix.incident import loader
from incidentix.worker.main import app

VALID_INCIDENT = {
    "id": "inc-001",
    "service": "payment-api",
    "alert_name": "HighErrorRate",
    "severity": "critical",
    "raw_payload": {"status": "firing"},
    "created_at": datetime(2026, 8, 29, 10, 0, 0, tzinfo=UTC).isoformat(),
}


@pytest.fixture
def mock_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(loader, "MOCK_ISSUES_DIR", tmp_path)
    loader._processed_paths.clear()
    return tmp_path


def _write_issue(directory: Path, name: str, payload: dict) -> None:
    (directory / name).write_text(json.dumps(payload), encoding="utf-8")


def test_startup_logs_when_no_issues(
    mock_dir: Path, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level(logging.INFO)
    with TestClient(app) as client:
        assert client.get("/health").status_code == 200
    assert "No mock issues found" in caplog.text


def test_startup_logs_picked_issue(
    mock_dir: Path, caplog: pytest.LogCaptureFixture
) -> None:
    _write_issue(mock_dir, "a.json", VALID_INCIDENT)
    caplog.set_level(logging.INFO)
    with TestClient(app):
        pass
    assert "id=inc-001" in caplog.text
    assert "service=payment-api" in caplog.text
    assert "alert_name=HighErrorRate" in caplog.text


def test_poll_returns_next_issue_after_startup(mock_dir: Path) -> None:
    _write_issue(mock_dir, "a.json", {**VALID_INCIDENT, "id": "inc-a"})
    _write_issue(mock_dir, "b.json", {**VALID_INCIDENT, "id": "inc-b"})
    with TestClient(app) as client:
        response = client.post("/poll")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "picked"
    assert body["id"] == "inc-b"
    assert body["service"] == "payment-api"
    assert body["alert_name"] == "HighErrorRate"


def test_poll_when_none_left_does_not_crash(mock_dir: Path) -> None:
    with TestClient(app) as client:
        response = client.post("/poll")
    assert response.status_code == 200
    assert response.json() == {"status": "no issues found"}
