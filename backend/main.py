from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import analysis, data, results, sse, system
from database import Base, engine
from models.analysis_result import AnalysisResult
from services.vibration_task import vibration_loop
from services.analysis_worker import analysis_worker
import asyncio

app = FastAPI(title="Vibration Fault Prediction API")

# CORS 설정 (프론트엔드 접근 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 필요 시 도메인 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ DB 자동 초기화 로직
# -------------------------------
@app.on_event("startup")
def init_database():
    with engine.connect() as connection:
        if not engine.dialect.has_table(connection, "analysis_results"):
            print("🧩 analysis_results 테이블이 존재하지 않습니다. 새로 생성합니다...")
            Base.metadata.create_all(bind=engine)
            print("✅ 데이터베이스 테이블 생성 완료.")
        else:
            print("📦 analysis_results 테이블이 이미 존재합니다. 스킵합니다.")

# -------------------------------
# 🚀 Redis Stream 소비 루프 시작
# -------------------------------
@app.on_event("startup")
async def start_vibration_consumer():
    asyncio.create_task(vibration_loop())   # 중요 ★
    print("🚀 vibration background task scheduled.")

@app.on_event("startup")
async def start_workers():
    asyncio.create_task(analysis_worker())
    asyncio.create_task(vibration_loop())


# 라우터 등록
app.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
app.include_router(data.router, prefix="/data", tags=["data"])
app.include_router(results.router, prefix="/results", tags=["results"])
app.include_router(sse.router, prefix="/sse", tags=["sse"])
app.include_router(system.router, tags=["system"])

@app.get("/")
def root():
    return {"status": "Backend is running!"}

# 실행방법
# uvicorn main:app --reload