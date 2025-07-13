from fastapi import FastAPI
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import subprocess

app = FastAPI()

# Define the Prometheus gauge metric for app health
health_score = Gauge("anomaly_score", "SmartOps app health score")

@app.get("/predict")
def predict():
    # ⚠️ Replace this with real prediction logic
    score = 0.84  # example dummy score
    health_score.set(score)
    return {"anomaly_score": score}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/restart")
def restart_smartops_app():
    try:
        subprocess.run([
            "kubectl", "rollout", "restart", "deployment/smartops-app",
            "-n", "smartops"
        ], check=True)
        return {"status": "success", "message": "smartops-app restarted."}
    except subprocess.CalledProcessError:
        return {"status": "error", "message": "Restart failed."}
