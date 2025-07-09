"""Event schemas for inter-service communication."""

from typing import Any, Dict, Optional
from datetime import datetime
from pydantic import BaseModel, Field, UUID4
from enum import Enum


class EventType(str, Enum):
    """Event types."""
    # Progress events
    PROGRESS_UPDATED = "progress.updated"
    CONCEPT_STARTED = "concept.started"
    CONCEPT_COMPLETED = "concept.completed"
    CONCEPT_MASTERED = "concept.mastered"
    
    # Gamification events
    POINTS_AWARDED = "points.awarded"
    BADGE_EARNED = "badge.earned"
    LEVEL_UP = "level.up"
    STREAK_UPDATED = "streak.updated"
    
    # Content events
    CONTENT_CREATED = "content.created"
    CONTENT_UPDATED = "content.updated"
    CONTENT_DELETED = "content.deleted"
    
    # Exercise events
    EXERCISE_SUBMITTED = "exercise.submitted"
    EXERCISE_EVALUATED = "exercise.evaluated"


class EventBase(BaseModel):
    """Base event schema."""
    event_id: UUID4 = Field(default_factory=lambda: UUID4())
    event_type: EventType
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source_service: str
    user_id: UUID4
    correlation_id: Optional[UUID4] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ProgressEvent(EventBase):
    """Progress-related event."""
    student_id: UUID4
    concept_id: Optional[UUID4] = None
    progress_data: Dict[str, Any]
    
    @property
    def is_milestone(self) -> bool:
        """Check if this is a milestone event."""
        milestone_types = [
            EventType.CONCEPT_MASTERED,
            EventType.LEVEL_UP
        ]
        return self.event_type in milestone_types


class GamificationEvent(EventBase):
    """Gamification-related event."""
    student_id: UUID4
    reward_type: str  # points, badge, achievement
    reward_value: Any
    reason: str
    
    @property
    def is_achievement(self) -> bool:
        """Check if this is an achievement event."""
        return self.reward_type in ["badge", "achievement"]


class ContentEvent(EventBase):
    """Content-related event."""
    content_id: UUID4
    content_type: str  # book, concept, exercise
    action: str  # created, updated, deleted
    changes: Optional[Dict[str, Any]] = None


class ExerciseEvent(EventBase):
    """Exercise-related event."""
    student_id: UUID4
    exercise_id: UUID4
    concept_id: UUID4
    submission_data: Optional[Dict[str, Any]] = None
    evaluation_data: Optional[Dict[str, Any]] = None