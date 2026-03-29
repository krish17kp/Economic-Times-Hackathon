from typing import Optional, Dict, Any, List
from app.models.portfolio import Portfolio
from app.models.analysis import (AnalysisResponse, Insight, ExpenseData,
                                  FundCost, OverlapItem, RebalancingAction)
from app.services.metrics_calculator import calculate_portfolio_metrics
from app.services.health_scorer import calculate_health_score, identify_concerns
from datetime import datetime


# Approximate expense ratios by category (SEBI-sourced averages)
EXPENSE_RATIO_MAP = {
    "Large Cap Equity": {"direct": 0.80, "regular": 1.55},
    "Mid Cap Equity": {"direct": 0.90, "regular": 1.70},
    "Small Cap Equity": {"direct": 1.00, "regular": 1.90},
    "Large & Mid Cap Equity": {"direct": 0.85, "regular": 1.65},
    "Flexi Cap Equity": {"direct": 0.85, "regular": 1.65},
    "ELSS": {"direct": 0.75, "regular": 1.60},
    "Index Fund": {"direct": 0.20, "regular": 0.50},
    "International Equity": {"direct": 0.70, "regular": 1.40},
    "Debt - Liquid": {"direct": 0.15, "regular": 0.40},
    "Debt - Short Duration": {"direct": 0.30, "regular": 0.70},
    "Debt - Long Duration": {"direct": 0.40, "regular": 0.85},
    "Debt - Gilt": {"direct": 0.30, "regular": 0.65},
    "Hybrid - Aggressive": {"direct": 0.90, "regular": 1.75},
    "Hybrid - Conservative": {"direct": 0.60, "regular": 1.30},
    "Uncategorized": {"direct": 0.85, "regular": 1.65},
}

# Benchmark annual returns by asset type (approximate 5Y CAGR)
BENCHMARK_RETURNS = {
    "equity": {"name": "Nifty 50 (5Y CAGR)", "return": 14.2},
    "debt": {"name": "Crisil Short Duration Index", "return": 6.8},
    "hybrid": {"name": "Crisil Hybrid 50+50", "return": 10.5},
}

# High-overlap fund category pairs
OVERLAP_PAIRS = [
    ("Large Cap Equity", "Index Fund"),
    ("Large Cap Equity", "Large & Mid Cap Equity"),
    ("Mid Cap Equity", "Large & Mid Cap Equity"),
    ("Small Cap Equity", "Mid Cap Equity"),
    ("Flexi Cap Equity", "Large Cap Equity"),
]


def get_expense_ratio(fund_name: str, category: str) -> float:
    """Return estimated expense ratio for a fund."""
    is_direct = "direct" in fund_name.lower()
    plan_type = "direct" if is_direct else "regular"
    ratios = EXPENSE_RATIO_MAP.get(category, EXPENSE_RATIO_MAP["Uncategorized"])
    return ratios[plan_type]


def calculate_expense_drag(portfolio: Portfolio, metrics) -> Dict[str, Any]:
    """Calculate how much expense ratios are costing the investor per year."""
    total_annual_cost = 0.0
    fund_costs = []

    for fund in portfolio.funds:
        er = get_expense_ratio(fund.fund_name, fund.category)
        annual_cost = fund.current_value * er / 100
        total_annual_cost += annual_cost
        fund_costs.append({
            "fund_name": fund.fund_name,
            "category": fund.category,
            "expense_ratio": er,
            "annual_cost": annual_cost,
            "is_direct": "direct" in fund.fund_name.lower()
        })

    # What could they save if all were direct?
    regular_funds = [f for f in fund_costs if not f["is_direct"]]
    potential_saving = sum(
        f["annual_cost"] - (f["annual_cost"] * 0.5)  # ~50% saving by switching to direct
        for f in regular_funds
    )

    return {
        "total_annual_cost": total_annual_cost,
        "potential_annual_saving": potential_saving,
        "fund_costs": fund_costs,
        "direct_plan_count": sum(1 for f in fund_costs if f["is_direct"]),
        "regular_plan_count": sum(1 for f in fund_costs if not f["is_direct"]),
    }


