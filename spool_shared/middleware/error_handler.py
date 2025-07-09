"""Global error handler middleware."""

from typing import Callable
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import structlog
import traceback

from spool_shared.exceptions import SpoolException
from spool_shared.schemas.common import ErrorResponse

logger = structlog.get_logger()


async def error_handler_middleware(request: Request, call_next: Callable) -> Response:
    """Global error handler for consistent error responses."""
    try:
        return await call_next(request)
        
    except SpoolException as e:
        # Handle custom Spool exceptions
        error_response = ErrorResponse(
            error=e.error_code,
            detail=e.detail,
            status_code=e.status_code,
            request_id=getattr(request.state, "correlation_id", None)
        )
        
        return JSONResponse(
            status_code=e.status_code,
            content=error_response.model_dump(),
            headers=e.headers
        )
        
    except ValueError as e:
        # Handle validation errors
        error_response = ErrorResponse(
            error="VALIDATION_ERROR",
            detail=str(e),
            status_code=422,
            request_id=getattr(request.state, "correlation_id", None)
        )
        
        return JSONResponse(
            status_code=422,
            content=error_response.model_dump()
        )
        
    except Exception as e:
        # Handle unexpected errors
        logger.error(
            "Unhandled exception",
            error=str(e),
            error_type=type(e).__name__,
            traceback=traceback.format_exc(),
            path=request.url.path,
            method=request.method
        )
        
        error_response = ErrorResponse(
            error="INTERNAL_SERVER_ERROR",
            detail="An unexpected error occurred",
            status_code=500,
            request_id=getattr(request.state, "correlation_id", None)
        )
        
        return JSONResponse(
            status_code=500,
            content=error_response.model_dump()
        )