"""
Statistics API endpoints.
Follows Single Responsibility Principle - handles only statistics endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException

from app.api.v1.dependencies import get_zammad_service
from app.domain.models import TicketStatistics
from app.services.zammad_service import ZammadService

router = APIRouter()


@router.get("/tickets", response_model=TicketStatistics)
async def get_ticket_statistics(
    service: ZammadService = Depends(get_zammad_service),
) -> TicketStatistics:
    """Get ticket statistics."""
    try:
        return await service.get_ticket_statistics()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error calculating statistics: {str(e)}"
        )

