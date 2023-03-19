from datetime import date, datetime, time

from sqlalchemy import and_, func, extract
from sqlalchemy.orm import Session

from models.models import Credit, Payment, Plan


def get_plan_performance_service(check_date: date, db: Session):
    """
    Returns information about the execution of plans for a certain date
    """
    plans = db.query(Plan)\
        .filter(extract("year", Plan.period) == check_date.year)\
        .filter(extract("month", Plan.period) == check_date.month).all()

    plan_performances = []

    for plan in plans:
        if plan.category.name == "видача":
            credit_sum = db.query(Credit).filter(and_(
                Credit.issuance_date >= datetime.combine(plan.period.replace(day=1), time.min),
                Credit.issuance_date <= datetime.combine(check_date, time.max))
            ).with_entities(func.sum(Credit.body)).scalar() or 0

            plan_performances.append({"month": plan.period,
                                      "category": plan.category.name,
                                      "plan_sum": plan.sum,
                                      "actual_sum": credit_sum,
                                      "percent": round(credit_sum / plan.sum * 100, 2) if credit_sum else 0})

        if plan.category.name == "збір":
            payments_sum = db.query(Payment).filter(and_(
                Payment.payment_date >= datetime.combine(plan.period.replace(day=1), time.min),
                Payment.payment_date <= datetime.combine(check_date, time.max))
            ).with_entities(func.sum(Payment.sum)).scalar() or 0

            plan_performances.append({"month": plan.period,
                                      "category": plan.category.name,
                                      "plan_sum": plan.sum,
                                      "actual_sum": payments_sum,
                                      "percent": round(payments_sum / plan.sum * 100, 2) if payments_sum else 0})

    return plan_performances