def detect_overlaps(portfolio: Portfolio) -> List[Dict[str, Any]]:
    """Detect category-level fund overlaps."""
    category_to_funds: Dict[str, List[str]] = {}
    for fund in portfolio.funds:
        cat = fund.category
        if cat not in category_to_funds:
            category_to_funds[cat] = []
        category_to_funds[cat].append(fund.fund_name)

    overlaps = []

    # Same-category overlapping funds
    for cat, funds in category_to_funds.items():
        if len(funds) >= 2:
            overlaps.append({
                "type": "same_category",
                "category": cat,
                "funds": funds,
                "severity": "high" if len(funds) > 2 else "medium",
                "message": f"{len(funds)} funds in {cat} — likely holding the same stocks"
            })

    # Cross-category overlaps
    categories_present = set(category_to_funds.keys())
    for cat_a, cat_b in OVERLAP_PAIRS:
        if cat_a in categories_present and cat_b in categories_present:
            overlaps.append({
                "type": "cross_category",
                "category": f"{cat_a} ↔ {cat_b}",
                "funds": category_to_funds.get(cat_a, []) + category_to_funds.get(cat_b, []),
                "severity": "medium",
                "message": f"Stocks in {cat_a} and {cat_b} heavily overlap"
            })

    return overlaps


def build_rebalancing_plan(portfolio: Portfolio, metrics) -> List[Dict[str, Any]]:
    """Generate a specific, actionable rebalancing recommendation."""
    actions = []
    total = metrics.current_value
    if total == 0:
        return actions

    equity_pct = metrics.asset_allocation.get('equity')
    equity_pct = equity_pct.percentage if equity_pct else 0
    debt_pct = metrics.asset_allocation.get('debt')
    debt_pct = debt_pct.percentage if debt_pct else 0

    # Target: age-based heuristic (assume 30-40 age group → 70:20:10)
    target_equity = 70.0
    target_debt = 20.0

    equity_val = total * equity_pct / 100
    debt_val = total * debt_pct / 100
    target_equity_val = total * target_equity / 100
    target_debt_val = total * target_debt / 100

    equity_diff = target_equity_val - equity_val
    debt_diff = target_debt_val - debt_val

    if abs(equity_diff) > total * 0.03:  # only suggest if > 3% off
        if equity_diff < 0:
            actions.append({
                "action": "reduce",
                "asset": "Equity",
                "amount": abs(equity_diff),
                "detail": f"Move ₹{abs(equity_diff)/100000:.2f}L from equity to debt to reach target 70% equity allocation",
                "priority": 1
            })
        else:
            actions.append({
                "action": "increase",
                "asset": "Equity",
                "amount": equity_diff,
                "detail": f"Add ₹{equity_diff/100000:.2f}L to equity funds (Large Cap or Index) for optimal growth",
                "priority": 1
            })

    if abs(debt_diff) > total * 0.03:
        if debt_diff > 0:
            actions.append({
                "action": "increase",
                "asset": "Debt",
                "amount": debt_diff,
                "detail": f"Add ₹{debt_diff/100000:.2f}L to short-duration or liquid debt funds for stability",
                "priority": 2
            })

    # Too many small cap / sectoral?
    small_cap = metrics.categories.get("Small Cap Equity")
    small_cap_pct = small_cap.percentage if small_cap else 0
    if small_cap_pct > 20:
        excess = (small_cap_pct - 15) / 100 * total
        actions.append({
            "action": "reduce",
            "asset": "Small Cap",
            "amount": excess,
            "detail": f"Small Cap at {small_cap_pct:.0f}% is high risk. Consider trimming ₹{excess/100000:.2f}L to Large Cap or Flexi Cap funds.",
            "priority": 3
        })

    if not actions:
        actions.append({
            "action": "hold",
            "asset": "Portfolio",
            "amount": 0,
            "detail": "Your portfolio allocation is well-balanced. No major rebalancing needed.",
            "priority": 1
        })

    return actions


def calculate_xirr_approx(portfolio: Portfolio, metrics) -> Optional[float]:
    """
    Approximate XIRR using a geometric mean approach.
    XIRR = ((current_value / invested) ^ (1 / years)) - 1
    Uses earliest purchase_date in portfolio if available.
    """
    try:
        from datetime import date

        dates = []
        for fund in portfolio.funds:
            if fund.purchase_date:
                try:
                    if isinstance(fund.purchase_date, str):
                        d = date.fromisoformat(fund.purchase_date[:10])
                        dates.append(d)
                except Exception:
                    continue

        if not dates:
            return None

        earliest = min(dates)
        today = date.today()
        years = (today - earliest).days / 365.25

        if years < 0.1 or metrics.total_invested <= 0:
            return None

        xirr = ((metrics.current_value / metrics.total_invested) ** (1 / years) - 1) * 100
        return round(xirr, 2)
    except Exception:
        return None


