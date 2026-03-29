from app.models.portfolio import Portfolio
from app.models.analysis import PortfolioMetrics, CategoryAllocation

def calculate_portfolio_metrics(portfolio: Portfolio) -> PortfolioMetrics:
    total_invested = sum(f.purchase_value for f in portfolio.funds)
    current_value = sum(f.current_value for f in portfolio.funds)
    absolute_return = current_value - total_invested
    return_pct = (absolute_return / total_invested * 100) if total_invested > 0 else 0.0
    
    categories = {}
    asset_allocation = {
        'equity': {'name': 'Equity', 'value': 0.0, 'percentage': 0.0, 'fund_count': 0},
        'debt': {'name': 'Debt', 'value': 0.0, 'percentage': 0.0, 'fund_count': 0},
        'hybrid': {'name': 'Hybrid', 'value': 0.0, 'percentage': 0.0, 'fund_count': 0},
        'other': {'name': 'Other', 'value': 0.0, 'percentage': 0.0, 'fund_count': 0}
    }
    
    for fund in portfolio.funds:
        fund.absolute_return = fund.current_value - fund.purchase_value
        fund.return_percentage = (fund.absolute_return / fund.purchase_value * 100) if fund.purchase_value > 0 else 0.0
        fund.allocation_percentage = (fund.current_value / current_value * 100) if current_value > 0 else 0.0
        
        cat = fund.category
        if cat not in categories:
            categories[cat] = {'name': cat, 'value': 0.0, 'percentage': 0.0, 'fund_count': 0}
        categories[cat]['value'] += fund.current_value
        categories[cat]['fund_count'] += 1
        
        asset = fund.asset_type if hasattr(fund, 'asset_type') and fund.asset_type else 'equity'
        if asset not in asset_allocation:
            asset = 'other'
        asset_allocation[asset]['value'] += fund.current_value
        asset_allocation[asset]['fund_count'] += 1
        
    for cat in categories.values():
        cat['percentage'] = (cat['value'] / current_value * 100) if current_value > 0 else 0.0
        
    for asset in asset_allocation.values():
        asset['percentage'] = (asset['value'] / current_value * 100) if current_value > 0 else 0.0
        
    categories_formatted = {k: CategoryAllocation(**v) for k, v in categories.items()}
    asset_allocation_formatted = {k: CategoryAllocation(**v) for k, v in asset_allocation.items()}
    
    sorted_funds = sorted(portfolio.funds, key=lambda f: f.current_value, reverse=True)
    largest_holding_pct = (sorted_funds[0].current_value / current_value * 100) if sorted_funds and current_value > 0 else 0.0
    top3_val = sum(f.current_value for f in sorted_funds[:3])
    concentration_top3_pct = (top3_val / current_value * 100) if current_value > 0 else 0.0
    
    return PortfolioMetrics(
        total_invested=total_invested,
        current_value=current_value,
        absolute_return=absolute_return,
        return_percentage=return_pct,
        fund_count=len(portfolio.funds),
        categories=categories_formatted,
        asset_allocation=asset_allocation_formatted,
        largest_holding_pct=largest_holding_pct,
        concentration_top3_pct=concentration_top3_pct,
        num_categories=len(categories)
    )
