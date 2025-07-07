import time
import requests
from kubernetes import client, config
import logging

# Logging config
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load in-cluster Kubernetes config
config.load_incluster_config()

# Kubernetes API clients
core_api = client.CoreV1Api()
custom_api = client.CustomObjectsApi()

# Settings
NAMESPACE = "smartops"
TARGET_POD_LABEL = "app=smartops-app"
PREDICT_URL = "http://smartops-anomaly-service.smartops.svc.cluster.local/predict"
FETCH_INTERVAL_SECONDS = 60  # 1 min

def get_pod_metrics():
    try:
        metrics = custom_api.list_namespaced_custom_object(
            group="metrics.k8s.io", version="v1beta1", namespace=NAMESPACE, plural="pods"
        )
        for pod in metrics['items']:
            if pod['metadata']['name'].startswith("smartops-app"):
                containers = pod['containers']
                for container in containers:
                    cpu = container['usage']['cpu']
                    memory = container['usage']['memory']
                    logging.info(f"CPU: {cpu}, Memory: {memory}")
                    return {"cpu": cpu, "memory": memory}
    except Exception as e:
        logging.error(f"Error fetching pod metrics: {e}")
    return None

def send_to_predict(payload):
    try:
        res = requests.post(PREDICT_URL, json=payload, timeout=5)
        logging.info(f"Prediction Result: {res.status_code}, {res.text}")
    except Exception as e:
        logging.error(f"Prediction request failed: {e}")

def main_loop():
    while True:
        metrics = get_pod_metrics()
        if metrics:
            send_to_predict(metrics)
        time.sleep(FETCH_INTERVAL_SECONDS)

if __name__ == "__main__":
    main_loop()
