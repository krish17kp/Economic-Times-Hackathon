"""
Buyer matching endpoint.
Location: backend/app/api/v1/buyers.py
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.services.match_engine import find_and_rank_buyers
from app.schemas.buyer import BuyerListResponse

router = APIRouter()


@router.get("/nearby", response_model=BuyerListResponse)
def get_nearby_buyers(
    waste_type: str = Query(..., examples=["rice_straw"]),
    lat: float = Query(None, ge=-90, le=90),
    long: float = Query(None, ge=-180, le=180),
    pincode: str = Query(None),
    radius_km: float = Query(50, ge=5, le=500),
    min_qty: float = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """Finds and ranks nearby buyers for a waste type."""
    # Extremely basic pincode to coord lookup for demo
    if not lat or not long:
        if pincode and str(pincode).startswith("300"): 
            lat, long = 26.91, 75.78 # Jaipur mock
        elif pincode and str(pincode).startswith("400"):
            lat, long = 19.0760, 72.8777 # Mumbai mock
        elif pincode and str(pincode).startswith("411"):
            lat, long = 18.5204, 73.8567 # Pune mock
        elif pincode:
            lat, long = 28.70, 77.10 # Delhi mock
        else:
            lat, long = 30.73, 76.77 # Chandigarh mock

    is_fallback = False
    buyers = find_and_rank_buyers(db, waste_type, lat, long, min_qty or 1000, radius_km)
    
    # Fallback mode: If no buyers are nearby, fetch pilot network buyers unconditionally
    if not buyers:
        buyers = find_and_rank_buyers(db, waste_type, lat, long, min_qty or 1000, radius_km=5000)[:5]
        is_fallback = True

    buyer_dicts = [
        {
            "id": b.buyer_id,
            "business_name": b.business_name,
            "buyer_type": b.buyer_type,
            "distance_km": b.distance_km,
            "price_per_kg": b.price_per_kg,
            "min_quantity_kg": b.min_quantity_kg,
            "provides_pickup": b.provides_pickup,
            "pickup_radius_km": b.pickup_radius_km,
            "transport_cost_estimate": b.transport_cost_estimate,
            "net_price_per_kg": b.net_price_per_kg,
            "phone": b.phone,
            "is_verified": b.is_verified,
            "match_score": b.match_score,
            "district": b.district,
            "state": b.state,
            "latitude": b.latitude,
            "longitude": b.longitude,
            "is_fallback": is_fallback,
        }
        for b in buyers
    ]

    return BuyerListResponse(
        buyers=buyer_dicts,
        total=len(buyer_dicts),
        search_params={"waste_type": waste_type, "radius_km": radius_km, "lat": lat, "long": long},
    )
