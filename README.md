# incidenTix

AI-powered incident root-cause-analysis (RCA) agent — investigates production alerts using an agentic tool-use loop (logs, metrics, deploy history) and produces structured root-cause findings.

Requires **Python 3.11+**. Licensed under [MIT](LICENSE). Copy `.env.example` to `.env` for local secrets — never commit `.env`.

## Setup

```
make install
```

Creates `.venv`, installs runtime and dev dependencies (`ruff`, `mypy`, `pre-commit`, `import-linter`, `pytest`), and enables pre-commit, commit-msg, and pre-push hooks.

## Run

```
source .venv/bin/activate
cp .env.example .env
uvicorn src.incidentix.main:app --reload
```

* Health: http://127.0.0.1:8000/health
* Docs: http://127.0.0.1:8000/docs

## Lint, format, and test

```
make lint
make format
make test
```

Activate `.venv` before committing so local hooks (`import-linter`, `pytest`) are on `PATH`. Commit messages must follow [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `chore:`, …). Tests run on `git push`, not on every commit.

## Layout

```
src/
  incidentix/
    main.py            # FastAPI server
    config.py          # global settings
    database.py        # global DB setup
    exceptions.py      # global custom exceptions
    agent/              # RCA agent orchestration (later)
      models.py
      service.py
      tools/            # agent tools (later)
    incident/            # core incident domain (later)
      models.py
      schemas.py
      service.py
      views.py
    provider/             # Loki / metrics adapters (later)
      models.py
      service.py
    worker/               # background jobs (later)
    common/                # shared helpers across features
tests/
```

# Ollama Setup — Tool-Calling Verification

## Setup

- **Installed via:** `brew install ollama`
- **Server:** `ollama serve` (localhost:11434)
- **Model:** `qwen2.5:latest` (4.7 GB)

## Model choice reasoning

`qwen2.5` was tested first pragmatically.
This was not a rigorous head-to-head model comparison — this is early exploration and model
choice wasn't deeply evaluated yet. If tool-calling proves unreliable in
later, more complex scenarios, `llama3.1` or another tool-use-focused model
should be tried and properly compared as an alternative.

## Tool-calling test results

### Test 1 — Generic single tool call
**Prompt:** "What is the weather in San Francisco?"
**Tool offered:** `get_weather(location)`

**Result: PASS**
```json
"tool_calls": [{
  "function": {
    "name": "get_weather",
    "arguments": {"location": "San Francisco"}
  }
}]
```
Model correctly triggered the tool call and extracted the argument.

### Test 2 — Realistic RCA-style scenario
**Prompt:** "Investigate why payment-api is throwing high error rates. Check
the logs first."
**Tool offered:** `get_logs(service, query, minutes_back)`

**Result: PASS**
```json
"tool_calls": [{
  "function": {
    "name": "get_logs",
    "arguments": {"service": "payment-api", "minutes_back": 60}
  }
}]
```
Model correctly:
- Selected `get_logs` when prompted to "check logs first"
- Extracted `service` correctly from the prompt
- Inferred a reasonable default for `minutes_back` (60) even though no
  explicit time window was given

## Performance notes

- `total_duration`: ~8.6-8.8 sec per call (includes `load_duration` of
  ~4.4-5.7 sec — model load time, expected to be faster on subsequent calls
  once the model stays resident in memory)
- `eval_duration` (actual generation time): ~1.7-2.1 sec


The `OllamaClient` wrapper (next issue) needs to:
1. Convert `GET_LOGS_SCHEMA`/`GET_METRICS_SCHEMA` into
   Ollama's `{"type": "function", "function": {...}}` shape before sending
2. Normalize Ollama's response `tool_calls` back into a consistent internal
   shape the agent loop expects

## Conclusion

`qwen2.5` supports tool-calling reliably in these two basic tests. Sufficient
to proceed with building the `OllamaClient` wrapper. Multi-turn behavior
(tool result fed back, does the model continue reasoning correctly) is not
yet tested — that will be validated as part of the agentic loop issue.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup, branch names, commits, and PRs.
