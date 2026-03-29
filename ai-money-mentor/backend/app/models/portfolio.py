from pydantic import BaseModel
from typing import List, Optional

class Fund(BaseModel):
    fund_name: str                          
    folio: Optional[str] = None             
    category: str = "Uncategorized"         
    asset_type: str = "equity"              
    units: Optional[float] = None           
    nav: Optional[float] = None             
    purchase_value: float                   
    current_value: float                    
    purchase_date: Optional[str] = None     
    absolute_return: Optional[float] = None 
    return_percentage: Optional[float] = None  
    allocation_percentage: Optional[float] = None  

class Portfolio(BaseModel):
    investor_name: str = "Investor"
    statement_date: Optional[str] = None
    funds: List[Fund]
    fund_count: int = 0
    parse_confidence: str = "high"          
    source: str = "csv"                     
