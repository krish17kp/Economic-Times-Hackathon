"""
Fetches conversion rules and calculates all options.
Location: backend/app/services/conversion_engine.py
"""

from decimal import Decimal
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.conversion_rule import ConversionRule
from app.services.profit_calculator import calculate_conversion_profit, ConversionProfit
from app.core.constants import DEFAULT_AMORTIZATION_BATCHES


def get_conversion_options(
    db: Session,
    waste_type: str,
    quantity_kg: float,
    quality: str,
    conversion_type: Optional[str] = None,
) -> List[ConversionProfit]:
    """
    Returns profitability for all (or one) conversion options.
    """
    query = db.query(ConversionRule).filter(ConversionRule.input_waste == waste_type)

    if conversion_type:
        query = query.filter(ConversionRule.output_product == conversion_type)

    rules = query.all()
    results = []

    for rule in rules:
        amort = DEFAULT_AMORTIZATION_BATCHES

        result = calculate_conversion_profit(
            quantity_kg=Decimal(str(quantity_kg)),
            quality=quality,
            conversion_ratio=Decimal(str(rule.conversion_ratio)),
            processing_cost_per_kg=Decimal(str(rule.processing_cost_per_kg)),
            output_price_per_kg=Decimal(str(rule.output_price_per_kg)),
            equipment_cost=Decimal(str(rule.equipment_cost or 0)),
            amortization_batches=amort,
            min_viable_qty_kg=Decimal(str(rule.min_viable_qty_kg)),
            processing_time_days=rule.processing_time_days or 7,
            conversion_type=rule.output_product.value if hasattr(rule.output_product, 'value') else str(rule.output_product),
        )

        results.append(result)

    return results
