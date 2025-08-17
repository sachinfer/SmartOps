# -*- coding: utf-8 -*-
"""
Pod Explorer and Logs - SmartOps AI
Simple Preview Page
"""

import streamlit as st
import pandas as pd
import requests
import time
from sidebar_utils import show_sidebar

# Page config
st.set_page_config(
    page_title="Pod Explorer - SmartOps AI",
    page_icon="🛰️",
    layout="wide"
)

# Sidebar
with st.sidebar:
    show_sidebar()

# Simple CSS for clean look
st.markdown("""
<style>
.main .block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    max-width: 1200px;
}

.stApp {
    background-color: #f8f9fa;
}

.dashboard-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 12px;
    margin-bottom: 2rem;
    color: white;
    text-align: center;
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

.section-box {
    background: white;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.section-title {
    font-size: 1.3rem;
    font-weight: 600;
    color: #495057;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.pod-card {
    background: white;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 1rem;
    margin: 0.5rem 0;
    transition: all 0.2s ease;
}

.pod-card:hover {
    border-color: #667eea;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.pod-name {
    font-weight: 600;
    color: #495057;
    margin-bottom: 0.5rem;
}

.pod-status {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.status-running {
    background: #d4edda;
    color: #155724;
}

.status-pending {
    background: #fff3cd;
    color: #856404;
}

.status-failed {
    background: #f8d7da;
    color: #721c24;
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
    margin: 1rem 0;
}

.metric-card {
    background: white;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    padding: 1rem;
    text-align: center;
}

.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: #667eea;
    margin-bottom: 0.25rem;
}

.metric-label {
    font-size: 0.8rem;
    color: #6c757d;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Simple functions
@st.cache_data(ttl=30)
def fetch_namespaces():
    try:
        url = "http://localhost:8000/namespaces"
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
        url = "http://localhost:8000/pods"
        resp = requests.get(url, params={"namespace": namespace}, timeout=5)
        if resp.status_code == 200:
            return resp.json().get("pods", [])
        else:
            return []
    except Exception as e:
        st.warning(f"Could not fetch pods: {e}")
        return []

# Main content
st.markdown("""
<div class="dashboard-header">
    <h1>🛰️ Pod Explorer</h1>
    <p>Simple and clean pod monitoring dashboard</p>
</div>
""", unsafe_allow_html=True)

# Namespace selector
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📁 Select Namespace</div>', unsafe_allow_html=True)

namespaces = fetch_namespaces()
if not namespaces:
    st.warning("No namespaces found.")
    st.stop()

namespace = st.selectbox("Choose namespace", namespaces, key="namespace_selector")
st.markdown('</div>', unsafe_allow_html=True)

# Pod metrics
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📊 Pod Overview</div>', unsafe_allow_html=True)

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
    st.info("No pods found in this namespace.")
st.markdown('</div>', unsafe_allow_html=True)

# Pod list
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🔍 Pod List</div>', unsafe_allow_html=True)

if pods:
    for pod in pods:
        pod_name = pod.get('name', 'Unknown')
        pod_status = pod.get('status', 'Unknown')
        pod_age = pod.get('age', 'Unknown')
        pod_ready = pod.get('ready', 'Unknown')
        
        # Status styling
        if pod_status == 'Running':
            status_class = 'status-running'
        elif pod_status == 'Pending':
            status_class = 'status-pending'
        elif pod_status == 'Failed':
            status_class = 'status-failed'
        else:
            status_class = 'status-running'
        
        st.markdown(f"""
        <div class="pod-card">
            <div class="pod-name">{pod_name}</div>
            <div class="pod-status {status_class}">{pod_status}</div>
            <div style="color: #6c757d; font-size: 0.9rem;">
                Age: {pod_age} | Ready: {pod_ready}
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No pods available to display.")
st.markdown('</div>', unsafe_allow_html=True)

# Simple log viewer
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📋 Log Viewer</div>', unsafe_allow_html=True)

if pods:
    pod_names = [pod.get('name', 'Unknown') for pod in pods]
    selected_pod = st.selectbox("Select a pod to view logs", pod_names, key="pod_selector")
    
    if st.button("📥 Load Logs", key="load_logs"):
        st.info(f"Loading logs for {selected_pod}...")
        st.write("**Note:** This is a preview. Log loading functionality would be implemented here.")
    else:
        st.info("Select a pod and click 'Load Logs' to view its logs.")
else:
    st.info("No pods available for log viewing.")
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 2rem; font-size: 0.9rem;">
    <p style="font-weight: 600; margin-bottom: 0.5rem;">🚀 SmartOps AI - Simple Pod Explorer</p>
    <p style="opacity: 0.8; margin: 0;">Last updated: """ + time.strftime('%Y-%m-%d %H:%M:%S') + """</p>
</div>
""", unsafe_allow_html=True) 