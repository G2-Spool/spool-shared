"""Permission checking utilities."""

from typing import List, Dict, Any
from fastapi import HTTPException, status


def check_permission(
    user_claims: Dict[str, Any],
    required_permission: str,
    resource_owner: str = None
) -> bool:
    """Check if user has required permission.
    
    Args:
        user_claims: User's JWT claims
        required_permission: Required permission string
        resource_owner: Optional resource owner ID for ownership checks
        
    Returns:
        True if permission granted
        
    Raises:
        HTTPException: If permission denied
    """
    # Check if user has admin role
    if has_role(user_claims, "admin"):
        return True
    
    # Check specific permissions
    permissions = user_claims.get("permissions", [])
    if required_permission in permissions:
        return True
    
    # Check resource ownership
    if resource_owner and user_claims.get("sub") == resource_owner:
        return True
    
    # Check role-based permissions
    roles = user_claims.get("roles", [])
    role_permissions = {
        "instructor": [
            "view_all_progress",
            "view_analytics",
            "create_content",
            "modify_content"
        ],
        "student": [
            "view_own_progress",
            "submit_exercises",
            "earn_badges"
        ]
    }
    
    for role in roles:
        if required_permission in role_permissions.get(role, []):
            return True
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Permission denied: {required_permission}"
    )


def has_role(user_claims: Dict[str, Any], role: str) -> bool:
    """Check if user has specific role.
    
    Args:
        user_claims: User's JWT claims
        role: Role to check
        
    Returns:
        True if user has role
    """
    roles = user_claims.get("roles", [])
    groups = user_claims.get("cognito:groups", [])
    
    # Check both roles claim and Cognito groups
    return role in roles or role in groups


def require_roles(required_roles: List[str]):
    """Decorator to require specific roles.
    
    Args:
        required_roles: List of acceptable roles (user needs at least one)
        
    Returns:
        Decorator function
    """
    def decorator(func):
        async def wrapper(*args, current_user: Dict[str, Any] = None, **kwargs):
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            user_roles = current_user.get("roles", [])
            user_groups = current_user.get("cognito:groups", [])
            all_user_roles = set(user_roles + user_groups)
            
            if not any(role in all_user_roles for role in required_roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Required roles: {required_roles}"
                )
            
            return await func(*args, current_user=current_user, **kwargs)
        
        return wrapper
    return decorator