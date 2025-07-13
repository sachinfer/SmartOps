from fastapi import FastAPI
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import subprocess

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

@app.post("/restart")
def restart_pod():
    try:
        # This assumes kubectl is available in the container and has permissions
        subprocess.run([
            "kubectl", "rollout", "restart", "deployment/smartops-anomaly-deployment", "-n", "smartops"
        ], check=True)
        return {"message": "Pod restart triggered!"}
    except Exception as e:
        return {"message": f"Error: {e}"}
