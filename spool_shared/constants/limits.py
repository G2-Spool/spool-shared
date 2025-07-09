"""System limits and constraints."""

from dataclasses import dataclass


@dataclass
class RateLimits:
    """API rate limits."""
    # Requests per minute
    DEFAULT = 60
    AUTHENTICATED = 120
    PREMIUM = 300
    
    # Specific endpoints
    LOGIN_ATTEMPTS = 5
    PASSWORD_RESET = 3
    FILE_UPLOAD = 10
    
    # Time windows (seconds)
    WINDOW_DEFAULT = 60
    WINDOW_LOGIN = 300  # 5 minutes
    WINDOW_RESET = 3600  # 1 hour


@dataclass
class Pagination:
    """Pagination limits."""
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
    MIN_PAGE_SIZE = 1
    
    DEFAULT_PAGE = 1
    
    # Service-specific limits
    EXERCISES_MAX = 50
    ANALYTICS_MAX = 200
    LEADERBOARD_MAX = 100


@dataclass
class FileUpload:
    """File upload limits."""
    # Size limits (bytes)
    MAX_PDF_SIZE = 50 * 1024 * 1024  # 50MB
    MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
    MAX_AVATAR_SIZE = 5 * 1024 * 1024  # 5MB
    
    # Allowed MIME types
    ALLOWED_PDF_TYPES = ["application/pdf"]
    ALLOWED_IMAGE_TYPES = [
        "image/jpeg",
        "image/png",
        "image/gif",
        "image/webp"
    ]
    
    # File count limits
    MAX_BATCH_UPLOAD = 10
    MAX_ATTACHMENTS = 5


@dataclass
class ContentLimits:
    """Content size limits."""
    # Text limits (characters)
    MAX_TITLE_LENGTH = 200
    MAX_DESCRIPTION_LENGTH = 1000
    MAX_EXERCISE_PROMPT = 5000
    MAX_RESPONSE_LENGTH = 10000
    
    # Concept limits
    MAX_CONCEPTS_PER_BOOK = 500
    MAX_EXERCISES_PER_CONCEPT = 20
    
    # Graph limits
    MAX_GRAPH_DEPTH = 10
    MAX_RELATED_CONCEPTS = 50


@dataclass
class GamificationLimits:
    """Gamification system limits."""
    # Points
    MAX_POINTS_PER_ACTION = 1000
    MAX_DAILY_POINTS = 5000
    
    # Badges
    MAX_BADGES_PER_USER = 100
    MAX_ACTIVE_BADGES = 50
    
    # Streaks
    MAX_STREAK_DAYS = 365
    STREAK_GRACE_HOURS = 4
    
    # Leaderboard
    LEADERBOARD_TOP_N = 100
    LEADERBOARD_CACHE_TTL = 300  # 5 minutes