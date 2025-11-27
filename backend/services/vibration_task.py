# backend/services/vibration_task.py
import asyncio
from services.redis_reader import redis_reader
from services.stream_db import stream_db

async def vibration_loop():
    print("🔥 vibration loop started!")

    while True:
        # Redis에서 다음 값 읽기
        value = redis_reader.get_next_value()

        # 데이터가 없으면 짧게 대기 후 다시 시도
        if value is None:
            await asyncio.sleep(0.001)
            continue

        # 큐에 데이터 push (batch size 체크 등 내부 처리)
        stream_db.push_vibration(value)

        # 너무 빠르게 도는 것을 방지, CPU 점유 최소화
        await asyncio.sleep(0.00001)
