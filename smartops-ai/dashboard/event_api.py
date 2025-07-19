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
    pod_list = []
    for pod in pods.items:
        restarts = sum([c.restart_count for c in pod.status.container_statuses or []])
        images = ', '.join([c.image for c in pod.spec.containers])
        pod_list.append({
            "name": pod.metadata.name,
            "namespace": pod.metadata.namespace,
            "status": pod.status.phase,
            "node": getattr(pod.spec, 'node_name', ''),
            "start_time": str(pod.status.start_time) if pod.status.start_time else '',
            "restarts": restarts,
            "images": images
        })
    return {"pods": pod_list}

@app.get("/namespaces")
def list_namespaces():
    try:
        config.load_incluster_config()
    except Exception:
        config.load_kube_config()
    v1 = client.CoreV1Api()
    ns_list = v1.list_namespace()
    namespaces = [ns.metadata.name for ns in ns_list.items]
    return {"namespaces": namespaces}

@app.get("/logs")
def get_pod_logs(namespace: str = Query(..., description="Namespace of the pod"), pod: str = Query(..., description="Pod name"), container: Optional[str] = Query(None, description="Container name (optional)")):
    """
    Fetch logs for a given pod in a given namespace. Optionally specify container.
    """
    try:
        config.load_incluster_config()
    except Exception:
        config.load_kube_config()
    v1 = client.CoreV1Api()
    try:
        logs = v1.read_namespaced_pod_log(name=pod, namespace=namespace, container=container)
    except Exception as e:
        return {"error": str(e), "logs": ""}
    return {"logs": logs} 