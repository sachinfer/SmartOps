import time
import requests
import logging
from kubernetes import client, config, watch
import os
import sqlite3
from datetime import datetime
import subprocess
import threading
import json
import re
from threading import Thread

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

NAMESPACE = os.getenv("SMARTOPS_NAMESPACE", "smartops")
TARGET_POD_LABEL = "app=smartops-app"
PREDICT_URL = "http://34.46.130.148/predict"
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

def load_kube_config_smart():
    try:
        config.load_incluster_config()
    except Exception:
        config.load_kube_config()

def get_pod_metrics():
    try:
        load_kube_config_smart()
        v1 = client.CoreV1Api()
        metrics = client.CustomObjectsApi()
        pods = v1.list_namespaced_pod(namespace=NAMESPACE, label_selector=TARGET_POD_LABEL)
        for pod in pods.items:
            pod_name = pod.metadata.name
            labels = pod.metadata.labels or {}
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
                return {"cpu": cpu, "memory": mem, "pod_name": pod_name, "labels": labels}
    except Exception as e:
        logging.error(f"Error fetching pod metrics: {e}")
    return None

def get_all_pod_metrics():
    metrics_list = []
    try:
        load_kube_config_smart()
        v1 = client.CoreV1Api()
        metrics = client.CustomObjectsApi()
        pods = v1.list_namespaced_pod(namespace=NAMESPACE, label_selector=TARGET_POD_LABEL)
        for pod in pods.items:
            pod_name = pod.metadata.name
            labels = pod.metadata.labels or {}
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
                metrics_list.append({
                    "cpu": cpu,
                    "memory": mem,
                    "pod_name": pod_name,
                    "labels": labels
                })
    except Exception as e:
        logging.error(f"Error fetching pod metrics: {e}")
    return metrics_list

