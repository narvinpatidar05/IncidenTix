"""Load mock incident JSON files from data/mock_issues/."""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import ValidationError

from incidentix.incident.models import Incident

_REPO_ROOT = Path(__file__).resolve().parents[3]
MOCK_ISSUES_DIR = _REPO_ROOT / "data" / "mock_issues"

_processed_paths: set[str] = set()


class IncidentLoadError(ValueError):
    """Raised when a mock issue file cannot be parsed into an Incident."""


def list_mock_issues() -> list[Path]:
    """Return sorted JSON file paths under the mock issues directory."""
    if not MOCK_ISSUES_DIR.is_dir():
        return []
    return sorted(path for path in MOCK_ISSUES_DIR.glob("*.json") if path.is_file())


def load_incident(path: Path | str) -> Incident:
    """Parse a JSON file into an Incident.

    Raises:
        IncidentLoadError: If the file is missing, not JSON, or fails validation.
    """
    file_path = Path(path)
    try:
        payload = json.loads(file_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise IncidentLoadError(f"Incident file not found: {file_path}") from exc
    except json.JSONDecodeError as exc:
        raise IncidentLoadError(
            f"Malformed incident JSON in {file_path}: {exc.msg}"
        ) from exc
    except OSError as exc:
        raise IncidentLoadError(
            f"Could not read incident file {file_path}: {exc}"
        ) from exc

    try:
        return Incident.model_validate(payload)
    except ValidationError as exc:
        raise IncidentLoadError(
            f"Malformed incident data in {file_path}: {exc}"
        ) from exc


def pick_next_issue() -> Incident | None:
    """Return the next unprocessed mock issue, or None if none remain."""
    for path in list_mock_issues():
        key = str(path.resolve())
        if key in _processed_paths:
            continue
        incident = load_incident(path)
        _processed_paths.add(key)
        return incident
    return None
