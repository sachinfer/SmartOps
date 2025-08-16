import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import plotly.graph_objects as go
import pytz
import requests

# Timezone setup
IST = pytz.timezone('Asia/Kolkata')

# Cached functions
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
        return []

@st.cache_data(ttl=30)
def load_anomalies_df():
    try:
        conn = sqlite3.connect("/app/dashboard/data/data.db")
        df = pd.read_sql_query("SELECT * FROM anomalies", conn)
        conn.close()
        return df
    except Exception as e:
        return pd.DataFrame()

@st.cache_data(ttl=30)
def fetch_cluster_metrics():
    """Fetch cluster-wide metrics"""
    try:
        url = "http://localhost:8000/cluster_metrics"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return resp.json()
        else:
            # Mock data for demonstration
            return {
                "cpu_usage": 2.5, 
                "memory_usage": 4.2 * (1024**3), 
                "cpu_capacity": 8, 
                "memory_capacity": 16 * (1024**3),
                "node_count": 3,
                "pod_count": 12,
                "service_count": 8
            }
    except Exception as e:
        return {
            "cpu_usage": 2.5, 
            "memory_usage": 4.2 * (1024**3), 
            "cpu_capacity": 8, 
            "memory_capacity": 16 * (1024**3),
            "node_count": 3,
            "pod_count": 12,
            "service_count": 8
        }

@st.cache_data(ttl=30)
def fetch_node_metrics():
    """Fetch node-level metrics"""
    try:
        url = "http://localhost:8000/node_metrics"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return resp.json().get("nodes", [])
        else:
            # Mock data for demonstration
            return [
                {
                    "name": "gke-smartops-cluster-default-pool-897bf21e-l5gp",
                    "cpu_usage": 2.5,
                    "cpu_capacity": 8,
                    "memory_usage": 4.2 * (1024**3),
                    "memory_capacity": 16 * (1024**3),
                    "status": "Ready",
                    "pods": 4
                },
                {
                    "name": "gke-smartops-cluster-default-pool-897bf21e-l6gp",
                    "cpu_usage": 1.8,
                    "cpu_capacity": 8,
                    "memory_usage": 3.1 * (1024**3),
                    "memory_capacity": 16 * (1024**3),
                    "status": "Ready",
                    "pods": 3
                },
                {
                    "name": "gke-smartops-cluster-default-pool-897bf21e-l7gp",
                    "cpu_usage": 3.2,
                    "cpu_capacity": 8,
                    "memory_usage": 5.8 * (1024**3),
                    "memory_capacity": 16 * (1024**3),
                    "status": "Ready",
                    "pods": 5
                }
            ]
    except Exception as e:
        return [
            {
                "name": "gke-smartops-cluster-default-pool-897bf21e-l5gp",
                "cpu_usage": 2.5,
                "cpu_capacity": 8,
                "memory_usage": 4.2 * (1024**3),
                "memory_capacity": 16 * (1024**3),
                "status": "Ready",
                "pods": 4
            },
            {
                "name": "gke-smartops-cluster-default-pool-897bf21e-l6gp",
                "cpu_usage": 1.8,
                "cpu_capacity": 8,
                "memory_usage": 3.1 * (1024**3),
                "memory_capacity": 16 * (1024**3),
                "status": "Ready",
                "pods": 3
            },
            {
                "name": "gke-smartops-cluster-default-pool-897bf21e-l7gp",
                "cpu_usage": 3.2,
                "cpu_capacity": 8,
                "memory_usage": 5.8 * (1024**3),
                "memory_capacity": 16 * (1024**3),
                "status": "Ready",
                "pods": 5
            }
        ]

@st.cache_data(ttl=30)
def fetch_pod_status_summary():
    """Fetch pod status summary"""
    try:
        url = "http://localhost:8000/pod_status_summary"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {
                "running": 10,
                "pending": 1,
                "failed": 0,
                "succeeded": 1,
                "total": 12
            }
    except Exception as e:
        return {
            "running": 10,
            "pending": 1,
            "failed": 0,
            "succeeded": 1,
            "total": 12
        }

