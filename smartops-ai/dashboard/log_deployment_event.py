import sys
import sqlite3
from datetime import datetime
import pytz
import os

# Path to the SQLite database (relative to dashboard directory)
db_path = "data/deployment_events.db"
# Ensure the data directory exists
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Get current time in IST
ist_tz = pytz.timezone('Asia/Kolkata')
timestamp = datetime.now(ist_tz).isoformat()

# Parse command line arguments
if len(sys.argv) < 3:
    print("Usage: python log_deployment_event.py <status> <message> [namespace]")
    sys.exit(1)

status = sys.argv[1]
message = sys.argv[2]
namespace = sys.argv[3] if len(sys.argv) > 3 else "default"

conn = sqlite3.connect(db_path)
c = conn.cursor()

# Create table with namespace column
c.execute("""
CREATE TABLE IF NOT EXISTS deployment_events (
    timestamp TEXT,
    status TEXT,
    message TEXT,
    namespace TEXT
)
""")

# Insert event with namespace
c.execute("INSERT INTO deployment_events (timestamp, status, message, namespace) VALUES (?, ?, ?, ?)", 
         (timestamp, status, message, namespace))
conn.commit()
conn.close()

print(f"Logged deployment event: {status} - {message} in namespace {namespace}") 