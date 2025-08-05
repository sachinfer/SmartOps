import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
from typing import Tuple
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pytz
import requests
import time

# Timezone setup
IST = pytz.timezone('Asia/Kolkata')

def convert_to_ist(timestamp_str):
    """Convert timestamp string to India Standard Time"""
    try:
        if isinstance(timestamp_str, str):
            if timestamp_str.endswith('Z') or '+00:00' in timestamp_str:
                dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            else:
                dt = datetime.fromisoformat(timestamp_str)
                dt = pytz.utc.localize(dt)
            ist_time = dt.astimezone(IST)
            return ist_time.strftime('%Y-%m-%d %H:%M:%S IST')
        else:
            return timestamp_str
    except Exception as e:
        return timestamp_str

# Cached functions
@st.cache_data(ttl=30)
def fetch_namespace_stats(ns):
    try:
        url = f"http://localhost:8000/namespace_stats"
        resp = requests.get(url, params={"namespace": ns}, timeout=5)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {"pod_count": 0, "service_count": 0}
    except Exception as e:
        st.warning(f"Could not fetch namespace stats: {e}")
        return {"pod_count": 0, "service_count": 0}

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
def load_anomalies_df():
    try:
        conn = sqlite3.connect("/app/dashboard/data/data.db")
        df = pd.read_sql_query("SELECT * FROM anomalies", conn)
        conn.close()
        return df
    except Exception as e:
        st.warning(f"Could not load anomalies data: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=30)
def fetch_cluster_metrics():
    """Fetch cluster-wide CPU and RAM metrics"""
    try:
        url = "http://localhost:8000/cluster_metrics"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {"cpu_usage": 0, "memory_usage": 0, "cpu_capacity": 1, "memory_capacity": 1}
    except Exception as e:
        st.warning(f"Could not fetch cluster metrics: {e}")
        return {"cpu_usage": 0, "memory_usage": 0, "cpu_capacity": 1, "memory_capacity": 1}

@st.cache_data(ttl=30)
def fetch_node_metrics():
    """Fetch node-level CPU and RAM metrics"""
    try:
        url = "http://localhost:8000/node_metrics"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return resp.json().get("nodes", [])
        else:
            return []
    except Exception as e:
        st.warning(f"Could not fetch node metrics: {e}")
        return []

@st.cache_data(ttl=30)
def fetch_pods(namespace):
    """Fetch pods for a specific namespace"""
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
def fetch_pod_logs(namespace, pod_name, container=None):
    """Fetch logs for a specific pod"""
    try:
        url = f"http://localhost:8000/logs"
        params = {"namespace": namespace, "pod": pod_name}
        if container:
            params["container"] = container
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code == 200:
            return resp.json().get("logs", "")
        else:
            return ""
    except Exception as e:
        st.warning(f"Could not fetch logs: {e}")
        return ""

def has_namespace_column(df):
    return 'namespace' in df.columns

def get_status_and_advice(latest_pred: str, cpu: float, memory: float) -> Tuple[str, str, str, str]:
    if latest_pred.lower() == "normal":
        return (
            "✅ All systems healthy!",
            "The system is operating normally. No action needed.",
            "success",
            "No action needed"
        )
    else:
        cpu_val = float(cpu)
        mem_val = float(memory)
        mem_gi = 1024*1024*1024
        if cpu_val > 0.8:
            action = "High CPU usage detected. Consider scaling up CPU resources for the affected pod."
        elif mem_val > 0.8 * mem_gi:
            action = "High memory usage detected. Consider scaling up memory resources for the affected pod."
        else:
            action = "Unusual resource usage detected. Check pod logs and recent deployments."
        return (
            "🚨 SmartOps Anomaly Detected!",
            "Anomaly detected in pod resource usage. " + action,
            "error",
            action
        )

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
</style>
""", unsafe_allow_html=True)

# Main content
st.markdown("""
<div class="dashboard-header">
    <h1>🏠 SmartOps AI Overview</h1>
    <p>Real-time Kubernetes monitoring with AI-powered anomaly detection</p>
</div>
""", unsafe_allow_html=True)

# Namespace selection
st.markdown('<div class="section-header">📊 Namespace Overview</div>', unsafe_allow_html=True)
namespace_options = ['all'] + fetch_namespaces()
selected_ns = st.selectbox('Select Namespace', namespace_options, index=0)

# Stats cards
stats = fetch_namespace_stats(selected_ns)
st.markdown(f"""
<div class="stats-container">
    <div class="stat-card">
        <div class="stat-number">{stats['pod_count']}</div>
        <div class="stat-label">Pods</div>
    </div>
    <div class="stat-card services">
        <div class="stat-number">{stats['service_count']}</div>
        <div class="stat-label">Services</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Status banner
df = load_anomalies_df()
if not df.empty:
    latest = df.iloc[-1]
    cpu_val = pd.to_numeric(latest['cpu'], errors='coerce') if pd.notna(latest['cpu']) else 0.0
    mem_val = pd.to_numeric(latest['memory'], errors='coerce') if pd.notna(latest['memory']) else 0.0
    status, advice, banner_type, latest_action = get_status_and_advice(latest['prediction'], cpu_val, mem_val)
    
    if banner_type == 'error':
        st.markdown(f"""
        <div class="alert-banner">
            <h3>🚨 {status}</h3>
            <p>{advice}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="success-banner">
            <h3>✅ {status}</h3>
            <p>{advice}</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="success-banner">
        <h3>✅ No Data Available</h3>
        <p>No anomalies detected. All systems are running smoothly!</p>
    </div>
    """, unsafe_allow_html=True)

# Cluster CPU and RAM Visualization
st.markdown('<div class="section-header">📊 Cluster CPU & RAM Visualization</div>', unsafe_allow_html=True)

# Fetch cluster metrics
cluster_metrics = fetch_cluster_metrics()
node_metrics = fetch_node_metrics()

# Create two columns for cluster overview
col1, col2 = st.columns(2)

with col1:
    # Cluster CPU Usage Gauge
    cpu_usage_percent = (cluster_metrics['cpu_usage'] / cluster_metrics['cpu_capacity']) * 100 if cluster_metrics['cpu_capacity'] > 0 else 0
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
    memory_usage_percent = (cluster_metrics['memory_usage'] / cluster_metrics['memory_capacity']) * 100 if cluster_metrics['memory_capacity'] > 0 else 0
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

# Node-level metrics table
if node_metrics:
    st.markdown('<div class="section-header">🖥️ Node-Level Resource Usage</div>', unsafe_allow_html=True)
    
    # Create node metrics dataframe
    node_data = []
    for node in node_metrics:
        node_data.append({
            'Node Name': node.get('name', 'Unknown'),
            'CPU Usage (%)': round((node.get('cpu_usage', 0) / node.get('cpu_capacity', 1)) * 100, 1),
            'Memory Usage (%)': round((node.get('memory_usage', 0) / node.get('memory_capacity', 1)) * 100, 1),
            'CPU Cores': node.get('cpu_capacity', 0),
            'Memory (GB)': round(node.get('memory_capacity', 0) / (1024**3), 1),
            'Status': node.get('status', 'Unknown')
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

# Historical resource usage trends (if anomaly data is available)
if not df.empty:
    st.markdown('<div class="section-header">📈 Resource Usage Trends</div>', unsafe_allow_html=True)
    
    # Prepare data for trends
    chart_df = df.copy()
    # Handle different timestamp formats more flexibly
    try:
        chart_df['timestamp'] = pd.to_datetime(chart_df['timestamp'], format='mixed', errors='coerce')
    except:
        # Fallback to more flexible parsing
        chart_df['timestamp'] = pd.to_datetime(chart_df['timestamp'], errors='coerce')
    
    chart_df['cpu_numeric'] = pd.to_numeric(chart_df['cpu'], errors='coerce').fillna(0)
    chart_df['cpu_percent'] = chart_df['cpu_numeric'] * 100
    chart_df['memory_numeric'] = pd.to_numeric(chart_df['memory'], errors='coerce').fillna(0)
    chart_df['memory_mb'] = chart_df['memory_numeric'] / (1024 * 1024)
    
    # Convert timestamps to IST with error handling
    try:
        # Remove any rows with invalid timestamps
        chart_df = chart_df.dropna(subset=['timestamp'])
        if not chart_df.empty:
            # Handle timezone conversion
            if chart_df['timestamp'].dt.tz is None:
                chart_df['timestamp_ist'] = chart_df['timestamp'].dt.tz_localize('UTC').dt.tz_convert(IST)
            else:
                chart_df['timestamp_ist'] = chart_df['timestamp'].dt.tz_convert(IST)
        else:
            st.warning("No valid timestamp data found for trends chart.")
            st.stop()
    except Exception as e:
        st.warning(f"Error processing timestamps: {e}")
        st.stop()
    
    # Validate data before creating chart
    if chart_df.empty or len(chart_df) < 2:
        st.warning("Insufficient data for trends chart. Need at least 2 data points.")
        st.stop()
    
    # Create trend chart
    fig_trends = make_subplots(
        rows=2, cols=1,
        subplot_titles=('CPU Usage Trend (IST)', 'Memory Usage Trend (IST)'),
        vertical_spacing=0.1
    )
    
    fig_trends.add_trace(
        go.Scatter(
            x=chart_df['timestamp_ist'], 
            y=chart_df['cpu_percent'],
            mode='lines+markers',
            name='CPU %',
            line=dict(color='#667eea', width=2),
            marker=dict(size=4)
        ),
        row=1, col=1
    )
    
    fig_trends.add_trace(
        go.Scatter(
            x=chart_df['timestamp_ist'], 
            y=chart_df['memory_mb'],
            mode='lines+markers',
            name='Memory MB',
            line=dict(color='#764ba2', width=2),
            marker=dict(size=4)
        ),
        row=2, col=1
    )
    
    fig_trends.update_layout(
        height=500,
        showlegend=False,
        title_text="Resource Usage Trends Over Time",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50')
    )
    
    fig_trends.update_xaxes(title_text="Time (IST)", row=1, col=1)
    fig_trends.update_xaxes(title_text="Time (IST)", row=2, col=1)
    fig_trends.update_yaxes(title_text="CPU Usage (%)", row=1, col=1)
    fig_trends.update_yaxes(title_text="Memory Usage (MB)", row=2, col=1)
    
    st.plotly_chart(fig_trends, use_container_width=True)

# Pod Explorer & Logs Section
st.markdown('<div class="section-header">🛰️ Pod Explorer & Logs</div>', unsafe_allow_html=True)
st.write("Explore pods and view their logs in real time.")

# Pod Explorer namespace selection
pod_namespace_options = fetch_namespaces()
if not pod_namespace_options:
    st.warning("No namespaces found.")
else:
    pod_namespace = st.selectbox("Select Namespace", pod_namespace_options, key="pod_explorer_ns")
    
    # Fetch pods for selected namespace
    pods = fetch_pods(pod_namespace)
    if not pods:
        st.warning("No pods found in this namespace.")
    else:
        # Show pod table with details
        pod_table = pd.DataFrame(pods)
        st.markdown("### Available Pods")
        
        # Select columns to display
        display_columns = ["name", "status", "node", "restarts", "images", "containers"]
        available_columns = [col for col in display_columns if col in pod_table.columns]
        
        if available_columns:
            st.dataframe(pod_table[available_columns], use_container_width=True)
        
        # Pod selection for logs
        pod_names = [pod["name"] for pod in pods]
        selected_pod = st.selectbox("Select Pod for Logs", pod_names, key="pod_selector")
        
        if selected_pod:
            # Get selected pod details
            pod_details = next((p for p in pods if p["name"] == selected_pod), None)
            
            if pod_details:
                # Container selection
                containers = pod_details.get("containers", [])
                selected_container = None
                if len(containers) > 1:
                    selected_container = st.selectbox("Select Container", containers, key="container_selector")
                elif len(containers) == 1:
                    selected_container = containers[0]
                
                # Log controls
                col1, col2 = st.columns([2, 1])
                with col1:
                    log_search = st.text_input("Search logs (keyword)", key="log_search")
                with col2:
                    time_filter = st.selectbox("Time Range", ["All", "Last 5m", "Last 1h", "Last 24h"], key="time_filter")
                
                # Refresh button
                refresh_logs = st.button("🔄 Refresh Logs", key="refresh_logs")
                
                # Fetch and display logs
                if refresh_logs or st.session_state.get("auto_refresh", False):
                    with st.spinner("Fetching logs..."):
                        logs = fetch_pod_logs(pod_namespace, selected_pod, selected_container)
                        
                        if logs:
                            # Log filtering
                            filtered_logs = logs
                            log_lines = logs.splitlines()
                            
                            # Time filter
                            if time_filter != "All":
                                import re
                                now = datetime.utcnow()
                                def line_in_time(line):
                                    if time_filter == "All":
                                        return True
                                    match = re.match(r"^(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2})", line)
                                    if not match:
                                        return True
                                    try:
                                        ts = match.group(1).replace('T', ' ')
                                        ts = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
                                    except Exception:
                                        return True
                                    delta = now - ts
                                    if time_filter == "Last 5m":
                                        return delta.total_seconds() <= 300
                                    elif time_filter == "Last 1h":
                                        return delta.total_seconds() <= 3600
                                    elif time_filter == "Last 24h":
                                        return delta.total_seconds() <= 86400
                                    return True
                                
                                filtered_lines = [l for l in log_lines if line_in_time(l)]
                                
                                # Keyword filter
                                if log_search:
                                    filtered_lines = [l for l in filtered_lines if log_search.lower() in l.lower()]
                                
                                filtered_logs = "\n".join(filtered_lines)
                            
                            # Download button
                            st.download_button(
                                label="⬇️ Download Logs as .txt",
                                data=filtered_logs,
                                file_name=f"{selected_pod}_{selected_container if selected_container else 'default'}_logs.txt",
                                mime="text/plain"
                            )
                            
                            # Display logs
                            st.text_area(
                                f"Pod Logs ({selected_container if selected_container else 'default'})",
                                filtered_logs,
                                height=400,
                                key="log_display"
                            )
                        else:
                            st.info("No logs available for this pod.")
                
                # Auto-refresh toggle
                auto_refresh = st.checkbox("Live Log Streaming (auto-refresh every 5s)", key="auto_refresh")
                if auto_refresh:
                    st.session_state["auto_refresh"] = True
                    time.sleep(5)
                    st.experimental_rerun()
                else:
                    st.session_state["auto_refresh"] = False 