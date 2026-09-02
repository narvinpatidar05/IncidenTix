"""Build the system prompt fed to the RCA agent."""

import json

from incidentix.incident.models import Incident

_PERSONA = """You are an SRE incident investigator.
Use tools to inspect logs and metrics before concluding a root cause.
Do not invent evidence. If data is missing, say so.
When you have enough evidence, submit structured findings."""


def build_system_prompt(incident: Incident) -> str:
    """Return persona instructions plus this incident's facts.

    Args:
        incident: Alert the agent must investigate.

    Returns:
        A single system prompt string.
    """
    payload = json.dumps(incident.raw_payload, default=str, indent=2)
    return (
        f"{_PERSONA}\n\n"
        "Incident:\n"
        f"- service: {incident.service}\n"
        f"- alert_name: {incident.alert_name}\n"
        f"- severity: {incident.severity}\n"
        f"- raw_payload:\n{payload}"
    )
