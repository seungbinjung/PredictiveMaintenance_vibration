import redis
from config import REDIS_HOST, REDIS_PORT, REDIS_DB

class RedisReader:
    def __init__(self):
        self.client = redis.Redis(
            host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True
        )
        self.current_index = 1  # 첫 번째 데이터부터 시작

    def get_next_value(self):
        """Redis에서 다음 인덱스의 데이터를 읽어서 반환"""
        value = self.client.get(self.current_index)
        if value is None:
            print("⚠️ No more data in Redis.")
            return None
        self.current_index += 1
        return float(value)

    def reset_index(self):
        """데이터 처음부터 다시 읽기"""
        self.current_index = 1

redis_reader = RedisReader()
