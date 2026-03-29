"""
Price intelligence endpoint.
Location: backend/app/api/v1/price.py
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.services.price_engine import get_current_price
from app.schemas.price import PriceResponse

router = APIRouter()


@router.get("/{waste_type}", response_model=PriceResponse)
def get_price(
    waste_type: str,
    region: str = Query("Punjab", examples=["Punjab"]),
    days: int = Query(30, ge=7, le=180),
    db: Session = Depends(get_db),
):
    """Returns price intelligence for a waste type in a region."""
    result = get_current_price(db, waste_type, region, days)
    return result
