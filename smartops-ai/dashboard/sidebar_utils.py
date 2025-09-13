import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import subprocess
import json

def get_anomaly_data():
    """Fetch recent actionable anomalies from the database"""
    try:
        # Try multiple possible database paths
        db_paths = [
            '/app/dashboard/data/data.db',  # Production path
            'smartops-ai/dashboard/data/data.db',  # Local development
            'data/data.db',  # Relative path
            'dashboard/data/data.db'  # Another relative path
        ]
        
        conn = None
        working_db = None
        for db_path in db_paths:
            try:
                conn = sqlite3.connect(db_path)
                # Test if the table exists
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='anomalies'")
                if cursor.fetchone():
                    working_db = db_path
                    break
                conn.close()
                conn = None
            except:
                if conn:
                    conn.close()
                conn = None
                continue
        
        if not conn:
            st.error("Could not connect to anomalies database")
            return pd.DataFrame()
        
        # Debug: Check table structure
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(anomalies)")
        columns_info = cursor.fetchall()
        
        # Debug: Show sample data
        cursor.execute("SELECT * FROM anomalies LIMIT 3")
        sample_data = cursor.fetchall()
        
        # Query for recent anomalies (last 24 hours) with high CPU usage
        query = """
        SELECT timestamp, pod_name, cpu, memory, prediction, labels
        FROM anomalies 
        WHERE timestamp >= datetime('now', '-24 hours')
        AND prediction = 'Anomaly detected'
        ORDER BY timestamp DESC
        LIMIT 10
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        # Convert CPU to percentage and memory to MB with proper error handling
        if not df.empty:
            # Handle CPU conversion - ensure it's numeric
            try:
                # Convert CPU to numeric, handling any string values
                df['cpu'] = pd.to_numeric(df['cpu'], errors='coerce')
                # Filter out rows where CPU conversion failed
                df = df.dropna(subset=['cpu'])
                # Filter for high CPU usage (> 50%)
                df = df[df['cpu'] > 0.5]
                
                # Convert CPU to percentage
                df['cpu_percent'] = (df['cpu'] * 100).round(1)
                
                # Handle memory conversion
                df['memory'] = pd.to_numeric(df['memory'], errors='coerce')
                df = df.dropna(subset=['memory'])
                df['memory_mb'] = (df['memory'] / (1024 * 1024)).round(1)
                
                # Convert timestamp
                df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
                df = df.dropna(subset=['timestamp'])
                
                # Add time ago
                df['time_ago'] = df['timestamp'].apply(lambda x: get_time_ago(x))
                
            except Exception as e:
                st.error(f"Error processing anomaly data: {e}")
                return pd.DataFrame()
        
        return df
    except Exception as e:
        st.error(f"Error fetching anomaly data: {e}")
        return pd.DataFrame()

def get_time_ago(timestamp):
    """Convert timestamp to human readable time ago"""
    try:
        now = datetime.now()
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        
        diff = now - timestamp
        
        if diff.days > 0:
            return f"{diff.days}d ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours}h ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes}m ago"
        else:
            return "Just now"
    except Exception as e:
        return "Unknown time"

def kill_pod(pod_name, namespace="smartops"):
    """Kill a problematic pod permanently"""
    try:
        # First check if kubectl is available
        result = subprocess.run(['which', 'kubectl'], capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            # kubectl not available, try alternative methods
            return False, f"kubectl not available. Pod {pod_name} cannot be killed from this container."
        
        # kubectl is available, proceed with deletion
        result = subprocess.run([
            'kubectl', 'delete', 'pod', pod_name, 
            '-n', namespace, '--force', '--grace-period=0'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            return True, f"Successfully killed pod {pod_name}"
        else:
            return False, f"Failed to kill pod: {result.stderr}"
    except subprocess.TimeoutExpired:
        return False, "Timeout while trying to kill pod"
    except FileNotFoundError:
        return False, "kubectl command not found. Pod killing is not available from this container."
    except Exception as e:
        return False, f"Error killing pod: {str(e)}"

def show_pod_killing_alternatives():
    """Show alternative ways to kill pods when kubectl is not available"""
    st.markdown("---")
    st.markdown("**🔧 Alternative Ways to Kill Pods:**")
    
    st.markdown("""
    Since kubectl is not available in this container, you can kill pods using:
    
    **1. From your local machine:**
    ```bash
    kubectl delete pod <pod-name> -n smartops --force --grace-period=0
    ```
    
    **2. From Cloud Shell:**
    ```bash
    kubectl delete pod <pod-name> -n smartops --force --grace-period=0
    ```
    
    **3. From another pod with kubectl:**
    ```bash
    kubectl exec -it <monitor-pod> -- kubectl delete pod <pod-name> -n smartops
    ```
    
    **4. Scale deployment to 0:**
    ```bash
    kubectl scale deployment <deployment-name> --replicas=0 -n smartops
    ```
    """)
    
    # Show current stress test pods
    st.markdown("**🚨 Current Stress Test Pods:**")
    st.markdown("Use these commands to kill the stress-test pod:")
    
    st.code("kubectl delete pod stress-test -n smartops --force --grace-period=0", language="bash")
    
    # Add a button to show more info
    if st.button("📋 Show All Pods"):
        show_all_pods_info()

def show_all_pods_info():
    """Show information about all pods in the smartops namespace"""
    st.markdown("**📊 All Pods in smartops Namespace:**")
    
    st.markdown("""
    To see all pods and their status:
    ```bash
    kubectl get pods -n smartops
    ```
    
    To see detailed pod information:
    ```bash
    kubectl describe pod <pod-name> -n smartops
    ```
    
    To see pod logs:
    ```bash
    kubectl logs <pod-name> -n smartops
    ```
    """)

def ignore_anomaly(pod_name):
    """Mark an anomaly as ignored (store in session state)"""
    if 'ignored_anomalies' not in st.session_state:
        st.session_state.ignored_anomalies = set()
    
    st.session_state.ignored_anomalies.add(pod_name)
    st.rerun()

def show_sidebar():
    # Simple, clean sidebar
    st.sidebar.title("SmartOps Dashboard")
    st.sidebar.markdown("---")
    
    # Simple navigation
    st.sidebar.markdown("### 📊 Dashboard")
    st.sidebar.markdown("• Overview")
    st.sidebar.markdown("• Pod Explorer")
    st.sidebar.markdown("• Kubernetes Shell")
    st.sidebar.markdown("• Anomaly Detection")
    st.sidebar.markdown("• Auto Scaling")
    st.sidebar.markdown("• Incident Timeline")
    st.sidebar.markdown("• AI Assistant")
    # st.sidebar.markdown("• AI Actions")  # Commented out - page exists but hidden from navigation
    st.sidebar.markdown("• Pod Management & Kill")
    st.sidebar.markdown("• Deployments")
    
    st.sidebar.markdown("---")
    
    # Quick actions
    st.sidebar.markdown("### ⚡ Quick Actions")
    if st.sidebar.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Status:** Online")

def get_current_page():
    """Get the current page from session state"""
    return st.session_state.get('current_page', 'overview')

def set_current_page(page_name):
    """Set the current page in session state"""
    st.session_state.current_page = page_name
