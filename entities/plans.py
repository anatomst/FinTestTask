from datetime import date

from pydantic import BaseModel


class PlanPerformance(BaseModel):
    month: date
    category: str
    plan_sum: float
    actual_sum: float
    percent: float
