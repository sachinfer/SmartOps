import time
import requests
import logging
from kubernetes import client, config
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

NAMESPACE = os.getenv("SMARTOPS_NAMESPACE", "smartops")
TARGET_POD_LABEL = "app=smartops-app"
PREDICT_URL = "http://localhost:8000/predict"
FETCH_INTERVAL_SECONDS = 60  # 1 min

def parse_cpu(cpu_str):
    # Convert Kubernetes CPU string (e.g., '123456n', '5m') to float (cores)
    if cpu_str.endswith('n'):
        return float(cpu_str[:-1]) / 1e9
    if cpu_str.endswith('u'):
        return float(cpu_str[:-1]) / 1e6
    if cpu_str.endswith('m'):
        return float(cpu_str[:-1]) / 1000
    return float(cpu_str)

def parse_mem(mem_str):
    # Convert Kubernetes memory string (e.g., '12345Ki', '12Mi') to float (bytes)
    if mem_str.endswith('Ki'):
        return float(mem_str[:-2]) * 1024
    if mem_str.endswith('Mi'):
        return float(mem_str[:-2]) * 1024 * 1024
    if mem_str.endswith('Gi'):
        return float(mem_str[:-2]) * 1024 * 1024 * 1024
    if mem_str.endswith('Ti'):
        return float(mem_str[:-2]) * 1024 * 1024 * 1024 * 1024
    return float(mem_str)

def get_pod_metrics():
    try:
        config.load_incluster_config()
        v1 = client.CoreV1Api()
        metrics = client.CustomObjectsApi()
        pods = v1.list_namespaced_pod(namespace=NAMESPACE, label_selector=TARGET_POD_LABEL)
        for pod in pods.items:
            pod_name = pod.metadata.name
            m = metrics.get_namespaced_custom_object(
                group="metrics.k8s.io",
                version="v1beta1",
                namespace=NAMESPACE,
                plural="pods",
                name=pod_name
            )
            containers = m["containers"]
            for c in containers:
                cpu = parse_cpu(c["usage"]["cpu"])
                mem = parse_mem(c["usage"]["memory"])
                return {"cpu": cpu, "memory": mem}
    except Exception as e:
        logging.error(f"Error fetching pod metrics: {e}")
    return None

def main_loop():
    while True:
        metrics = get_pod_metrics()
        if metrics:
            try:
                res = requests.post(PREDICT_URL, json=metrics, timeout=5)
                logging.info(f"Prediction Result: {res.status_code}, {res.text}")
            except Exception as e:
                logging.error(f"Prediction request failed: {e}")
        time.sleep(FETCH_INTERVAL_SECONDS)

if __name__ == "__main__":
    main_loop() 