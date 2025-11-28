import redis
import time
from config import REDIS_HOST, REDIS_PORT, REDIS_DB

class RedisStreamReader:
    def __init__(self):
        self.client = redis.Redis(
            host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True
        )
        self.last_id = "0-0"   # Stream 처음부터 읽기
        self.last_time = time.time()
        self.counter = 0

    def get_next_value(self):
        """
        Redis Stream에서 다음 데이터를 읽어오기
        """
        try:
            entries = self.client.xread(
                {"vibration_stream": self.last_id},
                count=1,
                block=1  # 100ms 대기 (데이터가 없으면 None 반환)
            )
        except Exception as e:
            print(f"❌ Redis XREAD Error: {e}")
            return None

        if not entries or len(entries) == 0:
            return None

        self.counter += 1
        if self.counter >= 500:  # 500개 읽을 때마다 속도 출력
            now = time.time()
            elapsed = now - self.last_time
            hz = self.counter / elapsed
            print(f"🔥 현재 Redis 스트림 수신 속도: {hz:.2f} Hz")
            self.counter = 0
            self.last_time = now

        # entries 예시: [('vibration_stream', [('1609459200000-0', {'value': '0.123'})])]
        stream, messages = entries[0]
        
        if not messages or len(messages) == 0:
            return None
            
        entry_id, data = messages[0]

        self.last_id = entry_id  # 다음 위치로 이동

        return float(data["value"])

redis_reader = RedisStreamReader()
