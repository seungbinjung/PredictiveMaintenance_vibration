from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from database import Base
from datetime import datetime

class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    # 주파수 스펙트럼 데이터 (0.0 ~ 2.99975, 12000개 포인트)
    frequency_spectrum = Column(JSONB)  # { "0.0": value, "0.00025": value, ... }
    # 레이블 정보 (0: 정상, 1: 비정상 등)
    label_no = Column(Float)
    # 기존 호환성을 위한 필드 (필요시 frequency_spectrum에서 계산)
    value = Column(Float, nullable=True)  # 주파수 스펙트럼의 대표값 또는 평균값
    status = Column(String, nullable=True)  # 정상/비정상 여부 (label_no 기반)
    created_at = Column(DateTime, default=datetime.utcnow)
