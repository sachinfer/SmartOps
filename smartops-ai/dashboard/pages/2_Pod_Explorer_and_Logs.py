# -*- coding: utf-8 -*-
"""
Pod Explorer and Logs - SmartOps AI
Dashbird-style monitoring dashboard
"""

import streamlit as st
import pandas as pd
import requests
import pytz
import time
import sqlite3
import json
from sidebar_utils import show_sidebar

# Page config
st.set_page_config(
    page_title="Pod Explorer and Logs - SmartOps AI",
    page_icon="🛰️",
    layout="wide"
)

# Sidebar
with st.sidebar:
    show_sidebar()

# Dashbird-style CSS
st.markdown("""
<style>
/* Dashbird-style dark theme */
.main .block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    max-width: 1400px;
    background-color: #1a1a1a;
}

/* Dark theme background */
.stApp {
    background-color: #1a1a1a;
}

/* Dashbird-style header */
.dashboard-header {
    background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
    padding: 2rem;
    border-radius: 8px;
    margin-bottom: 2rem;
    border: 1px solid #4a5568;
    position: relative;
}

.dashboard-header h1 {
    font-size: 2rem;
    margin-bottom: 0.5rem;
    font-weight: 600;
    color: #f7fafc;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.dashboard-header p {
    font-size: 1rem;
    opacity: 0.8;
    margin: 0;
    color: #e2e8f0;
}

/* Dashbird-style section headers */
.section-header {
    background: #2d3748;
    color: #f7fafc;
    padding: 1rem 1.5rem;
    border-radius: 6px;
    margin: 2rem 0 1rem 0;
    font-size: 1.1rem;
    font-weight: 600;
    border-left: 3px solid #3182ce;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

/* Dashbird-style namespace selector */
.namespace-selector {
    background: #2d3748;
    border: 1px solid #4a5568;
    border-radius: 8px;
    padding: 1.5rem;
    margin: 2rem 0;
}

.namespace-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
    font-size: 1rem;
    font-weight: 600;
    color: #f7fafc;
}

/* Dashbird-style pod cards */
.pod-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.pod-card {
    background: #2d3748;
    border: 1px solid #4a5568;
    border-radius: 8px;
    padding: 1.5rem;
    transition: all 0.2s ease;
    position: relative;
}

.pod-card:hover {
    border-color: #3182ce;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.pod-card.healthy {
    border-left: 4px solid #38a169;
}

.pod-card.warning {
    border-left: 4px solid #d69e2e;
}

.pod-card.error {
    border-left: 4px solid #e53e3e;
}

.pod-name {
    font-size: 1.1rem;
    font-weight: 600;
    color: #f7fafc;
    margin-bottom: 0.5rem;
}

.pod-status {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.25rem 0.75rem;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}

.pod-status.running {
    background: #38a169;
    color: white;
}

.pod-status.pending {
    background: #d69e2e;
    color: white;
}

.pod-status.failed {
    background: #e53e3e;
    color: white;
}

.pod-status.succeeded {
    background: #3182ce;
    color: white;
}

.pod-details {
    color: #a0aec0;
    font-size: 0.875rem;
    margin-bottom: 0.5rem;
}

.pod-actions {
    display: flex;
    gap: 0.5rem;
    margin-top: 1rem;
}

/* Dashbird-style log viewer */
.log-container {
    background: #2d3748;
    border: 1px solid #4a5568;
    border-radius: 8px;
    padding: 1.5rem;
    margin: 2rem 0;
}

.log-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
}

.log-icon {
    font-size: 1.25rem;
    color: #3182ce;
}

.log-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #f7fafc;
    margin: 0;
}

.log-content {
    background: #1a202c;
    border: 1px solid #4a5568;
    border-radius: 6px;
    padding: 1rem;
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
    font-size: 0.875rem;
    color: #e2e8f0;
    max-height: 400px;
    overflow-y: auto;
    white-space: pre-wrap;
}

/* Dashbird-style buttons */
.stButton > button {
    background: #3182ce !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
    padding: 0.5rem 1rem !important;
    font-size: 0.875rem !important;
}

.stButton > button:hover {
    background: #2c5aa0 !important;
    transform: translateY(-1px) !important;
}

.stButton > button.secondary {
    background: #4a5568 !important;
}

.stButton > button.secondary:hover {
    background: #2d3748 !important;
}

/* Dashbird-style selectboxes */
.stSelectbox > div > div {
    background: #2d3748 !important;
    border: 1px solid #4a5568 !important;
    color: #f7fafc !important;
}

.stSelectbox > div > div:hover {
    border-color: #3182ce !important;
}

/* Dashbird-style metrics */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin: 1.5rem 0;
}

.metric-card {
    background: #2d3748;
    border: 1px solid #4a5568;
    border-radius: 6px;
    padding: 1rem;
    text-align: center;
}

.metric-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: #f7fafc;
    margin-bottom: 0.25rem;
}

.metric-label {
    font-size: 0.75rem;
    color: #a0aec0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Responsive design */
@media (max-width: 768px) {
    .pod-grid {
        grid-template-columns: 1fr;
    }
    
    .metric-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}
</style>
""", unsafe_allow_html=True)

