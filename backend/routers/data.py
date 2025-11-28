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

@router.get("/stream/status")
def get_stream_status():
    """Redis Stream 상태 확인"""
    try:
        client = redis_reader.client
        stream_info = client.xinfo_stream("vibration_stream")
        length = client.xlen("vibration_stream")
        return {
            "stream_exists": True,
            "length": length,
            "info": stream_info if stream_info else None
        }
    except Exception as e:
        return {
            "stream_exists": False,
            "error": str(e)
        }

@router.delete("/reset")
def reset_queues():
    stream_db.clear_all()
    return {"message": "Queues cleared"}
