# incidenTix

AI-powered incident root-cause-analysis (RCA) agent — investigates production alerts using an agentic tool-use loop (logs, metrics, deploy history) and produces structured root-cause findings.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

- Health: http://127.0.0.1:8000/health
- Docs: http://127.0.0.1:8000/docs

## Lint and format

```bash
pip install -r requirements-dev.txt
ruff check .
ruff format .
pre-commit install
```

`pre-commit install` ke baad har `git commit` pe lint/format hooks chalenge.

## Layout

```
app/
  main.py            # FastAPI server
  api/               # HTTP routes
  agent/             # RCA agent (later)
  tools/             # agent tools (later)
  providers/         # Loki / metrics adapters (later)
  models/            # domain objects
tests/
```
