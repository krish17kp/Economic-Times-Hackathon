"""
Shared response schemas.
Location: backend/app/schemas/common.py
"""

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    error: str
    status_code: int


class MessageResponse(BaseModel):
    message: str
