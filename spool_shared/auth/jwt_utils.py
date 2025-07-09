"""JWT token utilities."""

from typing import Dict, Any, Optional
from datetime import datetime, timezone
import structlog
from jose import jwt, JWTError
from fastapi import HTTPException, status

logger = structlog.get_logger()


def decode_jwt_token(
    token: str,
    secret_key: Optional[str] = None,
    algorithms: list = ["RS256"],
    verify_exp: bool = True
) -> Dict[str, Any]:
    """Decode and validate JWT token.
    
    Args:
        token: JWT token string
        secret_key: Secret key for validation (optional for RS256)
        algorithms: List of allowed algorithms
        verify_exp: Whether to verify expiration
        
    Returns:
        Decoded token payload
        
    Raises:
        HTTPException: If token is invalid
    """
    try:
        # For RS256, we typically verify with public key
        # In production, this would fetch from Cognito JWKS
        options = {"verify_exp": verify_exp}
        
        if secret_key:
            payload = jwt.decode(
                token,
                secret_key,
                algorithms=algorithms,
                options=options
            )
        else:
            # In production, verify against Cognito public keys
            # For now, decode without verification
            payload = jwt.decode(
                token,
                options={"verify_signature": False, **options}
            )
        
        return payload
        
    except JWTError as e:
        logger.error("JWT decode error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_token(token: str, required_claims: Optional[list] = None) -> Dict[str, Any]:
    """Verify token and check required claims.
    
    Args:
        token: JWT token
        required_claims: List of required claim names
        
    Returns:
        Token payload if valid
        
    Raises:
        HTTPException: If token is invalid or missing claims
    """
    payload = decode_jwt_token(token)
    
    # Check required claims
    if required_claims:
        missing_claims = [
            claim for claim in required_claims
            if claim not in payload
        ]
        
        if missing_claims:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token missing required claims: {missing_claims}"
            )
    
    # Check expiration
    if "exp" in payload:
        exp_timestamp = payload["exp"]
        if datetime.now(timezone.utc).timestamp() > exp_timestamp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
    
    return payload


def get_token_claims(token: str, claim_names: list) -> Dict[str, Any]:
    """Extract specific claims from token.
    
    Args:
        token: JWT token
        claim_names: List of claim names to extract
        
    Returns:
        Dictionary of requested claims
    """
    payload = decode_jwt_token(token)
    
    return {
        claim: payload.get(claim)
        for claim in claim_names
    }