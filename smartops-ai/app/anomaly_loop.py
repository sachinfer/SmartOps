import time
from ai_detector import is_anomalous
from alert_telegram import send_alert
from log_monitor import detect_non_200_logs
from k8s_monitor import get_pod_restart_counts

while True:
    # Simulated inputs (replace with real metrics fetch)
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

    # 2. Non-200 HTTP Logs (simulate logs)
    logs = ["200 OK", "500 Internal Server Error", "404 Not Found"]
    non_200 = detect_non_200_logs(logs)
    for line in non_200:
        send_alert(f"⚠️ *Non-200 Log Detected:*\n`{line}`")

    # 3. Pod Health Check
    unhealthy_pods = get_pod_restart_counts()
    for pod, count in unhealthy_pods.items():
        send_alert(f"🔁 *Pod Restart Alert:*\nPod `{pod}` restarted {count} times!")

    time.sleep(60)  # Delay next loop 