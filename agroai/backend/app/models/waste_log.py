"""
WasteLog — what farmers submit (type, quantity, quality).
Location: backend/app/models/waste_log.py
"""

from sqlalchemy import Column, String, Numeric, Date, Text, Enum, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from app.models.base import Base, TimestampMixin, new_uuid
from app.core.constants import WasteType, QualityGrade


class WasteLog(Base, TimestampMixin):
    __tablename__ = "waste_logs"

    id = Column(String(36), primary_key=True, default=new_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    waste_type = Column(Enum(WasteType), nullable=False, index=True)
    quantity_kg = Column(Numeric(10, 2), nullable=False)
    quality = Column(Enum(QualityGrade), nullable=False, default=QualityGrade.SEMI_DRY)
    available_from = Column(Date)
    available_until = Column(Date)
    notes = Column(Text)

    # Relationships
    user = relationship("User", back_populates="waste_logs")

    __table_args__ = (
        CheckConstraint("quantity_kg > 0 AND quantity_kg <= 500000", name="valid_quantity"),
    )
