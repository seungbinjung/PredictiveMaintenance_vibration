from fastapi import APIRouter
from services.stream_db import stream_db
from services.redis_reader import redis_reader
import random

router = APIRouter()

@router.post("/push")
def push_redis_vibration():
    """redis에 저장된 진동값을 조회해서 두 큐 중 활성 큐로 푸시"""
    value = redis_reader.get_next_value()
    if value is None:
        return {"message": "No more data in Redis."}
    stream_db.push_vibration(value)
    return stream_db.get_queue_status()

@router.post("/infinitepush")
def push_infinite():
    """push_redis_vibration 함수 무한 반복 실행"""
    while True:
        push_redis_vibration()
    done
@router.get("/status")
def get_status():
    """두 큐의 상태 확인"""
    return stream_db.get_queue_status()

@router.delete("/reset")
def reset_queues():
    """두 큐 초기화"""
    stream_db.clear_all()
    return {"message": "Queues cleared"}
