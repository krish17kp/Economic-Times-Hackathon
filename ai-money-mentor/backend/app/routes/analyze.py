from fastapi import APIRouter
from app.models.api_models import AnalyzeRequest
from app.models.analysis import AnalysisResponse
from app.services.analysis_orchestrator import run_full_analysis

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_portfolio(req: AnalyzeRequest):
    return await run_full_analysis(req.portfolio, req.user_context)
