import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import pytz
import requests
import sys
import os

# Check if API service is running
def check_api_health():
    try:
        # Try the anomaly service first
        response = requests.get("http://smartops-anomaly-service.smartops.svc.cluster.local/", timeout=5)
        if response.status_code == 200:
            return True
    except Exception:
        pass
    
    try:
        # Fallback to localhost
        response = requests.get("http://localhost:8000/", timeout=5)
        return response.status_code == 200
    except Exception:
        return False

# Simple functions with better error handling
@st.cache_data(ttl=30)
def fetch_namespaces():
    try:
        # Try the anomaly service first
        url = "http://smartops-anomaly-service.smartops.svc.cluster.local/namespaces"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            namespaces = resp.json().get('namespaces', [])
            if namespaces:  # Only return if we got actual namespaces
                return namespaces
    except Exception as e:
        print(f"Error fetching namespaces from anomaly service: {e}")
    
    try:
        # Fallback to localhost
        url = "http://localhost:8000/namespaces"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            namespaces = resp.json().get('namespaces', [])
            if namespaces:  # Only return if we got actual namespaces
                return namespaces
    except Exception as e:
        print(f"Error fetching namespaces from localhost: {e}")
    
    # Final fallback - return common namespaces
    return ['smartops', 'default', 'kube-system', 'all']

@st.cache_data(ttl=30)
def load_anomalies_df():
    print("DEBUG: Starting to load anomaly data...")
    try:
        # Try to load from the real anomaly database first
        print("DEBUG: Trying to load from /app/dashboard/data/data.db")
        conn = sqlite3.connect('/app/dashboard/data/data.db')
        df = pd.read_sql_query("SELECT * FROM anomalies ORDER BY timestamp DESC LIMIT 100", conn)
        conn.close()
        
        print(f"DEBUG: Loaded {len(df)} records from data.db")
        if not df.empty:
            # Convert timestamp to datetime if it's a string
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            print("DEBUG: Successfully loaded real data from data.db")
            return df
    except Exception as e:
        print(f"DEBUG: Error loading from database: {e}")
    
    try:
        # Try to load from the old anomalies database
        print("DEBUG: Trying to load from /app/dashboard/data/anomalies.db")
        conn = sqlite3.connect('/app/dashboard/data/anomalies.db')
        df = pd.read_sql_query("SELECT * FROM anomalies ORDER BY timestamp DESC LIMIT 100", conn)
        conn.close()
        
        print(f"DEBUG: Loaded {len(df)} records from anomalies.db")
        if not df.empty:
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            print("DEBUG: Successfully loaded data from anomalies.db")
            return df
    except Exception as e:
        print(f"DEBUG: Error loading from old database: {e}")
    
    # If we get here, there's a problem - log it and return empty DataFrame
    print("WARNING: No anomaly data could be loaded from any source")
    return pd.DataFrame()

def has_namespace_column(df):
    return 'namespace' in df.columns

@st.cache_data(ttl=10)
def get_real_pod_metrics():
    """Get real-time pod metrics from the anomaly service"""
    try:
        # Try the anomaly service first
        url = "http://smartops-anomaly-service.smartops.svc.cluster.local/pods"
        resp = requests.get(url, params={"namespace": "smartops"}, timeout=5)
        if resp.status_code == 200:
            return resp.json().get('pods', [])
    except Exception:
        pass
    
    try:
        # Fallback to localhost
        url = "http://localhost:8000/pods"
        resp = requests.get(url, params={"namespace": "smartops"}, timeout=5)
        if resp.status_code == 200:
            return resp.json().get('pods', [])
    except Exception:
        pass
    
    return []

@st.cache_data(ttl=10)
def get_cluster_metrics():
    """Get real-time cluster metrics"""
    try:
        # Try the anomaly service first
        url = "http://smartops-anomaly-service.smartops.svc.cluster.local/cluster_metrics"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    
    try:
        # Fallback to localhost
        url = "http://localhost:8000/cluster_metrics"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    
    return {"cpu_usage": 0, "cpu_capacity": 1, "memory_usage": 0, "memory_capacity": 1}

# Main content
st.markdown("""
<div class="dashboard-header">
    <h1>🔥 Anomaly Detection</h1>
    <p>AI-powered anomaly detection and analysis</p>
</div>
""", unsafe_allow_html=True)

