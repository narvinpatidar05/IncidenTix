"""Anthropic-format tool schemas consumed by OllamaClient."""

GET_LOGS_SCHEMA = {
    "name": "get_logs",
    "description": "Fetch application logs for a service over a time window.",
    "input_schema": {
        "type": "object",
        "properties": {
            "service": {"type": "string", "description": "Service name"},
            "query": {"type": "string", "description": "Log search query"},
            "minutes_back": {
                "type": "integer",
                "description": "How many minutes of logs to fetch",
            },
        },
        "required": ["service", "minutes_back"],
    },
}

GET_METRICS_SCHEMA = {
    "name": "get_metrics",
    "description": "Fetch a metric series over a time window.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Metric name or PromQL"},
            "minutes_back": {
                "type": "integer",
                "description": "How many minutes of metrics to fetch",
            },
        },
        "required": ["query", "minutes_back"],
    },
}

SUBMIT_FINDINGS_SCHEMA = {
    "name": "submit_findings",
    "description": "Submit the final root-cause findings and stop the investigation.",
    "input_schema": {
        "type": "object",
        "properties": {
            "root_cause": {"type": "string"},
            "evidence": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 1,
            },
            "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
            "suggested_fix": {"type": "string"},
        },
        "required": ["root_cause", "evidence", "confidence", "suggested_fix"],
    },
}

AGENT_TOOLS = [GET_LOGS_SCHEMA, GET_METRICS_SCHEMA, SUBMIT_FINDINGS_SCHEMA]
