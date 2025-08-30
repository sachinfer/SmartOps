#!/usr/bin/env python3
"""
Add Deployment Event Utility
This script allows you to add new deployment workflow events to the database
with automatic IST timezone handling.
"""

import sys
import sqlite3
from datetime import datetime
import pytz
import os

# Path to the SQLite database
db_path = "data/deployment_events.db"

def add_deployment_event(status, message, namespace="default"):
    """Add a new deployment event to the database"""
    
    # Ensure the data directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Get current time in IST
    ist_tz = pytz.timezone('Asia/Kolkata')
    timestamp = datetime.now(ist_tz).isoformat()
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Ensure table exists
    c.execute("""
    CREATE TABLE IF NOT EXISTS deployment_events (
        timestamp TEXT,
        status TEXT,
        message TEXT,
        namespace TEXT
    )
    """)
    
    # Insert event
    c.execute("""
    INSERT INTO deployment_events (timestamp, status, message, namespace) 
    VALUES (?, ?, ?, ?)
    """, (timestamp, status, message, namespace))
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print(f"✅ Added deployment event:")
    print(f"   📅 Timestamp: {timestamp}")
    print(f"   📊 Status: {status}")
    print(f"   💬 Message: {message}")
    print(f"   🏷️  Namespace: {namespace}")
    print(f"   🕐 Timezone: IST (Asia/Kolkata)")

def interactive_add():
    """Interactive mode to add deployment events"""
    
    print("🚀 Deployment Event Logger")
    print("=" * 40)
    
    # Get status
    print("\n📊 Select Status:")
    print("1. success")
    print("2. failed")
    print("3. started")
    
    while True:
        choice = input("\nEnter choice (1-3): ").strip()
        if choice == "1":
            status = "success"
            break
        elif choice == "2":
            status = "failed"
            break
        elif choice == "3":
            status = "started"
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")
    
    # Get message
    message = input("\n💬 Enter deployment message: ").strip()
    if not message:
        print("❌ Message cannot be empty!")
        return
    
    # Get namespace
    namespace = input("\n🏷️  Enter namespace (default: default): ").strip()
    if not namespace:
        namespace = "default"
    
    # Add event
    add_deployment_event(status, message, namespace)

def main():
    """Main function"""
    
    if len(sys.argv) == 1:
        # Interactive mode
        interactive_add()
    elif len(sys.argv) >= 3:
        # Command line mode
        status = sys.argv[1]
        message = sys.argv[2]
        namespace = sys.argv[3] if len(sys.argv) > 3 else "default"
        
        if status not in ["success", "failed", "started"]:
            print("❌ Invalid status. Must be: success, failed, or started")
            sys.exit(1)
        
        add_deployment_event(status, message, namespace)
    else:
        print("Usage:")
        print("  Interactive mode: python add_deployment_event.py")
        print("  Command line: python add_deployment_event.py <status> <message> [namespace]")
        print("\nStatus options: success, failed, started")
        print("Example: python add_deployment_event.py success 'App deployed successfully' frontend")

if __name__ == "__main__":
    main()
