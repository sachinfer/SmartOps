from fastapi import FastAPI, Request
from pydantic import BaseModel
import numpy as np
import joblib

app = FastAPI()
model = joblib.load("/app/app/model/isolation_forest.pkl")

class InputData(BaseModel):
    cpu: float
    memory: float

@app.post("/predict")
def predict_anomaly(data: InputData):
    features = np.array([[data.cpu, data.memory]])
    prediction = model.predict(features)
    is_anomaly = bool(prediction[0] == -1)
    return {
        "anomaly": is_anomaly,
        "message": "Anomaly detected" if is_anomaly else "Normal"
    }

# Unit test for FastAPI endpoint
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Test code
from fastapi.testclient import TestClient

def test_predict():
    client = TestClient(app)
    response = client.post("/predict", json={"metrics": [0.1, 0.2, 0.3, 0.4]})
    assert response.status_code == 200
    assert "anomaly" in response.json()