# Initialize session state for favorite namespaces
if 'favorite_namespaces' not in st.session_state:
    st.session_state.favorite_namespaces = []

def save_favorite_namespaces():
    """Save favorite namespaces to session state"""
    st.session_state.favorite_namespaces = st.session_state.favorite_namespaces

def add_favorite_namespace(namespace):
    """Add a namespace to favorites"""
    if namespace not in st.session_state.favorite_namespaces:
        st.session_state.favorite_namespaces.append(namespace)
        save_favorite_namespaces()

def remove_favorite_namespace(namespace):
    """Remove a namespace from favorites"""
    if namespace in st.session_state.favorite_namespaces:
        st.session_state.favorite_namespaces.remove(namespace)
        save_favorite_namespaces()

@st.cache_data(ttl=30)
def fetch_namespaces():
    try:
        url = f"http://localhost:8000/namespaces"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return resp.json().get('namespaces', [])
        else:
            return []
    except Exception as e:
        st.warning(f"Could not fetch namespaces: {e}")
        return []

@st.cache_data(ttl=30)
def fetch_pods(namespace):
    try:
        url = f"http://localhost:8000/pods"
        resp = requests.get(url, params={"namespace": namespace}, timeout=5)
        if resp.status_code == 200:
            return resp.json().get("pods", [])
        else:
            return []
    except Exception as e:
        st.warning(f"Could not fetch pods: {e}")
        return []

@st.cache_data(ttl=30)
def load_anomalies_df():
    try:
        conn = sqlite3.connect("/app/dashboard/data/data.db")
        df = pd.read_sql_query("SELECT * FROM anomalies", conn)
        conn.close()
        return df
    except Exception as e:
        st.warning(f"Could not load anomalies data: {e}")
        return pd.DataFrame()

# Main content
st.markdown("""
<div class="dashboard-header">
    <h1>🛰️ Pod Explorer and Logs</h1>
    <p>Explore pods and view their logs in real time with professional monitoring</p>
</div>
""", unsafe_allow_html=True)

# Namespace selector
st.markdown("""
<div class="namespace-selector">
    <div class="namespace-header">📁 Select Namespace</div>
    <div style="display: grid; grid-template-columns: 4fr 1fr; gap: 1rem; align-items: end;">
""", unsafe_allow_html=True)

col1, col2 = st.columns([4, 1])

with col1:
    # Sort namespaces: favorites first, then others
    favorite_namespaces = [ns for ns in fetch_namespaces() if ns in st.session_state.favorite_namespaces]
    other_namespaces = [ns for ns in fetch_namespaces() if ns not in st.session_state.favorite_namespaces]
    sorted_namespaces = favorite_namespaces + other_namespaces
    
    if not sorted_namespaces:
        st.warning("No namespaces found.")
        st.stop()
    
    namespace = st.selectbox(
        "Choose namespace", 
        sorted_namespaces,
        format_func=lambda x: f"⭐ {x}" if x in st.session_state.favorite_namespaces else x,
        key="namespace_selector",
        label_visibility="collapsed"
    )

with col2:
    if namespace in st.session_state.favorite_namespaces:
        if st.button("💔 Remove Favorite", key="remove_fav", use_container_width=True):
            remove_favorite_namespace(namespace)
            st.rerun()
    else:
        if st.button("⭐ Add Favorite", key="add_fav", use_container_width=True):
            add_favorite_namespace(namespace)
            st.rerun()

