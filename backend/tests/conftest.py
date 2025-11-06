"""
Pytest configuration and fixtures.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock

from app.domain.models import Ticket, Organization, User
from app.repositories.zammad_repository import IZammadRepository
from app.services.zammad_service import ZammadService


@pytest.fixture
def mock_ticket() -> Ticket:
    """Create a mock ticket."""
    return Ticket(
        id=1,
        number="12345",
        title="Test Ticket",
        state="open",
        priority="high",
    )


@pytest.fixture
def mock_organization() -> Organization:
    """Create a mock organization."""
    return Organization(
        id=1,
        name="Test Organization",
        active=True,
    )


@pytest.fixture
def mock_user() -> User:
    """Create a mock user."""
    return User(
        id=1,
        login="testuser",
        firstname="Test",
        lastname="User",
        email="test@example.com",
        active=True,
    )


@pytest.fixture
def mock_repository() -> IZammadRepository:
    """Create a mock repository."""
    repository = MagicMock(spec=IZammadRepository)
    repository.get_tickets = AsyncMock(return_value=[])
    repository.get_ticket = AsyncMock(return_value=None)
    repository.get_organizations = AsyncMock(return_value=[])
    repository.get_users = AsyncMock(return_value=[])
    return repository


@pytest.fixture
def zammad_service(mock_repository: IZammadRepository) -> ZammadService:
    """Create a Zammad service with mocked repository."""
    return ZammadService(repository=mock_repository)