# Real-time cluster metrics
st.markdown('<div class="section-header">📊 Real-time Cluster Metrics</div>', unsafe_allow_html=True)
cluster_metrics = get_cluster_metrics()
if cluster_metrics:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        cpu_usage = cluster_metrics.get('cpu_usage', 0)
        cpu_capacity = cluster_metrics.get('cpu_capacity', 1)
        cpu_percent = (cpu_usage / cpu_capacity * 100) if cpu_capacity > 0 else 0
        st.metric("CPU Usage", f"{cpu_usage:.2f} cores", f"{cpu_percent:.1f}%")
    
    with col2:
        memory_usage = cluster_metrics.get('memory_usage', 0)
        memory_capacity = cluster_metrics.get('memory_capacity', 1)
        memory_percent = (memory_usage / memory_capacity * 100) if memory_capacity > 0 else 0
        st.metric("Memory Usage", f"{memory_usage / (1024**3):.2f} GB", f"{memory_percent:.1f}%")
    
    with col3:
        st.metric("CPU Capacity", f"{cpu_capacity:.2f} cores")
    
    with col4:
        st.metric("Memory Capacity", f"{memory_capacity / (1024**3):.2f} GB")

# Real-time pod status
st.markdown('<div class="section-header">🚀 Live Pod Status</div>', unsafe_allow_html=True)
real_pods = get_real_pod_metrics()
if real_pods:
    pod_df = pd.DataFrame(real_pods)
    st.dataframe(pod_df, use_container_width=True)
else:
    st.info("No pod data available from anomaly service")

# Namespace selection
st.markdown('<div class="section-header">📋 Select Namespace</div>', unsafe_allow_html=True)
namespaces = fetch_namespaces()
print(f"DEBUG: Available namespaces: {namespaces}")

if namespaces:
    selected_namespace = st.selectbox(
        "Choose a namespace to view anomalies:",
        options=namespaces,
        index=0 if 'smartops' in namespaces else 0,
        key="namespace_selector"
    )
    print(f"DEBUG: Selected namespace: {selected_namespace}")
else:
    st.error("No namespaces available. Please check the anomaly service connection.")
    selected_namespace = "smartops"

# Check if API service is running and show helpful message
api_health = check_api_health()
print(f"DEBUG: API health check result: {api_health}")

if not api_health:

    
    # Show current cluster status based on what we know
    # Get real cluster status
    try:
        node_response = requests.get("http://localhost:8000/kubectl_get", params={"resource_type": "nodes", "all_namespaces": "true"}, timeout=5)
        pod_response = requests.get("http://localhost:8000/kubectl_get", params={"resource_type": "pods", "all_namespaces": "true"}, timeout=5)
        namespace_response = requests.get("http://localhost:8000/namespaces", timeout=5)
        service_response = requests.get("http://localhost:8000/kubectl_get", params={"resource_type": "services", "all_namespaces": "true"}, timeout=5)
        
        node_count = len(node_response.json().get("items", [])) if node_response.status_code == 200 else 0
        pod_count = len(pod_response.json().get("items", [])) if pod_response.status_code == 200 else 0
        namespace_count = len(namespace_response.json().get("namespaces", [])) if namespace_response.status_code == 200 else 0
        service_count = len(service_response.json().get("items", [])) if service_response.status_code == 200 else 0
        
        # Get actual node names
        node_names = []
        if node_response.status_code == 200:
            nodes = node_response.json().get("items", [])
            node_names = [node.get("name", "") for node in nodes if node.get("name")]
        
        node_info = f"{node_count} ({', '.join(node_names)})" if node_names else f"{node_count}"
        
        st.success(f"✅ **Current Cluster Status**:\n- **Nodes**: {node_info}\n- **Pods**: {pod_count}\n- **Namespaces**: {namespace_count}\n- **Services**: {service_count}")
    except Exception:
        st.info("ℹ️ Using fallback cluster data")
    
    st.warning("⚠️ **Anomaly Detection**: Real-time anomaly detection requires the backend API service to be running.")

# Load and filter data
print("DEBUG: About to load anomaly data...")
df = load_anomalies_df()
print(f"DEBUG: Loaded DataFrame with shape: {df.shape}")
print(f"DEBUG: DataFrame columns: {df.columns.tolist()}")
print(f"DEBUG: DataFrame empty: {df.empty}")

if has_namespace_column(df) and selected_namespace != 'all':
    filtered_df = df[df['namespace'] == selected_namespace].copy()
    print(f"DEBUG: Filtered DataFrame shape: {filtered_df.shape}")
else:
    filtered_df = df.copy()
    print(f"DEBUG: Using full DataFrame, shape: {filtered_df.shape}")

