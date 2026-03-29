"""
Conversion estimation endpoint.
Location: backend/app/api/v1/convert.py
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.conversion import ConversionInput, ConversionResponse
from app.services.conversion_engine import get_conversion_options

router = APIRouter()


@router.post("/estimate", response_model=ConversionResponse)
def estimate_conversion(data: ConversionInput, db: Session = Depends(get_db)):
    """Returns conversion profit estimates for all (or specific) products."""
    results = get_conversion_options(
        db,
        data.waste_type.value,
        data.quantity_kg,
        data.quality.value,
        data.conversion_type.value if data.conversion_type else None,
    )

    options = [
        {
            "conversion_type": r.conversion_type,
            "output_quantity_kg": float(r.output_quantity_kg),
            "output_price_per_kg": 0,  # Filled from DB in service
            "gross_revenue": float(r.gross_revenue),
            "processing_cost": float(r.processing_cost),
            "equipment_cost": 0,
            "equipment_amortized": float(r.equipment_amortized),
            "net_profit": float(r.net_profit),
            "processing_time_days": r.time_to_money_days,
            "skill_level": "moderate",
            "is_viable": r.is_viable,
            "viability_note": r.viability_reason,
        }
        for r in results
    ]

    return ConversionResponse(options=options)
