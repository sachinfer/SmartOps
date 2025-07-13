from fastapi import FastAPI
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

app = FastAPI()

# Define the Prometheus gauge metric
anomaly_score = Gauge("anomaly_score", "SmartOps anomaly score")

@app.get("/predict")
def predict():
    # ⚠️ Replace this with real prediction logic
    score = 0.84  # example dummy score
    anomaly_score.set(score)
    return {"anomaly_score": score}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
