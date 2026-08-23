"""Shared pytest fixtures."""

import pytest
from fastapi.testclient import TestClient

from incidentix.main import app


@pytest.fixture
def client() -> TestClient:
    """Return a test client for the FastAPI application."""
    return TestClient(app)
