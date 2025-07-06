from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib

app = FastAPI()
model = joblib.load("model/isolation_forest.pkl")

class InputData(BaseModel):
    cpu_usage: float
    memory_usage: float

@app.post("/predict")
def predict_anomaly(data: InputData):
    features = np.array([[data.cpu_usage, data.memory_usage]])
    prediction = model.predict(features)
    is_anomaly = bool(prediction[0] == -1)  # Cast to native Python bool
    return {
        "anomaly": is_anomaly,
        "message": "Anomaly detected" if is_anomaly else "Normal"
    }
