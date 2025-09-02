import sys
import sqlite3
from datetime import datetime
import os

# Path to the SQLite database (relative to dashboard directory)
db_path = "data/deployment_events.db"
# Ensure the data directory exists
os.makedirs(os.path.dirname(db_path), exist_ok=True)

timestamp = datetime.utcnow().isoformat()
status = sys.argv[1]
message = sys.argv[2]

conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS deployment_events (
    timestamp TEXT,
    status TEXT,
    message TEXT
)
""")
c.execute("INSERT INTO deployment_events (timestamp, status, message) VALUES (?, ?, ?)", (timestamp, status, message))
conn.commit()
conn.close() 