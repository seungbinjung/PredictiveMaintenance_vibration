from sqlalchemy import Column, Integer, Float, String, JSON, DateTime
from sqlalchemy.sql import func
from database import Base

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, nullable=False)
    input_data = Column(JSON, nullable=False)
    prediction = Column(Float, nullable=False)
    probabilities = Column(JSON, nullable=True)   # ★ 추가됨
    label = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
