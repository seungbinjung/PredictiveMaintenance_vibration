# backend/services/analysis_worker.py
import asyncio
import time
from services.colab_client import send_prediction_request_async
from database import SessionLocal
from models.analysis_result import AnalysisResult
from config import COLAB_URL

analysis_queue = asyncio.Queue()

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
                batch_id=int(time.time()),
                input_data=batch,  # JSON 혹은 Array 로 저장 가능
                prediction=result.get("prediction"),
                probabilities=result.get("probabilities")
            )
            db.add(record)
            db.commit()
            db.close()

            print("💾 Saved analysis result to DB.")

        except Exception as e:
            print("❌ Analysis worker error:", e)
