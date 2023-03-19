from fastapi import APIRouter, UploadFile, File
from starlette.responses import JSONResponse

from models.db_connection import engine
from models.models import User, Credit, Dictionary, Plan, Payment, Base
from services.upload_service import TABLES, upload_users_csv_to_db, upload_credits_csv_to_db, \
    upload_dictionaries_csv_to_db, \
    upload_plans_csv_to_db, upload_payments_csv_to_db
from sqlalchemy import MetaData

meta = MetaData()

upload_csv_router = APIRouter(tags=["Preparation"])


@upload_csv_router.post("/upload_file/{table_name}")
def upload_csv_file(table_name: str, file: UploadFile = File(...)):
    model = TABLES.get(table_name)
    if not model:
        return JSONResponse(content={"error": "Invalid table name"})

    if model == User:
        upload_users_csv_to_db(file)
    if model == Credit:
        upload_credits_csv_to_db(file)
    if model == Dictionary:
        upload_dictionaries_csv_to_db(file)
    if model == Plan:
        upload_plans_csv_to_db(file)
    if model == Payment:
        upload_payments_csv_to_db(file)

    return JSONResponse(content={"info": "Uploaded!"})


@upload_csv_router.post("/db/clean")
def clean_all_data():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return JSONResponse(content={"info": "Your db is empty!"})
