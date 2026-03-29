"""
AI Assistant endpoint (RAG-based).
Location: backend/app/api/v1/assistant.py
"""

from fastapi import APIRouter, HTTPException
from app.schemas.assistant import AssistantQuery, AssistantResponse, ALLOWED_CATEGORIES
from app.services.assistant_service import ask_assistant

router = APIRouter()


@router.post("/ask", response_model=AssistantResponse)
def ask_question(data: AssistantQuery):
    if data.question_category not in ALLOWED_CATEGORIES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported category. Allowed: {', '.join(ALLOWED_CATEGORIES)}",
        )

    result = ask_assistant(data.question, data.question_category, data.language, data.context)

    return AssistantResponse(
        answer=result["answer"],
        sources=result["sources"],
        related_questions=result["related_questions"],
    )
