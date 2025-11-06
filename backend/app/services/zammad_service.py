"""
Service layer for Zammad business logic.
Follows Single Responsibility Principle - handles business logic for Zammad data.
Follows Dependency Inversion Principle - depends on repository interface.
"""
from typing import List, Optional

from app.domain.models import Organization, Ticket, TicketStatistics, User
from app.repositories.zammad_repository import IZammadRepository


class ZammadService:
    """
    Service for Zammad operations.
    Follows Open/Closed Principle - can be extended without modification.
    """

    def __init__(self, repository: IZammadRepository):
        """Initialize service with repository dependency."""
        self.repository = repository

    async def get_all_tickets(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> List[Ticket]:
        """Get all tickets."""
        return await self.repository.get_tickets(limit=limit, offset=offset)

    async def get_ticket_by_id(self, ticket_id: int) -> Optional[Ticket]:
        """Get ticket by ID."""
        return await self.repository.get_ticket(ticket_id)

    async def get_all_organizations(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> List[Organization]:
        """Get all organizations."""
        return await self.repository.get_organizations(limit=limit, offset=offset)

    async def get_all_users(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> List[User]:
        """Get all users."""
        return await self.repository.get_users(limit=limit, offset=offset)

    async def get_ticket_statistics(self) -> TicketStatistics:
        """Calculate ticket statistics."""
        tickets = await self.repository.get_tickets()

        total_tickets = len(tickets)
        open_tickets = sum(1 for t in tickets if t.state and t.state.lower() != "closed")
        closed_tickets = sum(1 for t in tickets if t.state and t.state.lower() == "closed")

        tickets_by_state: dict[str, int] = {}
        tickets_by_priority: dict[str, int] = {}

        for ticket in tickets:
            if ticket.state:
                tickets_by_state[ticket.state] = tickets_by_state.get(ticket.state, 0) + 1
            if ticket.priority:
                tickets_by_priority[ticket.priority] = (
                    tickets_by_priority.get(ticket.priority, 0) + 1
                )

        return TicketStatistics(
            total_tickets=total_tickets,
            open_tickets=open_tickets,
            closed_tickets=closed_tickets,
            tickets_by_state=tickets_by_state,
            tickets_by_priority=tickets_by_priority,
        )

