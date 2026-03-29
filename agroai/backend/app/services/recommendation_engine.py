"""
Final recommendation logic. Deterministic rules, no LLM.
Location: backend/app/services/recommendation_engine.py
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import List, Optional

from app.services.profit_calculator import RawSellProfit, ConversionProfit


@dataclass
class RecommendFactor:
    factor: str
    impact: str  # "positive", "negative", "neutral"
    detail: str


@dataclass
class Recommendation:
    action: str
    confidence: float
    reasoning_en: str
    reasoning_hi: str
    factors: List[RecommendFactor]
    alternatives: List[str]
    net_profit: float
    time_days: int
    risk_level: str


def generate_recommendation(
    raw_sell: Optional[RawSellProfit],
    conversions: List[ConversionProfit],
    has_nearby_buyer: bool,
    buyer_is_verified: bool,
    market_trend: str,
) -> Recommendation:
    """
    Decision rules:
    1. Safety first — is there a real buyer?
    2. Profit magnitude
    3. Time to money (farmers need cash fast)
    4. Risk (equipment cost, market uncertainty)
    5. Effort (farmers are exhausted after harvest)
    """
    factors: List[RecommendFactor] = []
    viable_conversions = [c for c in conversions if c.is_viable]
    best_conversion = max(viable_conversions, key=lambda c: c.net_profit, default=None)

    raw_profit: Decimal = raw_sell.net_profit if raw_sell else Decimal("0")
    conv_profit: Decimal = best_conversion.net_profit if best_conversion else Decimal("0")

    # ---------- Scenario 1: Raw sell is clearly better ----------
    if has_nearby_buyer and raw_sell is not None and raw_profit > Decimal("0"):
        if best_conversion is None or raw_profit > conv_profit * Decimal("1.3"):
            factors.append(RecommendFactor(
                factor="Raw sell dominates",
                impact="positive",
                detail=f"Raw: ₹{raw_profit} vs Conversion: ₹{conv_profit}",
            ))
            confidence = 0.90 if buyer_is_verified else 0.70

            return Recommendation(
                action="sell_raw",
                confidence=confidence,
                reasoning_en=f"Sell raw. Net profit ₹{raw_profit} in {raw_sell.time_to_money_days} days. Buyer: {raw_sell.buyer_name or 'available'}.",
                reasoning_hi=f"कच्चा बेचें। शुद्ध लाभ ₹{raw_profit}, {raw_sell.time_to_money_days} दिन में। खरीदार: {raw_sell.buyer_name or 'उपलब्ध'}।",
                factors=factors,
                alternatives=[f"convert_{c.conversion_type}" for c in viable_conversions],
                net_profit=float(raw_profit),
                time_days=raw_sell.time_to_money_days,
                risk_level="low",
            )

    # ---------- Scenario 2: Conversion is significantly better ----------
    if best_conversion and conv_profit > raw_profit * Decimal("1.5"):
        factors.append(RecommendFactor(
            factor="Conversion more profitable",
            impact="positive",
            detail=f"Conversion: ₹{conv_profit} vs Raw: ₹{raw_profit} (>50% more)",
        ))
        ctype = best_conversion.conversion_type

        return Recommendation(
            action=f"convert_{ctype}",
            confidence=0.75,
            reasoning_en=f"Convert to {ctype}. Net profit ₹{conv_profit} in {best_conversion.time_to_money_days} days.",
            reasoning_hi=f"{ctype} में बदलें। शुद्ध लाभ ₹{conv_profit}, {best_conversion.time_to_money_days} दिन में।",
            factors=factors,
            alternatives=["sell_raw"],
            net_profit=float(conv_profit),
            time_days=best_conversion.time_to_money_days,
            risk_level="medium",
        )

    # ---------- Scenario 3: Marginal — prefer raw (lower risk) ----------
    if has_nearby_buyer and raw_sell is not None and raw_profit > Decimal("0"):
        factors.append(RecommendFactor(
            factor="Similar returns — lower risk preferred",
            impact="neutral",
            detail="Raw sell is simpler and faster.",
        ))

        return Recommendation(
            action="sell_raw",
            confidence=0.65,
            reasoning_en=f"Sell raw for simplicity. ₹{raw_profit} in {raw_sell.time_to_money_days} days.",
            reasoning_hi=f"आसानी के लिए कच्चा बेचें। ₹{raw_profit}, {raw_sell.time_to_money_days} दिन में।",
            factors=factors,
            alternatives=[f"convert_{c.conversion_type}" for c in viable_conversions],
            net_profit=float(raw_profit),
            time_days=raw_sell.time_to_money_days,
            risk_level="low",
        )

    # ---------- Scenario 4: Rising market — hold ----------
    if market_trend == "rising":
        factors.append(RecommendFactor(
            factor="Rising market",
            impact="positive",
            detail="Prices trending up. Holding 1-2 weeks may help.",
        ))

        return Recommendation(
            action="hold",
            confidence=0.50,
            reasoning_en="Prices rising. Consider storing for 1-2 weeks.",
            reasoning_hi="कीमतें बढ़ रही हैं। 1-2 हफ्ते स्टोर करने पर विचार करें।",
            factors=factors,
            alternatives=["sell_raw"],
            net_profit=float(raw_profit),
            time_days=14,
            risk_level="medium",
        )

    # ---------- Scenario 5: Nothing works ----------
    return Recommendation(
        action="sell_raw" if raw_profit > Decimal("0") else "hold",
        confidence=0.40,
        reasoning_en="Limited options. Contact your local FPO for aggregation.",
        reasoning_hi="सीमित विकल्प। एकत्रीकरण के लिए अपने स्थानीय FPO से संपर्क करें।",
        factors=[RecommendFactor(factor="Limited options", impact="negative", detail="No strongly profitable option found.")],
        alternatives=[],
        net_profit=float(raw_profit),
        time_days=7,
        risk_level="high",
    )
