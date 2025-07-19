from fastapi import FastAPI, Request, Query
from pydantic import BaseModel
import sqlite3
from datetime import datetime
import os
import pytz
from typing import List, Optional

# Kubernetes client
from kubernetes import client, config

app = FastAPI()
DB_PATH = "data/deployment_events.db"

class Event(BaseModel):
    status: str
    message: str
    namespace: str = "smartops"
    timestamp: str = None

@app.post("/log_event")
def log_event(event: Event):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS deployment_events (
            timestamp TEXT,
            status TEXT,
            message TEXT,
            namespace TEXT
        )
    """)
    if event.timestamp:
        ts = event.timestamp
    else:
        ist = pytz.timezone('Asia/Kolkata')
        ts = datetime.now(ist).isoformat()
    conn.execute(
        "INSERT INTO deployment_events (timestamp, status, message, namespace) VALUES (?, ?, ?, ?)",
        (ts, event.status, event.message, event.namespace)
    )
    conn.commit()
    conn.close()
    return {"result": "success", "timestamp": ts}

@app.get("/pods")
def list_pods(namespace: Optional[str] = Query(None, description="Namespace to filter by")):
    try:
        config.load_incluster_config()
    except Exception:
        config.load_kube_config()
    v1 = client.CoreV1Api()
    if namespace and namespace != 'all':
        pods = v1.list_namespaced_pod(namespace=namespace)
    else:
        pods = v1.list_pod_for_all_namespaces()
    pod_list = [
        {
            "name": pod.metadata.name,
            "namespace": pod.metadata.namespace,
            "status": pod.status.phase
        }
        for pod in pods.items
    ]
    return {"pods": pod_list} 