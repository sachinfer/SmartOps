import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import json
import subprocess
import time
import sqlite3
import os

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
                    user_action BOOLEAN
                )
            """)
            
            # Insert the action
            cursor.execute("""
                INSERT INTO pod_actions (timestamp, action, pod_name, reason, user_action)
                VALUES (?, ?, ?, ?, ?)
            """, (datetime.now().isoformat(), action, pod_name, reason, user_action))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            st.error(f"Failed to log action: {e}")
            return False
    
    
    # Function to get individual pod resource usage
    def get_pod_resource_usage():
        try:
            response = requests.get(f"{API_URL}/pod_resources", timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                st.info("ℹ️ Resource usage not available (kubectl permissions required)")
                return {}
        except Exception:
            st.info("ℹ️ Resource usage not available (kubectl permissions required)")
            return {}
    
    # Enhanced function to get pod metrics from Kubernetes API
    def get_pod_metrics_k8s():
        """Get real-time pod metrics using kubectl top command"""
        try:
            result = subprocess.run(
                ["kubectl", "top", "pods", "-n", NAMESPACE, "--no-headers"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                metrics = {}
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 3:
                            pod_name = parts[0]
                            cpu = parts[1]
                            memory = parts[2]
                            metrics[pod_name] = {"cpu": cpu, "memory": memory}
                return metrics
            else:
                return {}
        except Exception as e:
            st.warning(f"Could not fetch pod metrics: {str(e)}")
            return {}
    
    # Function to get pod resource requests and limits
    def get_pod_resource_limits():
        """Get pod resource requests and limits"""
        try:
            result = subprocess.run(
                ["kubectl", "get", "pods", "-n", NAMESPACE, "-o", "json"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                pods_data = json.loads(result.stdout)
                resource_info = {}
                for pod in pods_data.get("items", []):
                    pod_name = pod["metadata"]["name"]
                    containers = pod.get("spec", {}).get("containers", [])
                    for container in containers:
                        resources = container.get("resources", {})
                        requests = resources.get("requests", {})
                        limits = resources.get("limits", {})
                        resource_info[pod_name] = {
                            "cpu_request": requests.get("cpu", "N/A"),
                            "memory_request": requests.get("memory", "N/A"),
                            "cpu_limit": limits.get("cpu", "N/A"),
                            "memory_limit": limits.get("memory", "N/A")
                        }
                return resource_info
            else:
                return {}
        except Exception as e:
            st.warning(f"Could not fetch pod resource limits: {str(e)}")
            return {}
    
    # Function to get all pods
    def get_all_pods():
        try:
            response = requests.get(f"{API_URL}/pods", timeout=10)
            if response.status_code == 200:
                pods = response.json()
                return pods
            else:
                st.error(f"API Error: {response.status_code}")
                return []
        except Exception as e:
            st.error(f"Connection Error: {str(e)}")
            # Fallback to kubectl command if API is not available
            return get_pods_kubectl_fallback()
    
    # Fallback function using kubectl command
    def get_pods_kubectl_fallback():
        try:
            # This would be a fallback if the API is not working
            st.info("Trying kubectl fallback...")
            
            # Try to get pods using kubectl if available
            import subprocess
            result = subprocess.run(
                ["kubectl", "get", "pods", "-n", "smartops", "-o", "json"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                import json
                pods_json = json.loads(result.stdout)
                pods = []
                for pod in pods_json.get("items", []):
                    pod_data = {
                        "name": pod["metadata"]["name"],
                        "status": pod["status"]["phase"],
                        "ready": f"{pod['status']['readyReplicas']}/{pod['spec']['replicas']}" if 'readyReplicas' in pod['status'] else "1/1",
                        "age": "unknown",
                        "namespace": pod["metadata"]["namespace"]
                    }
                    pods.append(pod_data)
                return {"pods": pods}
            else:
                st.warning(f"kubectl fallback failed: {result.stderr}")
                return {"pods": []}
                
        except Exception as e:
            st.warning(f"kubectl fallback error: {str(e)}")
            return {"pods": []}
    
    # Function to kill a pod
    def kill_pod(pod_name):
        try:
            response = requests.delete(f"{API_URL}/pods/{pod_name}", timeout=10)
            if response.status_code == 200:
                return True, f"✅ Successfully killed pod: {pod_name}"
            else:
                return False, f"❌ Failed to kill pod: {response.text}"
        except Exception as e:
            return False, f"❌ Error killing pod: {str(e)}"
    
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
        
        # Filter to show only HIGH resource consuming pods (CPU > 5% OR Memory > 500MB)
        high_resource_pods = latest_anomalies[
            (latest_anomalies['cpu_numeric'] > 0.05) |  # CPU > 5%
            (latest_anomalies['memory_numeric'] > 500 * 1024 * 1024)  # Memory > 500MB
        ]
        
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
                
                col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
                
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
                                st.rerun()
                            else:
                                st.error(message)
        else:
            st.success("✅ No pods with high resource consumption detected")
            st.info("💡 Create stress pods manually via terminal: `kubectl run stress-pod --image=busybox --namespace=smartops --command -- sh -c \"while true; do echo 'stress' > /dev/null; done\"`")
    else:
        st.info("ℹ️ No anomaly data available or no pods with high resource usage detected")
        st.info("💡 Create stress pods manually via terminal: `kubectl run stress-pod --image=busybox --namespace=smartops --command -- sh -c \"while true; do echo 'stress' > /dev/null; done\"`")
    
    # Only show high resource consuming pods - no need for regular pod listing
    
    # Footer
    st.markdown("---")
    st.markdown("*Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "*")
    st.markdown("**⚠️ Warning: Pod killing operations are irreversible. Use with caution!**")

if __name__ == "__main__":
    show_page()
