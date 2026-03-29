"""
Comparison engine endpoint — raw vs conversion side-by-side.
Location: backend/app/api/v1/compare.py
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.comparison import CompareInput, CompareResponse
from app.services.comparison_engine import build_comparison
from app.core.exceptions import LocationRequiredError

router = APIRouter()


@router.post("", response_model=CompareResponse)
def compare_options(data: CompareInput, db: Session = Depends(get_db)):
    """Builds side-by-side comparison of all options."""
    if not data.latitude and not data.pincode:
        raise LocationRequiredError()

    lat, lon = data.latitude, data.longitude
    pincode = data.pincode
    
    # Synchronize geolocator mock with nearby buyers
    if not lat or not lon:
        if pincode and str(pincode).startswith("300"): 
            lat, lon = 26.91, 75.78 # Jaipur mock
        elif pincode and str(pincode).startswith("400"):
            lat, lon = 19.0760, 72.8777 # Mumbai mock
        elif pincode and str(pincode).startswith("411"):
            lat, lon = 18.5204, 73.8567 # Pune mock
        elif pincode:
            lat, lon = 28.70, 77.10 # Delhi mock
        else:
            lat, lon = 30.73, 76.77 # Chandigarh mock

    try:
        result = build_comparison(
            db=db,
            waste_type=data.waste_type.value,
            quantity_kg=data.quantity_kg,
            quality=data.quality.value,
            latitude=lat,
            longitude=lon,
        )
        return result
    except Exception as e:
        import traceback
        raise HTTPException(status_code=500, detail=traceback.format_exc())
