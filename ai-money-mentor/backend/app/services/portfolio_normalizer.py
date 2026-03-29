from app.models.portfolio import Portfolio, Fund
from typing import List, Dict, Any

def normalize_portfolio(raw_records: List[Dict[str, Any]], source: str, raw_text: str = None) -> Portfolio:
    funds = []
    for r in raw_records:
        if 'fund_name' not in r:
            continue
            
        purchase = r.get('purchase_value') or 0.0
        current = r.get('current_value') or 0.0
        
        fund = Fund(
            fund_name=r['fund_name'],
            folio=r.get('folio'),
            category=r.get('category', 'Uncategorized'),
            units=r.get('units'),
            nav=r.get('nav'),
            purchase_value=purchase,
            current_value=current,
            purchase_date=r.get('purchase_date')
        )
        funds.append(fund)
        
    return Portfolio(
        investor_name="Investor",
        funds=funds,
        fund_count=len(funds),
        parse_confidence="high" if len(funds) > 0 else "low",
        source=source
    )
