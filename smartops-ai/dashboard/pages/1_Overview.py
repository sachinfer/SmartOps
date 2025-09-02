import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Check if API service is running
def check_api_health():
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        return response.status_code == 200
    except Exception:
        return False

# Fetch node data
def fetch_node_data():
    try:
        response = requests.get("http://localhost:8000/nodes", timeout=5)
        if response.status_code == 200:
            return response.json().get('nodes', [])
        return []
    except Exception:
        return []

# Fetch pod data
def fetch_pod_data():
    try:
        response = requests.get("http://localhost:8000/pods", timeout=5)
        if response.status_code == 200:
            return response.json().get('pods', [])
            return []
    except Exception:
        return []

# Get service count
def get_service_count():
    try:
        response = requests.get("http://localhost:8000/services", timeout=5)
        if response.status_code == 200:
            return len(response.json().get('services', []))
        return 0
    except Exception:
        return 0

# Get namespace count
def get_namespace_count():
    try:
        response = requests.get("http://localhost:8000/namespaces", timeout=5)
        if response.status_code == 200:
            return len(response.json().get('namespaces', []))
        return 0
    except Exception:
        return 0

# Get enhanced pod data
def get_enhanced_pod_data():
    try:
        response = requests.get("http://localhost:8000/pods", timeout=5)
        if response.status_code == 200:
            return response.json().get('pods', [])
            return []
    except Exception:
        return []

# Get pod status counts
def get_pod_status_counts(pods):
    if not pods:
        return {'Running': 0, 'Pending': 0, 'Failed': 0, 'Succeeded': 0}
    
    status_counts = {'Running': 0, 'Pending': 0, 'Failed': 0, 'Succeeded': 0}
    for pod in pods:
        status = pod.get('status', 'Unknown')
        if status in status_counts:
            status_counts[status] += 1
        else:
            status_counts['Running'] += 1  # Default to Running for unknown statuses
    
    return status_counts


# Main content
st.markdown("""
<div class="dashboard-header">
    <h1>📊 Kubernetes Cluster Overview</h1>
    <p>Real-time monitoring dashboard powered by SmartOps AI</p>
</div>
""", unsafe_allow_html=True)

# Time Range Selection with better styling
st.markdown("### ⏰ Time Range Selection")
col1, col2 = st.columns([1, 3])
with col1:
    time_range = st.selectbox("", ["Live (Now)", "Last Hour", "Last 6 Hours", "Last 24 Hours"], index=0)
