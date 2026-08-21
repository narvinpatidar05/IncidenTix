# Contributing

Project overview and how to run the app: [README.md](README.md).

## Local development setup

```bash
git clone https://github.com/peachjelly13/incidenTix.git
cd incidenTix
make install
```

`make install` creates `.venv`, installs the package in editable mode with dev extras, and turns on git hooks. See the [Makefile](Makefile).

If you need to attach hooks without a full reinstall:

```bash
pre-commit install
pre-commit install --hook-type commit-msg
```

Activate `.venv` before `git commit` / `git push` so local hooks (`import-linter`, `pytest`) are on `PATH`.

## Branch naming

`<prefix>/<short-kebab-case-description>`

| Prefix | Use |
|---|---|
| `feature/` | new functionality |
| `fix/` | bug fixes |
| `chore/` | tooling, config, dependencies, maintenance |
| `docs/` | documentation only |
| `refactor/` | restructure with no behavior change |

Example: `chore/add-dependabot-config`

## Commit messages

This repo uses [Conventional Commits](https://www.conventionalcommits.org/). The `conventional-pre-commit` hook rejects messages that do not match.

Common types: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`

## Pull requests

- Do not push to `main`. Open a PR.
- CI checks must pass before merge.
- Opening a PR fills in [`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md). Use that checklist; do not copy it here.

## Architecture rule

`incidentix.agent`, `incidentix.incident`, and `incidentix.provider` must not import `incidentix.worker`.

## Running checks locally

```bash
make lint     # ruff + mypy + import-linter
make test     # pytest
make format   # ruff check --fix + ruff format
```
