"""
Tests for the conversion engine service.
Location: backend/tests/test_conversion_engine.py
"""

import pytest
from decimal import Decimal
from sqlalchemy.orm import Session

from app.models.conversion_rule import ConversionRule
from app.services.conversion_engine import get_conversion_options


def _seed_rule(db: Session):
    """Insert one rice_straw → biochar rule for testing."""
    rule = ConversionRule(
        input_waste="rice_straw",
        output_product="biochar",
        conversion_ratio=Decimal("0.30"),
        processing_cost_per_kg=Decimal("1.50"),
        output_price_per_kg=Decimal("12.00"),
        equipment_cost=Decimal("85000"),
        min_viable_qty_kg=Decimal("1000"),
        processing_time_days=14,
        skill_level="moderate",
        source="Test",
    )
    db.add(rule)
    db.commit()
    return rule


class TestConversionEngine:
    def test_returns_results_for_known_waste(self, db):
        _seed_rule(db)
        results = get_conversion_options(db, "rice_straw", 5000, "semi_dry")
        assert len(results) >= 1
        assert results[0].conversion_type == "biochar"

    def test_viable_at_sufficient_quantity(self, db):
        _seed_rule(db)
        results = get_conversion_options(db, "rice_straw", 5000, "dry")
        viable = [r for r in results if r.is_viable]
        assert len(viable) >= 1

    def test_not_viable_below_minimum(self, db):
        _seed_rule(db)
        results = get_conversion_options(db, "rice_straw", 100, "dry")
        assert all(not r.is_viable for r in results)

    def test_empty_for_unknown_waste(self, db):
        results = get_conversion_options(db, "banana_peel", 5000, "dry")
        assert results == []

    def test_conversion_type_filter(self, db):
        _seed_rule(db)
        results = get_conversion_options(db, "rice_straw", 5000, "dry", conversion_type="biochar")
        assert all(r.conversion_type == "biochar" for r in results)
