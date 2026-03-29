"""
AI Assistant schemas.
Location: backend/app/schemas/assistant.py
"""

from pydantic import BaseModel, Field
from typing import Optional


ALLOWED_CATEGORIES = ["how_to_convert", "market_info", "equipment", "quality_tips", "carbon_info"]


class AssistantQuery(BaseModel):
    question_category: str = Field(..., examples=["how_to_convert"])
    question: str = Field(..., min_length=1, max_length=500)
    language: str = "en"
    context: Optional[dict] = None  # e.g., {"waste_type": "rice_straw"}


class AssistantSource(BaseModel):
    document: str
    page: Optional[int] = None


class AssistantResponse(BaseModel):
    answer: str
    sources: list[AssistantSource]
    related_questions: list[str]
