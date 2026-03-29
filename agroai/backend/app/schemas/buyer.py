"""
Buyer matching schemas.
Location: backend/app/schemas/buyer.py
"""

from pydantic import BaseModel
from typing import Optional


class BuyerMatch(BaseModel):
    id: str
    business_name: str
    buyer_type: str
    distance_km: float
    price_per_kg: Optional[float]
    min_quantity_kg: float
    provides_pickup: bool
    pickup_radius_km: int
    transport_cost_estimate: float
    net_price_per_kg: float
    phone: str  # Masked for anonymous, full for logged-in
    is_verified: bool
    match_score: float
    district: Optional[str]
    state: str
    latitude: float
    longitude: float
    is_fallback: bool = False


class BuyerListResponse(BaseModel):
    buyers: list[BuyerMatch]
    total: int
    search_params: dict
