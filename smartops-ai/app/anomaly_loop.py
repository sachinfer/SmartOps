import time
from ai_detector import is_anomalous
from alert_telegram import send_alert
from log_monitor import detect_non_200_logs
from k8s_monitor import get_pod_restart_counts
from kubernetes import client, config

# Configuration for log monitoring
NAMESPACE = "smartops"
POD_NAME = "smartops-app-6ccd6f5748-djbbx"  # Update this to match your pod name
CONTAINER_NAME = "fastapi"

# Initialize Kubernetes client
config.load_incluster_config()
v1 = client.CoreV1Api()

def get_pod_logs(namespace, pod_name, container_name, tail_lines=100):
    try:
        logs = v1.read_namespaced_pod_log(
            name=pod_name,
            namespace=namespace,
            container=container_name,
            tail_lines=tail_lines
        )
        return logs.splitlines()
    except Exception as e:
        print(f"Error fetching pod logs: {e}")
        return []

while True:
    # Simulated metrics (replace with real metrics fetch if available)
    cpu = 91.5
    memory = 75.3
    latency = 2.4

    # 1. Anomaly Detection
    is_outlier, score = is_anomalous(cpu, memory, latency)
    if is_outlier:
        msg = f"""🚨 *AI Anomaly Detected*
*CPU:* {cpu}% | *Mem:* {memory}% | *Latency:* {latency}s
*Score:* {score:.2f}
📊 [Open Dashboard](http://dashboard-url)
"""
        send_alert(msg)

    # 2. Non-200 HTTP Logs (read real logs from pod)
    logs = get_pod_logs(NAMESPACE, POD_NAME, CONTAINER_NAME, tail_lines=100)
    non_200 = detect_non_200_logs(logs)
    for line in non_200:
        send_alert(f"⚠️ *Non-200 Log Detected:*\n`{line}`")

    # 3. Pod Health Check
    unhealthy_pods = get_pod_restart_counts()
    for pod, count in unhealthy_pods.items():
        send_alert(f"🔁 *Pod Restart Alert:*\nPod `{pod}` restarted {count} times!")

    time.sleep(60)  # Delay next loop 