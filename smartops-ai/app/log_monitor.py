def detect_non_200_logs(log_lines):
    alerts = []
    for line in log_lines:
        if " 5" in line or " 4" in line:  # crude match for 4xx/5xx
            alerts.append(line.strip())
    return alerts 