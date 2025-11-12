import pandas as pd
import redis
from backend.config import REDIS_HOST, REDIS_PORT, REDIS_DB
from pathlib import Path

#실제 데이터를 생성할수 없어 학습에 사용되지 않은 데이터를 스트림 하기위해 사전에 redis에 저장하는 모듈

def parquet_to_redis(parquet_path: str): 
    # Redis 연결
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

    # 기존 데이터 초기화
    r.flushdb()

    # Parquet 로드
    df = pd.read_parquet(parquet_path)
    print(f"✅ Loaded Parquet: {df.shape} (rows, timesteps)")

    # Redis에 순차적으로 저장
    index_counter = 1  # Redis key는 1부터 시작
    for row_idx in range(df.shape[0]):
        row = df.iloc[row_idx].values  # shape: (12000,)
        for value in row:
            r.set(index_counter, float(value))
            index_counter += 1

    print(f"✅ Saved {index_counter-1} values into Redis.")

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent.parent  #프로젝트 폴더
    parquet_path = base_dir / "no_label.parquet"
    parquet_to_redis(str(parquet_path))

# 터미널에서 프로젝트 파일로 이동후 아래 커맨드 입력하여 redis에 데이터 저장
# python -m backend.services.parquet_to_redis
