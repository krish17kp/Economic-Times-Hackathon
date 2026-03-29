"""
Global exception handlers for FastAPI.
Location: backend/app/core/error_handlers.py
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.exceptions import AgroAIException


def register_error_handlers(app: FastAPI):

    @app.exception_handler(AgroAIException)
    async def agroai_exception_handler(request: Request, exc: AgroAIException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.message, "status_code": exc.status_code},
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        # Log the real error in production, return generic message
        print(f"[ERROR] {request.url}: {exc}")  # Replace with proper logging
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "status_code": 500},
        )
