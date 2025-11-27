import pandas as pd
import redis
import sys
from pathlib import Path

# base_dir을 sys.path에 추가하여 backend.config import 가능하게 함
base_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(base_dir))

from backend.config import REDIS_HOST, REDIS_PORT, REDIS_DB

def parquet_to_redis(parquet_path: str): 
    # Redis 연결
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

    # 기존 Stream/Key 전체 삭제
    r.flushdb()

    # Parquet 로드
    df = pd.read_parquet(parquet_path)
    print(f"✅ Loaded Parquet: {df.shape} (rows, timesteps)")

    # Stream 이름
    STREAM_KEY = "vibration_stream"

    # Redis Stream에 순차적으로 삽입
    count = 0
    for row_idx in range(df.shape[0]):
        row = df.iloc[row_idx].values  # shape: (12000,)
        for value in row:
            r.xadd(STREAM_KEY, {"value": float(value)})
            count += 1

    print(f"✅ Saved {count} values into Redis Stream: {STREAM_KEY}")

if __name__ == "__main__":
    parquet_path = base_dir / "no_label.parquet"
    parquet_to_redis(str(parquet_path))
