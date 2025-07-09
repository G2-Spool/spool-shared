"""Date and time utilities."""

from datetime import datetime, date, timedelta
from typing import Optional, Union
from dateutil import parser
import pytz


def parse_date(
    date_string: str,
    timezone: Optional[str] = None
) -> datetime:
    """Parse date string to datetime.
    
    Args:
        date_string: Date string to parse
        timezone: Optional timezone name
        
    Returns:
        Parsed datetime object
    """
    # Parse the date string
    dt = parser.parse(date_string)
    
    # Apply timezone if provided
    if timezone:
        tz = pytz.timezone(timezone)
        if dt.tzinfo is None:
            # Assume the datetime is in the given timezone
            dt = tz.localize(dt)
        else:
            # Convert to the given timezone
            dt = dt.astimezone(tz)
    
    return dt


def format_date(
    dt: Union[datetime, date],
    format_string: str = "%Y-%m-%d",
    timezone: Optional[str] = None
) -> str:
    """Format datetime to string.
    
    Args:
        dt: Datetime or date object
        format_string: strftime format string
        timezone: Optional timezone for conversion
        
    Returns:
        Formatted date string
    """
    # Convert date to datetime if needed
    if isinstance(dt, date) and not isinstance(dt, datetime):
        dt = datetime.combine(dt, datetime.min.time())
    
    # Apply timezone conversion if needed
    if timezone and isinstance(dt, datetime):
        tz = pytz.timezone(timezone)
        if dt.tzinfo is None:
            dt = pytz.utc.localize(dt)
        dt = dt.astimezone(tz)
    
    return dt.strftime(format_string)


def calculate_age(birth_date: date, as_of_date: Optional[date] = None) -> int:
    """Calculate age from birth date.
    
    Args:
        birth_date: Date of birth
        as_of_date: Date to calculate age as of (default: today)
        
    Returns:
        Age in years
    """
    if as_of_date is None:
        as_of_date = date.today()
    
    age = as_of_date.year - birth_date.year
    
    # Adjust if birthday hasn't occurred this year
    if (as_of_date.month, as_of_date.day) < (birth_date.month, birth_date.day):
        age -= 1
    
    return age


def relative_time(dt: datetime) -> str:
    """Get relative time string (e.g., "2 hours ago").
    
    Args:
        dt: Datetime to compare
        
    Returns:
        Relative time string
    """
    now = datetime.utcnow()
    if dt.tzinfo:
        now = pytz.utc.localize(now)
    
    diff = now - dt
    
    if diff.days > 365:
        years = diff.days // 365
        return f"{years} year{'s' if years > 1 else ''} ago"
    elif diff.days > 30:
        months = diff.days // 30
        return f"{months} month{'s' if months > 1 else ''} ago"
    elif diff.days > 0:
        return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    else:
        return "just now"


def business_days_between(
    start_date: date,
    end_date: date,
    holidays: Optional[list[date]] = None
) -> int:
    """Calculate business days between two dates.
    
    Args:
        start_date: Start date
        end_date: End date
        holidays: Optional list of holiday dates
        
    Returns:
        Number of business days
    """
    if holidays is None:
        holidays = []
    
    business_days = 0
    current_date = start_date
    
    while current_date <= end_date:
        # Check if it's a weekday and not a holiday
        if current_date.weekday() < 5 and current_date not in holidays:
            business_days += 1
        current_date += timedelta(days=1)
    
    return business_days