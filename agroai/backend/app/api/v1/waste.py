"""
Waste submission and type listing endpoints.
Location: backend/app/api/v1/waste.py
"""

import json
from pathlib import Path
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user, get_optional_user
from app.schemas.waste import WasteInput, WasteTypesResponse, WasteSubmitResponse
from app.models.waste_log import WasteLog
from app.models.user import User

router = APIRouter()

# Load waste types from seed file (cached at startup)
_waste_types_path = Path(__file__).parent.parent.parent.parent / "data" / "seed" / "waste_types.json"


@router.get("/types", response_model=WasteTypesResponse)
def get_waste_types():
    """Returns available waste types. No auth required."""
    with open(_waste_types_path, "r", encoding="utf-8") as f:
        types = json.load(f)
    return WasteTypesResponse(types=types)


@router.post("/submit", response_model=WasteSubmitResponse)
def submit_waste(
    data: WasteInput,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Logs a waste entry for a farmer. Auth required."""
    log = WasteLog(
        user_id=user.id,
        waste_type=data.waste_type,
        quantity_kg=data.quantity_kg,
        quality=data.quality,
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    return WasteSubmitResponse(
        waste_log_id=str(log.id),
        message="Waste logged. Fetching analysis...",
    )
