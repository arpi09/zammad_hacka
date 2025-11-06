"""
Integration tests for API endpoints.
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.zammad_service import ZammadService
from app.repositories.zammad_repository import IZammadRepository


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.mark.asyncio
async def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data

