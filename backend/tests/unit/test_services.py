"""
Unit tests for service layer.
"""
import pytest

from app.domain.models import Ticket, TicketStatistics
from app.services.zammad_service import ZammadService


@pytest.mark.asyncio
async def test_get_all_tickets(zammad_service: ZammadService):
    """Test getting all tickets."""
    mock_tickets = [
        Ticket(id=1, title="Ticket 1", state="open"),
        Ticket(id=2, title="Ticket 2", state="closed"),
    ]
    zammad_service.repository.get_tickets = pytest.AsyncMock(return_value=mock_tickets)

    result = await zammad_service.get_all_tickets()

    assert len(result) == 2
    assert result[0].id == 1
    zammad_service.repository.get_tickets.assert_called_once_with(limit=None, offset=None)


@pytest.mark.asyncio
async def test_get_ticket_statistics(zammad_service: ZammadService):
    """Test getting ticket statistics."""
    mock_tickets = [
        Ticket(id=1, state="open", priority="high"),
        Ticket(id=2, state="open", priority="low"),
        Ticket(id=3, state="closed", priority="high"),
    ]
    zammad_service.repository.get_tickets = pytest.AsyncMock(return_value=mock_tickets)

    result = await zammad_service.get_ticket_statistics()

    assert isinstance(result, TicketStatistics)
    assert result.total_tickets == 3
    assert result.open_tickets == 2
    assert result.closed_tickets == 1
    assert result.tickets_by_state["open"] == 2
    assert result.tickets_by_state["closed"] == 1
    assert result.tickets_by_priority["high"] == 2
    assert result.tickets_by_priority["low"] == 1

