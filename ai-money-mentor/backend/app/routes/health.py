from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "llm_configured": True,
        "llm_provider": "claude",
        "version": "1.0.0"
    }
