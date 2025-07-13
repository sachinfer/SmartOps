import time
import csv
from datetime import datetime
import sys

# Import get_pod_metrics and load_kube_config_smart from anomaly_loop.py
sys.path.append('.')
from anomaly_loop import get_pod_metrics, load_kube_config_smart

output_file = "real_metrics.csv"

# Load Kubernetes config smartly
load_kube_config_smart()

with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["timestamp", "cpu", "memory"])
    for i in range(100):  # Collect 100 samples
        metrics = get_pod_metrics()
        if metrics:
            writer.writerow([datetime.utcnow().isoformat(), metrics["cpu"], metrics["memory"]])
            print(f"[{i+1}/100] Logged: CPU={metrics['cpu']}, Mem={metrics['memory']}")
        else:
            print(f"[{i+1}/100] Failed to fetch metrics.")
        time.sleep(60)  # Wait 60 seconds before next sample 