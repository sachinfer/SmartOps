import re
import pandas as pd

# Example log line:
# [2025-07-11T13:45:22.345Z] WARN  [ube-service] 404 Not Found - GET /non-existent-route
# [2025-07-11T13:45:22.345Z] INFO  [ube-service] Request received: GET /non-existent-route
# [2025-07-11T13:45:22.345Z] DEBUG [ube-service] Headers: { "user-agent": "Mozilla/5.0", "host": "ube.example.com" }

LOG_PATTERN = re.compile(r"\[(?P<timestamp>[^\]]+)\]\s+(?P<level>\w+)\s+\[(?P<service>[^\]]+)\]\s+(?P<message>.*)")
STATUS_PATTERN = re.compile(r"(?P<status>\d{3}) [A-Za-z ]+ - (?P<method>\w+) (?P<path>/[\w\-/]*)")


def parse_log_line(line):
    match = LOG_PATTERN.match(line)
    if not match:
        return None
    d = match.groupdict()
    # Try to extract status code, method, path from message
    status_match = STATUS_PATTERN.search(d["message"])
    if status_match:
        d.update(status_match.groupdict())
    else:
        d["status"] = None
        d["method"] = None
        d["path"] = None
    return d


def parse_log_file(log_path, out_csv="parsed_logs.csv"):
    rows = []
    with open(log_path, "r") as f:
        for line in f:
            parsed = parse_log_line(line)
            if parsed:
                rows.append(parsed)
    df = pd.DataFrame(rows)
    df.to_csv(out_csv, index=False)
    print(f"Parsed {len(df)} log lines. Output: {out_csv}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python train_log_parser.py app.log [output.csv]")
        exit(1)
    log_path = sys.argv[1]
    out_csv = sys.argv[2] if len(sys.argv) > 2 else "parsed_logs.csv"
    parse_log_file(log_path, out_csv) 