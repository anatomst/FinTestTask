from datetime import date, datetime, time

from sqlalchemy import and_, func, extract
from sqlalchemy.orm import Session

from models.models import Credit, Payment, Plan, Base


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
            credit_sum = get_sum(Credit, "body", plan.period.replace(day=1), check_date, db)

            plan_performances.append({"month": plan.period,
                                      "category": plan.category.name,
                                      "plan_sum": plan.sum,
                                      "actual_sum": credit_sum,
                                      "percent": round(credit_sum / plan.sum * 100, 2) if credit_sum else 0})

        if plan.category.name == "збір":
            payments_sum = get_sum(Payment, "sum", plan.period.replace(day=1), check_date, db)

            plan_performances.append({"month": plan.period,
                                      "category": plan.category.name,
                                      "plan_sum": plan.sum,
                                      "actual_sum": payments_sum,
                                      "percent": round(payments_sum / plan.sum * 100, 2) if payments_sum else 0})

    return plan_performances


def get_sum(table: Base, sum_column: str, first_day: date, check_date: date, db: Session):
    """
    Calculates the amount of loans issued or the amount of payments for
    the period from the beginning of the plan month to the received date
    """
    return db.query(table).filter(and_(
        Payment.payment_date >= datetime.combine(first_day, time.min),
        Payment.payment_date <= datetime.combine(check_date, time.max))
    ).with_entities(func.sum(getattr(table, sum_column))).scalar() or 0
