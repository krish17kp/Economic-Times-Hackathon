"""
Transport cost calculation using Haversine distance.
Location: backend/app/services/transport_calculator.py

NO FastAPI imports. NO database imports.
Pure business logic. Testable in isolation.
"""

import math
from dataclasses import dataclass

from app.core.constants import (
    TRANSPORT_BASE_COST_INR,
    TRANSPORT_RATE_PER_KM_PER_TON_TRACTOR,
    TRANSPORT_RATE_PER_KM_PER_TON_TRUCK,
    TRACTOR_MAX_CAPACITY_KG,
    ROAD_CONDITION_FACTOR,
)


@dataclass
class TransportEstimate:
    distance_km: float
    road_distance_km: float
    cost_inr: float
    mode: str  # "pickup_by_buyer", "tractor_trolley", "hired_truck"
    notes: str


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Returns straight-line distance in km between two lat/long points.
    Accurate enough for distances < 500km.
    """
    R = 6371  # Earth radius in km

    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    return round(R * c, 2)


def estimate_transport_cost(
    distance_km: float,
    quantity_kg: float,
    buyer_provides_pickup: bool = False,
    buyer_pickup_radius_km: int = 0,
) -> TransportEstimate:
    """
    Calculates transport cost.
    Returns 0 cost if buyer picks up and farmer is within pickup radius.
    """
    if buyer_provides_pickup and distance_km <= buyer_pickup_radius_km:
        return TransportEstimate(
            distance_km=distance_km,
            road_distance_km=distance_km,
            cost_inr=0.0,
            mode="pickup_by_buyer",
            notes="Buyer provides free pickup within their radius",
        )

    quantity_tons = quantity_kg / 1000
    road_distance = round(distance_km * ROAD_CONDITION_FACTOR, 1)

    if quantity_kg <= TRACTOR_MAX_CAPACITY_KG:
        cost = TRANSPORT_BASE_COST_INR + (road_distance * quantity_tons * TRANSPORT_RATE_PER_KM_PER_TON_TRACTOR)
        mode = "tractor_trolley"
    else:
        cost = TRANSPORT_BASE_COST_INR + (road_distance * quantity_tons * TRANSPORT_RATE_PER_KM_PER_TON_TRUCK)
        mode = "hired_truck"

    return TransportEstimate(
        distance_km=distance_km,
        road_distance_km=road_distance,
        cost_inr=round(cost, 2),
        mode=mode,
        notes=f"Estimated road distance: {road_distance}km ({ROAD_CONDITION_FACTOR}x straight-line)",
    )
