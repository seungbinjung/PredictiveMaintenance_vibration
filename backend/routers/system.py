from fastapi import APIRouter
import redis
import requests
from database import engine
from config import REDIS_HOST, REDIS_PORT, REDIS_DB, COLAB_URL

router = APIRouter()

@router.get("/system/status")
def system_status():
    status = {}

    # FastAPI는 항상 True
    status["fastapi"] = True

    # Redis 상태 체크
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        r.ping()
        status["redis"] = True
    except:
        status["redis"] = False

    # PostgreSQL 체크
    try:
        conn = engine.connect()
        conn.close()
        status["postgresql"] = True
    except:
        status["postgresql"] = False

    # Colab 분석 서버 체크
    try:
        res = requests.get(f"{COLAB_URL}/", timeout=5)
        status["colab"] = (res.status_code != 200)
    except:
        status["colab"] = True

    return status
