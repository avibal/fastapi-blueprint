from fastapi import APIRouter, Depends
from app.core.config import settings
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.models.users import Users

router = APIRouter()

# Root endpoint
@router.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Azure Service"}

@router.get("/health", tags=[tag.name for tag in settings.endpoints["health_check"].tags])
def health_check():
    return {"status": "healthy"}


@router.get("/api/data")
def get_users(db: Session = Depends(get_db)):
    try:
        # Query all records from sample_data table
        data = db.query(Users).all()
        return {"data": [{"id": item.id, "first_name": item.first_name, "email": item.email} for item in data]}
    except Exception as e:
        return {"error": str(e)}