"""
Price intelligence schemas.
Location: backend/app/schemas/price.py
"""

from pydantic import BaseModel
from typing import Optional


class PriceCurrent(BaseModel):
    min: float
    max: float
    avg: float
    unit: str = "INR/kg"
    as_of: str  # Date string


class PriceHistoryPoint(BaseModel):
    date: str
    avg: float


class PriceResponse(BaseModel):
    waste_type: str
    region: str
    current: PriceCurrent
    trend: str  # "rising", "stable", "falling"
    data_points: int
    confidence: str  # "high", "medium", "low"
    history: list[PriceHistoryPoint]
