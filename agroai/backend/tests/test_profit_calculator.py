"""
Tests for profit calculation.
Location: backend/tests/test_profit_calculator.py
"""

from decimal import Decimal
from app.services.profit_calculator import calculate_raw_sell_profit, calculate_conversion_profit


class TestRawSellProfit:
    def test_dry_quality_full_price(self):
        result = calculate_raw_sell_profit(
            quantity_kg=Decimal("5000"),
            quality="dry",
            market_price_per_kg=Decimal("2.00"),
            transport_cost=Decimal("1500"),
        )
        assert result.gross_revenue == Decimal("10000.00")
        assert result.net_profit == Decimal("8500.00")

    def test_wet_quality_penalty(self):
        result = calculate_raw_sell_profit(
            quantity_kg=Decimal("5000"),
            quality="wet",
            market_price_per_kg=Decimal("2.00"),
            transport_cost=Decimal("1500"),
        )
        assert result.gross_revenue == Decimal("6000.00")
        assert result.net_profit == Decimal("4500.00")

    def test_transport_exceeds_revenue(self):
        result = calculate_raw_sell_profit(
            quantity_kg=Decimal("100"),
            quality="wet",
            market_price_per_kg=Decimal("1.50"),
            transport_cost=Decimal("2000"),
        )
        assert result.net_profit < 0


class TestConversionProfit:
    def test_below_minimum_not_viable(self):
        result = calculate_conversion_profit(
            quantity_kg=Decimal("500"),
            quality="dry",
            conversion_ratio=Decimal("0.30"),
            processing_cost_per_kg=Decimal("1.50"),
            output_price_per_kg=Decimal("12.00"),
            equipment_cost=Decimal("85000"),
            amortization_batches=20,
            min_viable_qty_kg=Decimal("1000"),
            processing_time_days=14,
            conversion_type="biochar",
        )
        assert result.is_viable is False
        assert result.net_profit == Decimal("0")

    def test_viable_biochar_math(self):
        result = calculate_conversion_profit(
            quantity_kg=Decimal("5000"),
            quality="semi_dry",
            conversion_ratio=Decimal("0.30"),
            processing_cost_per_kg=Decimal("1.50"),
            output_price_per_kg=Decimal("12.00"),
            equipment_cost=Decimal("85000"),
            amortization_batches=20,
            min_viable_qty_kg=Decimal("1000"),
            processing_time_days=14,
            conversion_type="biochar",
        )
        assert result.is_viable is True
        assert result.output_quantity_kg == Decimal("1275.00")  # 5000 * 0.30 * 0.85
        assert result.gross_revenue == Decimal("15300.00")      # 1275 * 12
        assert result.processing_cost == Decimal("7500.00")     # 5000 * 1.50
        assert result.equipment_amortized == Decimal("4250.00") # 85000 / 20
        assert result.net_profit == Decimal("3550.00")          # 15300 - 7500 - 4250
