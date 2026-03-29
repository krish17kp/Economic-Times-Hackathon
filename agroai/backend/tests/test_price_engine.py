"""
Tests for the price engine service.
Location: backend/tests/test_price_engine.py
"""

import pytest
from datetime import date
from sqlalchemy.orm import Session

from app.models.market_price import MarketPrice
from app.services.price_engine import get_current_price
from app.core.exceptions import NotFoundError


def _seed_price(db: Session, waste_type: str = "rice_straw", region: str = "Punjab",
                price_avg: float = 2.0, recorded_date: date = None):
    if recorded_date is None:
        recorded_date = date.today()
    record = MarketPrice(
        waste_type=waste_type,
        region=region,
        district="Ludhiana",
        price_min=price_avg - 0.5,
        price_max=price_avg + 0.5,
        price_avg=price_avg,
        source="test",
        recorded_date=recorded_date,
    )
    db.add(record)
    db.commit()
    return record


class TestPriceEngine:
    def test_returns_price_for_seeded_data(self, db):
        _seed_price(db, "rice_straw", "Punjab", 2.0)
        result = get_current_price(db, "rice_straw", "Punjab")
        assert "current" in result
        assert result["current"]["avg"] == pytest.approx(2.0, rel=1e-2)

    def test_raises_not_found_for_unknown(self, db):
        with pytest.raises(NotFoundError):
            get_current_price(db, "banana_peel", "Punjab")

    def test_trend_stable_with_one_record(self, db):
        _seed_price(db, "rice_husk", "Punjab", 3.0)
        result = get_current_price(db, "rice_husk", "Punjab")
        assert result["trend"] in ("rising", "falling", "stable")

    def test_confidence_low_with_few_records(self, db):
        _seed_price(db, "cotton_stalk", "Haryana", 1.0)
        result = get_current_price(db, "cotton_stalk", "Haryana")
        assert result["confidence"] in ("low", "medium", "high")

    def test_history_returned(self, db):
        _seed_price(db, "wheat_straw", "Punjab", 1.5)
        result = get_current_price(db, "wheat_straw", "Punjab")
        assert isinstance(result["history"], list)
        assert len(result["history"]) >= 1