def log_prediction(cpu, memory, result, pod_name=None, labels=None):
    try:
        conn = sqlite3.connect("/app/dashboard/data/data.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS anomalies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                cpu REAL,
                memory REAL,
                prediction TEXT,
                pod_name TEXT,
                labels TEXT
            )
        ''')
        cursor.execute(
            "INSERT INTO anomalies (timestamp, cpu, memory, prediction, pod_name, labels) VALUES (?, ?, ?, ?, ?, ?)",
            (datetime.utcnow().isoformat(), cpu, memory, result, pod_name, str(labels))
        )
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

def monitor_k8s_logs(send_alert_func):
    namespace = os.environ.get("MY_POD_NAMESPACE", "default")
    pod_name = os.environ.get("MY_POD_NAME")
    container_name = os.environ.get("MY_CONTAINER_NAME", "app")
    print(f"[DEBUG] Starting log monitor with namespace={namespace}, pod_name={pod_name}, container_name={container_name}")
    if not pod_name:
        print("Environment variable MY_POD_NAME not set. Skipping K8s log monitoring.")
        return
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    w = watch.Watch()
    status_pattern = re.compile(r'\s(\d{3})\s')
    for line in w.stream(v1.read_namespaced_pod_log,
                         name=pod_name,
                         namespace=namespace,
                         container=container_name,
                         follow=True,
                         _preload_content=False):
        if isinstance(line, bytes):
            line = line.decode('utf-8')
        print(f"[DEBUG] K8s log line: {repr(line)}")
        match = status_pattern.search(line)
        print(f"[DEBUG] Regex match: {match}")
        if match:
            status = match.group(1)
            if status != '200':
                alert_msg = (
                    f"just now - Status: {status} | Log: {line.strip()}"
                )
                print(f"[DEBUG] Would send alert: {alert_msg}")
                send_alert_func(alert_msg, raw=True)

def detect_anomaly(model, metrics):
    return model.predict([metrics])[0] == -1

def main_anomaly_loop():
    """Main loop that fetches real metrics and detects anomalies"""
    import joblib
    import requests
    
    # Load the trained model
    try:
        model = joblib.load("/app/app/model/isolation_forest.pkl")
        logging.info("ML model loaded successfully")
    except Exception as e:
        logging.error(f"Failed to load ML model: {e}")
        return
    
    logging.info("Starting main anomaly detection loop...")
    
    while True:
        try:
            # 1. Fetch real metrics from Kubernetes for all pods
            pod_metrics_list = get_all_pod_metrics()
            if not pod_metrics_list:
                logging.warning("Failed to fetch pod metrics, retrying in 60 seconds...")
                time.sleep(60)
                continue
            for metrics in pod_metrics_list:
                cpu = metrics['cpu']
                memory = metrics['memory']
                pod_name = metrics.get("pod_name", "unknown")
                labels = metrics.get("labels", {})
                logging.info(f"Fetched metrics - Pod: {pod_name}, Labels: {labels}, CPU: {cpu:.3f}, Memory: {memory:.0f} bytes")
                # 2. Call ML model via FastAPI
                try:
                    response = requests.post(
                        PREDICT_URL,
                        json={"cpu": cpu, "memory": memory},
                        timeout=10
                    )
                    if response.status_code == 200:
                        result = response.json()
                        is_anomaly = result["anomaly"]
                        message = result["message"]
                    else:
                        logging.error(f"ML API returned status {response.status_code}")
                        continue
                except Exception as e:
                    logging.error(f"Failed to call ML API: {e}")
                    continue
                # 3. Log the prediction
                log_prediction(cpu, memory, message, pod_name, labels)
                # 4. Hybrid approach: alert only if ML says anomaly AND outside normal band
                if is_anomaly:
                    # Fix: Always multiply by 100 to get percent
                    cpu_percent = cpu * 100
                    memory_mb = memory / (1024 * 1024)
                    # Alert only if outside normal band
                    if cpu_percent > 50 or memory_mb > 500:
                        alert_msg = (
                            f"🚨 AI Anomaly Detected\n"
                            f"Pod: {pod_name}\n"
                            f"Labels: {labels}\n"
                            f"CPU: {cpu_percent:.1f}% | Mem: {memory_mb:.1f}MB\n"
                            f"Score: {message}\n"
                            f"[📊 Open Dashboard]({DASHBOARD_URL})"
                        )
                        send_telegram_alert(alert_msg, raw=True)
                        logging.warning(f"ACTIONABLE ANOMALY - Pod: {pod_name}, Labels: {labels}, CPU: {cpu_percent:.1f}%, Memory: {memory_mb:.1f}MB")
                    else:
                        logging.info(f"Anomaly detected by model, but within normal band: Pod: {pod_name}, Labels: {labels}, CPU={cpu_percent:.1f}%, Mem={memory_mb:.1f}MB. No alert sent.")
                else:
                    logging.info(f"Normal operation - Pod: {pod_name}, Labels: {labels}, CPU: {cpu:.3f}, Memory: {memory:.0f} bytes")
            # 5. Wait before next check
            time.sleep(FETCH_INTERVAL_SECONDS)
        except Exception as e:
            logging.error(f"Error in main anomaly loop: {e}")
            time.sleep(60)

# Unit test for anomaly detection
if __name__ == "__main__":
    import joblib
    model = joblib.load("app/model/isolation_forest.pkl")
    # Dynamically create a test vector with the correct number of features
    test_vector = [0.1] * model.n_features_in_
    assert detect_anomaly(model, test_vector) in [True, False]

if __name__ == "__main__":
    send_telegram_alert("🚨 Test alert from SmartOps! If you see this, your bot is working.")
    threading.Thread(target=poll_telegram, daemon=True).start()
    threading.Thread(target=monitor_pods_status, daemon=True).start()
    # Start K8s log monitoring in a background thread
    Thread(target=monitor_k8s_logs, args=(send_telegram_alert,)).start()
    # Start the main anomaly detection loop
    main_anomaly_loop() 