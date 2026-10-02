"""Run get_logs / get_metrics against the mock providers."""

from __future__ import annotations

import json

from incidentix.incident.models import Incident
from incidentix.provider.registry import get_log_provider, get_metric_provider

_MOCK = "mock"


def _as_dict(arguments: dict | str) -> dict:
    if isinstance(arguments, str):
        loaded = json.loads(arguments)
        if not isinstance(loaded, dict):
            return {}
        return loaded
    return arguments


def execute_get_logs(arguments: dict | str, incident: Incident) -> str:
    """Fetch mock logs and return JSON for the model.

    Args:
        arguments: Tool args from the model (dict or JSON string).
        incident: Current incident; used for default service/query.

    Returns:
        JSON array of log records.
    """
    args = _as_dict(arguments)
    service = str(args.get("service") or incident.service)
    query = str(args.get("query") or incident.alert_name)
    minutes_back = int(args.get("minutes_back") or 60)
    logs = get_log_provider(_MOCK).fetch_logs(service, query, minutes_back)
    return json.dumps([log.model_dump(mode="json") for log in logs])


def execute_get_metrics(arguments: dict | str, incident: Incident) -> str:
    """Fetch mock metrics and return JSON for the model.

    Args:
        arguments: Tool args from the model (dict or JSON string).
        incident: Current incident; used for default query.

    Returns:
        JSON object for one metric series.
    """
    args = _as_dict(arguments)
    query = str(args.get("query") or incident.alert_name)
    minutes_back = int(args.get("minutes_back") or 60)
    record = get_metric_provider(_MOCK).fetch_metrics(query, minutes_back)
    return json.dumps(record.model_dump(mode="json"))
