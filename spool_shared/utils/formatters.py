"""Formatting utilities."""

import re
from decimal import Decimal
from typing import Optional


def format_phone(phone: str, country_code: str = "US") -> str:
    """Format phone number for display.
    
    Args:
        phone: Phone number to format
        country_code: ISO country code
        
    Returns:
        Formatted phone number
    """
    # Remove all non-numeric characters
    digits = re.sub(r'\D', '', phone)
    
    if country_code == "US" and len(digits) == 10:
        # Format as (XXX) XXX-XXXX
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    
    # Return original if can't format
    return phone


def format_currency(
    amount: float,
    currency: str = "USD",
    decimal_places: int = 2
) -> str:
    """Format currency for display.
    
    Args:
        amount: Amount to format
        currency: Currency code
        decimal_places: Number of decimal places
        
    Returns:
        Formatted currency string
    """
    # Use Decimal for precise formatting
    decimal_amount = Decimal(str(amount))
    
    # Format with appropriate decimal places
    formatted = f"{decimal_amount:.{decimal_places}f}"
    
    # Add currency symbol
    currency_symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥"
    }
    
    symbol = currency_symbols.get(currency, currency + " ")
    
    # Add thousands separators
    parts = formatted.split(".")
    parts[0] = "{:,}".format(int(parts[0]))
    formatted = ".".join(parts)
    
    return f"{symbol}{formatted}"


def format_percentage(
    value: float,
    decimal_places: int = 1,
    include_sign: bool = True
) -> str:
    """Format percentage for display.
    
    Args:
        value: Value to format (0.0-1.0 or 0-100)
        decimal_places: Number of decimal places
        include_sign: Whether to include % sign
        
    Returns:
        Formatted percentage string
    """
    # Convert to percentage if needed
    if 0 <= value <= 1:
        value = value * 100
    
    # Format with decimal places
    formatted = f"{value:.{decimal_places}f}"
    
    # Add % sign if requested
    if include_sign:
        formatted += "%"
    
    return formatted


def format_file_size(size_bytes: int) -> str:
    """Format file size for display.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Human-readable size string
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    
    return f"{size_bytes:.1f} PB"


def truncate_text(
    text: str,
    max_length: int,
    suffix: str = "..."
) -> str:
    """Truncate text to maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    # Account for suffix length
    truncate_at = max_length - len(suffix)
    
    # Try to break at word boundary
    if " " in text[:truncate_at]:
        truncate_at = text[:truncate_at].rfind(" ")
    
    return text[:truncate_at] + suffix