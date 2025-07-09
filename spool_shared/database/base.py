"""Base database models."""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, DateTime, Boolean, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()


class BaseModel(Base):
    """Base model with common fields."""
    __abstract__ = True
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class TimestampedModel(BaseModel):
    """Model with timestamp tracking."""
    __abstract__ = True
    
    created_by = Column(UUID(as_uuid=True), nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)


class SoftDeleteModel(TimestampedModel):
    """Model with soft delete support."""
    __abstract__ = True
    
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(UUID(as_uuid=True), nullable=True)
    
    def soft_delete(self, user_id: Optional[str] = None):
        """Soft delete the record."""
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()
        if user_id:
            self.deleted_by = user_id