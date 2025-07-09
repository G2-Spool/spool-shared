"""Base exception classes."""

from typing import Any, Dict, Optional
from fastapi import HTTPException, status


class SpoolException(HTTPException):
    """Base exception for Spool services."""
    
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.error_code = error_code or self.__class__.__name__


class ValidationException(SpoolException):
    """Validation error exception."""
    
    def __init__(self, detail: str, field: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {detail}" + (f" (field: {field})" if field else ""),
            error_code="VALIDATION_ERROR"
        )
        self.field = field


class NotFoundException(SpoolException):
    """Resource not found exception."""
    
    def __init__(self, resource: str, identifier: Any):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} not found: {identifier}",
            error_code="NOT_FOUND"
        )
        self.resource = resource
        self.identifier = identifier


class AuthenticationException(SpoolException):
    """Authentication failure exception."""
    
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code="AUTHENTICATION_FAILED",
            headers={"WWW-Authenticate": "Bearer"}
        )


class AuthorizationException(SpoolException):
    """Authorization failure exception."""
    
    def __init__(self, detail: str = "Insufficient permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_code="AUTHORIZATION_FAILED"
        )


class ConflictException(SpoolException):
    """Resource conflict exception."""
    
    def __init__(self, detail: str, resource: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            error_code="CONFLICT"
        )
        self.resource = resource


class RateLimitException(SpoolException):
    """Rate limit exceeded exception."""
    
    def __init__(
        self,
        detail: str = "Rate limit exceeded",
        retry_after: Optional[int] = None
    ):
        headers = {}
        if retry_after:
            headers["Retry-After"] = str(retry_after)
            
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail,
            error_code="RATE_LIMIT_EXCEEDED",
            headers=headers
        )
        self.retry_after = retry_after