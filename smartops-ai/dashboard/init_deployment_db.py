#!/usr/bin/env python3
"""
Initialize Deployment Events Database with Sample Data
This script creates the deployment_events.db with sample deployment workflow events
in India Standard Time (IST) timezone.
"""

import sqlite3
import os
from datetime import datetime, timedelta
import pytz

# Path to the SQLite database
db_path = "data/deployment_events.db"

# Ensure the data directory exists
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Sample deployment events data
sample_events = [
    {
        "status": "success",
        "message": "Frontend application deployment completed successfully",
        "namespace": "frontend"
    },
    {
        "status": "success", 
        "message": "Backend API service deployed to production cluster",
        "namespace": "backend"
    },
    {
        "status": "failed",
        "message": "Database migration failed due to connection timeout",
        "namespace": "database"
    },
    {
        "status": "success",
        "message": "Monitoring stack deployment completed",
        "namespace": "monitoring"
    },
    {
        "status": "failed",
        "message": "Load balancer configuration update failed",
        "namespace": "infrastructure"
    },
    {
        "status": "success",
        "message": "Security patches applied successfully",
        "namespace": "security"
    },
    {
        "status": "success",
        "message": "CI/CD pipeline deployment completed",
        "namespace": "cicd"
    },
    {
        "status": "failed",
        "message": "Container registry sync failed - network error",
        "namespace": "registry"
    },
    {
        "status": "success",
        "message": "Kubernetes cluster upgrade completed",
        "namespace": "k8s-cluster"
    },
    {
        "status": "success",
        "message": "Log aggregation system deployed",
        "namespace": "logging"
    }
]

def init_database():
    """Initialize the deployment events database with sample data"""
    
    # Connect to database (creates it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Create table
    c.execute("""
    CREATE TABLE IF NOT EXISTS deployment_events (
        timestamp TEXT,
        status TEXT,
        message TEXT,
        namespace TEXT
    )
    """)
    
    # Clear existing data
    c.execute("DELETE FROM deployment_events")
    
    # Get current time in IST
    ist_tz = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist_tz)
    
    # Insert sample events with timestamps spread over the last 24 hours
    for i, event in enumerate(sample_events):
        # Create timestamp for each event (spread over last 24 hours)
        event_time = current_time - timedelta(hours=i*2.4)  # Spread events over 24 hours
        timestamp = event_time.isoformat()
        
        c.execute("""
        INSERT INTO deployment_events (timestamp, status, message, namespace) 
        VALUES (?, ?, ?, ?)
        """, (timestamp, event['status'], event['message'], event['namespace']))
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print(f"✅ Deployment events database initialized at: {db_path}")
    print(f"📊 Added {len(sample_events)} sample deployment events")
    print(f"🕐 All timestamps are in India Standard Time (IST)")
    
    # Display sample data
    print("\n📋 Sample Events:")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT timestamp, status, message, namespace FROM deployment_events ORDER BY timestamp DESC LIMIT 5")
    
    for row in c.fetchall():
        timestamp, status, message, namespace = row
        status_icon = "🟢" if status == "success" else "🔴"
        print(f"{status_icon} {timestamp} - {status.upper()}: {message[:50]}... (ns: {namespace})")
    
    conn.close()

if __name__ == "__main__":
    init_database()
