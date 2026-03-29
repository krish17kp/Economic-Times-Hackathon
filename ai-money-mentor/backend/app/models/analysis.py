from pydantic import BaseModel
from typing import List, Dict, Optional

class CategoryAllocation(BaseModel):
    name: str
    value: float
    percentage: float
    fund_count: int

class PortfolioMetrics(BaseModel):
    total_invested: float
    current_value: float
    absolute_return: float
    return_percentage: float
    fund_count: int
    categories: Dict[str, CategoryAllocation]
    asset_allocation: Dict[str, CategoryAllocation]
    largest_holding_pct: float
    concentration_top3_pct: float
    num_categories: int

class SubScore(BaseModel):
    score: int                              
    label: str                              
    detail: str                             
    color: str                              

class HealthScore(BaseModel):
    overall: int                            
    label: str
    color: str
    sub_scores: Dict[str, SubScore]         

class Insight(BaseModel):
    id: str
    type: str                               
    icon: str                               
    title: str
    description: str
    priority: int                           

class RebalancingAction(BaseModel):
    action: str        # 'reduce' | 'increase' | 'hold'
    asset: str
    amount: float
    detail: str
    priority: int

class FundCost(BaseModel):
    fund_name: str
    category: str
    expense_ratio: float
    annual_cost: float
    is_direct: bool

class ExpenseData(BaseModel):
    total_annual_cost: float
    potential_annual_saving: float
    fund_costs: List[FundCost]
    direct_plan_count: int
    regular_plan_count: int

class OverlapItem(BaseModel):
    type: str
    category: str
    funds: List[str]
    severity: str
    message: str

class AnalysisResponse(BaseModel):
    success: bool = True
    metrics: PortfolioMetrics
    health_score: HealthScore
    insights: List[Insight]
    plain_english_summary: str
    ai_generated: bool
    warnings: List[str] = []
    analysis_timestamp: str
    xirr: Optional[float] = None
    expense_data: Optional[ExpenseData] = None
    overlaps: List[OverlapItem] = []
    rebalancing: List[RebalancingAction] = []
