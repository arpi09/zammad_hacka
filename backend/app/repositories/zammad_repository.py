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
        self,
        per_page: Optional[int] = 500,
        page: Optional[int] = 1,
        sort_by: Optional[str] = "created_at",
        order: Optional[str] = "desc",
        fetch_all: bool = False,
    ) -> List[Ticket]:
        """Get tickets from Zammad with pagination and sorting."""
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
        self,
        per_page: Optional[int] = 500,
        page: Optional[int] = 1,
        sort_by: Optional[str] = "created_at",
        order: Optional[str] = "desc",
        fetch_all: bool = False,
    ) -> List[Ticket]:
        """Get tickets from Zammad with pagination and sorting using search endpoint."""
        # Use search endpoint for sorting support
        endpoint = "/api/v1/tickets/search"
        all_tickets = []
        current_page = page if page is not None else 1
        
        # Use maximum per_page if not specified
        if per_page is None:
            per_page = 500
        
        # Default sorting to latest first
        if sort_by is None:
            sort_by = "created_at"
        if order is None:
            order = "desc"
        
        while True:
            # Search endpoint uses 'order_by' instead of 'order' and requires 'query=*' for all tickets
            params = [
                f"query=*",  # Get all tickets
                f"page={current_page}",
                f"per_page={per_page}",
                f"sort_by={sort_by}",
                f"order_by={order}"  # Note: search endpoint uses 'order_by' not 'order'
            ]
            endpoint_with_params = f"{endpoint}?{'&'.join(params)}"
            
            data = await self._make_request(endpoint_with_params)
            
            if not data or len(data) == 0:
                break  # No more tickets
            
            all_tickets.extend([Ticket(**ticket) for ticket in data])
            
            # Stop if not fetching all, or got less than requested (last page)
            if not fetch_all or len(data) < per_page:
                break
            
            current_page += 1
        
        return all_tickets

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

