"""Agentic investigation loop: Ollama + tools until Findings or max iterations."""

from __future__ import annotations

import json
import logging
from typing import Protocol

from pydantic import ValidationError

from incidentix.agent.client import OllamaClient
from incidentix.agent.prompts import build_system_prompt
from incidentix.agent.tools.executors import execute_get_logs, execute_get_metrics
from incidentix.agent.tools.specs import AGENT_TOOLS
from incidentix.incident.models import Findings, Incident

MAX_ITERATIONS = 6
logger = logging.getLogger(__name__)


class InvestigationError(RuntimeError):
    """Raised when the loop ends without valid Findings."""


class ToolClient(Protocol):
    """Anything that can run a tool-use turn (OllamaClient or a test fake)."""

    def run_with_tools(
        self, system_prompt: str, tools: list[dict], messages: list[dict]
    ) -> dict:
        """Return normalized ``{text, tool_calls}`` for one model turn."""
        ...


def _tool_input(raw: dict | str) -> dict:
    if isinstance(raw, str):
        loaded = json.loads(raw)
        return loaded if isinstance(loaded, dict) else {}
    return raw


def run_investigation(incident: Incident, client: ToolClient | None = None) -> Findings:
    """Call Ollama with tools until submit_findings or MAX_ITERATIONS.

    Args:
        incident: Alert to investigate.
        client: Optional client (tests inject a fake). Defaults to OllamaClient.

    Returns:
        Validated Findings from submit_findings.

    Raises:
        InvestigationError: If the model never submits valid findings.
    """
    client = client or OllamaClient()
    system_prompt = build_system_prompt(incident)
    messages: list[dict] = [
        {
            "role": "user",
            "content": "Investigate this incident with tools, then submit_findings.",
        }
    ]

    for iteration in range(1, MAX_ITERATIONS + 1):
        response = client.run_with_tools(system_prompt, AGENT_TOOLS, messages)
        text = response.get("text") or ""
        tool_calls = response.get("tool_calls") or []
        logger.info("iteration=%s reasoning=%s", iteration, text)
        messages.append(
            {"role": "assistant", "content": text, "tool_calls": tool_calls}
        )

        if not tool_calls:
            logger.info("iteration=%s no tool calls", iteration)
            continue

        for call in tool_calls:
            name = call["name"]
            args = _tool_input(call.get("input") or {})
            logger.info("iteration=%s tool=%s args=%s", iteration, name, args)

            if name == "submit_findings":
                try:
                    findings = Findings.model_validate(args)
                except ValidationError as exc:
                    err = f"Invalid findings: {exc}"
                    logger.info("iteration=%s %s", iteration, err)
                    messages.append({"role": "tool", "content": err})
                    break
                logger.info(
                    "investigation done id=%s confidence=%s",
                    incident.id,
                    findings.confidence,
                )
                return findings

            if name == "get_logs":
                result = execute_get_logs(args, incident)
            elif name == "get_metrics":
                result = execute_get_metrics(args, incident)
            else:
                result = f"Unknown tool: {name}"
            logger.info(
                "iteration=%s tool=%s result_chars=%s",
                iteration,
                name,
                len(result),
            )
            messages.append({"role": "tool", "content": result})

    raise InvestigationError(
        f"No submit_findings after {MAX_ITERATIONS} iterations "
        f"for incident {incident.id}"
    )
