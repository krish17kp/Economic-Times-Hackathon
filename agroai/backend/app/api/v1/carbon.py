"""
Carbon estimation endpoint.
Location: backend/app/api/v1/carbon.py
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.carbon import CarbonInput, CarbonResponse
from app.services.carbon_calculator import estimate_carbon

router = APIRouter()


@router.post("/estimate", response_model=CarbonResponse)
def carbon_estimate(data: CarbonInput, db: Session = Depends(get_db)):
    result = estimate_carbon(db, data.waste_type.value, data.quantity_kg)

    return CarbonResponse(
        co2_if_burned_kg=result["if_burned"]["co2_kg"],
        co2_avoided_kg=result["if_sold"]["co2_kg"],
        co2_sequestered_kg=result["if_biochar"]["co2_kg"],
        equivalent=result["equivalent"],
        source=result["source"],
    )
