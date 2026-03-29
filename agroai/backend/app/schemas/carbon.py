"""
Carbon estimation schemas.
Location: backend/app/schemas/carbon.py
"""

from pydantic import BaseModel
from app.core.constants import WasteType


class CarbonInput(BaseModel):
    waste_type: WasteType
    quantity_kg: float
    action: str = "sell_raw"  # "sell_raw", "convert_biochar", "convert_briquette"


class CarbonResponse(BaseModel):
    co2_if_burned_kg: float
    co2_avoided_kg: float
    co2_sequestered_kg: float
    equivalent: str
    source: str
