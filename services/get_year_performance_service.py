from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from models.models import Plan, Dictionary, Credit, Payment, Base


def get_year_performance_service(year: int, db: Session):
    """
    Returns information about year performance for every month
    """
    result = []
    for month in range(1, 13):
        month_data = {"month": month, "year": year}
        credits_query = (
            db.query(func.count(Credit.id), func.sum(Credit.body))
            .filter(
                extract("year", Credit.issuance_date) == year,
                extract("month", Credit.issuance_date) == month,
            )
            .one()
        )
        month_data["credits_issued"] = credits_query[0]
        month_data["credit_plan_sum"] = calculate_plan_sum(db, "видача", year, month)
        month_data["credits_sum"] = credits_query[1] or 0
        month_data["credit_plan_completion"] = calculate_plan_completion(
            month_data["credits_sum"], month_data["credit_plan_sum"]
        )

        payments_query = (
            db.query(func.count(Payment.id), func.sum(Payment.sum))
            .filter(
                extract("year", Payment.payment_date) == year,
                extract("month", Payment.payment_date) == month,
            )
            .one()
        )
        month_data["payments_made"] = payments_query[0]
        month_data["payment_plan_sum"] = calculate_plan_sum(db, "збір", year, month)
        month_data["payments_sum"] = payments_query[1] or 0
        month_data["payment_plan_completion"] = calculate_plan_completion(
            month_data["payments_sum"], month_data["payment_plan_sum"]
        )

        month_data["credits_sum_percent"] = calculate_percent_of_year_sum(
            month_data["credits_sum"], year, Credit, "body", "issuance_date", db
        )
        month_data["payments_sum_percent"] = calculate_percent_of_year_sum(
            month_data["payments_sum"], year, Payment, "sum", "payment_date", db
        )

        result.append(month_data)

    return result


def calculate_plan_sum(db: Session, plan_type: str, year: int, month: int) -> float:
    """
    Calculates the amount from the plan for expenses or fees per month
    """
    sum_query = (
        db.query(func.sum(Plan.sum))
        .join(Dictionary)
        .filter(
            extract("year", Plan.period) == year,
            extract("month", Plan.period) == month,
            Dictionary.name == plan_type,
        )
        .one()
    )
    return sum_query[0] or 0


def calculate_plan_completion(current_sum: float, plan_sum: float) -> float:
    """
    Calculates the implementation of the plan for issues or fees
    """
    if plan_sum == 0:
        return 100.0
    return round((current_sum / plan_sum) * 100, 2)


def calculate_percent_of_year_sum(current_sum: float, year: int, table: Base, sum_column: str,
                                  date_column: str, db: Session) -> float:
    """
    Calculates year sum for credits and payments
    """
    year_sum_query = db.query(func.sum(getattr(table, sum_column))).filter(
        extract("year", getattr(table, date_column)) == year
    ).one()
    year_sum = year_sum_query[0] or 0
    if year_sum == 0:
        return 100.0
    return round((current_sum / year_sum) * 100, 2)
