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

# Remove global auto_refresh(60)
# Only use auto-refresh in log-related pages/functions

# Main page title and description
st.title("🏠 Dashboard")
st.markdown("## SmartOps AI Dashboard")
st.write("Welcome to the SmartOps AI-Driven DevOps Automation & Monitoring Platform.")

# Namespace selection dropdown
namespaces = fetch_namespaces() if 'fetch_namespaces' in globals() else []
if namespaces:
    selected_ns = st.selectbox("Select Namespace", ["all"] + namespaces, key="dashboard_ns_select")
else:
    selected_ns = "all"

# Page config with modern theme
st.set_page_config(
    page_title="SmartOps AI Dashboard", 
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Timezone setup
IST = pytz.timezone('Asia/Kolkata')

def convert_to_ist(timestamp_str):
    """Convert timestamp string to India Standard Time"""
    try:
        # Parse the timestamp (assuming it's in UTC)
        if isinstance(timestamp_str, str):
            # Remove timezone info if present and parse as UTC
            if timestamp_str.endswith('Z') or '+00:00' in timestamp_str:
                dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            else:
                # Assume UTC if no timezone info
                dt = datetime.fromisoformat(timestamp_str)
                dt = pytz.utc.localize(dt)
            
            # Convert to IST
            ist_time = dt.astimezone(IST)
            return ist_time.strftime('%Y-%m-%d %H:%M:%S IST')
        else:
            return timestamp_str
    except Exception as e:
        # Return original if conversion fails
        return timestamp_str

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 0.5rem;
    }
    .alert-banner {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(255,107,107,0.3);
    }
    .success-banner {
        background: linear-gradient(135deg, #00b894 0%, #00a085 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,184,148,0.3);
    }
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Ensure deployment_events table exists
try:
    db_path = "data/deployment_events.db"
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS deployment_events (
            timestamp TEXT,
            status TEXT,
            message TEXT
        )
    """)
    conn.commit()
    conn.close()
except Exception as e:
    st.warning(f"Could not initialize deployment_events table: {e}")

# Top-level cached functions
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
def fetch_resource_types():
    try:
        resp = requests.get("http://localhost:8000/kubectl_resource_types", timeout=5)
        return resp.json().get("resource_types", [])
    except Exception:
        return ["pods", "services", "deployments", "nodes", "events"]

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

# Check if 'namespace' column exists in the anomalies table
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
        # ML-based action: if CPU > 0.8, suggest scaling CPU; if memory > 80% of 1Gi, suggest scaling memory
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

# --- Dashboard Page ---
def dashboard_page():
    import pandas as pd
    
    # Modern CSS styling
    st.markdown("""
    <style>
    /* Modern Dashboard Styling */
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
    
    /* Enhanced Selectbox Styling */
    .stSelectbox > div > div {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        border: 2px solid #3498db;
        border-radius: 10px;
        padding: 8px 12px;
        color: white;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .stSelectbox > div > div:hover {
        border-color: #5dade2;
        box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
    }
    .stSelectbox > div > div:focus {
        border-color: #2980b9;
        box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.2);
    }
    
    /* Smaller Button Styling */
    .stButton > button {
        padding: 0.3rem 0.8rem !important;
        font-size: 0.9rem !important;
        height: auto !important;
        min-height: 32px !important;
        border-radius: 6px !important;
    }
    
    /* Stats Cards */
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
    
    /* Section Headers */
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
    
    /* Data Tables */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Alert Banners */
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
    
    /* Charts Container */
    .charts-container {
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin: 2rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Modern Header
    st.markdown("""
    <div class="dashboard-header">
        <h1>🚀 SmartOps AI Dashboard</h1>
        <p>Real-time Kubernetes monitoring with AI-powered anomaly detection</p>
    </div>
    """, unsafe_allow_html=True)

    # Connect to DB and define df immediately
    conn = sqlite3.connect("/app/dashboard/data/data.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS anomalies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            cpu REAL,
            memory REAL,
            prediction TEXT,
            pod_name TEXT,
            labels TEXT
        )
    """)
    conn.commit()
    df = pd.read_sql_query("SELECT * FROM anomalies", conn)
    conn.close()

    # Enhanced Namespace Selection
    st.markdown('<div class="section-header">📊 Namespace Overview</div>', unsafe_allow_html=True)
    
    # Fetch namespaces for dropdown
    namespace_options = ['all'] + fetch_namespaces()
    
    # Create a container for the namespace selector
    ns_container = st.container()
    with ns_container:
        selected_ns = st.selectbox(
            'Select Namespace',
            namespace_options,
            index=0,
            help="Choose a namespace to filter data, or 'all' to view everything"
        )

    # Display selected namespace with visual indicator
    if selected_ns == 'all':
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            text-align: center;
            font-size: 1.2rem;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        ">
            🌐 Currently Viewing: <strong>ALL NAMESPACES</strong>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            text-align: center;
            font-size: 1.2rem;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(0, 184, 148, 0.3);
        ">
            🎯 Currently Viewing: <strong>{selected_ns.upper()}</strong> Namespace
        </div>
        """, unsafe_allow_html=True)

    # Namespace stats with modern cards
    ns_stats = fetch_namespace_stats(selected_ns)
    st.markdown(f"""
    <div class="stats-container">
        <div class="stat-card">
            <div class="stat-number">{ns_stats['pod_count']}</div>
            <div class="stat-label">Pods</div>
        </div>
        <div class="stat-card services">
            <div class="stat-number">{ns_stats['service_count']}</div>
            <div class="stat-label">Services</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Filter dataframe by namespace if applicable
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

    # Status Banner
    if filtered_df.empty:
        st.markdown("""
        <div class="success-banner">
            <h3>✅ No Data Available</h3>
            <p>No anomalies detected for the selected namespace. All systems are running smoothly!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        filtered_df['timestamp'] = pd.to_datetime(filtered_df['timestamp'])
        latest = filtered_df.iloc[-1]
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

        # Analytics Dashboard Section
        st.markdown('<div class="section-header">📈 Analytics Dashboard</div>', unsafe_allow_html=True)
        
        chart_df = filtered_df.copy()
        chart_df['cpu_numeric'] = pd.to_numeric(chart_df['cpu'], errors='coerce').fillna(0)
        chart_df['memory_numeric'] = pd.to_numeric(chart_df['memory'], errors='coerce').fillna(0)
        chart_df['cpu_percent'] = chart_df['cpu_numeric'] * 100
        chart_df['memory_mb'] = chart_df['memory_numeric'] / (1024 * 1024)
        
        def parse_anomaly_timestamp(ts):
            try:
                if pd.isna(ts):
                    return ts
                if isinstance(ts, str):
                    if 'T' in ts:
                        dt = pd.to_datetime(ts, format='ISO8601')
                        if dt.tzinfo is None:
                            dt = pytz.utc.localize(dt)
                        return dt.astimezone(IST)
                    else:
                        dt = pd.to_datetime(ts)
                        if dt.tzinfo is None:
                            dt = pytz.utc.localize(dt)
                        return dt.astimezone(IST)
                else:
                    if ts.tzinfo is None:
                        ts = pytz.utc.localize(ts)
                    return ts.astimezone(IST)
            except Exception:
                return ts
        
        chart_df['timestamp_ist'] = chart_df['timestamp'].apply(parse_anomaly_timestamp)
        
        # Charts in a modern container
        st.markdown('<div class="charts-container">', unsafe_allow_html=True)
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('CPU Usage Over Time (IST)', 'Memory Usage Over Time (IST)', 'CPU Distribution', 'Memory Distribution'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        fig.add_trace(
            go.Scatter(x=chart_df['timestamp_ist'], y=chart_df['cpu_percent'], 
                      mode='lines+markers', name='CPU %', line=dict(color='#667eea')),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=chart_df['timestamp_ist'], y=chart_df['memory_mb'], 
                      mode='lines+markers', name='Memory MB', line=dict(color='#764ba2')),
            row=1, col=2
        )
        fig.add_trace(
            go.Histogram(x=chart_df['cpu_percent'], name='CPU Distribution', 
                        marker_color='#667eea', opacity=0.7),
            row=2, col=1
        )
        fig.add_trace(
            go.Histogram(x=chart_df['memory_mb'], name='Memory Distribution', 
                        marker_color='#764ba2', opacity=0.7),
            row=2, col=2
        )
        
        fig.update_layout(
            height=600, 
            showlegend=False, 
            title_text="Resource Usage Analytics",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#2c3e50')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # AI Action History Section
    st.markdown('<div class="section-header">📜 AI Action History</div>', unsafe_allow_html=True)
    
    try:
        resp = requests.get("http://localhost:8000/ai_actions", params={"all": "true"}, timeout=5)
        actions = resp.json().get("actions", [])
    except Exception as e:
        st.warning(f"Could not fetch AI action history: {e}")
        actions = []
    
    if not actions:
        st.info("No AI actions in history.")
    else:
        import pandas as pd
        actions_df = pd.DataFrame(actions)
        if not actions_df.empty:
            actions_df = actions_df.rename(columns={
                "timestamp": "Timestamp",
                "pod_name": "Pod Name",
                "namespace": "Namespace",
                "reason": "Reason",
                "status": "Status"
            })
            # Summary counts
            status_counts = actions_df["Status"].value_counts().to_dict()
            st.markdown(f"**Completed:** {status_counts.get('completed', 0)} | **Pending:** {status_counts.get('pending', 0)} | **Failed:** {status_counts.get('failed', 0)} | **Not Found:** {status_counts.get('not_found', 0)}")
            
            # Color-code status
            def color_status(val):
                if val == "completed":
                    return "background-color: #00b894; color: white;"
                elif val == "pending":
                    return "background-color: #fdcb6e; color: black;"
                elif val == "failed":
                    return "background-color: #e74c3c; color: white;"
                elif val == "not_found":
                    return "background-color: #95a5a6; color: white;"
                else:
                    return ""
            
            st.dataframe(actions_df.style.applymap(color_status, subset=['Status']), use_container_width=True)

    # --- Deployment Workflow Events Summary ---
    try:
        db_path = "data/deployment_events.db"
        conn = sqlite3.connect(db_path)
        events = pd.read_sql_query("SELECT * FROM deployment_events ORDER BY timestamp DESC", conn)
        conn.close()
        if not events.empty:
            # Count by status
            status_counts = events["status"].value_counts().to_dict()
            st.markdown(f"""
            <div style='display: flex; align-items: center; gap: 1rem;'>
                <span style='font-size:2rem; font-weight:bold;'>🚀 Deployment Workflow Events</span>
                <span style='background:#00b894; color:white; border-radius:8px; padding:0.3em 0.8em; font-weight:bold;'>Successful: {status_counts.get('success', 0)}</span>
                <span style='background:#d63031; color:white; border-radius:8px; padding:0.3em 0.8em; font-weight:bold;'>Failed: {status_counts.get('failed', 0)}</span>
                <span style='background:#fdcb6e; color:#222; border-radius:8px; padding:0.3em 0.8em; font-weight:bold;'>Started: {status_counts.get('started', 0)}</span>
            </div>
            """, unsafe_allow_html=True)
            # (existing event table code follows)
            # Convert timestamps to IST
            def parse_deployment_timestamp(ts_str):
                try:
                    if pd.isna(ts_str):
                        return ts_str
                    if isinstance(ts_str, str):
                        if 'T' in ts_str:
                            dt = pd.to_datetime(ts_str, format='ISO8601')
                            if dt.tzinfo is None:
                                dt = pytz.utc.localize(dt)
                            return dt
                        else:
                            dt = pd.to_datetime(ts_str)
                            if dt.tzinfo is None:
                                dt = pytz.utc.localize(dt)
                            return dt
                    else:
                        if ts_str.tzinfo is None:
                            ts_str = pytz.utc.localize(ts_str)
                        return ts_str
                except Exception:
                    return pd.to_datetime(ts_str)
            events['timestamp_ist'] = events['timestamp'].apply(parse_deployment_timestamp)
            events['timestamp_ist'] = events['timestamp_ist'].apply(lambda x: x.astimezone(IST) if hasattr(x, 'astimezone') else x)
            events = events.rename(columns={'timestamp_ist': 'Timestamp (IST)', 'status': 'Status', 'message': 'Message', 'namespace': 'Namespace'})
            st.dataframe(events[['Timestamp (IST)', 'Status', 'Message', 'Namespace']], use_container_width=True)
        else:
            st.markdown("""
            <div style='display: flex; align-items: center; gap: 1rem;'>
                <span style='font-size:2rem; font-weight:bold;'>🚀 Deployment Workflow Events</span>
                <span style='background:#00b894; color:white; border-radius:8px; padding:0.3em 0.8em; font-weight:bold;'>Successful: 0</span>
                <span style='background:#d63031; color:white; border-radius:8px; padding:0.3em 0.8em; font-weight:bold;'>Failed: 0</span>
                <span style='background:#fdcb6e; color:#222; border-radius:8px; padding:0.3em 0.8em; font-weight:bold;'>Started: 0</span>
            </div>
            """, unsafe_allow_html=True)
            st.info("No deployment events found.")
    except Exception as e:
        st.warning(f"Could not load deployment events: {e}")

# --- Sidebar navigation ---
# --- Commented out: Unwanted or now-multipage logic ---
# pages = {
#     "Dashboard": dashboard_page,
#     "Pod Explorer & Logs": pod_explorer_page,
#     "Cluster Explorer": cluster_explorer_page,
#     "Kubernetes Shell": kubernetes_shell_page
# }
# --- Enhanced Sidebar navigation ---
st.markdown("""
<style>
/* Sidebar styling */
section[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    height: 100vh;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    border-top-right-radius: 20px;
    border-bottom-right-radius: 20px;
    box-shadow: 2px 0 16px rgba(102,126,234,0.08);
}
.sidebar-logo {
    text-align: center;
    margin-bottom: 2rem;
}
.sidebar-logo span {
    font-size: 2.2rem;
    display: block;
}
.sidebar-logo .project {
    font-size: 1.3rem;
    font-weight: bold;
    color: #fff;
    letter-spacing: 1px;
}
.sidebar-logo .subtitle {
    font-size: 0.9rem;
    color: #dfe6e9;
}
.sidebar-nav {
    margin-bottom: 2rem;
}
.sidebar-nav label {
    font-size: 1.1rem;
    font-weight: bold;
    color: #fff;
    margin-bottom: 0.5rem;
    display: block;
}
.sidebar-nav .stRadio > div {
    flex-direction: column;
}
.sidebar-nav .stRadio label {
    padding: 0.7em 1.2em;
    border-radius: 8px;
    margin-bottom: 0.3em;
    transition: background 0.2s;
    cursor: pointer;
}
.sidebar-nav .stRadio label[data-selected="true"] {
    background: #fff;
    color: #764ba2;
    font-weight: bold;
}
.sidebar-nav .stRadio label:hover {
    background: #a29bfe;
    color: #fff;
}
.sidebar-section {
    border-top: 1px solid #dfe6e9;
    margin-top: 1.5rem;
    padding-top: 1.2rem;
}
/* Main content padding */
section.main > div.block-container {
    padding-left: 2.5rem;
    padding-right: 2.5rem;
}
</style>
""", unsafe_allow_html=True)

sidebar_icons = {
    "Dashboard": "🏠",
    "Pod Explorer & Logs": "🛰️",
    "Cluster Explorer": "🔍",
    "Kubernetes Shell": "🖥️"
}
with st.sidebar:
    st.markdown("""
    <div class='sidebar-logo'>
        <span>🚀</span>
        <span class='project'>SmartOps</span>
        <div class='subtitle'>AI Kubernetes Platform</div>
    </div>
    """, unsafe_allow_html=True)
    # --- Commented out: Unwanted or now-multipage logic ---
    # ai_actions_section()
    # retrain_model_section()

# Main page title and description
st.title("🏠 Dashboard")
st.markdown("## SmartOps AI Dashboard")
st.write("Welcome to the SmartOps AI-Driven DevOps Automation & Monitoring Platform.")

# Namespace selection dropdown
namespaces = fetch_namespaces() if 'fetch_namespaces' in globals() else []
if namespaces:
    selected_ns = st.selectbox("Select Namespace", ["all"] + namespaces, key="dashboard_ns_select")
else:
    selected_ns = "all"

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🚀 Powered by SmartOps AI | Real-time Kubernetes Monitoring</p>
    <p>Built with ❤️ using Streamlit and AI/ML</p>
</div>
""", unsafe_allow_html=True) 