.PHONY: install lint test format

VENV := .venv
BIN := $(VENV)/bin
PYTHON := python3

install:
	@$(PYTHON) -c 'import sys; assert sys.version_info >= (3, 11), "Python 3.11+ is required. Install Python 3.11 or newer and try again."' 
	$(PYTHON) -m venv $(VENV)
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
