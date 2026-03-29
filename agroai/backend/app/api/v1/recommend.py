"""
Recommendation endpoint.
Location: backend/app/api/v1/recommend.py
"""

from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_optional_user
from app.schemas.recommendation import RecommendInput, RecommendResponse
from app.models.waste_log import WasteLog
from app.models.recommendation_log import RecommendationLog
from app.services.price_engine import get_current_price
from app.services.match_engine import find_and_rank_buyers
from app.services.conversion_engine import get_conversion_options
from app.services.profit_calculator import calculate_raw_sell_profit
from app.services.recommendation_engine import generate_recommendation
from app.services.carbon_calculator import estimate_carbon

router = APIRouter()


@router.post("", response_model=RecommendResponse)
def get_recommendation(
    data: RecommendInput,
    db: Session = Depends(get_db),
    user=Depends(get_optional_user),
):
    """Generates a full recommendation based on a waste log entry."""
    waste_log = db.query(WasteLog).filter(WasteLog.id == data.waste_log_id).first()
    if not waste_log:
        raise HTTPException(status_code=404, detail="Waste log not found")

    waste_type = waste_log.waste_type.value
    quantity = float(waste_log.quantity_kg)
    quality = waste_log.quality.value

    # Get user location
    log_user = waste_log.user
    lat = float(log_user.latitude) if log_user.latitude else 30.73
    lon = float(log_user.longitude) if log_user.longitude else 76.77

    # 1. Price data
    try:
        price_data = get_current_price(db, waste_type, log_user.state or "Punjab")
        market_price = Decimal(str(price_data["current"]["avg"]))
        trend = price_data["trend"]
    except Exception:
        market_price = Decimal("1.50")
        trend = "stable"

    # 2. Buyer matching
    buyers = find_and_rank_buyers(db, waste_type, lat, lon, quantity)
    best_buyer = buyers[0] if buyers else None

    # 3. Raw sell profit
    transport_cost = Decimal(str(best_buyer.transport_cost_estimate)) if best_buyer else Decimal("0")
    raw_sell = calculate_raw_sell_profit(
        quantity_kg=Decimal(str(quantity)),
        quality=quality,
        market_price_per_kg=Decimal(str(best_buyer.price_per_kg)) if best_buyer else market_price,
        transport_cost=transport_cost,
        buyer_name=best_buyer.business_name if best_buyer else None,
    )

    # 4. Conversion options
    conversions = get_conversion_options(db, waste_type, quantity, quality)

    # 5. Generate recommendation
    rec = generate_recommendation(
        raw_sell=raw_sell,
        conversions=conversions,
        has_nearby_buyer=best_buyer is not None,
        buyer_is_verified=best_buyer.is_verified if best_buyer else False,
        market_trend=trend,
    )

    # 6. Carbon
    carbon = estimate_carbon(db, waste_type, quantity)
    carbon_saved = carbon["if_sold"]["co2_kg"]

    # 7. Log recommendation
    viable_convs = [c for c in conversions if c.is_viable]
    log_entry = RecommendationLog(
        user_id=user.id if user else None,
        waste_type=waste_type,
        quantity_kg=quantity,
        quality=quality,
        user_latitude=lat,
        user_longitude=lon,
        raw_sell_revenue=float(raw_sell.gross_revenue),
        transport_cost=float(raw_sell.transport_cost),
        net_raw_profit=float(raw_sell.net_profit),
        best_conversion=viable_convs[0].conversion_type if viable_convs else None,
        net_conversion_profit=float(viable_convs[0].net_profit) if viable_convs else 0,
        recommendation=rec.action,
        confidence_score=rec.confidence,
        reasoning=rec.reasoning_en,
        carbon_saved_kg=carbon_saved,
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)

    return RecommendResponse(
        recommendation=rec.action,
        confidence=rec.confidence,
        reasoning_en=rec.reasoning_en,
        reasoning_hi=rec.reasoning_hi,
        factors=[{"factor": f.factor, "impact": f.impact, "detail": f.detail} for f in rec.factors],
        alternatives=rec.alternatives,
        carbon_saved_kg=carbon_saved,
        net_profit=rec.net_profit,
        time_days=rec.time_days,
        log_id=str(log_entry.id),
    )
