import time
import requests
import logging
from kubernetes import client, config
import os
import sqlite3
from datetime import datetime
import subprocess
import threading

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

NAMESPACE = os.getenv("SMARTOPS_NAMESPACE", "smartops")
TARGET_POD_LABEL = "app=smartops-app"
PREDICT_URL = "http://localhost:8000/predict"
FETCH_INTERVAL_SECONDS = 60  # 1 min

TELEGRAM_BOT_TOKEN = "7740618650:AAEMnkAevBQMZ_fz0WVdAx7iwtBf5tqjh4c"
TELEGRAM_CHAT_ID = "5520324585"  # Use your group chat ID (negative number) for group alerts
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

def send_telegram_alert(message, cpu=None, memory=None, details=None):
    alert = "🚨 *SmartOps Anomaly Detected!*\n"
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
                if text.startswith("kubectl") and str(chat_id) == TELEGRAM_CHAT_ID:
                    reply = handle_telegram_command(text)
                    send_telegram_alert(reply)
        except Exception as e:
            print(f"Telegram polling error: {e}")
        time.sleep(5)

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
                        details=res.text
                    )
            except Exception as e:
                logging.error(f"Prediction request failed: {e}")
        time.sleep(FETCH_INTERVAL_SECONDS)

if __name__ == "__main__":
    # Send a test alert on startup
    send_telegram_alert("🚨 Test alert from SmartOps! If you see this, your bot is working.")
    # Start Telegram polling in a background thread
    threading.Thread(target=poll_telegram, daemon=True).start()
    main_loop() 