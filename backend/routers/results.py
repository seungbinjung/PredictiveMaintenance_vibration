from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.analysis_result import AnalysisResult
from database import SessionLocal


router = APIRouter()

@router.get("/results")
def get_results(db: Session = Depends(get_db)):
    """분석 결과 목록 조회"""
    results = db.query(AnalysisResult).order_by(AnalysisResult.id.desc()).limit(10).all()
    return results

@router.get("/latest")
def get_latest_result():
    """가장 최신 분석 결과 반환"""
    db: Session = SessionLocal()
    result = (
        db.query(AnalysisResult)
        .order_by(AnalysisResult.created_at.desc())
        .first()
    )
    db.close()

    if not result:
        raise HTTPException(404, "No analysis results found")

    return {
        "id": result.id,
        "input_length": len(result.input_data),
        "prediction": result.prediction,
        "label": result.label,
        "created_at": result.created_at,
    }

@router.get("/recent")
def get_recent_results():
    db = SessionLocal()
    results = (
        db.query(AnalysisResult)
        .order_by(AnalysisResult.created_at.desc())
        .limit(10)
        .all()
    )
    db.close()
    return [
        {
            "id": r.id,
            "prediction": r.prediction,
            "label": r.label,
            "timestamp": r.created_at,
        }
        for r in results
    ]