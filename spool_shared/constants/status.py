"""Status constants and enums."""

from enum import Enum


class Status(str, Enum):
    """General status values."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ProgressStatus(str, Enum):
    """Learning progress status."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    MASTERED = "mastered"
    NEEDS_REVIEW = "needs_review"


class ExerciseStatus(str, Enum):
    """Exercise submission status."""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    EVALUATING = "evaluating"
    EVALUATED = "evaluated"
    NEEDS_RETRY = "needs_retry"


class ContentStatus(str, Enum):
    """Content processing status."""
    UPLOADING = "uploading"
    PROCESSING = "processing"
    READY = "ready"
    ERROR = "error"
    ARCHIVED = "archived"


class NotificationStatus(str, Enum):
    """Notification delivery status."""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    READ = "read"