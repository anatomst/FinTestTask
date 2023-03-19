from datetime import date
from typing import Optional

from pydantic import BaseModel


class PlanPerformance(BaseModel):
    month: date
    category: str
    plan_sum: float
    actual_sum: float
    percent: float


class MonthPerformance(BaseModel):
    month: int
    year: int
    credits_issued: int
    credit_plan_sum: Optional[float]
    credits_sum: float
    credit_plan_completion: Optional[float]
    payments_made: int
    payment_plan_sum: Optional[float]
    payments_sum: float
    payment_plan_completion: Optional[float]
    credits_sum_percent: Optional[float]
    payments_sum_percent: Optional[float]
