from fastapi import FastAPI, Request
from pydantic import BaseModel
import sqlite3
from datetime import datetime
import os
import pytz

app = FastAPI()
DB_PATH = "data/deployment_events.db"

class Event(BaseModel):
    status: str
    message: str
    timestamp: str = None

@app.post("/log_event")
def log_event(event: Event):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS deployment_events (
            timestamp TEXT,
            status TEXT,
            message TEXT
        )
    """)
    if event.timestamp:
        ts = event.timestamp
    else:
        ist = pytz.timezone('Asia/Kolkata')
        ts = datetime.now(ist).isoformat()
    conn.execute(
        "INSERT INTO deployment_events (timestamp, status, message) VALUES (?, ?, ?)",
        (ts, event.status, event.message)
    )
    conn.commit()
    conn.close()
    return {"result": "success", "timestamp": ts} 