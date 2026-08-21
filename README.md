# incidenTix

AI-powered incident root-cause-analysis (RCA) agent — investigates production alerts using an agentic tool-use loop (logs, metrics, deploy history) and produces structured root-cause findings.


## Run

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn src.incidentix.main:app --reload
```

* Health: http://127.0.0.1:8000/health
* Docs: http://127.0.0.1:8000/docs

## Lint and format

```
pip install -r requirements-dev.txt
ruff check .
ruff format .
pre-commit install
```

After `pre-commit install`, every `git commit` runs lint and format hooks.

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
    common/                # shared helpers across features
tests/
```
