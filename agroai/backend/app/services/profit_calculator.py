"""
Profit calculation for raw sell and conversion options.
Location: backend/app/services/profit_calculator.py

NO FastAPI imports. Pure math.
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from app.core.constants import QUALITY_MULTIPLIER, QualityGrade, RAW_SALE_TIME_DAYS, CONVERTED_PRODUCT_SELL_TIME_DAYS


@dataclass
class RawSellProfit:
    gross_revenue: Decimal
    transport_cost: Decimal
    net_profit: Decimal
    price_per_kg_used: Decimal
    buyer_name: Optional[str]
    time_to_money_days: int


@dataclass
class ConversionProfit:
    conversion_type: str
    output_quantity_kg: Decimal
    gross_revenue: Decimal
    processing_cost: Decimal
    equipment_amortized: Decimal
    net_profit: Decimal
    time_to_money_days: int
    is_viable: bool
    viability_reason: Optional[str]


def calculate_raw_sell_profit(
    quantity_kg: Decimal,
    quality: str,
    market_price_per_kg: Decimal,
    transport_cost: Decimal,
    buyer_name: Optional[str] = None,
) -> RawSellProfit:
    quality_enum = QualityGrade(quality)
    quality_factor = Decimal(str(QUALITY_MULTIPLIER.get(quality_enum, 0.85)))
    effective_price = market_price_per_kg * quality_factor

    gross = quantity_kg * effective_price
    net = gross - transport_cost

    return RawSellProfit(
        gross_revenue=round(gross, 2),
        transport_cost=round(transport_cost, 2),
        net_profit=round(net, 2),
        price_per_kg_used=round(effective_price, 4),
        buyer_name=buyer_name,
        time_to_money_days=RAW_SALE_TIME_DAYS,
    )


def calculate_conversion_profit(
    quantity_kg: Decimal,
    quality: str,
    conversion_ratio: Decimal,
    processing_cost_per_kg: Decimal,
    output_price_per_kg: Decimal,
    equipment_cost: Decimal,
    amortization_batches: int,
    min_viable_qty_kg: Decimal,
    processing_time_days: int,
    conversion_type: str,
) -> ConversionProfit:
    quality_enum = QualityGrade(quality)
    quality_factor = Decimal(str(QUALITY_MULTIPLIER.get(quality_enum, 0.85)))

    # Viability check
    if quantity_kg < min_viable_qty_kg:
        return ConversionProfit(
            conversion_type=conversion_type,
            output_quantity_kg=Decimal("0"),
            gross_revenue=Decimal("0"),
            processing_cost=Decimal("0"),
            equipment_amortized=Decimal("0"),
            net_profit=Decimal("0"),
            time_to_money_days=processing_time_days,
            is_viable=False,
            viability_reason=f"Minimum {min_viable_qty_kg}kg required. You have {quantity_kg}kg.",
        )

    output_qty = quantity_kg * conversion_ratio * quality_factor
    gross = output_qty * output_price_per_kg
    processing = quantity_kg * processing_cost_per_kg
    equip_amort = equipment_cost / Decimal(str(amortization_batches)) if amortization_batches > 0 else Decimal("0")

    net = gross - processing - equip_amort
    total_time = processing_time_days + CONVERTED_PRODUCT_SELL_TIME_DAYS

    return ConversionProfit(
        conversion_type=conversion_type,
        output_quantity_kg=round(output_qty, 2),
        gross_revenue=round(gross, 2),
        processing_cost=round(processing, 2),
        equipment_amortized=round(equip_amort, 2),
        net_profit=round(net, 2),
        time_to_money_days=total_time,
        is_viable=True,
        viability_reason=None,
    )
