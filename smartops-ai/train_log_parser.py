import re
import pandas as pd

# Python logging format
LOG_PATTERN = re.compile(r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) (?P<level>\w+) (?P<message>.*)')
# Uvicorn access log format
# Use non-greedy match for path, and match up to HTTP/version
UVICORN_PATTERN = re.compile(r'^\s*(?P<level>\w+):\s+(?P<ip>[\d\.]+):(?P<port>\d+) - "(?P<method>\w+) (?P<path>.+?) HTTP/[\d\.]+" (?P<status>\d{3}) (?P<msg>.*)$')
ENDPOINT_PATTERN = re.compile(r'(endpoint|accessed|called|performed|added|updated|deleted|login|logout|refreshed|placed|checked|viewed|triggered|not found|cancelled|failed|error|timeout)[^/]*(/\w+)?', re.IGNORECASE)
STATUS_PATTERN = re.compile(r'(\d{3})')

def parse_log_line(line):
    line = line.rstrip("\n")
    if not line.strip():
        return None  # Skip empty lines
    # Try Python logging format
    match = LOG_PATTERN.match(line)
    if match:
        d = match.groupdict()
        endpoint_match = ENDPOINT_PATTERN.search(d["message"])
        d["endpoint"] = endpoint_match.group(2) if endpoint_match and endpoint_match.group(2) else None
        status_match = STATUS_PATTERN.search(d["message"])
        d["status"] = status_match.group(1) if status_match else None
        d["method"] = None
        d["path"] = None
        return d
    # Try Uvicorn access log format
    match = UVICORN_PATTERN.match(line)
    if match:
        d = match.groupdict()
        d["timestamp"] = None
        d["message"] = d["msg"]
        d["endpoint"] = d["path"]
        return d
    print(f"NO MATCH: {repr(line.strip())}")  # Debug print for unmatched lines
    return None

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