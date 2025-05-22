import pytest
import json
from main import app


@pytest.fixture
def client():
    """Create a test client for the app."""
    with app.test_client() as client:
        yield client


def test_index(client):
    """Test the index endpoint returns correct status and message."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello, DevOps!" in response.data


def test_health(client):
    """Test the health endpoint returns healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "healthy"
    assert "version" in data


def test_not_found(client):
    """Test that non-existent routes return 404 status code."""
    response = client.get("/nonexistent-route")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data
    assert data["error"] == "Not found"


def test_metrics(client):
    """Test that metrics endpoint is available."""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert b"flask_exporter_info" in response.data
