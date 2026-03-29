"""
MarketPrice — historical mandi/market price data.
Location: backend/app/models/market_price.py
"""

from sqlalchemy import Column, Integer, String, Numeric, Date, Enum, CheckConstraint

from app.models.base import Base, TimestampMixin
from app.core.constants import WasteType


class MarketPrice(Base, TimestampMixin):
    __tablename__ = "market_prices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    waste_type = Column(Enum(WasteType), nullable=False)
    region = Column(String(100), nullable=False)
    district = Column(String(100))
    price_min = Column(Numeric(8, 2), nullable=False)
    price_max = Column(Numeric(8, 2), nullable=False)
    price_avg = Column(Numeric(8, 2), nullable=False)
    unit = Column(String(10), default="per_kg")
    source = Column(String(50), default="manual")
    recorded_date = Column(Date, nullable=False, index=True)

    __table_args__ = (
        CheckConstraint("price_min >= 0", name="positive_min"),
        CheckConstraint("price_max >= price_min", name="max_gte_min"),
        CheckConstraint("price_avg >= price_min AND price_avg <= price_max", name="valid_avg"),
    )
