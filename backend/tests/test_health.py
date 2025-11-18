"""
Tests for health check endpoints
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.mark.api
def test_root_endpoint():
    """Test root endpoint returns welcome message"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "docs" in data


@pytest.mark.api
def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


@pytest.mark.api
def test_api_health_endpoint():
    """Test API health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    assert "service" in data
    assert "version" in data
    assert "timestamp" in data


@pytest.mark.api
def test_liveness_check():
    """Test liveness check endpoint"""
    response = client.get("/api/v1/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"
    assert "timestamp" in data


# Example of a slow test
@pytest.mark.slow
def test_example_slow_test():
    """Example of a test marked as slow"""
    import time
    time.sleep(0.1)
    assert True
