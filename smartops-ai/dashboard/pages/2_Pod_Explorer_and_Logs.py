# -*- coding: utf-8 -*-
"""
Pod Explorer and Logs - SmartOps AI
Updated to match Deployment page styling
"""

import streamlit as st
import pandas as pd
import requests
import time

# Page config
st.set_page_config(
    page_title="Pod Explorer - SmartOps AI",
    page_icon="🛰️",
    layout="wide"
)

# Custom CSS for better styling - matching Deployment page
st.markdown("""
<style>
.section-header {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
    text-align: center;
    font-size: 1.5rem;
    font-weight: bold;
}

.dashboard-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem;
    border-radius: 15px;
    margin: 1rem 0;
    text-align: center;
}

.dashboard-header h1 {
    margin: 0;
    font-size: 2.5rem;
    font-weight: bold;
}

.dashboard-header p {
    margin: 0.5rem 0 0 0;
    font-size: 1.2rem;
    opacity: 0.9;
}
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

@st.cache_data(ttl=10)
def fetch_pod_logs(pod_name, namespace, container_name=None, tail_lines=100):
    """Fetch logs for a specific pod"""
    try:
        url = "http://localhost:8000/pod-logs"
        params = {
            "pod_name": pod_name,
            "namespace": namespace,
            "tail_lines": tail_lines
        }
        if container_name:
            params["container_name"] = container_name
            
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code == 200:
            return resp.json().get("logs", "")
        else:
            return f"Error fetching logs: {resp.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

@st.cache_data(ttl=30)
def fetch_pod_containers(pod_name, namespace):
    """Fetch container names for a pod"""
    try:
        url = "http://localhost:8000/pod-containers"
        resp = requests.get(url, params={"pod_name": pod_name, "namespace": namespace}, timeout=5)
        if resp.status_code == 200:
            return resp.json().get("containers", [])
        else:
            return []
    except Exception as e:
        return []

# Main content
st.markdown("""
<div class="dashboard-header">
    <h1>🛰️ Pod Explorer</h1>
    <p>Simple and clean pod monitoring dashboard</p>
</div>
""", unsafe_allow_html=True)

# Namespace selector
st.markdown('<div class="section-header">📁 Select Namespace</div>', unsafe_allow_html=True)

namespaces = fetch_namespaces()
if not namespaces:
    st.warning("No namespaces found.")
    st.stop()

namespace = st.selectbox("Choose namespace", namespaces, key="namespace_selector")

# Pod metrics
st.markdown('<div class="section-header">📊 Pod Overview</div>', unsafe_allow_html=True)

pods = fetch_pods(namespace)
if pods:
    # Calculate metrics
    total_pods = len(pods)
    running_pods = len([p for p in pods if p.get('status') == 'Running'])
    pending_pods = len([p for p in pods if p.get('status') == 'Pending'])
    failed_pods = len([p for p in pods if p.get('status') == 'Failed'])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Pods", total_pods)
    
    with col2:
        st.metric("Running", running_pods)
    
    with col3:
        st.metric("Pending", pending_pods)
    
    with col4:
        st.metric("Failed", failed_pods)
else:
    st.info("No pods found in this namespace.")

# Pod list
st.markdown('<div class="section-header">🔍 Pod List</div>', unsafe_allow_html=True)

if pods:
    # Create a more compact display
    for i, pod in enumerate(pods):
        pod_name = pod.get('name', 'Unknown')
        pod_status = pod.get('status', 'Unknown')
        pod_age = pod.get('age', 'Unknown')
        pod_ready = pod.get('ready', 'Unknown')
        
        # Status styling
        if pod_status == 'Running':
            status_icon = '🟢'
        elif pod_status == 'Pending':
            status_icon = '🟡'
        elif pod_status == 'Failed':
            status_icon = '🔴'
        else:
            status_icon = '⚪'
        
        # Compact display - all info on one line
        st.write(f"{status_icon} **{pod_name}** | Status: {pod_status} | Age: {pod_age} | Ready: {pod_ready}")
        
        # Only add separator if not the last pod
        if i < len(pods) - 1:
            st.markdown("---")
else:
    st.info("No pods available to display.")

# Simple log viewer
st.markdown('<div class="section-header">📋 Log Viewer</div>', unsafe_allow_html=True)

if pods:
    pod_names = [pod.get('name', 'Unknown') for pod in pods]
    selected_pod = st.selectbox("Select a pod to view logs", pod_names, key="pod_selector")
    
    # Get containers for the selected pod
    containers = fetch_pod_containers(selected_pod, namespace)
    
    # Log viewing options
    col1, col2 = st.columns(2)
    with col1:
        tail_lines = st.selectbox("Number of lines", [50, 100, 200, 500, 1000], index=1, key="tail_lines")
    
    with col2:
        container_name = None
        if containers:
            container_name = st.selectbox("Container", ["All"] + containers, key="container_selector")
            if container_name == "All":
                container_name = None
    
    if st.button("📥 Load Logs", key="load_logs"):
        with st.spinner(f"Loading logs for {selected_pod}..."):
            # Fetch actual logs
            logs = fetch_pod_logs(selected_pod, namespace, container_name, tail_lines)
            
            if logs and not logs.startswith("Error"):
                st.success(f"✅ Logs loaded successfully!")
                
                # Log display options
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown("**Log Content:**")
                with col2:
                    if st.button("🔄 Refresh", key="refresh_logs"):
                        st.rerun()
                
                # Display logs in a scrollable text area
                st.text_area(
                    "Pod Logs",
                    value=logs,
                    height=400,
                    disabled=True,
                    key="logs_display"
                )
                
                # Log statistics
                log_lines = len(logs.split('\n')) if logs else 0
                st.info(f"📊 Log Statistics: {log_lines} lines loaded | Pod: {selected_pod} | Container: {container_name or 'All'}")
                
            else:
                st.error(f"❌ Failed to load logs: {logs}")
                st.info("💡 Make sure the pod is running and the Kubernetes API is accessible")
    else:
        st.info("Select a pod and click 'Load Logs' to view its logs.")
        if containers:
            st.info(f"📦 Available containers: {', '.join(containers)}")
else:
    st.info("No pods available for log viewing.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 2rem; font-size: 0.9rem;">
    <p style="font-weight: 600; margin-bottom: 0.5rem;">🚀 SmartOps AI - Pod Explorer</p>
    <p style="opacity: 0.8; margin: 0;">Last updated: """ + time.strftime('%Y-%m-%d %H:%M:%S') + """</p>
</div>
""", unsafe_allow_html=True) 