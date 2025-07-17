import os
import json
from kubernetes import client, config
import requests
import time

# Kubernetes setup
config.load_kube_config()  # Use config.load_incluster_config() if running inside the cluster
v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()

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

def check_deployments(namespace="smartops"):
    try:
        deployments = apps_v1.list_namespaced_deployment(namespace=namespace)
        pods = v1.list_namespaced_pod(namespace=namespace)
        pod_list = list(pods.items)
        for deploy in deployments.items:
            deploy_name = deploy.metadata.name
            expected_replicas = deploy.spec.replicas
            selector = deploy.spec.selector.match_labels
            # Build a label selector string
            label_selector = ",".join([f"{k}={v}" for k, v in selector.items()])
            # Count running pods matching the selector
            running_pods = [
                pod for pod in pod_list
                if pod.status.phase == "Running" and all(
                    pod.metadata.labels.get(k) == v for k, v in selector.items()
                )
            ]
            running_count = len(running_pods)
            if running_count < expected_replicas:
                send_telegram_alert(
                    f"🚨 *ALERT*: Deployment `{deploy_name}` in namespace `{namespace}` has *{running_count}/{expected_replicas}* running pods!"
                )
            else:
                print(f"Deployment {deploy_name}: {running_count}/{expected_replicas} pods running (OK).")
    except Exception as e:
        send_telegram_alert(f"❌ *Error checking deployments in namespace {namespace}*: {e}")

if __name__ == "__main__":
    while True:
        check_deployments("smartops")
        # No sleep, runs as fast as possible 