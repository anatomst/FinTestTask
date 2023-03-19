import io

import pandas as pd
from fastapi import HTTPException
from sqlalchemy import and_

from models.models import Dictionary, Plan


def upload_plans_from_excel(file, db):
    """
    Checks the information from the excel file and inserts the data into the database
    """
    df = pd.read_excel(io.BytesIO(file.file.read()))
    plans = []
    for i, row in df.iterrows():
        period = row["місяць плану"]
        category_name = row["назва категорії плану"]
        amount = row["сума"]

        category = db.query(Dictionary).filter(Dictionary.name == category_name).first()

        if not category:
            raise HTTPException(status_code=400, detail=f"Check category for period {period} - {category_name}!")

        if db.query(Plan).filter(and_(Plan.category == category, Plan.period == period)).first():
            raise HTTPException(status_code=400, detail=f"Plan: category={category_name}, period={period} exists!")

        if period.day != 1:
            raise HTTPException(status_code=400, detail=f"Period day should be first day of month!")

        if pd.isna(amount):
            raise HTTPException(status_code=400,
                                detail=f"Sum column of category {category_name}, period {period} is empty!")

        plan = Plan(period=period, sum=amount, category_id=category.id)
        db.add(plan)
        plans.append(plan)
    db.commit()
    return plans
