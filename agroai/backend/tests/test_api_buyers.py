"""
API integration tests for buyer endpoints.
Location: backend/tests/test_api_buyers.py
"""

import json
from app.models.buyer import Buyer
from app.models.base import new_uuid


def _create_buyer(db, lat, lon, waste_types, price=2.0, is_active=True):
    buyer = Buyer(
        id=new_uuid(),
        business_name=f"Test Buyer {lat}",
        buyer_type="biomass_plant",
        accepted_waste=json.dumps(waste_types),
        price_per_kg=price,
        min_quantity_kg=500,
        max_capacity_kg=50000,
        provides_pickup=False,
        pickup_radius_km=0,
        state="Punjab",
        latitude=lat,
        longitude=lon,
        phone="9876543210",
        is_verified=True,
        is_active=is_active,
    )
    db.add(buyer)
    db.commit()
    return buyer


class TestBuyersAPI:
    def test_nearby_returns_200(self, client, db):
        _create_buyer(db, lat=30.91, lon=75.86, waste_types=["rice_straw"])
        response = client.get("/api/v1/buyers/nearby", params={
            "waste_type": "rice_straw",
            "lat": 30.90,
            "long": 75.85,
            "radius_km": 80,
        })
        assert response.status_code == 200
        data = response.json()
        assert "buyers" in data
        assert "total" in data

    def test_no_buyers_returns_empty_list(self, client, db):
        response = client.get("/api/v1/buyers/nearby", params={
            "waste_type": "sugarcane_bagasse",
            "lat": 28.63,
            "long": 77.22,
            "radius_km": 10,
        })
        assert response.status_code == 200
        assert response.json()["total"] == 0

    def test_inactive_buyer_excluded(self, client, db):
        _create_buyer(db, lat=30.91, lon=75.86, waste_types=["rice_husk"], is_active=False)
        response = client.get("/api/v1/buyers/nearby", params={
            "waste_type": "rice_husk",
            "lat": 30.90,
            "long": 75.85,
        })
        assert response.status_code == 200
        # Inactive buyer should not appear
        for b in response.json().get("buyers", []):
            assert b["business_name"] != "Test Buyer 30.91"
