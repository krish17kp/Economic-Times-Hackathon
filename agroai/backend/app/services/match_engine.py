"""
Buyer matching — Haversine + weighted scoring.
Location: backend/app/services/match_engine.py
"""

import json
from dataclasses import dataclass
from typing import List

from sqlalchemy.orm import Session

from app.models.buyer import Buyer
from app.services.transport_calculator import haversine_distance, estimate_transport_cost
from app.core.constants import (
    BUYER_WEIGHT_PRICE,
    BUYER_WEIGHT_DISTANCE,
    BUYER_WEIGHT_PICKUP,
    BUYER_WEIGHT_VERIFIED,
    BUYER_WEIGHT_CAPACITY,
)


@dataclass
class ScoredBuyer:
    buyer_id: str
    business_name: str
    buyer_type: str
    distance_km: float
    price_per_kg: float
    min_quantity_kg: float
    provides_pickup: bool
    pickup_radius_km: int
    transport_cost_estimate: float
    net_price_per_kg: float
    phone: str
    is_verified: bool
    match_score: float
    district: str
    state: str
    latitude: float
    longitude: float


def _parse_accepted_waste(raw) -> List[str]:
    """Parse accepted_waste column — handles both JSON string and Python list."""
    if raw is None:
        return []
    if isinstance(raw, list):
        return raw
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return [raw]  # Fallback for plain string


def find_and_rank_buyers(
    db: Session,
    waste_type: str,
    user_lat: float,
    user_lon: float,
    quantity_kg: float,
    radius_km: float = 80,
) -> List[ScoredBuyer]:
    """
    Finds buyers who accept this waste type, within radius, and scores them.
    """
    # Fetch all active buyers
    all_buyers = (
        db.query(Buyer)
        .filter(Buyer.is_active == True)
        .all()
    )

    # Filter by waste type and distance, then calculate transport
    candidates = []
    for b in all_buyers:
        accepted = _parse_accepted_waste(b.accepted_waste)
        if waste_type not in accepted:
            continue

        dist = haversine_distance(user_lat, user_lon, float(b.latitude), float(b.longitude))
        if dist > radius_km:
            continue

        transport = estimate_transport_cost(
            distance_km=dist,
            quantity_kg=quantity_kg,
            buyer_provides_pickup=b.provides_pickup,
            buyer_pickup_radius_km=b.pickup_radius_km or 0,
        )

        price = float(b.price_per_kg) if b.price_per_kg else 0.0
        net_price = price - (transport.cost_inr / quantity_kg) if quantity_kg > 0 else 0.0
        net_price = max(net_price, 0.0)

        candidates.append({
            "buyer": b,
            "distance": dist,
            "transport_cost": transport.cost_inr,
            "net_price": net_price,
        })

    if not candidates:
        return []

    # Normalize and score
    max_price = max(c["net_price"] for c in candidates) or 1.0
    max_dist = max(c["distance"] for c in candidates) or 1.0

    results = []
    for c in candidates:
        b = c["buyer"]

        price_score = c["net_price"] / max_price if max_price > 0 else 0
        distance_score = 1 - (c["distance"] / max_dist)
        pickup_score = 1.0 if b.provides_pickup else 0.0
        verified_score = 1.0 if b.is_verified else 0.0
        capacity_score = 1.0 if (b.max_capacity_kg is None or float(b.max_capacity_kg) >= quantity_kg) else 0.5

        total = (
            BUYER_WEIGHT_PRICE * price_score
            + BUYER_WEIGHT_DISTANCE * distance_score
            + BUYER_WEIGHT_PICKUP * pickup_score
            + BUYER_WEIGHT_VERIFIED * verified_score
            + BUYER_WEIGHT_CAPACITY * capacity_score
        )

        results.append(ScoredBuyer(
            buyer_id=str(b.id),
            business_name=b.business_name,
            buyer_type=b.buyer_type,
            distance_km=round(c["distance"], 1),
            price_per_kg=float(b.price_per_kg) if b.price_per_kg else 0.0,
            min_quantity_kg=float(b.min_quantity_kg) if b.min_quantity_kg else 0,
            provides_pickup=b.provides_pickup,
            pickup_radius_km=b.pickup_radius_km or 0,
            transport_cost_estimate=round(c["transport_cost"], 2),
            net_price_per_kg=round(c["net_price"], 4),
            phone=b.phone,
            is_verified=b.is_verified,
            match_score=round(total, 2),
            district=b.district,
            state=b.state,
            latitude=float(b.latitude),
            longitude=float(b.longitude),
        ))

    results.sort(key=lambda x: x.match_score, reverse=True)
    return results
