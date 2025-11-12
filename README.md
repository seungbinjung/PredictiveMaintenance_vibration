프로젝트 설명
전동기의 진동데이터를 학습하여 설비이상을 탐지한다.
센서로 들어온 데이터를 학습한 데이터 형태로 만들어 colab의 분석서버로 보낸다음 예측결과를 다시 받아와 대시보드에 출력해준다.

실행방법 
1. colab분석서버를 킨다
2. 백엔드서버를 킨다
3. parquet_to_redis.py를 실행시킨다.
    # 터미널에서 프로젝트 파일로 이동후 아래 커맨드 입력하여 redis에 데이터 저장
    # python -m backend.services.parquet_to_redis
4. 터미널에 curl -X POST "http://127.0.0.1:8000/data/infinitepush" 를 입력한다