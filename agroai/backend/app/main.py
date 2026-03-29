
"""
AgroAI — FastAPI Application Factory v1.7
Location: backend/app/main.py
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.config import settings
from app.api.v1.router import api_router
from app.core.error_handlers import register_error_handlers


def create_app() -> FastAPI:
    app = FastAPI(
        title="AgroAI API",
        description="Decision-support platform for agro-waste utilization",
        version="1.0.0",
        docs_url="/docs" if settings.environment == "development" else None,
        redoc_url=None,
    )

    # --- Middleware ---
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(GZipMiddleware, minimum_size=500)  # Compress responses > 500 bytes

    # --- Routes ---
    app.include_router(api_router, prefix="/api/v1")

    # --- Error Handlers ---
    register_error_handlers(app)

    # --- Health Check ---
    @app.get("/health")
    def health():
        return {"status": "ok", "version": "1.0.0"}

    return app


app = create_app()