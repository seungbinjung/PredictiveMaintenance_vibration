import redis
import json
from config import REDIS_HOST, REDIS_PORT, REDIS_DB
from services.colab_client import send_prediction_request
from config import COLAB_URL

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
            # 다음 데이터를 inactive 큐에 넣기 시작
            self.client.rpush(self.inactive_queue, value)

            # inactive 큐에 첫 데이터가 들어갔다는 것은,
            # active 큐가 이미 가득 찼음을 의미하므로 분석 서버로 전송
            batch = self.client.lrange(self.active_queue, 0, -1)
            batch = [float(x) for x in batch]
            self.send_to_analysis(batch)

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
        """가득 찬 큐의 데이터를 Colab 분석 서버로 전송"""
        try:
            response = send_prediction_request(f"{COLAB_URL}/predict", data)
            print(f"✅ Sent batch ({len(data)} pts) to analysis. Result: {response}")
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
