"""Tests for the FastAPI application."""

from fastapi.testclient import TestClient


def test_health_check(client: TestClient) -> None:
    """Test that the health endpoint returns a healthy status."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
