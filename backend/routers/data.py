from fastapi import APIRouter
from services.stream_db import stream_db
from services.redis_reader import redis_reader
import asyncio

router = APIRouter()

# 루프 동작 여부 체크
vibration_task = None        

@router.get("/status")
def get_status():
    return stream_db.get_queue_status()

@router.delete("/reset")
def reset_queues():
    stream_db.clear_all()
    return {"message": "Queues cleared"}
