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
    limit: Optional[int] = Query(None, ge=1, le=100),
    offset: Optional[int] = Query(None, ge=0),
    service: ZammadService = Depends(get_zammad_service),
) -> List[Ticket]:
    """Get all tickets."""
    try:
        return await service.get_all_tickets(limit=limit, offset=offset)
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

