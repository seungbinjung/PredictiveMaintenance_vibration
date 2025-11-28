# colab_api.py
from fastapi import FastAPI
from pydantic import BaseModel
import tensorflow as tf
import numpy as np

model = tf.keras.models.load_model("best_model.keras")

app = FastAPI()

class PredictInput(BaseModel):
    input: list

@app.post("/predict")
async def predict(data: PredictInput):
    x = np.array(data.input).reshape(1,12000,1)
    pred = model.predict(x)
    idx = int(np.argmax(pred, axis=1)[0])
    return {
        "success": True,
        "prediction": idx,
        "probabilities": pred[0].tolist()
    }
