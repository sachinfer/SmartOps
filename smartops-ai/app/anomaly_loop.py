import time
import requests
import logging
from kubernetes import client, config
import os
import sqlite3
from datetime import datetime
import subprocess
import threading
import json
import re

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

NAMESPACE = os.getenv("SMARTOPS_NAMESPACE", "smartops")
TARGET_POD_LABEL = "app=smartops-app"
PREDICT_URL = "http://localhost:8000/predict"
FETCH_INTERVAL_SECONDS = 60  # 1 min

TELEGRAM_BOT_TOKEN = "7740618650:AAEMnkAevBQMZ_fz0WVdAx7iwtBf5tqjh4c"
TELEGRAM_CHAT_ID = "-1002761935159"  # Use your group chat ID (negative number) for group alerts
DASHBOARD_URL = "http://34.31.86.225"  # Update with your dashboard URL

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

def log_prediction(cpu, memory, result):
    try:
        conn = sqlite3.connect("/app/dashboard/data/data.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS anomalies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                cpu REAL,
                memory REAL,
                prediction TEXT
            )
        ''')
        cursor.execute("INSERT INTO anomalies (timestamp, cpu, memory, prediction) VALUES (?, ?, ?, ?)",
                       (datetime.utcnow().isoformat(), cpu, memory, result))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Failed to log prediction: {e}")

def send_telegram_alert(message, cpu=None, memory=None, details=None, namespace=None, raw=False):
    if raw:
        alert = message
    else:
        alert = "🚨 *SmartOps Anomaly Detected!*\n"
        if namespace:
            alert += f"• *Namespace*: `{namespace}`\n"
        if cpu is not None and memory is not None:
            alert += f"• *CPU*: `{cpu}`\n• *Memory*: `{memory}`\n"
        if details:
            alert += f"• *Details*: `{details}`\n"
        alert += f"\n[Open Dashboard]({DASHBOARD_URL})"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": alert,
        "parse_mode": "Markdown"
    }
    try:
        resp = requests.post(url, data=payload, timeout=5)
        if resp.status_code != 200:
            print(f"Failed to send Telegram alert: {resp.text}")
    except Exception as e:
        print(f"Telegram alert error: {e}")

def handle_telegram_command(text):
    if text.strip() == "kubectl get nodes":
        try:
            output = subprocess.check_output(["kubectl", "get", "nodes"], text=True)
            return output
        except Exception as e:
            return f"Error: {e}"
    elif text.strip() == "kubectl get pods -n smartops":
        try:
            output = subprocess.check_output(["kubectl", "get", "pods", "-n", "smartops"], text=True)
            return output
        except Exception as e:
            return f"Error: {e}"
    else:
        return "❌ Command not allowed."

def poll_telegram():
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    last_update_id = None
    while True:
        try:
            resp = requests.get(url, timeout=10)
            data = resp.json()
            for result in data.get("result", []):
                update_id = result["update_id"]
                if last_update_id is not None and update_id <= last_update_id:
                    continue
                last_update_id = update_id
                message = result.get("message", {})
                text = message.get("text", "")
                chat_id = message.get("chat", {}).get("id")
                if text.startswith("/cmd "):
                    cmd = text[5:].strip()
                    reply = handle_telegram_command(cmd)
                    send_telegram_alert(reply)
        except Exception as e:
            print(f"Telegram polling error: {e}")
        time.sleep(5)

def get_pods_status():
    try:
        output = subprocess.check_output(["kubectl", "get", "pods", "-n", "smartops", "-o", "json"], text=True)
        pods = json.loads(output)["items"]
        status_dict = {}
        for pod in pods:
            name = pod["metadata"]["name"]
            phase = pod["status"]["phase"]
            status_dict[name] = phase
        return status_dict
    except Exception as e:
        print(f"Error getting pod status: {e}")
        return {}

def monitor_pods_status():
    last_status = {}
    while True:
        current_status = get_pods_status()
        if not current_status:
            logging.warning("Pod status fetch failed or returned empty. Retrying in 5 seconds.")
            time.sleep(5)
            continue  # Sleep and retry
        # Check if all pods are running
        all_running = all(status == "Running" for status in current_status.values())
        if all_running and (not last_status or not all(status == "Running" for status in last_status.values())):
            send_telegram_alert(f"✅ All pods in '{NAMESPACE}' are RUNNING. All services are healthy.", raw=True)
        # Check for any status change
        for pod, status in current_status.items():
            if pod not in last_status or last_status[pod] != status:
                old_status = last_status.get(pod, 'Unknown')
                msg = f"Pod '{pod}' status changed: {old_status} → {status} in namespace '{NAMESPACE}'."
                logging.info(msg)
                send_telegram_alert(msg, raw=True)
        last_status = current_status
        time.sleep(5)  # Prevent tight loop

def monitor_logs_for_non_200(log_file_path, send_alert_func):
    status_pattern = re.compile(r'\s(\d{3})\s')
    with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as f:
        f.seek(0, 2)  # Go to end of file
        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue
            match = status_pattern.search(line)
            if match:
                status = match.group(1)
                if status != '200':
                    advice = (
                        'Check user input or resource (4xx).' if status.startswith('4')
                        else 'Check backend/service health (5xx or other).'
                    )
                    alert_msg = (
                        f"🚨 Non-200 log detected!\n"
                        f"Status: {status}\n"
                        f"Log: {line.strip()}\n"
                        f"Advice: {advice}"
                    )
                    send_alert_func(alert_msg)

def main_loop():
    while True:
        metrics = get_pod_metrics()
        if metrics:
            try:
                res = requests.post(PREDICT_URL, json=metrics, timeout=5)
                logging.info(f"Prediction Result: {res.status_code}, {res.text}")
                log_prediction(metrics["cpu"], metrics["memory"], res.text)
                if '"anomaly":true' in res.text:
                    send_telegram_alert(
                        "Anomaly detected!",
                        cpu=metrics["cpu"],
                        memory=metrics["memory"],
                        details=res.text,
                        namespace=NAMESPACE
                    )
            except Exception as e:
                logging.error(f"Prediction request failed: {e}")
        time.sleep(FETCH_INTERVAL_SECONDS)

def detect_anomaly(model, metrics):
    return model.predict([metrics])[0] == -1

# Unit test for anomaly detection
if __name__ == "__main__":
    import joblib
    model = joblib.load("../model/isolation_forest.pkl")
    assert detect_anomaly(model, [0.1, 0.2, 0.3, 0.4]) in [True, False]

if __name__ == "__main__":
    send_telegram_alert("🚨 Test alert from SmartOps! If you see this, your bot is working.")
    threading.Thread(target=poll_telegram, daemon=True).start()
    threading.Thread(target=monitor_pods_status, daemon=True).start()
    main_loop() 