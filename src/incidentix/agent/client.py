"""Ollama client wrapper for tool-use calls.

Translates between Anthropic-format tool schemas (the source of truth in
agent/tools/specs.py) and Ollama's API format. This file is the only place
that knows Ollama-specific details, so switching to the Anthropic API later
requires no changes to specs.py or the agent loop.
"""

import requests


def anthropic_tool_to_ollama(anthropic_tool: dict) -> dict:
    """Converts one Anthropic-format tool schema into Ollama's nested format.

    Anthropic shape:  {"name": ..., "description": ..., "input_schema": {...}}
    Ollama shape:      {"type": "function", "function": {"name": ...,
                        "description": ..., "parameters": {...}}}
    """
    return {
        "type": "function",
        "function": {
            "name": anthropic_tool["name"],
            "description": anthropic_tool["description"],
            "parameters": anthropic_tool["input_schema"],
        },
    }


def normalize_ollama_response(ollama_response: dict) -> dict:
    """Converts Ollama's raw response into a normalized shape.

    The agent loop can consume this shape regardless of which LLM provider
    is behind it.

    Normalized shape:
        {
            "text": "...",
            "tool_calls": [{"name": "...", "input": {...}}, ...]
        }
    """
    message = ollama_response.get("message", {})
    raw_tool_calls = message.get("tool_calls", [])

    tool_calls = [
        {
            "name": tc["function"]["name"],
            "input": tc["function"]["arguments"],
        }
        for tc in raw_tool_calls
    ]

    return {
        "text": message.get("content", ""),
        "tool_calls": tool_calls,
    }


class OllamaClient:
    """Thin wrapper around Ollama's /api/chat endpoint."""

    def __init__(
        self, model: str = "qwen2.5", base_url: str = "http://localhost:11434"
    ):
        """Initializes the client with a model name and Ollama server URL."""
        self.model = model
        self.base_url = base_url

    def run_with_tools(
        self, system_prompt: str, tools: list[dict], messages: list[dict]
    ) -> dict:
        """Sends a chat request with tools to Ollama and returns a normalized response.

        Args:
            system_prompt: the system-level instructions for the agent.
            tools: list of Anthropic-format tool schemas (e.g. GET_LOGS_SCHEMA).
            messages: conversation history (user/assistant/tool messages).

        Returns:
            Normalized dict: {"text": str, "tool_calls": [{"name", "input"}, ...]}
        """
        ollama_tools = [anthropic_tool_to_ollama(t) for t in tools]

        full_messages = [{"role": "system", "content": system_prompt}] + messages

        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": full_messages,
                "tools": ollama_tools,
                "stream": False,
            },
        )
        response.raise_for_status()

        return normalize_ollama_response(response.json())
