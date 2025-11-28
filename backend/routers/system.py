from fastapi import APIRouter
import redis
from database import engine
from config import REDIS_HOST, REDIS_PORT, REDIS_DB

router = APIRouter()

@router.get("/system/status")
def system_status():
    # FastAPI always running if you reached this endpoint
    api_ok = True

    # Redis connection test
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        r.ping()
        redis_ok = True
    except:
        redis_ok = False

    # Postgres connection test
    try:
        conn = engine.connect()
        conn.close()
        db_ok = True
    except:
        db_ok = False

    # Colab 테스트는 단순 예시
    colab_ok = True

    return {
        "fastapi": api_ok,
        "redis": redis_ok,
        "postgresql": db_ok,
        "colab": colab_ok,
    }
