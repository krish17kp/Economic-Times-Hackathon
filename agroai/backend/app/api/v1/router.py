"""
Aggregates all v1 route modules.
Location: backend/app/api/v1/router.py
"""

from fastapi import APIRouter

from app.api.v1 import auth, waste, price, buyers, convert, compare, recommend, carbon, assistant

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(waste.router, prefix="/waste", tags=["Waste"])
api_router.include_router(price.router, prefix="/price", tags=["Price"])
api_router.include_router(buyers.router, prefix="/buyers", tags=["Buyers"])
api_router.include_router(convert.router, prefix="/convert", tags=["Conversion"])
api_router.include_router(compare.router, prefix="/compare", tags=["Comparison"])
api_router.include_router(recommend.router, prefix="/recommend", tags=["Recommendation"])
api_router.include_router(carbon.router, prefix="/carbon", tags=["Carbon"])
api_router.include_router(assistant.router, prefix="/assistant", tags=["Assistant"])
