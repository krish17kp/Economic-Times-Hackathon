"""
Tests for transport cost calculation.
Location: backend/tests/test_transport_calculator.py
"""

from app.services.transport_calculator import haversine_distance, estimate_transport_cost


class TestHaversine:
    def test_same_point_zero_distance(self):
        assert haversine_distance(30.0, 75.0, 30.0, 75.0) == 0.0

    def test_ludhiana_to_amritsar(self):
        # ~130km straight line
        dist = haversine_distance(30.9010, 75.8573, 31.6340, 74.8723)
        assert 120 < dist < 140

    def test_short_distance(self):
        dist = haversine_distance(30.90, 75.85, 30.92, 75.87)
        assert dist < 5


class TestTransportCost:
    def test_buyer_pickup_free(self):
        result = estimate_transport_cost(20, 5000, buyer_provides_pickup=True, buyer_pickup_radius_km=30)
        assert result.cost_inr == 0.0
        assert result.mode == "pickup_by_buyer"

    def test_buyer_pickup_outside_radius(self):
        result = estimate_transport_cost(50, 5000, buyer_provides_pickup=True, buyer_pickup_radius_km=30)
        assert result.cost_inr > 0
        assert result.mode == "tractor_trolley"

    def test_truck_for_large_quantity(self):
        result = estimate_transport_cost(50, 10000, buyer_provides_pickup=False)
        assert result.mode == "hired_truck"

    def test_cost_increases_with_distance(self):
        short = estimate_transport_cost(10, 5000)
        long = estimate_transport_cost(50, 5000)
        assert long.cost_inr > short.cost_inr
