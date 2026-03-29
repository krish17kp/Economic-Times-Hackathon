"""
Import all models so Alembic can detect them.
Location: backend/app/models/__init__.py
"""

from app.models.base import Base
from app.models.user import User
from app.models.waste_log import WasteLog
from app.models.market_price import MarketPrice
from app.models.buyer import Buyer
from app.models.conversion_rule import ConversionRule
from app.models.carbon_factor import CarbonFactor
from app.models.transaction import Transaction
from app.models.recommendation_log import RecommendationLog

__all__ = [
    "Base",
    "User",
    "WasteLog",
    "MarketPrice",
    "Buyer",
    "ConversionRule",
    "CarbonFactor",
    "Transaction",
    "RecommendationLog",
]
