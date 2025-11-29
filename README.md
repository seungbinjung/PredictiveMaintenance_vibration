프로젝트 설명
전동기의 진동데이터를 학습하여 설비이상을 탐지한다.
센서로 들어온 데이터를 학습한 데이터 형태로 만들어 colab의 분석서버로 보낸다음 예측결과를 다시 받아와 대시보드에 출력해준다.

환경설정
redis 설치 방법


service redis stop #redis종료

PostgreSQL설치

brew install postgresql
brew services start postgresql  // 자동 실행
brew services list  //실행중인 서버리스트 확인
initdb /opt/homebrew/var/postgresql@14/data //서버 초기화 방법 (선택)
psql -d postgres //postgresDB로 이동 \du 하면 현재 존재하는 역할 확인가능
슈퍼유저 계정 등록
createuser -s postgres //터미널에서 입력

PATH등록
echo 'export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc



실행방법 
1. colab분석서버를 킨다
2. 프론트엔드를 킨다 (frontend폴더에서)
    // npm run dev
3. parquet_to_redis.py를 실행시킨다.
    // 터미널에서 프로젝트 파일로 이동후 아래 커맨드 입력하여 redis에 데이터 저장
    //python -m backend.services.parquet_to_redis
4. 백엔드서버를 킨다 (backend폴더에서)
    // uvicorn main:app --reload