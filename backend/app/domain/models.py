"""
Domain models representing business entities.
Follows Single Responsibility Principle - each model represents one entity.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Ticket(BaseModel):
    """Ticket domain model."""

    id: int
    number: Optional[str] = None
    title: Optional[str] = None
    state: Optional[str] = None
    priority: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    customer_id: Optional[int] = None
    organization_id: Optional[int] = None

    class Config:
        """Pydantic config."""

        from_attributes = True


class Organization(BaseModel):
    """Organization domain model."""

    id: int
    name: Optional[str] = None
    active: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        """Pydantic config."""

        from_attributes = True


class User(BaseModel):
    """User domain model."""

    id: int
    login: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    active: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        """Pydantic config."""

        from_attributes = True


class TicketStatistics(BaseModel):
    """Statistics model for tickets."""

    total_tickets: int
    open_tickets: int
    closed_tickets: int
    tickets_by_state: dict[str, int] = Field(default_factory=dict)
    tickets_by_priority: dict[str, int] = Field(default_factory=dict)

