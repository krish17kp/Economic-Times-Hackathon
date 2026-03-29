"""
Side-by-side comparison of all options (raw sell vs conversions).
Location: backend/app/services/comparison_engine.py
"""

from typing import Optional

from sqlalchemy.orm import Session

from app.services.price_engine import get_current_price
from app.services.match_engine import find_and_rank_buyers
from app.services.conversion_engine import get_conversion_options
from app.services.carbon_calculator import estimate_carbon


def build_comparison(
    db: Session,
    waste_type: str,
    quantity_kg: float,
    quality: str,
    latitude: Optional[float],
    longitude: Optional[float],
    region: str = "Punjab",
) -> dict:
    """
    Builds a full comparison of all options.
    Returns structured dict ready for API response.
    """
    options = []

    # --- RAW SELL OPTION ---
    raw_option = {
        "option_type": "sell_raw",
        "label_en": "Sell as raw material",
        "label_hi": "कच्चे माल के रूप में बेचें",
        "net_profit": 0.0,
        "time_to_money_days": 3,
        "effort_level": "low",
        "risk_level": "low",
        "requires_equipment": False,
        "equipment_cost": None,
        "best_buyer": None,
        "gross_revenue": None,
        "transport_cost": None,
    }

    if latitude and longitude:
        buyers = find_and_rank_buyers(db, waste_type, latitude, longitude, quantity_kg, radius_km=250)
        if buyers:
            best = buyers[0]
            gross = round(best.price_per_kg * quantity_kg, 2)
            net = round(best.net_price_per_kg * quantity_kg, 2)
            raw_option["net_profit"] = net
            raw_option["best_buyer"] = best.business_name
            raw_option["gross_revenue"] = gross
            raw_option["transport_cost"] = round(best.transport_cost_estimate, 2)

    options.append(raw_option)

    # --- CONVERSION OPTIONS ---
    conversions = get_conversion_options(db, waste_type, quantity_kg, quality)

    conversion_labels = {
        "biochar": ("Convert to Biochar", "बायोचार में बदलें"),
        "briquette": ("Convert to Briquettes", "ब्रिकेट में बदलें"),
        "mushroom_substrate": ("Convert to Mushroom Substrate", "मशरूम सब्सट्रेट में बदलें"),
    }

    best_conversion_profit = 0.0
    best_conversion_type = None

    for c in conversions:
        if not c.is_viable:
            continue
        labels = conversion_labels.get(c.conversion_type, (c.conversion_type, c.conversion_type))
        net_p = float(c.net_profit)
        options.append({
            "option_type": f"convert_{c.conversion_type}",
            "label_en": labels[0],
            "label_hi": labels[1],
            "net_profit": net_p,
            "time_to_money_days": c.time_to_money_days,
            "effort_level": "medium" if c.conversion_type == "briquette" else "high",
            "risk_level": "medium",
            "requires_equipment": True,
            "equipment_cost": float(c.equipment_amortized) if c.equipment_amortized else None,
            "best_buyer": None,
            "gross_revenue": float(c.gross_revenue),
            "transport_cost": None,
            "output_quantity_kg": float(c.output_quantity_kg),
            "processing_time_days": c.time_to_money_days,
            "processing_cost": float(c.processing_cost) + (float(c.equipment_amortized) if c.equipment_amortized else 0),
        })
        if net_p > best_conversion_profit:
            best_conversion_profit = net_p
            best_conversion_type = c.conversion_type

    # --- DERIVED FIELDS ---
    raw_profit = raw_option["net_profit"]
    is_conversion_better = best_conversion_profit > raw_profit
    best_option = f"convert_{best_conversion_type}" if is_conversion_better else "sell_raw"

    # --- CARBON IMPACT ---
    carbon = estimate_carbon(db, waste_type, quantity_kg)

    return {
        "options": options,
        "carbon_impact": carbon,
        "is_conversion_better": is_conversion_better,
        "best_option": best_option or "sell_raw",
        "raw_sell_net_profit": raw_profit,
        "best_conversion_net_profit": best_conversion_profit,
        "best_conversion_type": best_conversion_type,
    }
