"""Tests for the application skeleton endpoints."""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint() -> None:
    """The health endpoint should return an ok status."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_root_endpoint() -> None:
    """The root endpoint should return a welcome message."""
    response = client.get("/")

    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]