def generate_rich_insights(portfolio: Portfolio, metrics, health_score,
                           expense_data, overlaps) -> List[Insight]:
    """Generate 6 rich, specific, actionable insights."""
    insights = []
    equity_pct = metrics.asset_allocation.get('equity')
    equity_pct = equity_pct.percentage if equity_pct else 0
    debt_pct = metrics.asset_allocation.get('debt')
    debt_pct = debt_pct.percentage if debt_pct else 0
    ret_pct = metrics.return_percentage
    n = metrics.fund_count

    # 1. Returns
    if ret_pct > 20:
        insights.append(Insight(id="i_ret", type="positive", icon="✅",
            title="Strong Portfolio Returns",
            description=f"Your portfolio has returned {ret_pct:.1f}% overall — well above fixed deposit rates. "
                        f"Stay invested and avoid switching funds based on short-term market moves.",
            priority=1))
    elif ret_pct > 0:
        insights.append(Insight(id="i_ret", type="info", icon="📊",
            title="Portfolio in Positive Territory",
            description=f"Returns of {ret_pct:.1f}% are positive. Compare with your fund categories' "
                        f"3-year benchmark to see if you're getting value for the risk.",
            priority=1))
    else:
        insights.append(Insight(id="i_ret", type="warning", icon="⚠️",
            title="Portfolio Currently in the Red",
            description=f"Your portfolio is down {abs(ret_pct):.1f}%. For long-term equity investments, "
                        f"this is often temporary. Review if any fund has been consistently underperforming its category.",
            priority=1))

    # 2. Asset allocation
    if equity_pct > 85:
        insights.append(Insight(id="i_eq", type="warning", icon="⚠️",
            title="Very High Equity Concentration",
            description=f"{equity_pct:.0f}% in equity creates high volatility risk. "
                        f"A 15-20% debt allocation would buffer a market downturn significantly.",
            priority=2))
    elif 60 <= equity_pct <= 80:
        insights.append(Insight(id="i_eq", type="positive", icon="✅",
            title="Healthy Equity Balance",
            description=f"Your {equity_pct:.0f}% equity allocation is ideal for long-term wealth creation "
                        f"while the {debt_pct:.0f}% debt provides a stability buffer.",
            priority=2))
    else:
        insights.append(Insight(id="i_eq", type="suggestion", icon="💡",
            title="Equity Allocation Review Needed",
            description=f"You have {equity_pct:.0f}% in equity. Depending on your age and goals, "
                        f"you may want to adjust this. General rule: 100 minus your age = equity %.",
            priority=2))

    # 3. Expense ratio / cost
    total_cost = expense_data["total_annual_cost"]
    saving = expense_data["potential_annual_saving"]
    regular_count = expense_data["regular_plan_count"]
    if regular_count > 0 and saving > 1000:
        insights.append(Insight(id="i_cost", type="suggestion", icon="💡",
            title=f"Save ₹{saving:,.0f}/yr by Switching to Direct Plans",
            description=f"You have {regular_count} regular plan fund(s) costing you extra ₹{saving:,.0f} per year in commissions. "
                        f"Switch to direct plans via MF Central or your fund house website/app — it's free.",
            priority=3))
    elif expense_data["direct_plan_count"] == n:
        insights.append(Insight(id="i_cost", type="positive", icon="✅",
            title="All Direct Plans — Great Cost Discipline",
            description=f"Your annual expense cost is ₹{total_cost:,.0f}. All your funds are direct plans, "
                        f"saving you thousands annually compared to regular plan investors.",
            priority=3))

    # 4. Fund overlap
    if overlaps:
        top_overlap = overlaps[0]
        insights.append(Insight(id="i_overlap", type="warning", icon="⚠️",
            title="Fund Overlap Detected",
            description=f"{top_overlap['message']}. "
                        f"This means you're paying expense ratios twice for essentially the same exposure. "
                        f"Consider consolidating into one strong fund per category.",
            priority=4))
    else:
        insights.append(Insight(id="i_overlap", type="positive", icon="✅",
            title="No Significant Fund Overlap",
            description="Your funds appear to cover distinct market segments with minimal duplication. "
                        "This means your diversification is genuine, not just superficial.",
            priority=4))

    # 5. Fund count
    if n > 12:
        insights.append(Insight(id="i_count", type="suggestion", icon="💡",
            title=f"Too Many Funds ({n})",
            description=f"Managing {n} funds adds complexity without proportional benefit. "
                        f"Most experts recommend 5-8 well-chosen funds. Identify your weakest-performing duplicates and consolidate.",
            priority=5))
    elif n < 3:
        insights.append(Insight(id="i_count", type="warning", icon="⚠️",
            title="Under-diversified Portfolio",
            description=f"Only {n} fund(s) means high concentration risk. "
                        f"Add a Large Cap Index Fund, a Mid Cap fund, and a Debt/Liquid fund for a solid base.",
            priority=5))
    else:
        insights.append(Insight(id="i_count", type="info", icon="📊",
            title=f"Good Fund Count ({n} funds)",
            description=f"Your {n} funds provide good diversification. Focus on reviewing performance quarterly "
                        f"rather than adding more funds.",
            priority=5))

    # 6. Benchmark
    equity_benchmark = BENCHMARK_RETURNS["equity"]
    if ret_pct > equity_benchmark["return"] and equity_pct > 50:
        insights.append(Insight(id="i_bench", type="positive", icon="✅",
            title="Beating Market Benchmark",
            description=f"Your {ret_pct:.1f}% return beats the {equity_benchmark['name']} ({equity_benchmark['return']}% CAGR). "
                        f"Your fund selection has added alpha. Continue reviewing annually.",
            priority=6))
    elif equity_pct > 50:
        insights.append(Insight(id="i_bench", type="suggestion", icon="💡",
            title="Consider Adding an Index Fund",
            description=f"The {equity_benchmark['name']} delivers {equity_benchmark['return']}% with minimal cost. "
                        f"Adding a Nifty 50 index fund (lowest expense ratio) as a core holding is a proven strategy.",
            priority=6))

    return insights[:6]


