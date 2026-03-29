"""
CarbonFactor — emission/sequestration data per waste type.
Location: backend/app/models/carbon_factor.py
"""

from sqlalchemy import Column, Integer, String, Numeric, Enum, UniqueConstraint

from app.models.base import Base
from app.core.constants import WasteType, ConversionType


class CarbonFactor(Base):
    __tablename__ = "carbon_factors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    waste_type = Column(Enum(WasteType), nullable=False)
    burn_emission_kg_co2_per_kg = Column(Numeric(6, 3), nullable=False)
    conversion_type = Column(Enum(ConversionType), nullable=True)  # NULL = general
    sequestration_kg_co2_per_kg = Column(Numeric(6, 3), default=0)
    source = Column(String(100))

    __table_args__ = (
        UniqueConstraint("waste_type", "conversion_type", name="unique_waste_conversion"),
    )
