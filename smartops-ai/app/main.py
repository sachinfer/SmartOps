from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib
import threading
import time
import requests
from kubernetes import client, config
import os

app = FastAPI()
model = joblib.load("model/isolation_forest.pkl")

# Settings
NAMESPACE = os.getenv("SMARTOPS_NAMESPACE", "smartops")
TARGET_LABEL = "app=smartops-app"
PREDICT_URL = "http://localhost:8000/predict"  # This service's own endpoint
FETCH_INTERVAL = 30  # seconds

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

# Helper to fetch pod metrics
def fetch_pod_metrics():
    try:
        config.load_incluster_config()
        v1 = client.CoreV1Api()
        metrics = client.CustomObjectsApi()
        pods = v1.list_namespaced_pod(namespace=NAMESPACE, label_selector=TARGET_LABEL)
        for pod in pods.items:
            pod_name = pod.metadata.name
            # Fetch metrics from metrics.k8s.io
            m = metrics.get_namespaced_custom_object(
                group="metrics.k8s.io",
                version="v1beta1",
                namespace=NAMESPACE,
                plural="pods",
                name=pod_name
            )
            containers = m["containers"]
            for c in containers:
                cpu = c["usage"]["cpu"]
                mem = c["usage"]["memory"]
                cpu_val = parse_cpu(cpu)
                mem_val = parse_mem(mem)
                yield {"pod": pod_name, "cpu_usage": cpu_val, "memory_usage": mem_val}
    except Exception as e:
        print(f"[Metrics Fetch Error] {e}")

# Parse CPU (e.g., '5m' to 0.005)
def parse_cpu(cpu_str):
    if cpu_str.endswith('n'):
        return float(cpu_str[:-1]) / 1e9
    if cpu_str.endswith('u'):
        return float(cpu_str[:-1]) / 1e6
    if cpu_str.endswith('m'):
        return float(cpu_str[:-1]) / 1000
    return float(cpu_str)

def parse_mem(mem_str):
    if mem_str.endswith('Ki'):
        return float(mem_str[:-2]) * 1024
    if mem_str.endswith('Mi'):
        return float(mem_str[:-2]) * 1024 * 1024
    if mem_str.endswith('Gi'):
        return float(mem_str[:-2]) * 1024 * 1024 * 1024
    if mem_str.endswith('Ti'):
        return float(mem_str[:-2]) * 1024 * 1024 * 1024 * 1024
    return float(mem_str)

# Background loop
def metrics_loop():
    while True:
        for metric in fetch_pod_metrics():
            data = {
                "cpu_usage": metric["cpu_usage"],
                "memory_usage": metric["memory_usage"]
            }
            try:
                resp = requests.post(PREDICT_URL, json=data)
                result = resp.json()
                print(f"[AnomalyCheck] Pod: {metric['pod']} | CPU: {data['cpu_usage']} | Mem: {data['memory_usage']} | Anomaly: {result['anomaly']}")
                # Optionally: trigger action if result['anomaly']
            except Exception as e:
                print(f"[Predict Error] {e}")
        time.sleep(FETCH_INTERVAL)

@app.on_event("startup")
def start_metrics_thread():
    t = threading.Thread(target=metrics_loop, daemon=True)
    t.start()