def build_plain_english_summary(portfolio: Portfolio, metrics, health_score,
                                xirr: Optional[float], expense_data: dict) -> str:
    lakh = 100000
    n = metrics.fund_count
    cv = metrics.current_value
    inv = metrics.total_invested
    ret = metrics.return_percentage
    eq_pct = metrics.asset_allocation.get('equity')
    eq_pct = eq_pct.percentage if eq_pct else 0

    cv_str = f"₹{cv/lakh:.2f} lakhs" if cv >= lakh else f"₹{cv:,.0f}"
    inv_str = f"₹{inv/lakh:.2f} lakhs" if inv >= lakh else f"₹{inv:,.0f}"
    cost_str = f"₹{expense_data['total_annual_cost']:,.0f}"
    xirr_str = f"Your annualised XIRR is {xirr:.1f}%. " if xirr else ""

    name = getattr(portfolio, 'investor_name', 'You')
    name_prefix = f"{name}'s portfolio has" if name and name != "Investor" else "Your portfolio has"

    return (
        f"{name_prefix} {inv_str} invested across {n} mutual funds, currently valued at {cv_str} "
        f"— a return of {ret:.1f}%. {xirr_str}"
        f"With {eq_pct:.0f}% in equity, your portfolio is {health_score.label.lower()} "
        f"with a health score of {health_score.overall}/100. "
        f"Your annual expense cost is {cost_str}. "
        f"{'Keep up the disciplined investing — consistency beats timing every time.' if ret > 10 else 'Stay invested and review your fund choices annually for long-term success.'}"
    )


async def run_full_analysis(portfolio: Portfolio,
                            user_context: Optional[Dict[str, Any]] = None) -> AnalysisResponse:
    metrics = calculate_portfolio_metrics(portfolio)
    health_score = calculate_health_score(portfolio, metrics)

    # Enrich with additional analyses
    expense_data_raw = calculate_expense_drag(portfolio, metrics)
    overlaps_raw = detect_overlaps(portfolio)
    rebalancing_raw = build_rebalancing_plan(portfolio, metrics)
    xirr = calculate_xirr_approx(portfolio, metrics)
    insights = generate_rich_insights(portfolio, metrics, health_score, expense_data_raw, overlaps_raw)
    summary = build_plain_english_summary(portfolio, metrics, health_score, xirr, expense_data_raw)

    expense_model = ExpenseData(
        total_annual_cost=expense_data_raw["total_annual_cost"],
        potential_annual_saving=expense_data_raw["potential_annual_saving"],
        direct_plan_count=expense_data_raw["direct_plan_count"],
        regular_plan_count=expense_data_raw["regular_plan_count"],
        fund_costs=[FundCost(**fc) for fc in expense_data_raw["fund_costs"]]
    )
    overlap_models = [OverlapItem(**o) for o in overlaps_raw]
    rebalancing_models = [RebalancingAction(**r) for r in rebalancing_raw]

    return AnalysisResponse(
        success=True,
        metrics=metrics,
        health_score=health_score,
        insights=insights,
        plain_english_summary=summary,
        ai_generated=False,
        analysis_timestamp=datetime.utcnow().isoformat() + "Z",
        xirr=xirr,
        expense_data=expense_model,
        overlaps=overlap_models,
        rebalancing=rebalancing_models,
    )