st.markdown("</div></div>", unsafe_allow_html=True)

# Pod metrics
st.markdown('<div class="section-header">📊 Pod Metrics</div>', unsafe_allow_html=True)

pods = fetch_pods(namespace)
if pods:
    # Calculate metrics
    total_pods = len(pods)
    running_pods = len([p for p in pods if p.get('status') == 'Running'])
    pending_pods = len([p for p in pods if p.get('status') == 'Pending'])
    failed_pods = len([p for p in pods if p.get('status') == 'Failed'])
    
    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card">
            <div class="metric-value">{total_pods}</div>
            <div class="metric-label">Total Pods</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{running_pods}</div>
            <div class="metric-label">Running</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{pending_pods}</div>
            <div class="metric-label">Pending</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{failed_pods}</div>
            <div class="metric-label">Failed</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.warning("No pods found in this namespace.")

# Pod explorer
st.markdown('<div class="section-header">🔍 Pod Explorer</div>', unsafe_allow_html=True)

if pods:
    st.markdown("""
    <div class="pod-grid">
    """, unsafe_allow_html=True)
    
    for pod in pods:
        pod_name = pod.get('name', 'Unknown')
        pod_status = pod.get('status', 'Unknown')
        pod_age = pod.get('age', 'Unknown')
        pod_ready = pod.get('ready', 'Unknown')
        pod_restarts = pod.get('restarts', 0)
        
        # Determine card class based on status
        if pod_status == 'Running':
            card_class = 'healthy'
            status_class = 'running'
        elif pod_status == 'Pending':
            card_class = 'warning'
            status_class = 'pending'
        elif pod_status == 'Failed':
            card_class = 'error'
            status_class = 'failed'
        else:
            card_class = 'healthy'
            status_class = 'succeeded'
        
        st.markdown(f"""
        <div class="pod-card {card_class}">
            <div class="pod-name">{pod_name}</div>
            <div class="pod-status {status_class}">{pod_status}</div>
            <div class="pod-details">Age: {pod_age}</div>
            <div class="pod-details">Ready: {pod_ready}</div>
            <div class="pod-details">Restarts: {pod_restarts}</div>
            <div class="pod-actions">
                <button class="stButton" onclick="viewLogs('{pod_name}')">📋 View Logs</button>
                <button class="stButton secondary" onclick="viewDetails('{pod_name}')">🔍 Details</button>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("No pods available to display.")

# Log viewer
st.markdown('<div class="section-header">📋 Log Viewer</div>', unsafe_allow_html=True)

st.markdown("""
<div class="log-container">
    <div class="log-header">
        <div class="log-icon">📋</div>
        <div class="log-title">Pod Logs</div>
    </div>
    <div class="log-content">
Select a pod above to view its logs in real-time.

Logs will appear here when you select a specific pod.
    </div>
</div>
""", unsafe_allow_html=True)

# Anomaly detection section
st.markdown('<div class="section-header">🚨 Anomaly Detection</div>', unsafe_allow_html=True)

df = load_anomalies_df()
if not df.empty:
    latest_anomalies = df.tail(5)
    
    st.markdown("""
    <div class="log-container">
        <div class="log-header">
            <div class="log-icon">🚨</div>
            <div class="log-title">Recent Anomalies</div>
        </div>
        <div class="log-content">
    """, unsafe_allow_html=True)
    
    for _, row in latest_anomalies.iterrows():
        st.write(f"**{row.get('timestamp', 'Unknown')}** - {row.get('prediction', 'Unknown')}")
        st.write(f"Pod: {row.get('pod_name', 'Unknown')}")
        st.write("---")
    
    st.markdown("</div></div>", unsafe_allow_html=True)
else:
    st.success("✅ No anomalies detected. All pods are running normally!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #a0aec0; padding: 2rem; font-size: 0.9rem;">
    <p style="font-weight: 600; margin-bottom: 0.5rem;">🚀 Powered by SmartOps AI | Enterprise Kubernetes Monitoring</p>
    <p style="opacity: 0.8; margin: 0;">Last updated: """ + time.strftime('%Y-%m-%d %H:%M:%S') + """</p>
</div>
""", unsafe_allow_html=True) 