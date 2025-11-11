from fastapi import APIRouter
from services.stream_db import stream_db
import random

router = APIRouter()

@router.post("/push")
def push_random_vibration():
    """랜덤 진동값을 두 큐 중 활성 큐로 푸시"""
    value = round(random.uniform(-1, 1), 6)
    stream_db.push_vibration(value)
    return stream_db.get_queue_status()

@router.post("/infinitepush")
def push_infinite():
    """push_random_vibration 함수 무한 반복 실행"""
    while True:
        push_random_vibration()
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
