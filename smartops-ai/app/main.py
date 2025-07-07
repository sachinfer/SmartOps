import time
import requests
from kubernetes import client, config
import logging
import sqlite3
from datetime import datetime
import os
from pymongo import MongoClient

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
MONGO_URI = "mongodb+srv://nsachinfe:pKfE9I4V9SmzLQ2t@smartops.c2fnfp6.mongodb.net/?retryWrites=true&w=majority&appName=smartops"

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

def log_prediction(cpu, memory, result):
    try:
        db_path = os.path.join(os.path.dirname(__file__), '../dashboard/data.db')
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS anomalies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                cpu TEXT,
                memory TEXT,
                prediction TEXT
            )
        ''')
        cursor.execute("INSERT INTO anomalies (timestamp, cpu, memory, prediction) VALUES (?, ?, ?, ?)",
                       (datetime.utcnow().isoformat(), cpu, memory, result))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(f"Failed to log prediction: {e}")

def log_prediction_mongo(cpu, memory, result):
    try:
        client = MongoClient(MONGO_URI)
        db = client.smartops
        collection = db.anomalies
        doc = {
            "timestamp": datetime.utcnow().isoformat(),
            "cpu": cpu,
            "memory": memory,
            "prediction": result
        }
        collection.insert_one(doc)
        client.close()
    except Exception as e:
        logging.error(f"Failed to log prediction to MongoDB: {e}")

def send_to_predict(payload):
    try:
        res = requests.post(PREDICT_URL, json=payload, timeout=5)
        logging.info(f"Prediction Result: {res.status_code}, {res.text}")
        log_prediction(payload.get('cpu'), payload.get('memory'), res.text)
        log_prediction_mongo(payload.get('cpu'), payload.get('memory'), res.text)
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
