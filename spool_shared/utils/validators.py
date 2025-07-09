"""Validation utilities."""

import re
from typing import Optional
from uuid import UUID


def validate_uuid(value: str) -> bool:
    """Validate UUID string.
    
    Args:
        value: String to validate
        
    Returns:
        True if valid UUID
    """
    try:
        UUID(value)
        return True
    except (ValueError, AttributeError):
        return False


def validate_email(email: str) -> bool:
    """Validate email address.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid email
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str, country_code: Optional[str] = "US") -> bool:
    """Validate phone number.
    
    Args:
        phone: Phone number to validate
        country_code: ISO country code (default: US)
        
    Returns:
        True if valid phone number
    """
    # Remove all non-numeric characters
    digits = re.sub(r'\D', '', phone)
    
    if country_code == "US":
        # US phone numbers should have 10 digits
        return len(digits) == 10 and digits[0] != '0' and digits[0] != '1'
    
    # Generic validation for international numbers
    return 7 <= len(digits) <= 15


def validate_password(password: str) -> tuple[bool, Optional[str]]:
    """Validate password strength.
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, None


def sanitize_input(value: str, max_length: Optional[int] = None) -> str:
    """Sanitize user input.
    
    Args:
        value: Input value to sanitize
        max_length: Maximum allowed length
        
    Returns:
        Sanitized string
    """
    # Strip whitespace
    value = value.strip()
    
    # Remove control characters
    value = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', value)
    
    # Limit length
    if max_length:
        value = value[:max_length]
    
    return value