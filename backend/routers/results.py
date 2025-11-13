from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.analysis_result import AnalysisResult

router = APIRouter()

@router.get("/results")
def get_results(db: Session = Depends(get_db)):
    """분석 결과 목록 조회"""
    results = db.query(AnalysisResult).order_by(AnalysisResult.id.desc()).limit(10).all()
    return results
