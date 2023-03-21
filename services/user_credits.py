from datetime import datetime

from sqlalchemy.orm import Session

from models.models import User, Payment


def get_user(user_id: int, db: Session):
    return db.query(User).filter(User.id == user_id).first()


def get_credits_info(user: User, db: Session):
    """
    Collects information about all user credits
    """
    credits_info = []
    for credit in user.credits:

        credit_info = {"issuance_date": credit.issuance_date,
                       "is_closed": True if credit.actual_return_date else False,
                       "body": credit.body,
                       "percent": credit.percent
                       }

        if credit.actual_return_date is not None:
            credit_info["return_date"] = credit.actual_return_date
            credit_info["payments_sum"] = sum(payment.sum for payment in credit.payments)
        else:
            credit_info["return_date"] = credit.return_date

            if credit.return_date < datetime.now().date():
                credit_info["days_overdue"] = (datetime.now().date() - credit.return_date).days
            else:
                credit_info["days_overdue"] = 0

            credit_body_payments = db.query(Payment) \
                .filter(Payment.credit_id == credit.id, Payment.type_id == 1).all()

            credit_info["body_payments_sum"] = sum(payment.sum for payment in credit_body_payments)

            credit_percent_payments = db.query(Payment) \
                .filter(Payment.credit_id == credit.id, Payment.type_id == 2).all()

            credit_info["percent_payments_sum"] = sum(payment.sum for payment in credit_percent_payments)

        credits_info.append(credit_info)

    return credits_info
