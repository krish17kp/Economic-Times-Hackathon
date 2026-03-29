"""
User model — farmers, buyers, FPO managers.
Location: backend/app/models/user.py
"""

from sqlalchemy import Column, String, Numeric, Enum
from sqlalchemy.orm import relationship

from app.models.base import Base, TimestampMixin, new_uuid
from app.core.constants import UserRole


class User(Base, TimestampMixin):
    __tablename__ = "users"

    # String(36) UUID works on both PostgreSQL and SQLite
    id = Column(String(36), primary_key=True, default=new_uuid)
    phone = Column(String(15), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    state = Column(String(50))
    district = Column(String(100))
    pincode = Column(String(6), index=True)
    latitude = Column(Numeric(9, 6))
    longitude = Column(Numeric(9, 6))
    language_pref = Column(String(5), default="hi")

    # Relationships
    waste_logs = relationship("WasteLog", back_populates="user", cascade="all, delete-orphan")
    recommendation_logs = relationship("RecommendationLog", back_populates="user")

    def __repr__(self):
        return f"<User {self.name} ({self.role})>"
