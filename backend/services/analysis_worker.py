# backend/services/analysis_worker.py
import asyncio
import time

from pyarrow import record_batch
from services.colab_client import send_prediction_request_async
from database import SessionLocal
from services.sse_manager import sse_manager
from models.analysis_result import AnalysisResult
from config import COLAB_URL

analysis_queue = asyncio.Queue()

LABEL_MAP = {
    0: "정상",
    1: "회전체불평형",
    2: "축정렬불량",
}

async def analysis_worker():
    print("🚀 Analysis worker started")
    while True:
        batch = await analysis_queue.get()   # 스트림에서 넘어온 batch (length=12000)

        try:
            # -------------------------
            # 1) Colab 분석 요청(비동기)
            # -------------------------
            endpoint = f"{COLAB_URL}/predict"
            result = await send_prediction_request_async(endpoint, batch)

            print(f"🤖 Analysis Result: {result}")

            # -------------------------
            # 2) PostgreSQL에 저장
            # -------------------------
            db = SessionLocal()
            record = AnalysisResult(
                input_data=batch,  # JSON 혹은 Array 로 저장 가능
                prediction=result.get("prediction"),
                probabilities=result.get("probabilities"),
                label=LABEL_MAP.get(result.get("prediction"), "Unknown")
            )
            db.add(record)
            db.commit()
            db.refresh(record)
            db.close()

            print("💾 Saved analysis result to DB.")

            await sse_manager.broadcast_result({
                "created_at": record.created_at.isoformat(),
                "label": record.label,
                "prediction": record.prediction
            })


        except Exception as e:
            print("❌ Analysis worker error:", e)
