from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import asyncio
from services.sse_manager import sse_manager
import json

router = APIRouter()

async def sse_stream(queue: asyncio.Queue):
    try:
        while True:
            # queue.get()은 push될 때까지 기다림 (폴링 없음)
            value = await queue.get()
            payload = json.dumps({"value": value})
            yield f"data: {payload}\n\n"
    except asyncio.CancelledError:
        pass
    finally:
        sse_manager.unsubscribe(queue)

@router.get("/vibration")
async def stream():
    queue = sse_manager.subscribe()  # SSE 클라이언트 전용 큐
    return StreamingResponse(
        sse_stream(queue),
        media_type="text/event-stream"
    )
