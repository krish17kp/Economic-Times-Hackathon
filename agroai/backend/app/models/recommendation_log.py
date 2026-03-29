"""
RecommendationLog — audit trail for every recommendation made.
Location: backend/app/models/recommendation_log.py
"""

from sqlalchemy import Column, String, Numeric, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base, TimestampMixin, new_uuid
from app.core.constants import WasteType, QualityGrade, ConversionType


class RecommendationLog(Base, TimestampMixin):
    __tablename__ = "recommendation_logs"

    id = Column(String(36), primary_key=True, default=new_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    waste_type = Column(Enum(WasteType), nullable=False)
    quantity_kg = Column(Numeric(10, 2), nullable=False)
    quality = Column(Enum(QualityGrade), nullable=False)
    user_latitude = Column(Numeric(9, 6))
    user_longitude = Column(Numeric(9, 6))

    # Snapshot of calculations
    raw_sell_revenue = Column(Numeric(12, 2))
    best_buyer_id = Column(String(36), ForeignKey("buyers.id"), nullable=True)
    transport_cost = Column(Numeric(10, 2))
    net_raw_profit = Column(Numeric(12, 2))

    best_conversion = Column(Enum(ConversionType), nullable=True)
    conversion_revenue = Column(Numeric(12, 2))
    conversion_cost = Column(Numeric(12, 2))
    net_conversion_profit = Column(Numeric(12, 2))

    recommendation = Column(String(30), nullable=False)
    confidence_score = Column(Numeric(3, 2))
    reasoning = Column(Text, nullable=False)
    carbon_saved_kg = Column(Numeric(10, 2))

    # Relationships
    user = relationship("User", back_populates="recommendation_logs")
