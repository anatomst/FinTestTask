import pandas as pd

from models.db_connection import engine
from models.models import User, Credit, Payment, Plan, Dictionary

TABLES = {
    "users": User,
    "credits": Credit,
    "payments": Payment,
    "plans": Plan,
    "dictionary": Dictionary,
}


def upload_users_csv_to_db(file):
    df = pd.read_csv(file.file, delimiter='\t')
    df['registration_date'] = pd.to_datetime(df['registration_date']).dt.strftime('%Y-%m-%d')
    df.to_sql(name='users', con=engine, if_exists='append', index=False)


def upload_credits_csv_to_db(file):
    df = pd.read_csv(file.file, delimiter='\t')
    df['issuance_date'] = pd.to_datetime(df['issuance_date']).dt.strftime('%Y-%m-%d')
    df['return_date'] = pd.to_datetime(df['return_date']).dt.strftime('%Y-%m-%d')
    df['actual_return_date'] = pd.to_datetime(df['actual_return_date']).dt.strftime('%Y-%m-%d')
    df.to_sql(name='credits', con=engine, if_exists='append', index=False)


def upload_dictionaries_csv_to_db(file):
    df = pd.read_csv(file.file, delimiter='\t')
    df.to_sql(name='dictionary', con=engine, if_exists='append', index=False)


def upload_plans_csv_to_db(file):
    df = pd.read_csv(file.file, delimiter='\t')
    df['period'] = pd.to_datetime(df['period']).dt.strftime('%Y-%m-%d')
    df.to_sql(name='plans', con=engine, if_exists='append', index=False)


def upload_payments_csv_to_db(file):
    df = pd.read_csv(file.file, delimiter='\t')
    df['payment_date'] = pd.to_datetime(df['payment_date']).dt.strftime('%Y-%m-%d')
    df.to_sql(name='payments', con=engine, if_exists='append', index=False)
