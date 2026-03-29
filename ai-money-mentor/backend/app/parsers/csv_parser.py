import pandas as pd
from typing import Dict, Any, List
from app.parsers.parser_utils import clean_number

COLUMN_MAPPINGS = {
    'fund_name': ['fund_name', 'scheme_name', 'fund', 'scheme', 'mutual_fund', 'name'],
    'folio': ['folio', 'folio_no', 'folio_number'],
    'units': ['units', 'unit_balance', 'balance_units', 'quantity'],
    'purchase_value': ['purchase_value', 'cost_value', 'cost', 'invested', 'investment_value', 'amount_invested'],
    'current_value': ['current_value', 'market_value', 'value', 'valuation', 'nav_value'],
    'nav': ['nav', 'current_nav', 'latest_nav'],
    'category': ['category', 'fund_category', 'type', 'fund_type'],
    'purchase_date': ['purchase_date', 'date', 'investment_date', 'start_date']
}

def normalize_column_name(col: str) -> str:
    col_lower = str(col).strip().lower().replace(' ', '_')
    for std_name, aliases in COLUMN_MAPPINGS.items():
        if col_lower in aliases:
            return std_name
    return col_lower

def parse_csv(file_path: str) -> List[Dict[str, Any]]:
    df = pd.read_csv(file_path)
    df.columns = [normalize_column_name(c) for c in df.columns]
    
    records = []
    for _, row in df.iterrows():
        record = {}
        for col in df.columns:
            val = row[col]
            if pd.isna(val):
                continue
            
            if col in ['units', 'purchase_value', 'current_value', 'nav']:
                record[col] = clean_number(str(val))
            else:
                record[col] = str(val).strip() if isinstance(val, str) else val
                
        if 'fund_name' in record and ('purchase_value' in record or 'current_value' in record):
            records.append(record)
            
    return records
