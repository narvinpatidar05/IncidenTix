# tests/agent/test_client_integration.py
"""Integration tests for OllamaClient — requires a running local Ollama
server with qwen2.5 pulled. These are SKIPPED automatically if Ollama
isn't reachable, so they don't break CI.
"""

import pytest
import requests

from incidentix.agent.client import OllamaClient


def _ollama_is_running() -> bool:
    """Checks if a local Ollama server is reachable before running these tests."""
    try:
        requests.get("http://localhost:11434", timeout=2)
        return True
    except requests.exceptions.ConnectionError:
        return False


requires_ollama = pytest.mark.skipif(
    not _ollama_is_running(),
    reason="Ollama server not running locally on port 11434",
)


@requires_ollama
class TestOllamaClientIntegration:
    """Real, end-to-end tests against a locally running Ollama + qwen2.5."""

    def test_run_with_tools_returns_valid_tool_call(self):
        client = OllamaClient(model="qwen2.5")

        response = client.run_with_tools(
            system_prompt="You are an SRE investigating an incident.",
            tools=[
                {
                    "name": "get_logs",
                    "description": "Fetch application logs for a specific service.",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "service": {
                                "type": "string",
                                "description": "service name",
                            },
                            "minutes_back": {
                                "type": "integer",
                                "description": "time window",
                            },
                        },
                        "required": ["service", "minutes_back"],
                    },
                }
            ],
            messages=[
                {
                    "role": "user",
                    "content": "Check logs for payment-api, last 30 minutes.",
                }
            ],
        )

        # Structural checks — the normalized shape is always correct
        assert "text" in response
        assert "tool_calls" in response
        assert isinstance(response["tool_calls"], list)

        # Behavioral checks — did the model actually pick the right tool
        # and extract the right arguments from the prompt?
        assert len(response["tool_calls"]) == 1
        tool_call = response["tool_calls"][0]
        assert tool_call["name"] == "get_logs"
        assert tool_call["input"]["service"] == "payment-api"
        assert tool_call["input"]["minutes_back"] == 30
