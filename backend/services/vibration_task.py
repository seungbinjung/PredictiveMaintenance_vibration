# backend/services/vibration_task.py

import asyncio
from services.redis_reader import redis_reader
from services.stream_db import stream_db
from services.sse_manager import sse_manager

DOWNSAMPLE_RATE = 5   # 550Hz → 110Hz로 감소 (=550/5)

counter = 0

async def vibration_loop():
    global counter
    while True:
        value = redis_reader.get_next_value()

        if value is None:
            await asyncio.sleep(0.001)
            continue
        
        print("BROADCAST VALUE:", value)

        # DB에는 원본(550Hz)을 그대로 저장
        stream_db.push_vibration(value)

        # SSE는 downsample해서 전송
        counter += 1
        if counter % DOWNSAMPLE_RATE == 0:
            await sse_manager.broadcast(value)

        await asyncio.sleep(0.0001)
