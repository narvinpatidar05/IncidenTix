VENV := .venv
BIN := $(VENV)/bin

install:
	python3 -m venv $(VENV)
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -e ".[dev]"
	$(BIN)/pre-commit install
	$(BIN)/pre-commit install --hook-type commit-msg
	$(BIN)/pre-commit install --hook-type pre-push

lint:
	$(BIN)/ruff check src tests
	$(BIN)/mypy
	$(BIN)/lint-imports

format:
	$(BIN)/ruff check --fix src tests
	$(BIN)/ruff format src tests

test:
	$(BIN)/pytest
