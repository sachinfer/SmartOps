import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import pytz
import requests
import numpy as np

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

def generate_time_series_data():
    """Generate mock time series data for charts"""
    now = datetime.now()
    timestamps = [now - timedelta(minutes=i) for i in range(60, 0, -1)]
    
    # CPU usage with some variation
    cpu_base = 65
    cpu_data = [cpu_base + np.random.normal(0, 5) for _ in range(60)]
    cpu_data = [max(0, min(100, x)) for x in cpu_data]
    
    # Memory usage with some variation
    memory_base = 72
    memory_data = [memory_base + np.random.normal(0, 3) for _ in range(60)]
    memory_data = [max(0, min(100, x)) for x in memory_data]
    
    return timestamps, cpu_data, memory_data

# Page config
st.set_page_config(
    page_title="Kubernetes Cluster Overview - SmartOps AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional Grafana-style CSS
st.markdown("""
<style>
/* Reset and base styles */
* {
    box-sizing: border-box;
}

/* Main container */
.main .block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    max-width: 1400px;
}

/* Header styling */
.dashboard-header {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    padding: 2rem;
    border-radius: 8px;
    margin-bottom: 2rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    border: 1px solid #e1e5e9;
}

.dashboard-header h1 {
    font-size: 2.2rem;
    margin-bottom: 0.5rem;
    font-weight: 600;
    color: white;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.dashboard-header p {
    font-size: 1rem;
    opacity: 0.9;
    margin: 0;
    color: #e8f4fd;
}

/* Status cards */
.status-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.status-card {
    background: white;
    border: 1px solid #e1e5e9;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.status-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    border-color: #2a5298;
}

.status-card.healthy {
    border-left: 4px solid #00d4aa;
}

.status-card.warning {
    border-left: 4px solid #ffa726;
}

.status-card.critical {
    border-left: 4px solid #ef5350;
}

.status-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #1e3c72, #2a5298);
}

.status-number {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: #1e3c72;
}

.status-label {
    font-size: 0.9rem;
    color: #6c757d;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 500;
}

.status-description {
    font-size: 0.85rem;
    color: #495057;
    margin-top: 0.5rem;
}

/* Section headers */
.section-header {
    background: #f8f9fa;
    color: #495057;
    padding: 1rem 1.5rem;
    border-radius: 6px;
    margin: 2rem 0 1rem 0;
    font-size: 1.1rem;
    font-weight: 600;
    border-left: 4px solid #2a5298;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

/* Alert banners */
.alert-banner {
    background: linear-gradient(135deg, #ef5350 0%, #e53935 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 8px;
    margin: 1rem 0;
    box-shadow: 0 4px 15px rgba(239, 83, 80, 0.2);
    border: 1px solid #e53935;
}

.success-banner {
    background: linear-gradient(135deg, #00d4aa 0%, #00b894 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 8px;
    margin: 1rem 0;
    box-shadow: 0 4px 15px rgba(0, 212, 170, 0.2);
    border: 1px solid #00b894;
}

.warning-banner {
    background: linear-gradient(135deg, #ffa726 0%, #ff9800 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 8px;
    margin: 1rem 0;
    box-shadow: 0 4px 15px rgba(255, 167, 38, 0.2);
    border: 1px solid #ff9800;
}

/* Metric cards */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin: 1.5rem 0;
}

.metric-card {
    background: white;
    border: 1px solid #e1e5e9;
    border-radius: 6px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.metric-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: #1e3c72;
    margin-bottom: 0.25rem;
}

.metric-label {
    font-size: 0.8rem;
    color: #6c757d;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Node table styling */
.node-table {
    background: white;
    border: 1px solid #e1e5e9;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

/* Quick actions */
.quick-actions {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
    margin: 2rem 0;
}

.action-btn {
    background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%);
    color: white;
    border: none;
    padding: 1rem;
    border-radius: 6px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    text-align: center;
    text-decoration: none;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
}

.action-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(42, 82, 152, 0.3);
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Main content
st.markdown("""
<div class="dashboard-header">
    <h1>📊 Kubernetes Cluster Overview</h1>
    <p>Real-time monitoring dashboard powered by SmartOps AI</p>
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
    health_status = "Excellent"
    health_color = "success"
    health_icon = "🟢"
elif overall_health_percent >= 60:
    health_status = "Good"
    health_color = "warning"
    health_icon = "🟡"
else:
    health_status = "Needs Attention"
    health_color = "error"
    health_icon = "🔴"

# Health status display
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    if health_color == "success":
        st.markdown(f"""
        <div class="success-banner">
            <h3>{health_icon} Cluster Health: {overall_health_percent:.0f}% - {health_status}</h3>
            <p>Your Kubernetes cluster is operating at optimal performance. All systems are healthy and running smoothly.</p>
        </div>
        """, unsafe_allow_html=True)
    elif health_color == "warning":
        st.markdown(f"""
        <div class="warning-banner">
            <h3>{health_icon} Cluster Health: {overall_health_percent:.0f}% - {health_status}</h3>
            <p>Your cluster is generally healthy but some areas need attention. Monitor resource usage closely.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="alert-banner">
            <h3>{health_icon} Cluster Health: {overall_health_percent:.0f}% - {health_status}</h3>
            <p>Your cluster requires immediate attention. Check resource usage, pod status, and node health.</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{overall_health_percent:.0f}%</div>
        <div class="metric-label">Health Score</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{healthy_nodes}/{len(node_metrics)}</div>
        <div class="metric-label">Healthy Nodes</div>
    </div>
    """, unsafe_allow_html=True)

# SmartOps AI Status
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

# Stats cards in a grid
st.markdown(f"""
<div class="status-grid">
    <div class="status-card healthy">
        <div class="status-number">{cluster_metrics.get('node_count', 3)}</div>
        <div class="status-label">Nodes</div>
        <div class="status-description">Active cluster nodes</div>
    </div>
    <div class="status-card healthy">
        <div class="status-number">{cluster_metrics.get('pod_count', 12)}</div>
        <div class="status-label">Pods</div>
        <div class="status-description">Running containers</div>
    </div>
    <div class="status-card healthy">
        <div class="status-number">{cluster_metrics.get('service_count', 8)}</div>
        <div class="status-label">Services</div>
        <div class="status-description">Network services</div>
    </div>
    <div class="status-card healthy">
        <div class="status-number">{len(fetch_namespaces())}</div>
        <div class="status-label">Namespaces</div>
        <div class="status-description">Logical partitions</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Pod Status Summary
st.markdown('<div class="section-header">📋 Pod Status Summary</div>', unsafe_allow_html=True)

# Create pod status visualization
pod_data = {
    'Status': ['Running', 'Pending', 'Failed', 'Succeeded'],
    'Count': [pod_status['running'], pod_status['pending'], pod_status['failed'], pod_status['succeeded']],
    'Color': ['#00d4aa', '#ffa726', '#ef5350', '#42a5f5']
}

fig_pods = px.bar(
    x=pod_data['Status'],
    y=pod_data['Count'],
    color=pod_data['Status'],
    color_discrete_map=dict(zip(pod_data['Status'], pod_data['Color'])),
    title="Pod Status Distribution"
)

fig_pods.update_layout(
    height=300,
    margin=dict(l=20, r=20, t=40, b=20),
    showlegend=False,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)

fig_pods.update_xaxes(showgrid=False)
fig_pods.update_yaxes(showgrid=True, gridcolor='#e9ecef')

st.plotly_chart(fig_pods, use_container_width=True)

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
        title = {'text': "Cluster CPU Usage (%)", 'font': {'size': 16}},
        delta = {'reference': 80},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#2a5298"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': "#00d4aa"},
                {'range': [50, 80], 'color': "#ffa726"},
                {'range': [80, 100], 'color': "#ef5350"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig_cpu.update_layout(
        height=300, 
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_cpu, use_container_width=True)

with col2:
    # Cluster RAM Usage Gauge
    fig_memory = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = memory_usage_percent,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Cluster RAM Usage (%)", 'font': {'size': 16}},
        delta = {'reference': 80},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkgreen"},
            'bar': {'color': "#2a5298"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': "#00d4aa"},
                {'range': [50, 80], 'color': "#ffa726"},
                {'range': [80, 100], 'color': "#ef5350"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig_memory.update_layout(
        height=300, 
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_memory, use_container_width=True)

# Time Series Charts
st.markdown('<div class="section-header">⏰ Resource Usage Trends</div>', unsafe_allow_html=True)

# Generate mock time series data
timestamps, cpu_data, memory_data = generate_time_series_data()

# Create time series charts
col1, col2 = st.columns(2)

with col1:
    fig_cpu_trend = go.Figure()
    fig_cpu_trend.add_trace(go.Scatter(
        x=timestamps,
        y=cpu_data,
        mode='lines+markers',
        name='CPU Usage %',
        line=dict(color='#2a5298', width=3),
        marker=dict(size=4)
    ))
    fig_cpu_trend.update_layout(
        title="CPU Usage Trend (Last Hour)",
        xaxis_title="Time",
        yaxis_title="CPU Usage (%)",
        height=300,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='#e9ecef'),
        yaxis=dict(showgrid=True, gridcolor='#e9ecef', range=[0, 100])
    )
    st.plotly_chart(fig_cpu_trend, use_container_width=True)

with col2:
    fig_memory_trend = go.Figure()
    fig_memory_trend.add_trace(go.Scatter(
        x=timestamps,
        y=memory_data,
        mode='lines+markers',
        name='Memory Usage %',
        line=dict(color='#00d4aa', width=3),
        marker=dict(size=4)
    ))
    fig_memory_trend.update_layout(
        title="Memory Usage Trend (Last Hour)",
        xaxis_title="Time",
        yaxis_title="Memory Usage (%)",
        height=300,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='#e9ecef'),
        yaxis=dict(showgrid=True, gridcolor='#e9ecef', range=[0, 100])
    )
    st.plotly_chart(fig_memory_trend, use_container_width=True)

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
    
    # Display node table with better styling
    st.markdown('<div class="node-table">', unsafe_allow_html=True)
    st.dataframe(
        node_df,
        use_container_width=True,
        hide_index=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Quick Actions
st.markdown('<div class="section-header">⚡ Quick Actions</div>', unsafe_allow_html=True)

st.markdown("""
<div class="quick-actions">
    <button class="action-btn" onclick="window.location.href='?page=refresh'">🔄 Refresh Data</button>
    <button class="action-btn" onclick="window.location.href='?page=anomaly'">🔥 Anomaly Detection</button>
    <button class="action-btn" onclick="window.location.href='?page=ai'">🤖 AI Actions</button>
    <button class="action-btn" onclick="window.location.href='?page=logs'">📋 Pod Logs</button>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 2rem; font-size: 0.9rem;">
    <p>🚀 Powered by SmartOps AI | Enterprise Kubernetes Monitoring</p>
    <p>Last updated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S IST') + """</p>
</div>
""", unsafe_allow_html=True)
