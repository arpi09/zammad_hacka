"""
Custom exceptions for the application.
Follows Single Responsibility Principle - handles only exception definitions.
"""
from fastapi import HTTPException, status


class ZammadAPIError(HTTPException):
    """Exception raised when Zammad API returns an error."""

    def __init__(self, detail: str, status_code: int = status.HTTP_502_BAD_GATEWAY):
        super().__init__(status_code=status_code, detail=detail)


class ConfigurationError(Exception):
    """Exception raised when configuration is invalid."""

    pass

