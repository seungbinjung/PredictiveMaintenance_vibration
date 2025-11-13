from sqlalchemy import Column, Integer, Float, String, JSON, DateTime
from sqlalchemy.sql import func
from database import Base

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, nullable=False)        # 몇 번째 배치인지
    input_data = Column(JSON, nullable=False)         # 12000개 float 리스트 (JSON으로 저장)
    prediction = Column(Float, nullable=False)        # Colab 예측 결과
    label = Column(String, nullable=True)             # 분류 모델이면 label 저장
    created_at = Column(DateTime(timezone=True), server_default=func.now())
