from datetime import date
from typing import List

from fastapi import FastAPI, Depends, UploadFile, File
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from api.upload_csv import upload_csv_router
from entities.credits import UserCreditsResponse
from entities.plans import PlanPerformance
from models.db_connection import get_session
from services.plan_performance import get_plan_performance_service
from services.upload_exel_with_plans import upload_plans_from_excel
from services.user_credits import get_user, get_credits_info

app = FastAPI()

app.include_router(upload_csv_router)


@app.get("/user_credits/{user_id}", response_model=UserCreditsResponse)
def get_user_credits(user_id: int, db: Session = Depends(get_session)):
    user = get_user(user_id, db)
    if user is None:
        return JSONResponse(content={"error": "user doesn't exist!"})

    credits_info = get_credits_info(user, db)

    return {"user_id": user.id,
            "login": user.login,
            "registration_date": user.registration_date,
            "credits_info": credits_info}


@app.post("/upload_plans")
def upload_plans(file: UploadFile = File(...), db: Session = Depends(get_session)):
    plans = upload_plans_from_excel(file, db)
    if plans:
        return {"info": "plans added!"}


@app.get("/plans_performance", response_model=List[PlanPerformance])
def get_plans_performance(check_date: date, db: Session = Depends(get_session)):
    result = get_plan_performance_service(check_date, db)
    return result

