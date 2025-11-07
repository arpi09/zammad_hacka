"""
Statistics API endpoints.
Follows Single Responsibility Principle - handles only statistics endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.v1.dependencies import get_zammad_service
from app.domain.models import TicketStatistics, TopCustomersResponse
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


@router.get("/top-customers", response_model=TopCustomersResponse)
async def get_top_customers(
    limit: int = Query(10, ge=1, le=100, description="Number of top customers to return"),
    service: ZammadService = Depends(get_zammad_service),
) -> TopCustomersResponse:
    """Get top customers by ticket count from latest tickets."""
    try:
        return await service.get_top_customers_by_tickets(limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting top customers: {str(e)}"
        )

