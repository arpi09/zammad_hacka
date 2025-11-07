"""
Tickets API endpoints.
Follows Single Responsibility Principle - handles only ticket endpoints.
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.v1.dependencies import get_zammad_service
from app.domain.models import Ticket
from app.services.zammad_service import ZammadService

router = APIRouter()


@router.get("/", response_model=List[Ticket])
async def get_tickets(
    per_page: Optional[int] = Query(500, ge=1, le=500),
    page: Optional[int] = Query(1, ge=1),
    fetch_all: bool = Query(False),
    service: ZammadService = Depends(get_zammad_service),
) -> List[Ticket]:
    """Get tickets with pagination. Set fetch_all=True to get all tickets."""
    try:
        return await service.get_all_tickets(
            per_page=per_page,
            page=page,
            fetch_all=fetch_all
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tickets: {str(e)}")


@router.get("/{ticket_id}", response_model=Ticket)
async def get_ticket(
    ticket_id: int,
    service: ZammadService = Depends(get_zammad_service),
) -> Ticket:
    """Get a single ticket by ID."""
    ticket = await service.get_ticket_by_id(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

