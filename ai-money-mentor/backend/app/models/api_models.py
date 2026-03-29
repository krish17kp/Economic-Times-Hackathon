from pydantic import BaseModel
from typing import Dict, Any, Optional

from app.models.portfolio import Portfolio

class AnalyzeRequest(BaseModel):
    portfolio: Portfolio
    user_context: Optional[Dict[str, Any]] = None

class UploadResponse(BaseModel):
    success: bool
    source: Optional[str] = None
    portfolio: Optional[Portfolio] = None
    warnings: list[str] = []
    error: Optional[str] = None
    message: Optional[str] = None
    suggestion: Optional[str] = None
    partial_data: Optional[Dict[str, Any]] = None