# Page config
st.set_page_config(
    page_title="Overview - SmartOps AI",
    page_icon="🏠",
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
.stats-container {
    display: flex;
    gap: 1.5rem;
    margin: 2rem 0;
    flex-wrap: wrap;
}
.stat-card {
    background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 15px;
    flex: 1;
    min-width: 200px;
    text-align: center;
    box-shadow: 0 8px 25px rgba(0, 184, 148, 0.2);
    transition: transform 0.3s ease;
}
.stat-card:hover {
    transform: translateY(-5px);
}
.stat-card.services {
    background: linear-gradient(135deg, #0984e3 0%, #74b9ff 100%);
    box-shadow: 0 8px 25px rgba(9, 132, 227, 0.2);
}
.stat-card.deployments {
    background: linear-gradient(135deg, #e17055 0%, #fab1a0 100%);
    box-shadow: 0 8px 25px rgba(225, 112, 85, 0.2);
}
.stat-card.nodes {
    background: linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%);
    box-shadow: 0 8px 25px rgba(108, 92, 231, 0.2);
}
.stat-number {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}
.stat-label {
    font-size: 1rem;
    opacity: 0.9;
    text-transform: uppercase;
    letter-spacing: 1px;
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
.alert-banner {
    background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 10px;
    margin: 1rem 0;
    box-shadow: 0 4px 15px rgba(231, 76, 60, 0.2);
}
.success-banner {
    background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 10px;
    margin: 1rem 0;
    box-shadow: 0 4px 15px rgba(0, 184, 148, 0.2);
}
.warning-banner {
    background: linear-gradient(135deg, #f39c12 0%, #f1c40f 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 10px;
    margin: 1rem 0;
    box-shadow: 0 4px 15px rgba(243, 156, 18, 0.2);
}
</style>
""", unsafe_allow_html=True)

# Main content
st.markdown("""
<div class="dashboard-header">
    <h1>🏠 SmartOps AI Overview</h1>
    <p>Real-time Kubernetes cluster health monitoring with AI-powered insights</p>
</div>
""", unsafe_allow_html=True)

# Fetch all data
cluster_metrics = fetch_cluster_metrics()
node_metrics = fetch_node_metrics()
pod_status = fetch_pod_status_summary()
df = load_anomalies_df()

# Overall Cluster Health Status
st.markdown('<div class="section-header">🏥 Cluster Health Status</div>', unsafe_allow_html=True)

# Calculate overall health score
health_score = 0
total_checks = 0

# CPU health check
cpu_usage_percent = (cluster_metrics['cpu_usage'] / cluster_metrics['cpu_capacity']) * 100 if cluster_metrics['cpu_capacity'] > 0 else 0
if cpu_usage_percent < 70:
    health_score += 1
total_checks += 1

# Memory health check
memory_usage_percent = (cluster_metrics['memory_usage'] / cluster_metrics['memory_capacity']) * 100 if cluster_metrics['memory_capacity'] > 0 else 0
if memory_usage_percent < 70:
    health_score += 1
total_checks += 1

# Pod health check
if pod_status['failed'] == 0:
    health_score += 1
total_checks += 1

# Node health check
healthy_nodes = sum(1 for node in node_metrics if node.get('status') == 'Ready')
if healthy_nodes == len(node_metrics):
    health_score += 1
total_checks += 1

# Anomaly health check
if df.empty or df.iloc[-1]['prediction'].lower() == 'normal':
    health_score += 1
total_checks += 1

overall_health_percent = (health_score / total_checks) * 100

# Display health status
if overall_health_percent >= 80:
    health_status = "✅ Excellent"
    health_color = "success"
    health_icon = "🟢"
elif overall_health_percent >= 60:
    health_status = "⚠️ Good"
    health_color = "warning"
    health_icon = "🟡"
else:
    health_status = "🚨 Needs Attention"
    health_color = "error"
    health_icon = "🔴"

if health_color == "success":
    st.markdown(f"""
    <div class="success-banner">
        <h3>{health_icon} {health_status} - Cluster Health: {overall_health_percent:.0f}%</h3>
        <p>Your Kubernetes cluster is operating at optimal performance. All systems are healthy and running smoothly.</p>
    </div>
    """, unsafe_allow_html=True)
elif health_color == "warning":
    st.markdown(f"""
    <div class="warning-banner">
        <h3>{health_icon} {health_status} - Cluster Health: {overall_health_percent:.0f}%</h3>
        <p>Your cluster is generally healthy but some areas need attention. Monitor resource usage closely.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="alert-banner">
        <h3>{health_icon} {health_status} - Cluster Health: {overall_health_percent:.0f}%</h3>
        <p>Your cluster requires immediate attention. Check resource usage, pod status, and node health.</p>
    </div>
    """, unsafe_allow_html=True)

# Anomaly Detection Status
if not df.empty:
    latest = df.iloc[-1]
    if latest['prediction'].lower() == 'normal':
        st.markdown("""
        <div class="success-banner">
            <h3>✅ SmartOps AI Status</h3>
            <p>No anomalies detected. All systems are running smoothly!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="alert-banner">
            <h3>🚨 SmartOps AI Alert</h3>
            <p>Anomaly detected in pod resource usage. Check the Anomaly Detection page for details.</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="success-banner">
        <h3>✅ SmartOps AI Status</h3>
        <p>No anomalies detected. All systems are running smoothly!</p>
    </div>
    """, unsafe_allow_html=True)

# Cluster Statistics
st.markdown('<div class="section-header">📊 Cluster Statistics</div>', unsafe_allow_html=True)

# Stats cards
st.markdown(f"""
<div class="stats-container">
    <div class="stat-card nodes">
        <div class="stat-number">{cluster_metrics.get('node_count', 3)}</div>
        <div class="stat-label">Nodes</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">{cluster_metrics.get('pod_count', 12)}</div>
        <div class="stat-label">Pods</div>
    </div>
    <div class="stat-card services">
        <div class="stat-number">{cluster_metrics.get('service_count', 8)}</div>
        <div class="stat-label">Services</div>
    </div>
    <div class="stat-card deployments">
        <div class="stat-number">{len(fetch_namespaces())}</div>
        <div class="stat-label">Namespaces</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Pod Status Summary
st.markdown('<div class="section-header">📋 Pod Status Summary</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Running", pod_status['running'], delta=None, delta_color="normal")
with col2:
    st.metric("Pending", pod_status['pending'], delta=None, delta_color="normal")
with col3:
    st.metric("Failed", pod_status['failed'], delta=None, delta_color="inverse")
with col4:
    st.metric("Total", pod_status['total'], delta=None, delta_color="normal")

# Resource Usage Visualization
st.markdown('<div class="section-header">📈 Resource Usage Overview</div>', unsafe_allow_html=True)

# Show notice about mock data
st.info("📊 **Note:** Currently showing demonstration data. Real-time metrics will be available once the API is fully deployed.")

# Create two columns for cluster overview
col1, col2 = st.columns(2)

with col1:
    # Cluster CPU Usage Gauge
    fig_cpu = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = cpu_usage_percent,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Cluster CPU Usage (%)"},
        delta = {'reference': 80},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 80], 'color': "yellow"},
                {'range': [80, 100], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig_cpu.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_cpu, use_container_width=True)

with col2:
    # Cluster RAM Usage Gauge
    fig_memory = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = memory_usage_percent,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Cluster RAM Usage (%)"},
        delta = {'reference': 80},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkgreen"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 80], 'color': "yellow"},
                {'range': [80, 100], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig_memory.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_memory, use_container_width=True)

# Node Health Table
st.markdown('<div class="section-header">🖥️ Node Health Status</div>', unsafe_allow_html=True)

if node_metrics:
    # Create node metrics dataframe
    node_data = []
    for node in node_metrics:
        cpu_percent = (node.get('cpu_usage', 0) / node.get('cpu_capacity', 1)) * 100
        memory_percent = (node.get('memory_usage', 0) / node.get('memory_capacity', 1)) * 100
        
        # Determine health status
        if cpu_percent < 70 and memory_percent < 70 and node.get('status') == 'Ready':
            health_status = "🟢 Healthy"
        elif cpu_percent > 80 or memory_percent > 80:
            health_status = "🔴 Critical"
        else:
            health_status = "🟡 Warning"
        
        node_data.append({
            'Node Name': node.get('name', 'Unknown'),
            'Status': node.get('status', 'Unknown'),
            'Health': health_status,
            'CPU Usage (%)': round(cpu_percent, 1),
            'Memory Usage (%)': round(memory_percent, 1),
            'CPU Cores': node.get('cpu_capacity', 0),
            'Memory (GB)': round(node.get('memory_capacity', 0) / (1024**3), 1),
            'Pods': node.get('pods', 0)
        })
    
    node_df = pd.DataFrame(node_data)
    
    # Color code the usage percentages
    def color_usage(val):
        if val > 80:
            return 'background-color: #ff6b6b; color: white;'
        elif val > 60:
            return 'background-color: #fdcb6e; color: black;'
        else:
            return 'background-color: #00b894; color: white;'
    
    st.dataframe(
        node_df.style.applymap(color_usage, subset=['CPU Usage (%)', 'Memory Usage (%)']),
        use_container_width=True
    )

# Quick Actions
st.markdown('<div class="section-header">⚡ Quick Actions</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

with col2:
    if st.button("🔥 Anomaly Detection", use_container_width=True):
        st.switch_page("pages/4_Anomaly_Detection.py")

with col3:
    if st.button("🤖 AI Actions", use_container_width=True):
        st.switch_page("pages/8_AI_Actions.py")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🚀 Powered by SmartOps AI | Real-time Kubernetes Monitoring</p>
    <p>Last updated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S IST') + """</p>
</div>
""", unsafe_allow_html=True)
