"""
SQLAlchemy declarative base + common mixins.
Location: backend/app/models/base.py
"""

import uuid
from sqlalchemy import Column, DateTime, String, func
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    """Adds created_at and updated_at to any model."""
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


def new_uuid() -> str:
    """Generate a UUID string. Works across all DB backends."""
    return str(uuid.uuid4())
