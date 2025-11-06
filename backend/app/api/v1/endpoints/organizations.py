"""
Organizations API endpoints.
Follows Single Responsibility Principle - handles only organization endpoints.
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.v1.dependencies import get_zammad_service
from app.domain.models import Organization
from app.services.zammad_service import ZammadService

router = APIRouter()


@router.get("/", response_model=List[Organization])
async def get_organizations(
    limit: Optional[int] = Query(None, ge=1, le=100),
    offset: Optional[int] = Query(None, ge=0),
    service: ZammadService = Depends(get_zammad_service),
) -> List[Organization]:
    """Get all organizations."""
    try:
        return await service.get_all_organizations(limit=limit, offset=offset)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching organizations: {str(e)}"
        )

