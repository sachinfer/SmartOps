from kubernetes import client, config
import requests

# Kubernetes setup
config.load_kube_config()  # Use config.load_incluster_config() if running inside the cluster
v1 = client.CoreV1Api()

# Telegram setup
TELEGRAM_BOT_TOKEN = "7740618650:AAEMnkAevBQMZ_fz0WVdAx7iwtBf5tqjh4c"
TELEGRAM_CHAT_ID = "-1002761935159"

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

def check_all_pods(namespace="smartops"):
    try:
        pods = v1.list_namespaced_pod(namespace=namespace)
        healthy = True
        for pod in pods.items:
            pod_name = pod.metadata.name
            status = pod.status.phase
            restarts = sum([c.restart_count for c in (pod.status.container_statuses or [])])
            if status != "Running" or restarts > 0:
                healthy = False
                message = (
                    f"🚨 *ALERT*: Pod `{pod_name}` in namespace `{namespace}` is *{status}* with *{restarts}* restarts!"
                )
                send_telegram_alert(message)
            else:
                print(f"Pod {pod_name} is healthy.")
        if healthy:
            print(f"All pods in namespace '{namespace}' are healthy.")
    except Exception as e:
        send_telegram_alert(f"❌ *Error checking pods in namespace {namespace}*: {e}")

if __name__ == "__main__":
    check_all_pods("smartops") 