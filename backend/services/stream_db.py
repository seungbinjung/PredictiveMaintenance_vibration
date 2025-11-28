import redis
import json
import time
from config import REDIS_HOST, REDIS_PORT, REDIS_DB
from services.colab_client import send_prediction_request_async
from config import COLAB_URL
from database import SessionLocal
from models.analysis_result import AnalysisResult
from services.analysis_worker import analysis_queue
#스트림되는 데이터를 큐에 저장해서 분석서버에 보내기 적합한 형태 (1,12000)로 만든 후 request보내는 모듈

BATCH_SIZE = 12000

class StreamDB:
    def __init__(self):
        self.client = redis.Redis(
            host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True
        )
        self.active_queue = "queue_1"   # 현재 데이터가 쌓이는 큐 이름
        self.inactive_queue = "queue_2" # 대기 큐

    def push_vibration(self, value: float):
        """새로운 진동값을 active 큐에 추가"""
        active_len = self.client.llen(self.active_queue)
        inactive_len = self.client.llen(self.inactive_queue)

        # 현재 active 큐가 가득 찼을 때
        if active_len >= BATCH_SIZE:

            # active 큐가 이미 가득 찼음을 의미하므로 분석 서버로 전송
            batch = self.client.lrange(self.active_queue, 0, -1)
            batch = [float(x) for x in batch]
            self.send_to_analysis(batch)

            # 다음 데이터를 inactive 큐에 넣기 시작
            self.client.rpush(self.inactive_queue, value)

            # active 큐 초기화 및 교대
            self.client.delete(self.active_queue)
            self._swap_queues()

        else:
            # 아직 active 큐에 여유가 있다면 계속 추가
            self.client.rpush(self.active_queue, value)

    def _swap_queues(self):
        """두 큐 이름 교환"""
        self.active_queue, self.inactive_queue = self.inactive_queue, self.active_queue

    def send_to_analysis(self, data):
        """가득 찬 큐의 배치를 분석 대기열에 넣기 (non-blocking)"""
        try:
             # AI 분석 워커에게 배치 전달 (즉시 반환됨)
            analysis_queue.put_nowait(data)
            print(f"📦 Batch queued for analysis ({len(data)} pts)")

        except Exception as e:
            print(f"❌ Failed to send batch to analysis: {e}")

    def get_queue_status(self):
        """현재 큐 상태 확인용"""
        return {
            "active_queue": self.active_queue,
            "active_len": self.client.llen(self.active_queue),
            "inactive_queue": self.inactive_queue,
            "inactive_len": self.client.llen(self.inactive_queue),
        }

    def clear_all(self):
        """두 큐 전부 초기화"""
        self.client.delete("queue_1")
        self.client.delete("queue_2")
        self.active_queue = "queue_1"
        self.inactive_queue = "queue_2"

# 인스턴스 생성
stream_db = StreamDB()
