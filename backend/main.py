from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import analysis, data

app = FastAPI(title="Vibration Fault Prediction API")

# CORS 설정 (프론트엔드 접근 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 필요 시 도메인 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(analysis.router, prefix="/analysis")
app.include_router(data.router, prefix="/data")

@app.get("/")
def root():
    return {"status": "Backend is running!"}

# 실행방법
# uvicorn main:app --reload