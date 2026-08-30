"""Tests for incident mock-issue loader."""

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from incidentix.incident import loader
from incidentix.incident.models import Incident

VALID_INCIDENT = {
    "id": "inc-001",
    "service": "payment-api",
    "alert_name": "HighErrorRate",
    "severity": "critical",
    "raw_payload": {"status": "firing", "value": 0.42},
    "created_at": datetime(2026, 8, 29, 10, 0, 0, tzinfo=UTC).isoformat(),
}


@pytest.fixture
def mock_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(loader, "MOCK_ISSUES_DIR", tmp_path)
    loader._processed_paths.clear()
    return tmp_path


def _write_issue(directory: Path, name: str, payload: dict) -> Path:
    path = directory / name
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_list_mock_issues_missing_dir_returns_empty(mock_dir: Path) -> None:
    mock_dir.rmdir()
    assert loader.list_mock_issues() == []


def test_list_mock_issues_returns_sorted_json_paths(mock_dir: Path) -> None:
    _write_issue(mock_dir, "z-last.json", VALID_INCIDENT)
    _write_issue(mock_dir, "a-first.json", VALID_INCIDENT)
    (mock_dir / "notes.txt").write_text("ignore me", encoding="utf-8")
    (mock_dir / "nested").mkdir()
    _write_issue(mock_dir / "nested", "hidden.json", VALID_INCIDENT)

    paths = loader.list_mock_issues()
    assert [path.name for path in paths] == ["a-first.json", "z-last.json"]


def test_load_incident_parses_valid_json(mock_dir: Path) -> None:
    path = _write_issue(mock_dir, "issue.json", VALID_INCIDENT)
    incident = loader.load_incident(path)
    assert isinstance(incident, Incident)
    assert incident.id == "inc-001"
    assert incident.service == "payment-api"
    assert incident.alert_name == "HighErrorRate"
    assert incident.severity == "critical"
    assert incident.raw_payload == {"status": "firing", "value": 0.42}


def test_load_incident_invalid_json_raises(mock_dir: Path) -> None:
    path = mock_dir / "bad.json"
    path.write_text("{not-json", encoding="utf-8")
    with pytest.raises(loader.IncidentLoadError, match="Malformed incident JSON"):
        loader.load_incident(path)


def test_load_incident_missing_fields_raises(mock_dir: Path) -> None:
    path = _write_issue(mock_dir, "incomplete.json", {"id": "inc-002"})
    with pytest.raises(loader.IncidentLoadError, match="Malformed incident data"):
        loader.load_incident(path)


def test_load_incident_missing_file_raises(mock_dir: Path) -> None:
    with pytest.raises(loader.IncidentLoadError, match="not found"):
        loader.load_incident(mock_dir / "nope.json")


def test_pick_next_issue_returns_incidents_then_none(mock_dir: Path) -> None:
    first = {**VALID_INCIDENT, "id": "inc-a"}
    second = {**VALID_INCIDENT, "id": "inc-b"}
    _write_issue(mock_dir, "b.json", second)
    _write_issue(mock_dir, "a.json", first)

    picked_first = loader.pick_next_issue()
    picked_second = loader.pick_next_issue()
    picked_third = loader.pick_next_issue()

    assert picked_first is not None and picked_first.id == "inc-a"
    assert picked_second is not None and picked_second.id == "inc-b"
    assert picked_third is None


def test_pick_next_issue_empty_dir_returns_none(mock_dir: Path) -> None:
    assert loader.pick_next_issue() is None
