"""
Repository for Zammad API interactions.
Follows Interface Segregation and Dependency Inversion Principles.
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.models import Organization, Ticket, User


class IZammadRepository(ABC):
    """Interface for Zammad repository. Follows Interface Segregation Principle."""

    @abstractmethod
    async def get_tickets(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> List[Ticket]:
        """Get tickets from Zammad."""
        pass

    @abstractmethod
    async def get_ticket(self, ticket_id: int) -> Optional[Ticket]:
        """Get a single ticket by ID."""
        pass

    @abstractmethod
    async def get_organizations(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> List[Organization]:
        """Get organizations from Zammad."""
        pass

    @abstractmethod
    async def get_users(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> List[User]:
        """Get users from Zammad."""
        pass


class ZammadRepository(IZammadRepository):
    """
    Concrete implementation of Zammad repository.
    Follows Single Responsibility Principle - handles only Zammad API communication.
    """

    def __init__(self, base_url: str, api_token: str):
        """Initialize repository with Zammad API configuration."""
        self.base_url = base_url.rstrip("/")
        self.api_token = api_token
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        }

    async def _make_request(self, endpoint: str) -> dict:
        """Make HTTP request to Zammad API."""
        import httpx

        url = f"{self.base_url}{endpoint}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, timeout=30.0)
            response.raise_for_status()
            return response.json()

    async def get_tickets(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> List[Ticket]:
        """Get tickets from Zammad."""
        endpoint = "/api/v1/tickets"
        params = []
        if limit:
            params.append(f"limit={limit}")
        if offset:
            params.append(f"offset={offset}")
        if params:
            endpoint += "?" + "&".join(params)

        data = await self._make_request(endpoint)
        return [Ticket(**ticket) for ticket in data]

    async def get_ticket(self, ticket_id: int) -> Optional[Ticket]:
        """Get a single ticket by ID."""
        endpoint = f"/api/v1/tickets/{ticket_id}"
        try:
            data = await self._make_request(endpoint)
            return Ticket(**data)
        except Exception:
            return None

    async def get_organizations(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> List[Organization]:
        """Get organizations from Zammad."""
        endpoint = "/api/v1/organizations"
        params = []
        if limit:
            params.append(f"limit={limit}")
        if offset:
            params.append(f"offset={offset}")
        if params:
            endpoint += "?" + "&".join(params)

        data = await self._make_request(endpoint)
        return [Organization(**org) for org in data]

    async def get_users(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> List[User]:
        """Get users from Zammad."""
        endpoint = "/api/v1/users"
        params = []
        if limit:
            params.append(f"limit={limit}")
        if offset:
            params.append(f"offset={offset}")
        if params:
            endpoint += "?" + "&".join(params)

        data = await self._make_request(endpoint)
        return [User(**user) for user in data]

