"""
Price lookup and trend analysis from market_prices table.
Location: backend/app/services/price_engine.py
"""

from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.market_price import MarketPrice
from app.core.exceptions import NotFoundError


def get_current_price(db: Session, waste_type: str, region: str, days: int = 30):
    """
    Returns latest price data for a waste type in a region.
    Aggregates from last N days of records.
    """
    cutoff = date.today() - timedelta(days=days)

    records = (
        db.query(MarketPrice)
        .filter(
            MarketPrice.waste_type == waste_type,
            MarketPrice.region == region,
            MarketPrice.recorded_date >= cutoff,
        )
        .order_by(desc(MarketPrice.recorded_date))
        .all()
    )

    if not records:
        # Try without date filter (use all historical data)
        records = (
            db.query(MarketPrice)
            .filter(
                MarketPrice.waste_type == waste_type,
                MarketPrice.region == region,
            )
            .order_by(desc(MarketPrice.recorded_date))
            .limit(12)
            .all()
        )

    if not records:
        raise NotFoundError("Price data", f"{waste_type} in {region}")

    # Aggregate — use plain float to avoid Decimal/float mixing
    prices = [float(r.price_avg) for r in records]
    all_min = float(min(r.price_min for r in records))
    all_max = float(max(r.price_max for r in records))
    all_avg = sum(prices) / len(prices)

    # Trend: compare first half vs second half
    mid = len(records) // 2
    if mid > 0:
        recent_avg = sum(prices[:mid]) / mid
        older_avg = sum(prices[mid:]) / (len(records) - mid)
        if recent_avg > older_avg * 1.05:
            trend = "rising"
        elif recent_avg < older_avg * 0.95:
            trend = "falling"
        else:
            trend = "stable"
    else:
        trend = "stable"

    # Confidence based on data points
    data_points = len(records)
    if data_points >= 20:
        confidence = "high"
    elif data_points >= 5:
        confidence = "medium"
    else:
        confidence = "low"

    # History
    history = [
        {"date": str(r.recorded_date), "avg": float(r.price_avg)}
        for r in records[:12]  # Last 12 entries
    ]

    return {
        "waste_type": waste_type,
        "region": region,
        "current": {
            "min": all_min,
            "max": all_max,
            "avg": round(all_avg, 2),
            "unit": "INR/kg",
            "as_of": str(records[0].recorded_date),
        },
        "trend": trend,
        "data_points": data_points,
        "confidence": confidence,
        "history": history,
    }
