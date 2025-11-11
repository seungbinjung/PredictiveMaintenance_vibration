from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.sensor import SensorData

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/save")
def save_data(value: float, status: str, db: Session = Depends(get_db)):
    data = SensorData(value=value, status=status)
    db.add(data)
    db.commit()
    return {"result": "saved"}