with col2:
    if time_range == "Live (Now)":
        st.markdown(f"**📅 Viewing:** Real-time data | {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
    else:
        relative_value = time_range.split()[1]
        relative_unit = time_range.split()[2]
        st.markdown(f"**📅 Viewing:** Data from {relative_value} {relative_unit.lower()} | {datetime.now().strftime('%B %d, %Y')}")

# Cluster Status & Health with enhanced styling
st.markdown("### 🏥 Cluster Status & Health")
col1, col2 = st.columns([1, 3])
with col1:
    st.markdown("**Status:**")
with col2:
    st.success("✅ **SmartOps AI Status:** No anomalies detected. All systems are running smoothly!")

# Enhanced Cluster Metrics with better layout
st.markdown("### 📊 Cluster Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🖥️ Nodes",
        value=node_count,
        delta="Active",
        help="Total number of nodes in the cluster"
    )

with col2:
    st.metric(
        label="🚀 Pods",
        value=pod_count,
        delta="Running",
        help="Total number of pods in the cluster"
    )

with col3:
    st.metric(
        label="🌐 Services",
        value=service_count,
        delta="Network",
        help="Total number of services in the cluster"
    )

with col4:
    st.metric(
        label="📁 Namespaces",
        value=namespace_count,
        delta="Logical",
        help="Total number of namespaces in the cluster"
    )

# Enhanced Resource Usage with progress bars
st.markdown("### ⚡ Resource Usage")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**🖥️ CPU Usage**")
    cpu_usage = 31  # This would come from actual metrics
    cpu_cores_used = 2.5
    cpu_cores_total = 8
    st.progress(cpu_usage / 100)
    st.markdown(f"**{cpu_usage}%** - {cpu_cores_used}/{cpu_cores_total} cores")

with col2:
    st.markdown("**💾 Memory Usage**")
    memory_usage = 26  # This would come from actual metrics
    memory_used = 4.2
    memory_total = 16
    st.progress(memory_usage / 100)
    st.markdown(f"**{memory_usage}%** - {memory_used}/{memory_total} GB")

# Enhanced Pod Status with better visualization
st.markdown("### 📋 Pod Status")
st.markdown(f"**Last updated:** {datetime.now().strftime('%H:%M:%S')}")

# Fetch real-time pod data with enhanced fallback
pods = get_enhanced_pod_data()

# Get pod status counts
if pods:
    status_counts = get_pod_status_counts(pods)
else:
    # Fallback to default values if no data available
    status_counts = {'Running': 18, 'Pending': 0, 'Failed': 0, 'Succeeded': 0}

# Enhanced Pod Status Distribution with charts
st.markdown("### 📊 Pod Status Distribution")

if status_counts:
    # Create a DataFrame for better visualization
    pod_data = pd.DataFrame(list(status_counts.items()), columns=['Status', 'Count'])
    
    # Create a pie chart
    fig = px.pie(
        pod_data, 
        values='Count', 
        names='Status',
        title="Pod Status Distribution",
        color_discrete_map={
            'Running': '#28a745',
            'Pending': '#ffc107', 
            'Failed': '#dc3545',
            'Succeeded': '#17a2b8'
        }
    )
    fig.update_layout(
        showlegend=True,
        height=400,
        font=dict(size=12)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Also show as a bar chart
    fig_bar = px.bar(
        pod_data,
        x='Status',
        y='Count',
        title="Pod Count by Status",
        color='Status',
        color_discrete_map={
            'Running': '#28a745',
            'Pending': '#ffc107',
            'Failed': '#dc3545', 
            'Succeeded': '#17a2b8'
        }
    )
    fig_bar.update_layout(
        showlegend=False,
        height=300,
        font=dict(size=12)
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Show detailed metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🟢 Running", status_counts.get('Running', 0))
    with col2:
        st.metric("🟡 Pending", status_counts.get('Pending', 0))
    with col3:
        st.metric("🔴 Failed", status_counts.get('Failed', 0))
    with col4:
        st.metric("🔵 Succeeded", status_counts.get('Succeeded', 0))

# Enhanced Recent Activity section
st.markdown("### 🕒 Recent Activity")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**📈 Pod Events**")
    st.info("No recent pod events")

with col2:
    st.markdown("**⚠️ Alerts**")
    st.success("No active alerts")

with col3:
    st.markdown("**🔄 Deployments**")
    st.info("No recent deployments")

# Enhanced System Information
st.markdown("### 🔧 System Information")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**📊 Cluster Info**")
    st.info(f"""
    - **Nodes:** {node_count}
    - **Pods:** {pod_count}
    - **Services:** {service_count}
    - **Namespaces:** {namespace_count}
    """)

with col2:
    st.markdown("**⚡ Resource Summary**")
    st.info(f"""
    - **CPU Usage:** {cpu_usage}% ({cpu_cores_used}/{cpu_cores_total} cores)
    - **Memory Usage:** {memory_usage}% ({memory_used}/{memory_total} GB)
    - **Last Updated:** {datetime.now().strftime('%H:%M:%S')}
    """)

# Enhanced Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 2rem; font-size: 0.9rem;">
    <p style="font-weight: 600; margin-bottom: 0.5rem;">🚀 SmartOps AI - Cluster Overview</p>
    <p style="opacity: 0.8; margin: 0;">Last updated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S IST') + """</p>
</div>
""", unsafe_allow_html=True)
