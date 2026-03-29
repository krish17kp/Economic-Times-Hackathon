"""
Waste input/output schemas.
Location: backend/app/schemas/waste.py
"""

from pydantic import BaseModel, Field
from typing import Optional
from app.core.constants import WasteType, QualityGrade


class WasteInput(BaseModel):
    waste_type: WasteType
    quantity_kg: float = Field(..., gt=0, le=500000, examples=[5000])
    quality: QualityGrade = QualityGrade.SEMI_DRY
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    pincode: Optional[str] = Field(None, pattern=r"^\d{6}$")


class WasteTypeInfo(BaseModel):
    id: str
    label_en: str
    label_hi: str
    icon: str
    typical_season: str


class WasteTypesResponse(BaseModel):
    types: list[WasteTypeInfo]


class WasteSubmitResponse(BaseModel):
    waste_log_id: str
    message: str
