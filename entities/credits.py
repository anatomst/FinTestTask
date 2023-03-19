from datetime import date
from typing import List, Union
from pydantic import BaseModel


class ClosedCreditInfo(BaseModel):
    issuance_date: date
    closed: bool = True
    return_date: date
    body: float
    percent: float
    payments_sum: float


class OpenCreditInfo(BaseModel):
    issuance_date: date
    closed: bool = False
    return_date: date
    days_overdue: int
    body: float
    percent: float
    body_payments_sum: float
    percent_payments_sum: float


class UserCreditsResponse(BaseModel):
    user_id: int
    login: str
    registration_date: date
    credits_info: List[Union[OpenCreditInfo, ClosedCreditInfo]]
