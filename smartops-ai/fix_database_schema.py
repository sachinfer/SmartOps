#!/usr/bin/env python3
"""
Script to fix the database schema by adding missing columns to the anomalies table
"""
import sqlite3
import os

def fix_database_schema():
    db_path = "/app/dashboard/data/data.db"
    print(f"Fixing database schema at {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='anomalies'")
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("Anomalies table exists, checking columns...")
            
            # Get current columns
            cursor.execute("PRAGMA table_info(anomalies)")
            columns = [column[1] for column in cursor.fetchall()]
            print(f"Current columns: {columns}")
            
            # Add missing columns if they don't exist
            if 'pod_name' not in columns:
                print("Adding pod_name column...")
                cursor.execute("ALTER TABLE anomalies ADD COLUMN pod_name TEXT")
            
            if 'labels' not in columns:
                print("Adding labels column...")
                cursor.execute("ALTER TABLE anomalies ADD COLUMN labels TEXT")
            
            # Verify the changes
            cursor.execute("PRAGMA table_info(anomalies)")
            new_columns = [column[1] for column in cursor.fetchall()]
            print(f"Updated columns: {new_columns}")
            
            conn.commit()
            print("Database schema updated successfully!")
        else:
            print("Anomalies table doesn't exist, creating it...")
            cursor.execute('''
                CREATE TABLE anomalies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    cpu REAL,
                    memory REAL,
                    prediction TEXT,
                    pod_name TEXT,
                    labels TEXT
                )
            ''')
            conn.commit()
            print("Anomalies table created successfully!")
        
        conn.close()
        
    except Exception as e:
        print(f"Error fixing database schema: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_database_schema() 