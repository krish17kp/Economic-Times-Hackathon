from app.models.portfolio import Portfolio
from app.models.analysis import HealthScore, SubScore, PortfolioMetrics
from typing import List

def has_international_funds(metrics: PortfolioMetrics) -> bool:
    return 'International Equity' in metrics.categories

def get_category_pct(metrics: PortfolioMetrics, category: str) -> float:
    return metrics.categories.get(category, type('obj', (object,), {'percentage': 0.0})).percentage

def extract_amc(fund_name: str) -> str:
    return fund_name.split()[0].lower() if fund_name else ""

def score_diversification(metrics: PortfolioMetrics) -> int:
    score = 0
    equity_pct = metrics.asset_allocation.get('equity', type('obj', (object,), {'percentage': 0.0})).percentage
    if 50 <= equity_pct <= 75:
        score += 30
    elif 40 <= equity_pct <= 85:
        score += 20
    elif 30 <= equity_pct <= 90:
        score += 10
        
    num_cats = metrics.num_categories
    if num_cats >= 5: score += 25
    elif num_cats >= 4: score += 20
    elif num_cats >= 3: score += 15
    elif num_cats >= 2: score += 8
        
    n = metrics.fund_count
    if 5 <= n <= 12: score += 15
    elif 3 <= n <= 15: score += 10
    elif 2 <= n <= 20: score += 5
        
    top3 = metrics.concentration_top3_pct
    if top3 < 50: score += 20
    elif top3 < 65: score += 15
    elif top3 < 80: score += 8
        
    if has_international_funds(metrics):
        score += 10
        
    return min(score, 100)

def score_overlap(portfolio: Portfolio, metrics: PortfolioMetrics) -> int:
    score = 100
    category_counts = {}
    for fund in portfolio.funds:
        cat = fund.category
        category_counts[cat] = category_counts.get(cat, 0) + 1
        
    for cat, count in category_counts.items():
        if count > 3: score -= 25
        elif count > 2: score -= 15
        elif count > 1: score -= 5
            
    large_cap_count = category_counts.get('Large Cap Equity', 0)
    index_fund_count = category_counts.get('Index Fund', 0)
    if large_cap_count >= 1 and index_fund_count >= 1:
        score -= 10
        
    amc_category_pairs = set()
    for fund in portfolio.funds:
        amc = extract_amc(fund.fund_name)
        pair = f"{amc}_{fund.category}"
        if pair in amc_category_pairs:
            score -= 15
        amc_category_pairs.add(pair)
        
    return max(score, 0)

def score_cost_efficiency(portfolio: Portfolio) -> int:
    score = 0
    direct_count = 0
    regular_count = 0
    index_count = 0
    
    for fund in portfolio.funds:
        name = fund.fund_name.lower()
        if 'direct' in name:
            direct_count += 1
        else:
            regular_count += 1
            
        if 'index' in name or 'nifty' in name or 'sensex' in name:
            index_count += 1
            
    total = direct_count + regular_count
    if total > 0:
        direct_ratio = direct_count / total
        score += int(direct_ratio * 60)
        
    if index_count >= 2: score += 20
    elif index_count >= 1: score += 15
    else: score += 5
        
    n = len(portfolio.funds)
    if n <= 8: score += 20
    elif n <= 12: score += 15
    elif n <= 15: score += 10
        
    return min(score, 100)

