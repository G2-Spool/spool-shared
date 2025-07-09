"""Custom exceptions."""

from .base import (
    SpoolException, ValidationException, NotFoundException,
    AuthenticationException, AuthorizationException,
    ConflictException, RateLimitException
)

__all__ = [
    "SpoolException", "ValidationException", "NotFoundException",
    "AuthenticationException", "AuthorizationException",
    "ConflictException", "RateLimitException"
]