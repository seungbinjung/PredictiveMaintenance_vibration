import redis
from config import REDIS_HOST, REDIS_PORT, REDIS_DB

class RedisStreamReader:
    def __init__(self):
        self.client = redis.Redis(
            host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True
        )
        self.last_id = "0-0"   # Stream 처음부터 읽기

    def get_next_value(self):
        """
        Redis Stream에서 다음 데이터를 읽어오기
        """
        try:
            entries = self.client.xread(
                {"vibration_stream": self.last_id},
                count=1,
                block=0  # 데이터 없으면 기다림
            )
        except Exception as e:
            print(f"❌ Redis XREAD Error: {e}")
            return None

        if not entries:
            return None

        # entries 예시: [('vibration_stream', [('1609459200000-0', {'value': '0.123'})])]
        stream, messages = entries[0]
        entry_id, data = messages[0]

        self.last_id = entry_id  # 다음 위치로 이동

        return float(data["value"])

redis_reader = RedisStreamReader()
