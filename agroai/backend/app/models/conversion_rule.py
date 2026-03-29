"""
ConversionRule — deterministic conversion math.
Location: backend/app/models/conversion_rule.py
"""

from sqlalchemy import Column, Integer, String, Numeric, Text, Date, Enum, UniqueConstraint

from app.models.base import Base
from app.core.constants import WasteType, ConversionType


class ConversionRule(Base):
    __tablename__ = "conversion_rules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    input_waste = Column(Enum(WasteType), nullable=False)
    output_product = Column(Enum(ConversionType), nullable=False)
    conversion_ratio = Column(Numeric(5, 3), nullable=False)         # e.g., 0.30
    processing_cost_per_kg = Column(Numeric(8, 2), nullable=False)   # ₹ per kg INPUT
    output_price_per_kg = Column(Numeric(8, 2), nullable=False)      # ₹ per kg OUTPUT
    equipment_cost = Column(Numeric(12, 2))                          # One-time
    min_viable_qty_kg = Column(Numeric(10, 2), nullable=False, default=1000)
    processing_time_days = Column(Integer, default=7)
    skill_level = Column(String(20), default="moderate")
    # Use Text instead of JSONB — cross-DB compatible
    quality_penalty = Column(Text, default='{"dry": 1.0, "semi_dry": 0.85, "wet": 0.6}')
    notes = Column(Text)
    source = Column(String(100))
    last_updated = Column(Date)

    __table_args__ = (
        UniqueConstraint("input_waste", "output_product", name="unique_waste_product"),
    )
