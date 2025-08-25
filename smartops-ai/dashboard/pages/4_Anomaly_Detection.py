import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import pytz
import requests
import sys
import os

# Import Misi from the dashboard directory
try:
    from misi_chatbot_widget import add_misi_to_page
    MISI_AVAILABLE = True
except ImportError:
    MISI_AVAILABLE = False
    st.warning("Misi AI Chatbot not available. Please ensure the chatbot is properly installed.")

# Check if API service is running
def check_api_health():
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        return response.status_code == 200
    except Exception:
        return False

# Timezone setup
IST = pytz.timezone('Asia/Kolkata')

# Cached functions
@st.cache_data(ttl=30)
def fetch_namespaces():
    try:
        url = f"http://localhost:8000/namespaces"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return resp.json().get('namespaces', [])
        else:
            return []
    except Exception:
        return []

@st.cache_data(ttl=30)
def load_anomalies_df():
    try:
        conn = sqlite3.connect("/app/dashboard/data/data.db")
        df = pd.read_sql_query("SELECT * FROM anomalies", conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()

def has_namespace_column(df):
    return 'namespace' in df.columns

# Page config
st.set_page_config(
    page_title="Anomaly Detection - SmartOps AI",
    page_icon="🔥",
    layout="wide"
)

# Modern CSS styling
st.markdown("""
<style>
.dashboard-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.1);
    text-align: center;
    color: white;
}
.dashboard-header h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    font-weight: 700;
}
.dashboard-header p {
    font-size: 1.1rem;
    opacity: 0.9;
    margin: 0;
}
.section-header {
    background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 10px;
    margin: 2rem 0 1rem 0;
    font-size: 1.3rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.stDataFrame {
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}
</style>
""", unsafe_allow_html=True)

# Main content
st.markdown("""
<div class="dashboard-header">
    <h1>🔥 Anomaly Detection</h1>
    <p>AI-powered anomaly detection and analysis</p>
</div>
""", unsafe_allow_html=True)

# Check if API service is running and show helpful message
if not check_api_health():

    
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

# Namespace selection
namespace_options = ['all'] + fetch_namespaces()
selected_ns = st.selectbox('Select Namespace', namespace_options, index=0, key="anomaly_ns")

# Load and filter data
df = load_anomalies_df()
if has_namespace_column(df) and selected_ns != 'all':
    filtered_df = df[df['namespace'] == selected_ns].copy()
else:
    filtered_df = df.copy()

# Top Anomalies Section
st.markdown('<div class="section-header">🔥 Top Anomalies by CPU Usage</div>', unsafe_allow_html=True)
if not filtered_df.empty:
    chart_df = filtered_df.copy()
    chart_df['cpu_numeric'] = pd.to_numeric(chart_df['cpu'], errors='coerce').fillna(0)
    chart_df['cpu_percent'] = chart_df['cpu_numeric'] * 100
    chart_df['memory_numeric'] = pd.to_numeric(chart_df['memory'], errors='coerce').fillna(0)
    chart_df['memory_mb'] = chart_df['memory_numeric'] / (1024 * 1024)
    top_cpu_df = chart_df.nlargest(5, 'cpu_percent')[['timestamp', 'pod_name', 'cpu_percent', 'memory_mb', 'prediction']]
    top_cpu_df['cpu_percent'] = top_cpu_df['cpu_percent'].round(1).astype(str) + '%'
    top_cpu_df['memory_mb'] = top_cpu_df['memory_mb'].round(1).astype(str) + 'MB'
    top_cpu_df = top_cpu_df.rename(columns={'timestamp': 'Timestamp', 'pod_name': 'Pod Name'})
    st.dataframe(top_cpu_df, use_container_width=True)
else:
    st.info("No anomaly data available for the selected namespace.")

# Recent Anomalies Section
st.markdown('<div class="section-header">🕒 Recent Anomalies</div>', unsafe_allow_html=True)
if not filtered_df.empty:
    display_cols = ['timestamp', 'cpu', 'memory', 'prediction']
    if 'pod_name' in filtered_df.columns:
        display_cols.append('pod_name')
    if 'labels' in filtered_df.columns:
        display_cols.append('labels')
    show_df = filtered_df[display_cols].copy()
    show_df = show_df.sort_values('timestamp', ascending=False).head(20)
    show_df['cpu_numeric'] = pd.to_numeric(show_df['cpu'], errors='coerce').fillna(0)
    show_df['memory_numeric'] = pd.to_numeric(show_df['memory'], errors='coerce').fillna(0)
    show_df['cpu_display'] = (show_df['cpu_numeric'] * 100).round(1).astype(str) + '%'
    show_df['memory_display'] = (show_df['memory_numeric'] / (1024 * 1024)).round(1).astype(str) + 'MB'
    display_df = show_df[['timestamp', 'cpu_display', 'memory_display', 'prediction']].copy()
    if 'pod_name' in show_df.columns:
        display_df['pod_name'] = show_df['pod_name']
    if 'labels' in show_df.columns:
        display_df['labels'] = show_df['labels']
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

# Add Misi AI Chatbot Widget
if MISI_AVAILABLE:
    add_misi_to_page("bottom-right")
else:
    st.info("🤖 Misi AI Chatbot integration is being set up. You'll see the floating 🤖 icon soon!") 