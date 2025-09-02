import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import json
import subprocess
import time
import sqlite3
import os
import pytz

# Get IST timezone
IST = pytz.timezone('Asia/Kolkata')

def get_ist_time():
    """Get current time in IST timezone"""
    return datetime.now(IST)

def show_page():
    st.title("🔴 Pod Management & Kill Operations")
    st.markdown("Monitor and manage pods in real-time. Kill stressed or problematic pods directly from this dashboard.")
    
    # Configuration
    API_URL = "http://localhost:8000"
    NAMESPACE = "smartops"
    
    # Function to get anomaly data for high resource usage pods
    def get_anomaly_data():
        """Get anomaly data from the database to identify high resource usage pods"""
        try:
            conn = sqlite3.connect('/app/dashboard/data/data.db')
            df = pd.read_sql_query("""
                SELECT pod_name, cpu, memory, prediction, timestamp, labels
                FROM anomalies 
                WHERE prediction = 'Anomaly detected'
                ORDER BY timestamp DESC 
                LIMIT 50
            """, conn)
            conn.close()
            return df
        except Exception as e:
            st.warning(f"Could not load anomaly data: {e}")
            return pd.DataFrame()
    
    # Function to check if pod still exists
    def pod_exists(pod_name):
        """Check if a pod still exists in the cluster"""
        try:
            result = subprocess.run(
                f"kubectl get pod {pod_name} -n {NAMESPACE}",
                shell=True,
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except:
            return False
    
    # Function to log pod actions to database
    def log_pod_action(action, pod_name, reason="", user_action=True):
        """Log pod actions (kill/ignore) to the database"""
        try:
            conn = sqlite3.connect('/app/dashboard/data/data.db')
            cursor = conn.cursor()
            
            # Create actions table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pod_actions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    action TEXT,
                    pod_name TEXT,
                    reason TEXT,
                    user_action INTEGER
                )
            """)
            
            # Insert the action
            cursor.execute("""
                INSERT INTO pod_actions (timestamp, action, pod_name, reason, user_action)
                VALUES (?, ?, ?, ?, ?)
            """, (get_ist_time().isoformat(), action, pod_name, reason, 1 if user_action else 0))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            st.warning(f"Could not log action: {e}")
            return False
    
    # Function to kill a pod
    def kill_pod(pod_name):
        """Kill a pod using kubectl command"""
        try:
            # Use kubectl delete command directly without timeout
            result = subprocess.run(
                f"kubectl delete pod {pod_name} -n {NAMESPACE}",
                shell=True,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return True, f"✅ Successfully killed pod: {pod_name}"
            else:
                return False, f"❌ Failed to kill pod: {result.stderr.strip()}"
        except Exception as e:
            return False, f"❌ Error killing pod: {str(e)}"
    
    def ignore_pod(pod_name):
        """Add a pod to ignore list (just log the action)"""
        try:
            # For now, just log the ignore action
            # In a real implementation, you might want to store ignored pods in a database
            return True, f"✅ Pod {pod_name} added to ignore list"
        except Exception as e:
            return False, f"❌ Error ignoring pod: {str(e)}"
    
    # Refresh button
    st.markdown("### 📊 Real-Time Pod Monitoring")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Refresh Data", key="refresh_btn"):
            st.rerun()
    
    # Show pods with high resource usage from anomaly detection
    st.markdown("### 🚨 High Resource Usage Pods (From Anomaly Detection)")
    anomaly_df = get_anomaly_data()
    
    if not anomaly_df.empty:
        # Group by pod_name and get latest anomaly for each pod
        latest_anomalies = anomaly_df.groupby('pod_name').first().reset_index()
        
        # Convert CPU and memory to numeric for sorting
        latest_anomalies['cpu_numeric'] = pd.to_numeric(latest_anomalies['cpu'], errors='coerce').fillna(0)
        latest_anomalies['memory_numeric'] = pd.to_numeric(latest_anomalies['memory'], errors='coerce').fillna(0)
        
        # Filter to show only HIGH resource consuming pods (CPU > 50% OR Memory > 500MB)
        high_resource_pods = latest_anomalies[
            (latest_anomalies['cpu_numeric'] > 0.50) |  # CPU > 50%
            (latest_anomalies['memory_numeric'] > 500 * 1024 * 1024)  # Memory > 500MB
        ]
        
        # Filter out pods that no longer exist in the cluster
        existing_pods = []
        for idx, row in high_resource_pods.iterrows():
            if pod_exists(row['pod_name']):
                existing_pods.append(idx)
        
        high_resource_pods = high_resource_pods.loc[existing_pods]
        
        if not high_resource_pods.empty:
            # Sort by CPU usage (highest first)
            high_resource_pods = high_resource_pods.sort_values('cpu_numeric', ascending=False)
            
            st.info(f"🔍 Found {len(high_resource_pods)} pods with HIGH resource consumption")
        
            # Display high resource usage pods
            for idx, row in high_resource_pods.iterrows():
                pod_name = row['pod_name']
                cpu_usage = row['cpu_numeric'] * 100  # Convert to percentage
                memory_usage = row['memory_numeric'] / (1024 * 1024)  # Convert to MB
                timestamp = row['timestamp']
                
                col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 1, 1, 1])
                
                with col1:
                    st.write(f"**{pod_name}**")
                with col2:
                    st.write(f"CPU: {cpu_usage:.1f}%")
                with col3:
                    st.write(f"Memory: {memory_usage:.1f}MB")
                with col4:
                    st.write(f"Time: {timestamp[:19]}")
                with col5:
                    if st.button("🔴 Kill", key=f"kill_anomaly_{pod_name}"):
                        with st.spinner(f"Killing {pod_name}..."):
                            success, message = kill_pod(pod_name)
                            if success:
                                log_pod_action("kill", pod_name, f"High resource usage - CPU: {cpu_usage:.1f}%, Memory: {memory_usage:.1f}MB")
                                st.success(message)
                                # Force immediate refresh to update the display
                                time.sleep(1)  # Brief pause to ensure pod is deleted
                                st.rerun()
                            else:
                                st.error(message)
                with col6:
                    if st.button("🚫 Ignore", key=f"ignore_anomaly_{pod_name}"):
                        with st.spinner(f"Ignoring {pod_name}..."):
                            success, message = ignore_pod(pod_name)
                            if success:
                                log_pod_action("ignore", pod_name, f"High resource usage - CPU: {cpu_usage:.1f}%, Memory: {memory_usage:.1f}MB")
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)
        else:
            st.success("✅ No pods with high resource consumption detected")
    else:
        st.info("ℹ️ No anomaly data available or no pods with high resource usage detected")
    
    # Only show high resource consuming pods - no need for regular pod listing
    
    # Footer
    st.markdown("---")
    st.markdown("*Last updated: " + get_ist_time().strftime("%Y-%m-%d %H:%M:%S IST") + "*")
    st.markdown("**⚠️ Warning: Pod killing operations are irreversible. Use with caution!**")

if __name__ == "__main__":
    show_page()