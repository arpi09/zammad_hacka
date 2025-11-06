"""
Main API router.
Follows Single Responsibility Principle - handles only routing.
"""
from fastapi import APIRouter

from app.api.v1.endpoints import tickets, statistics, organizations, users

api_router = APIRouter()

api_router.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
api_router.include_router(statistics.router, prefix="/statistics", tags=["statistics"])
api_router.include_router(organizations.router, prefix="/organizations", tags=["organizations"])
api_router.include_router(users.router, prefix="/users", tags=["users"])

