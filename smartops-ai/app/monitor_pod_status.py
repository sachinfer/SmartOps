import os
import json
from kubernetes import client, config
import requests

# Kubernetes setup
config.load_kube_config()  # Use config.load_incluster_config() if running inside the cluster
v1 = client.CoreV1Api()

# Telegram setup
TELEGRAM_BOT_TOKEN = "7740618650:AAEMnkAevBQMZ_fz0WVdAx7iwtBf5tqjh4c"
TELEGRAM_CHAT_ID = "-1002761935159"
STATUS_FILE = "pod_status.json"

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        resp = requests.post(url, data=payload, timeout=5)
        if resp.status_code != 200:
            print(f"Failed to send Telegram alert: {resp.text}")
    except Exception as e:
        print(f"Telegram alert error: {e}")

def load_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_status(status_dict):
    with open(STATUS_FILE, "w") as f:
        json.dump(status_dict, f)

def check_all_pods(namespace="smartops"):
    last_status = load_status()
    current_status = {}
    try:
        pods = v1.list_namespaced_pod(namespace=namespace)
        found_pods = set()
        for pod in pods.items:
            pod_name = pod.metadata.name
            found_pods.add(pod_name)
            status = pod.status.phase
            restarts = sum([c.restart_count for c in (pod.status.container_statuses or [])])
            current_status[pod_name] = status

            # Red alert if not running
            if status != "Running":
                message = (
                    f"🚨 *ALERT*: Pod `{pod_name}` in namespace `{namespace}` is *{status}* with *{restarts}* restarts!"
                )
                send_telegram_alert(message)

            # Green alert if pod was not running before and is now running
            if last_status.get(pod_name) and last_status[pod_name] != "Running" and status == "Running":
                message = (
                    f"🟢 *RECOVERY*: Pod `{pod_name}` in namespace `{namespace}` is back to *Running* state!"
                )
                send_telegram_alert(message)

            print(f"Pod {pod_name} is {status}.")

        # Alert for missing pods
        missing_pods = set(last_status.keys()) - found_pods
        for missing in missing_pods:
            send_telegram_alert(f"🚨 *ALERT*: Pod `{missing}` is MISSING from namespace `{namespace}`!")

        save_status(current_status)
    except Exception as e:
        send_telegram_alert(f"❌ *Error checking pods in namespace {namespace}*: {e}")

if __name__ == "__main__":
    check_all_pods("smartops") 