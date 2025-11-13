"""
Rugby Atlas - Health Check Tests
Tests for the health check endpoint
"""
import pytest
from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_health_endpoint():
    """Test the /health endpoint returns 200 OK"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "Rugby Atlas API"}


def test_healthz_endpoint():
    """Test the /healthz endpoint returns 200 OK"""
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "Rugby Atlas API"}


def test_root_endpoint():
    """Test the root endpoint returns service information"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert "version" in data
    assert "status" in data
    assert data["status"] == "running"
