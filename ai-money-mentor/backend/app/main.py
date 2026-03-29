from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.health import router as health_router
from app.routes.upload import router as upload_router
from app.routes.analyze import router as analyze_router
app = FastAPI(title="AI Money Mentor", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api")
app.include_router(upload_router, prefix="/api")
app.include_router(analyze_router, prefix="/api")
