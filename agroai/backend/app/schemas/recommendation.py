"""
Recommendation schemas.
Location: backend/app/schemas/recommendation.py
"""

from pydantic import BaseModel
from typing import Optional


class RecommendInput(BaseModel):
    waste_log_id: str


class RecommendFactor(BaseModel):
    factor: str
    impact: str  # "positive", "negative", "neutral"
    detail: str


class RecommendResponse(BaseModel):
    recommendation: str
    confidence: float
    reasoning_en: str
    reasoning_hi: str
    factors: list[RecommendFactor]
    alternatives: list[str]
    carbon_saved_kg: float
    net_profit: float
    time_days: int
    log_id: Optional[str] = None
