"""
Comparison engine schemas.
Location: backend/app/schemas/comparison.py
"""

from pydantic import BaseModel
from typing import Optional, List
from app.core.constants import WasteType, QualityGrade


class CompareInput(BaseModel):
    waste_type: WasteType
    quantity_kg: float
    quality: QualityGrade = QualityGrade.SEMI_DRY
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    pincode: Optional[str] = None


class CompareOption(BaseModel):
    option_type: str
    label_en: str
    label_hi: str
    net_profit: float
    time_to_money_days: int
    effort_level: str
    risk_level: str
    requires_equipment: bool = False
    equipment_cost: Optional[float] = None
    best_buyer: Optional[str] = None
    gross_revenue: Optional[float] = None
    transport_cost: Optional[float] = None
    output_quantity_kg: Optional[float] = None
    processing_time_days: Optional[int] = None
    processing_cost: Optional[float] = None


class CarbonScenario(BaseModel):
    co2_kg: float
    label_en: str
    label_hi: str

class CarbonImpact(BaseModel):
    if_burned: CarbonScenario
    if_sold: CarbonScenario
    if_biochar: CarbonScenario
    equivalent_en: str
    equivalent_hi: str
    source: str


class CompareResponse(BaseModel):
    options: List[CompareOption]
    carbon_impact: CarbonImpact
    # Derived convenience fields for frontend
    is_conversion_better: bool
    best_option: str                 # option_type of highest net_profit option
    raw_sell_net_profit: float
    best_conversion_net_profit: float
    best_conversion_type: Optional[str] = None
