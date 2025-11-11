import numpy as np
import requests
import pandas as pd
import sys
from pathlib import Path
from config import COLAB_URL

def dataloader(datapath):
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    EXTRA_PATHS = [
        str(PROJECT_ROOT),                      
        str(PROJECT_ROOT / "backend")        
    ]

    print("📂 Current file:", __file__)
    print("📍 PROJECT_ROOT:", PROJECT_ROOT)
    for p in EXTRA_PATHS:
        if p not in sys.path:
            sys.path.insert(0, p)

    df = pd.read_parquet(f"{PROJECT_ROOT}/{datapath}")
    return df

def datarowloader(df, rowindex):
    row = df.iloc[rowindex]
    return row

def send_prediction_request(endpoint, arr):
    arr = arr.tolist()
    res = requests.post(endpoint, json={"input": arr})
    try:
        return res.json()
    except requests.exceptions.JSONDecodeError:
        print("❌ JSONDecodeError: Flask 서버 응답이 비었거나 JSON 형식이 아닙니다.")
        print("🔎 Response text:", res.text)
        return {"success": False, "error": "Invalid JSON response from Colab"}


# 사용 예시

# data = datarowloader(dataloader("no_label.parquet"), 0)
# print(send_prediction_request(f"{COLAB_URL}/predict", data))
