from fastapi import APIRouter, HTTPException
import requests
from config import COLAB_URL
from services.colab_client import send_prediction_request_async

router = APIRouter()

@router.post("/predict")
def predict_from_colab(data: dict):
    try:

        result = send_prediction_request_async(f"{COLAB_URL}/predict", input_data)
        print(result)
        return {
            "source": "colab",
            "success": result.get("success", False),
            "probabilities": result.get("probabilities", None),
            "prediction": result.get("prediction", None)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))