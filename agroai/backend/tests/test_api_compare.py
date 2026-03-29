"""
API integration tests for compare endpoint.
Location: backend/tests/test_api_compare.py
"""

import json
import pytest
from decimal import Decimal

from app.models.buyer import Buyer
from app.models.conversion_rule import ConversionRule
from app.models.carbon_factor import CarbonFactor
from app.models.base import new_uuid


def _seed_test_data(db):
    """Seed minimal data needed for compare endpoint to work."""
    # One buyer
    buyer = Buyer(
        id=new_uuid(),
        business_name="Compare Test Buyer",
        buyer_type="biomass_plant",
        accepted_waste=json.dumps(["rice_straw"]),
        price_per_kg=Decimal("2.00"),
        min_quantity_kg=Decimal("500"),
        provides_pickup=True,
        pickup_radius_km=50,
        state="Punjab",
        latitude=Decimal("30.90"),
        longitude=Decimal("75.85"),
        phone="9876543210",
        is_verified=True,
        is_active=True,
    )
    db.add(buyer)

    # One conversion rule
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
    )
    db.add(rule)

    # One carbon factor
    cf = CarbonFactor(
        waste_type="rice_straw",
        burn_emission_kg_co2_per_kg=Decimal("1.50"),
        conversion_type=None,
        sequestration_kg_co2_per_kg=Decimal("0"),
        source="IPCC",
    )
    db.add(cf)

    db.commit()


class TestCompareAPI:
    def test_compare_returns_200_with_options(self, client, db):
        _seed_test_data(db)
        response = client.post("/api/v1/compare", json={
            "waste_type": "rice_straw",
            "quantity_kg": 5000,
            "quality": "semi_dry",
            "latitude": 30.90,
            "longitude": 75.85,
        })
        assert response.status_code == 200
        data = response.json()
        assert "options" in data
        assert "carbon_impact" in data
        assert "is_conversion_better" in data
        assert len(data["options"]) >= 1

    def test_compare_requires_location(self, client, db):
        """Without lat/lon and without pincode, should raise 400."""
        response = client.post("/api/v1/compare", json={
            "waste_type": "rice_straw",
            "quantity_kg": 5000,
            "quality": "dry",
        })
        assert response.status_code == 400

    def test_compare_has_sell_raw_option(self, client, db):
        _seed_test_data(db)
        response = client.post("/api/v1/compare", json={
            "waste_type": "rice_straw",
            "quantity_kg": 5000,
            "quality": "dry",
            "latitude": 30.90,
            "longitude": 75.85,
        })
        data = response.json()
        option_types = [o["option_type"] for o in data["options"]]
        assert "sell_raw" in option_types