# Top Anomalies Section
st.markdown('<div class="section-header">🔥 Top Anomalies</div>', unsafe_allow_html=True)
if not filtered_df.empty:
    chart_df = filtered_df.copy()
    
    # Check what columns are available and create safe numeric conversions
    if 'cpu' in chart_df.columns:
        chart_df['cpu_numeric'] = pd.to_numeric(chart_df['cpu'], errors='coerce').fillna(0)
        chart_df['cpu_percent'] = chart_df['cpu_numeric'] * 100
    else:
        chart_df['cpu_percent'] = 0
    
    if 'memory' in chart_df.columns:
        chart_df['memory_numeric'] = pd.to_numeric(chart_df['memory'], errors='coerce').fillna(0)
        chart_df['memory_mb'] = chart_df['memory_numeric'] / (1024 * 1024)
    else:
        chart_df['memory_mb'] = 0
    
    # Create display dataframe with available columns
    display_cols = ['timestamp', 'pod_name']
    if 'cpu_percent' in chart_df.columns:
        display_cols.append('cpu_percent')
    if 'memory_mb' in chart_df.columns:
        display_cols.append('memory_mb')
    if 'prediction' in chart_df.columns:
        display_cols.append('prediction')
    
    # Determine the sort column - use the first available metric column
    sort_column = None
    if 'cpu_percent' in chart_df.columns:
        sort_column = 'cpu_percent'
    elif 'memory_mb' in chart_df.columns:
        sort_column = 'memory_mb'
    elif 'prediction' in chart_df.columns:
        sort_column = 'prediction'
    else:
        # If no metric columns available, just take the first 5 rows
        top_anomalies_df = chart_df.head(5)[display_cols]
        sort_column = None
    
    if sort_column:
        top_anomalies_df = chart_df.nlargest(5, sort_column)[display_cols]
    
    # Format the display
    if 'cpu_percent' in top_anomalies_df.columns:
        top_anomalies_df['cpu_percent'] = top_anomalies_df['cpu_percent'].round(1).astype(str) + '%'
    if 'memory_mb' in top_anomalies_df.columns:
        top_anomalies_df['memory_mb'] = top_anomalies_df['memory_mb'].round(1).astype(str) + 'MB'
    
    top_anomalies_df = top_anomalies_df.rename(columns={'timestamp': 'Timestamp', 'pod_name': 'Pod Name'})
    st.dataframe(top_anomalies_df, use_container_width=True)
else:
    st.info("No anomaly data available for the selected namespace.")

# Recent Anomalies Section
st.markdown('<div class="section-header">🕒 Recent Anomalies</div>', unsafe_allow_html=True)
if not filtered_df.empty:
    # Build display columns dynamically based on what's available
    display_cols = ['timestamp']
    
    # Add metric columns if they exist
    if 'cpu' in filtered_df.columns:
        display_cols.append('cpu')
    if 'memory' in filtered_df.columns:
        display_cols.append('memory')
    if 'prediction' in filtered_df.columns:
        display_cols.append('prediction')
    if 'cpu_percent' in filtered_df.columns:
        display_cols.append('cpu_percent')
    if 'memory_mb' in filtered_df.columns:
        display_cols.append('memory_mb')
    
    # Add metadata columns if they exist
    if 'pod_name' in filtered_df.columns:
        display_cols.append('pod_name')
    if 'labels' in filtered_df.columns:
        display_cols.append('labels')
    
    # Only select columns that actually exist
    available_cols = [col for col in display_cols if col in filtered_df.columns]
    show_df = filtered_df[available_cols].copy()
    show_df = show_df.sort_values('timestamp', ascending=False).head(20)
    
    # Format CPU column if it exists
    if 'cpu' in show_df.columns:
        show_df['cpu_numeric'] = pd.to_numeric(show_df['cpu'], errors='coerce').fillna(0)
        show_df['cpu_display'] = (show_df['cpu_numeric'] * 100).round(1).astype(str) + '%'
    elif 'cpu_percent' in show_df.columns:
        show_df['cpu_display'] = show_df['cpu_percent'].astype(str) + '%'
    
    # Format Memory column if it exists
    if 'memory' in show_df.columns:
        show_df['memory_numeric'] = pd.to_numeric(show_df['memory'], errors='coerce').fillna(0)
        show_df['memory_display'] = (show_df['memory_numeric'] / (1024 * 1024)).round(1).astype(str) + 'MB'
    elif 'memory_mb' in show_df.columns:
        show_df['memory_display'] = show_df['memory_mb'].astype(str) + 'MB'
    
    # Create final display dataframe with available formatted columns
    final_display_cols = ['timestamp']
    
    if 'cpu_display' in show_df.columns:
        final_display_cols.append('cpu_display')
    if 'memory_display' in show_df.columns:
        final_display_cols.append('memory_display')
    if 'prediction' in show_df.columns:
        final_display_cols.append('prediction')
    if 'pod_name' in show_df.columns:
        final_display_cols.append('pod_name')
    if 'labels' in show_df.columns:
        final_display_cols.append('labels')
    
    # Only select columns that actually exist
    available_final_cols = [col for col in final_display_cols if col in show_df.columns]
    display_df = show_df[available_final_cols].copy()
    display_df = display_df.rename(columns={
        'timestamp': 'Timestamp',
        'cpu_display': 'CPU',
        'memory_display': 'Memory',
        'pod_name': 'Pod Name',
        'labels': 'Labels'
    })
    st.dataframe(display_df, use_container_width=True)
else:
    st.info("No recent anomalies found.")

# Misi AI Chatbot Widget removed - not using MISI AI page-wise 