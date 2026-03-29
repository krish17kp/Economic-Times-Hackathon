"""
Conversion estimation schemas.
Location: backend/app/schemas/conversion.py
"""

from pydantic import BaseModel
from typing import Optional
from app.core.constants import WasteType, QualityGrade, ConversionType


class ConversionInput(BaseModel):
    waste_type: WasteType
    quantity_kg: float
    quality: QualityGrade = QualityGrade.SEMI_DRY
    conversion_type: Optional[ConversionType] = None  # None = show all


class ConversionOption(BaseModel):
    conversion_type: str
    output_quantity_kg: float
    output_price_per_kg: float
    gross_revenue: float
    processing_cost: float
    equipment_cost: float
    equipment_amortized: float
    net_profit: float
    processing_time_days: int
    skill_level: str
    is_viable: bool
    viability_note: Optional[str]


class ConversionResponse(BaseModel):
    options: list[ConversionOption]
