"""
Users API endpoints.
Follows Single Responsibility Principle - handles only user endpoints.
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.v1.dependencies import get_zammad_service
from app.domain.models import User
from app.services.zammad_service import ZammadService

router = APIRouter()


@router.get("/", response_model=List[User])
async def get_users(
    limit: Optional[int] = Query(None, ge=1, le=100),
    offset: Optional[int] = Query(None, ge=0),
    service: ZammadService = Depends(get_zammad_service),
) -> List[User]:
    """Get all users."""
    try:
        return await service.get_all_users(limit=limit, offset=offset)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")

