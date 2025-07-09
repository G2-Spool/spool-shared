"""Authentication schemas."""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, UUID4


class TokenData(BaseModel):
    """JWT token data."""
    sub: str = Field(..., description="Subject (user ID)")
    email: Optional[str] = None
    roles: List[str] = Field(default_factory=list)
    permissions: List[str] = Field(default_factory=list)
    exp: Optional[int] = None
    iat: Optional[int] = None
    iss: Optional[str] = None


class UserClaims(BaseModel):
    """User claims from JWT."""
    sub: UUID4
    email: str
    email_verified: bool = False
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    roles: List[str] = Field(default_factory=list)
    groups: List[str] = Field(default_factory=list, alias="cognito:groups")
    permissions: List[str] = Field(default_factory=list)
    custom_attributes: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        populate_by_name = True


class AuthenticationRequest(BaseModel):
    """Authentication request."""
    username: str
    password: str


class RefreshTokenRequest(BaseModel):
    """Refresh token request."""
    refresh_token: str


class TokenResponse(BaseModel):
    """Token response."""
    access_token: str
    token_type: str = "Bearer"
    expires_in: int
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None