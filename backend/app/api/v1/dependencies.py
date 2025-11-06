"""
Dependency injection for API endpoints.
Follows Dependency Inversion Principle - provides dependencies to endpoints.
"""
from app.core.config import settings
from app.repositories.zammad_repository import ZammadRepository
from app.services.zammad_service import ZammadService


def get_zammad_repository() -> ZammadRepository:
    """Create and return Zammad repository instance."""
    return ZammadRepository(
        base_url=settings.ZAMMAD_API_URL,
        api_token=settings.ZAMMAD_API_TOKEN,
    )


def get_zammad_service() -> ZammadService:
    """Create and return Zammad service instance."""
    repository = get_zammad_repository()
    return ZammadService(repository=repository)