def score_risk_balance(portfolio: Portfolio, metrics: PortfolioMetrics) -> int:
    score = 0
    equity_pct = metrics.asset_allocation.get('equity', type('obj', (object,), {'percentage': 0.0})).percentage
    debt_pct = metrics.asset_allocation.get('debt', type('obj', (object,), {'percentage': 0.0})).percentage
    
    if debt_pct >= 20 and equity_pct >= 40: score += 35
    elif debt_pct >= 10: score += 25
    elif debt_pct >= 5: score += 15
    else: score += 5
        
    small_cap_pct = get_category_pct(metrics, 'Small Cap Equity')
    sectoral_pct = get_category_pct(metrics, 'Sectoral/Thematic Equity')
    high_risk_pct = small_cap_pct + sectoral_pct
    
    if high_risk_pct <= 15: score += 25
    elif high_risk_pct <= 25: score += 20
    elif high_risk_pct <= 35: score += 10
        
    large_cap_pct = get_category_pct(metrics, 'Large Cap Equity')
    index_pct = get_category_pct(metrics, 'Index Fund')
    stable_pct = large_cap_pct + index_pct
    
    if stable_pct >= 25: score += 20
    elif stable_pct >= 15: score += 15
    elif stable_pct >= 5: score += 10
    else: score += 5
        
    liquid_pct = get_category_pct(metrics, 'Debt - Liquid')
    if liquid_pct >= 5: score += 20
    elif debt_pct >= 10: score += 10
        
    return min(score, 100)

def get_label_and_color(score: int) -> tuple[str, str]:
    if score <= 30: return "Needs Attention", "#ef4444"
    if score <= 50: return "Below Average", "#f97316"
    if score <= 65: return "Moderate", "#eab308"
    if score <= 80: return "Good", "#22c55e"
    return "Excellent", "#10b981"

def calculate_health_score(portfolio: Portfolio, metrics: PortfolioMetrics) -> HealthScore:
    div_score = score_diversification(metrics)
    ovr_score = score_overlap(portfolio, metrics)
    cost_score = score_cost_efficiency(portfolio)
    risk_score = score_risk_balance(portfolio, metrics)
    
    overall = int(
        div_score * 0.30 +
        ovr_score * 0.20 +
        cost_score * 0.25 +
        risk_score * 0.25
    )
    
    lbl, col = get_label_and_color(overall)
    
    return HealthScore(
        overall=overall,
        label=lbl,
        color=col,
        sub_scores={
            "diversification": SubScore(score=div_score, label=get_label_and_color(div_score)[0], detail="Measures asset and category spread", color=get_label_and_color(div_score)[1]),
            "overlap": SubScore(score=ovr_score, label=get_label_and_color(ovr_score)[0], detail="Checks for redundancy between funds", color=get_label_and_color(ovr_score)[1]),
            "cost_efficiency": SubScore(score=cost_score, label=get_label_and_color(cost_score)[0], detail="Evaluates direct/regular plan mix", color=get_label_and_color(cost_score)[1]),
            "risk_balance": SubScore(score=risk_score, label=get_label_and_color(risk_score)[0], detail="Assesses high vs low risk assets", color=get_label_and_color(risk_score)[1])
        }
    )

def identify_concerns(metrics: PortfolioMetrics, health_score: HealthScore) -> List[str]:
    concerns = []
    if metrics.asset_allocation.get('equity', type('obj', (object,), {'percentage': 0.0})).percentage > 80:
        concerns.append("equity_heavy: Portfolio is over 80% equity")
    if metrics.asset_allocation.get('debt', type('obj', (object,), {'percentage': 0.0})).percentage < 10:
        concerns.append("low_debt: Less than 10% in debt instruments")
    if metrics.concentration_top3_pct > 60:
        concerns.append(f"concentrated: Top 3 funds make up {metrics.concentration_top3_pct:.0f}% of portfolio")
    if health_score.sub_scores.get('overlap', SubScore(score=0,label="",detail="",color="")).score < 60:
        concerns.append("fund_overlap: Multiple funds in same categories")
    if health_score.sub_scores.get('cost_efficiency', SubScore(score=0,label="",detail="",color="")).score < 50:
        concerns.append("high_costs: Many regular plan funds, consider switching to direct")
    if not has_international_funds(metrics):
        concerns.append("no_international: No international/global fund exposure")
    if metrics.fund_count > 15:
        concerns.append(f"too_many_funds: {metrics.fund_count} funds is likely over-diversified")
    if metrics.fund_count < 3:
        concerns.append(f"too_few_funds: Only {metrics.fund_count} funds, very concentrated")
    return concerns
