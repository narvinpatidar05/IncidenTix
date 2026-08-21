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

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup, branch names, commits, and PRs.
