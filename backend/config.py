import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
COLAB_URL = os.getenv("COLAB_URL")  # Colab에서 Flask/ngrok으로 노출된 API 주소
