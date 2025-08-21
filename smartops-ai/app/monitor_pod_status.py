import os
import json
from kubernetes import client, config
import requests
import time

# Kubernetes setup
config.load_incluster_config()
v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()

# Telegram setup
# Load from environment variables or config file
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "your_bot_token_here")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "your_chat_id_here")
STATUS_FILE = "monitor_status.json"
# Get dashboard URL from environment variable or use service discovery
DASHBOARD_URL = os.environ.get("DASHBOARD_URL", "http://smartops-dashboard-service.smartops.svc.cluster.local:8000")
DASHBOARD_EVENT_API = f"{DASHBOARD_URL}:8000/log_event"

# Log event to dashboard API
def log_dashboard_event(status, message, namespace="smartops"):
    payload = {
        "status": status,
        "message": message,
        "namespace": namespace
    }
    try:
        resp = requests.post(DASHBOARD_EVENT_API, json=payload, timeout=5)
        if resp.status_code != 200:
            print(f"Failed to log dashboard event: {resp.text}")
    except Exception as e:
        print(f"Dashboard event log error: {e}")

def send_telegram_alert(message, status="info", namespace="smartops"):
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
    # Also log to dashboard
    log_dashboard_event(status, message, namespace)

def load_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_status(status_dict):
    with open(STATUS_FILE, "w") as f:
        json.dump(status_dict, f)

def check_deployments(namespace="smartops"):
    last_status = load_status()
    current_status = {}
    try:
        deployments = apps_v1.list_namespaced_deployment(namespace=namespace)
        pods = v1.list_namespaced_pod(namespace=namespace)
        pod_list = list(pods.items)
        
        print(f"Found {len(pod_list)} total pods in namespace {namespace}")
        for pod in pod_list:
            print(f"Pod: {pod.metadata.name}, Status: {pod.status.phase}, Labels: {pod.metadata.labels}")
        
        for deploy in deployments.items:
            deploy_name = deploy.metadata.name
            expected_replicas = deploy.spec.replicas
            selector = deploy.spec.selector.match_labels
            print(f"\nChecking deployment: {deploy_name}")
            print(f"Expected replicas: {expected_replicas}")
            print(f"Label selector: {selector}")
            
            running_pods = [
                pod for pod in pod_list
                if pod.status.phase == "Running" and pod.metadata.labels is not None and all(
                    pod.metadata.labels.get(k) == v for k, v in selector.items()
                )
            ]
            running_count = len(running_pods)
            print(f"Found {running_count} running pods matching selector:")
            for pod in running_pods:
                print(f"  - {pod.metadata.name} (labels: {pod.metadata.labels})")
            
            is_unhealthy = running_count < expected_replicas
            last_state = last_status.get(deploy_name, "healthy")
            current_state = "unhealthy" if is_unhealthy else "healthy"
            dashboard_link = f"[Open Dashboard]({DASHBOARD_URL}/?namespace={namespace}&deployment={deploy_name})"
            # Only alert on state change
            if is_unhealthy and last_state != "unhealthy":
                msg = (
                    f"🚨 *ALERT*: Deployment `{deploy_name}` in namespace `{namespace}` has *{running_count}/{expected_replicas}* running pods!\n"
                    f"{dashboard_link}"
                )
                send_telegram_alert(msg, status="unhealthy", namespace=namespace)
            elif not is_unhealthy and last_state == "unhealthy":
                msg = (
                    f"🟢 *RECOVERY*: Deployment `{deploy_name}` in namespace `{namespace}` is healthy again with *{running_count}/{expected_replicas}* running pods.\n"
                    f"{dashboard_link}"
                )
                send_telegram_alert(msg, status="healthy", namespace=namespace)
            print(f"Deployment {deploy_name}: {running_count}/{expected_replicas} pods running ({'UNHEALTHY' if is_unhealthy else 'OK'}).")
            current_status[deploy_name] = current_state
        save_status(current_status)
    except Exception as e:
        msg = f"❌ *Error checking deployments in namespace {namespace}*: {e}\n[Open Dashboard]({DASHBOARD_URL}/?namespace={namespace})"
        send_telegram_alert(msg, status="error", namespace=namespace)

if __name__ == "__main__":
    while True:
        print("Monitor loop running...")
        check_deployments("smartops")
        time.sleep(60)  # Check every 60 seconds 