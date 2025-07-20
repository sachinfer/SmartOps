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

# Optional: Auto-refresh every 60 seconds
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=60 * 1000)
except ImportError:
    pass

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
        background: white;
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
        col1, col2 = st.columns([2, 1])
        with col1:
            selected_ns = st.selectbox(
                'Select Namespace',
                namespace_options,
                index=0,
                help="Choose a namespace to filter data, or 'all' to view everything"
            )
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔄 Refresh Data", type="primary"):
                st.rerun()

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

# --- Pod Explorer & Logs Page ---
def pod_explorer_page():
    st.title("🛰️ Pod Explorer & Logs")
    st.write("Explore pods and view their logs in real time.")

    namespaces = fetch_namespaces()
    if not namespaces:
        st.warning("No namespaces found.")
        return
    namespace = st.selectbox("Select Namespace", namespaces)

    pods = fetch_pods(namespace)
    if not pods:
        st.warning("No pods found in this namespace.")
        return

    # Show pod table with details
    pod_table = pd.DataFrame(pods)
    st.markdown("### Available Pods")
    st.dataframe(pod_table[["name", "status", "node", "restarts", "images", "containers"]], use_container_width=True)

    pod_names = [pod["name"] for pod in pods]
    pod = st.selectbox("Select Pod", pod_names)
    selected_pod = next((p for p in pods if p["name"] == pod), None)

    container = None
    if selected_pod:
        containers = selected_pod.get("containers", [])
        if len(containers) > 1:
            container = st.selectbox("Select Container", containers)
        elif len(containers) == 1:
            container = containers[0]

    # Add a refresh button
    refresh = st.button("🔄 Refresh Logs")

    # Live log streaming toggle
    auto_refresh = st.checkbox("Live Log Streaming (auto-refresh every 5s)", value=False)
    if auto_refresh:
        from streamlit_autorefresh import st_autorefresh
        st_autorefresh(interval=5000, key="log_autorefresh")

    # Log search/filter UI
    col1, col2 = st.columns([2,1])
    with col1:
        log_search = st.text_input("Search logs (keyword)", "")
    with col2:
        time_filter = st.selectbox("Time Range", ["All", "Last 5m", "Last 1h", "Last 24h"])

    # Pod actions UI
    st.markdown("### Pod Actions")
    action_col1, action_col2, action_col3 = st.columns(3)
    pod_action_result = st.empty()
    if pod:
        with action_col1:
            if st.button("🔄 Restart Pod", key="restart_pod"):
                if st.confirm("Are you sure you want to restart this pod? It will be deleted and recreated by the deployment."):
                    resp = requests.post("http://localhost:8000/restart_pod", params={"namespace": namespace, "pod": pod})
                    if resp.status_code == 200:
                        pod_action_result.success("Pod restart requested.")
                    else:
                        pod_action_result.error(f"Restart failed: {resp.text}")
        with action_col2:
            if st.button("🗑️ Delete Pod", key="delete_pod"):
                if st.confirm("Are you sure you want to delete this pod? It may not be recreated if not managed by a controller."):
                    resp = requests.post("http://localhost:8000/delete_pod", params={"namespace": namespace, "pod": pod})
                    if resp.status_code == 200:
                        pod_action_result.success("Pod deleted.")
                    else:
                        pod_action_result.error(f"Delete failed: {resp.text}")
        with action_col3:
            if st.button("🔍 Describe Pod", key="describe_pod"):
                resp = requests.get("http://localhost:8000/describe_pod", params={"namespace": namespace, "pod": pod})
                if resp.status_code == 200:
                    pod_desc = resp.json()
                    with st.expander("Pod Description (JSON)"):
                        import json
                        st.json(pod_desc)
                else:
                    pod_action_result.error(f"Describe failed: {resp.text}")

    # --- Pod Resource Graphs ---
    # Load anomalies data for pod resource usage
    pod_resource_df = pd.DataFrame()
    if not load_anomalies_df().empty and pod:
        if 'pod_name' in load_anomalies_df().columns:
            pod_resource_df = load_anomalies_df()[load_anomalies_df()['pod_name'] == pod].copy()
    if not pod_resource_df.empty:
        pod_resource_df['timestamp'] = pd.to_datetime(pod_resource_df['timestamp'])
        pod_resource_df['cpu_numeric'] = pd.to_numeric(pod_resource_df['cpu'], errors='coerce').fillna(0)
        pod_resource_df['cpu_percent'] = pod_resource_df['cpu_numeric'] * 100
        pod_resource_df['memory_numeric'] = pd.to_numeric(pod_resource_df['memory'], errors='coerce').fillna(0)
        pod_resource_df['memory_mb'] = pod_resource_df['memory_numeric'] / (1024 * 1024)
        # Convert timestamps to IST
        import pytz
        IST = pytz.timezone('Asia/Kolkata')
        pod_resource_df['timestamp_ist'] = pod_resource_df['timestamp'].dt.tz_localize('UTC').dt.tz_convert(IST)
        import plotly.graph_objects as go
        st.markdown("### Pod Resource Usage (CPU & Memory)")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=pod_resource_df['timestamp_ist'], y=pod_resource_df['cpu_percent'], mode='lines+markers', name='CPU %', line=dict(color='#667eea')))
        fig.add_trace(go.Scatter(x=pod_resource_df['timestamp_ist'], y=pod_resource_df['memory_mb'], mode='lines+markers', name='Memory MB', line=dict(color='#764ba2')))
        fig.update_layout(title=f"Resource Usage for {pod}", xaxis_title="Time (IST)", yaxis_title="Usage", legend_title="Metric", height=350)
        st.plotly_chart(fig, use_container_width=True)
    elif pod:
        st.info("No resource data available for this pod.")

    if pod:
        url = f"http://localhost:8000/logs"
        params = {"namespace": namespace, "pod": pod}
        if container:
            params["container"] = container
        logs = ""
        error = None
        if refresh or True:  # Always fetch logs on first render and on refresh
            try:
                resp = requests.get(url, params=params, timeout=10)
                data = resp.json()
                logs = data.get("logs", "")
                error = data.get("error", None)
            except Exception as e:
                error = str(e)
        if error:
            st.error(f"Error fetching logs: {error}")
        # --- Log filtering ---
        filtered_logs = logs
        if logs:
            log_lines = logs.splitlines()
            # Time filter (assume log lines start with ISO timestamp or RFC3339)
            import re, datetime
            now = datetime.datetime.utcnow()
            def line_in_time(line):
                if time_filter == "All":
                    return True
                match = re.match(r"^(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2})", line)
                if not match:
                    return True  # If no timestamp, include
                try:
                    ts = match.group(1).replace('T', ' ')
                    ts = datetime.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
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
            file_name=f"{pod}_{container if container else 'default'}_logs.txt",
            mime="text/plain"
        )
        st.text_area(f"Pod Logs ({container if container else 'default'})", filtered_logs, height=400)

# --- AI Recommendations / Pending AI Actions ---
def ai_actions_section():
    st.markdown("## 🤖 AI Recommendations (Pending Actions)")
    try:
        resp = requests.get("http://localhost:8000/ai_actions", timeout=5)
        actions = resp.json().get("actions", [])
    except Exception as e:
        st.warning(f"Could not fetch AI actions: {e}")
        actions = []
    if not actions:
        st.info("No pending AI actions.")
        return
    for action in actions:
        with st.expander(f"Pod: {action['pod_name']} | Namespace: {action['namespace']}"):
            st.write(f"**Reason:** {action['reason']}")
            st.write(f"**Timestamp:** {action['timestamp']}")
            col1, col2 = st.columns(2)
            with col1:
                confirm_btn = st.button(f"✅ Confirm Delete Pod {action['pod_name']}", key=f"confirm_{action['id']}")
            with col2:
                ignore_btn = st.button(f"🚫 Ignore", key=f"ignore_{action['id']}")
            if confirm_btn:
                with st.spinner("Deleting pod..."):
                    resp = requests.post("http://localhost:8000/confirm_ai_action", params={"action_id": action['id']})
                    if resp.status_code == 200:
                        st.success(f"Pod {action['pod_name']} deleted.")
                    else:
                        try:
                            data = resp.json()
                            if data.get("status") == "not_found":
                                st.info(data.get("error", "Pod not found."))
                                # Show Ignore button for not_found
                                if st.button(f"🚫 Ignore (mark as ignored)", key=f"ignore_notfound_{action['id']}"):
                                    resp2 = requests.post("http://localhost:8000/ignore_ai_action", params={"action_id": action['id']})
                                    if resp2.status_code == 200:
                                        st.success("Action marked as ignored.")
                                    else:
                                        st.error(f"Ignore failed: {resp2.text}")
                            else:
                                st.error(f"Delete failed: {resp.text}")
                        except Exception:
                            st.error(f"Delete failed: {resp.text}")
            if ignore_btn:
                with st.spinner("Marking as ignored..."):
                    resp = requests.post("http://localhost:8000/ignore_ai_action", params={"action_id": action['id']})
                    if resp.status_code == 200:
                        st.success("Action marked as ignored.")
                    else:
                        st.error(f"Ignore failed: {resp.text}")

# --- Model Retraining Button ---
def retrain_model_section():
    st.markdown("## 🧠 Retrain Anomaly Detection Model")
    if st.button("🔄 Retrain Model", key="retrain_model_btn"):
        with st.spinner("Retraining model... this may take a minute..."):
            try:
                resp = requests.post("http://localhost:8000/retrain_model", timeout=60)
                if resp.status_code == 200:
                    st.success("Model retrained and deployed!")
                else:
                    st.error(f"Retrain failed: {resp.text}")
            except Exception as e:
                st.error(f"Retrain error: {e}")

# --- Cluster Explorer Page ---
def cluster_explorer_page():
    st.title("🔍 Cluster Explorer")
    st.write("Run safe kubectl-like queries on your cluster.")

    # Fetch resource types and namespaces for autocomplete
    resource_types = fetch_resource_types()
    namespaces = fetch_namespaces()

    # UI for resource type and namespace
    resource = st.selectbox("Resource Type", resource_types, index=0)
    ns = st.selectbox("Namespace", ["All"] + namespaces, index=0)
    all_ns = ns == "All"
    if st.button("Fetch"):
        with st.spinner("Fetching data..."):
            try:
                params = {"resource_type": resource, "all_namespaces": str(all_ns).lower()}
                resp = requests.get("http://localhost:8000/kubectl_get", params=params, timeout=15)
                items = resp.json().get("items", [])
                if not items:
                    st.info("No results found.")
                else:
                    import pandas as pd
                    df = pd.DataFrame(items)
                    st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"Error fetching data: {e}")

# --- Kubernetes Shell Page ---
def kubernetes_shell_page():
    st.title("🖥️ Kubernetes Shell")
    st.info("Only 'kubectl get', 'kubectl describe', and 'kubectl logs' commands are allowed.")
    
    # Initialize session state for shell history and current command
    if "kube_shell_history" not in st.session_state:
        st.session_state.kube_shell_history = []
    if "last_command_output" not in st.session_state:
        st.session_state.last_command_output = ""
    if "current_command" not in st.session_state:
        st.session_state.current_command = ""
    if "history_index" not in st.session_state:
        st.session_state.history_index = -1
    
    # Terminal-like interface
    st.markdown("""
    <style>
    .terminal-container {
        background-color: #1e1e1e;
        border-radius: 8px;
        padding: 20px;
        font-family: 'Courier New', monospace;
        color: #00ff00;
        border: 1px solid #333;
        margin: 10px 0;
    }
    .terminal-prompt {
        color: #00ff00;
        font-weight: bold;
    }
    .terminal-input {
        background: transparent;
        border: none;
        color: #00ff00;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        outline: none;
        width: 100%;
    }
    .terminal-output {
        color: #ffffff;
        white-space: pre-wrap;
        font-family: 'Courier New', monospace;
        font-size: 12px;
        background-color: #2d2d2d;
        padding: 10px;
        border-radius: 4px;
        margin: 10px 0;
        max-height: 400px;
        overflow-y: auto;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Command input with history navigation
    col1, col2 = st.columns([1, 20])
    with col1:
        st.markdown('<div class="terminal-prompt">$</div>', unsafe_allow_html=True)
    with col2:
        # Create a unique key for the command input
        cmd_key = f"shell_cmd_{len(st.session_state.kube_shell_history)}"
        
        # Handle command submission
        if st.button("⏎ Execute", key="execute_btn"):
            if st.session_state.current_command.strip():
                # Add to history
                if st.session_state.current_command not in st.session_state.kube_shell_history:
                    st.session_state.kube_shell_history.append(st.session_state.current_command)
                
                # Execute command
                execute_kubectl_command(st.session_state.current_command)
                st.session_state.current_command = ""
                st.session_state.history_index = -1
                st.rerun()
        
        # Command input with placeholder
        shell_cmd = st.text_input(
            "kubectl >", 
            value=st.session_state.current_command,
            key=cmd_key,
            placeholder="Type kubectl command here...",
            help="Use ↑↓ arrows to navigate history, Enter to execute"
        )
        
        # Update current command
        if shell_cmd != st.session_state.current_command:
            st.session_state.current_command = shell_cmd
    
    # History navigation buttons
    if st.session_state.kube_shell_history:
        st.markdown("**📜 Command History Navigation:**")
        hist_cols = st.columns(5)
        with hist_cols[0]:
            if st.button("↑ Previous", key="hist_up"):
                if st.session_state.history_index < len(st.session_state.kube_shell_history) - 1:
                    st.session_state.history_index += 1
                    st.session_state.current_command = st.session_state.kube_shell_history[-(st.session_state.history_index + 1)]
                    st.rerun()
        with hist_cols[1]:
            if st.button("↓ Next", key="hist_down"):
                if st.session_state.history_index > 0:
                    st.session_state.history_index -= 1
                    st.session_state.current_command = st.session_state.kube_shell_history[-(st.session_state.history_index + 1)]
                    st.experimental_rerun()
                elif st.session_state.history_index == 0:
                    st.session_state.history_index = -1
                    st.session_state.current_command = ""
                    st.rerun()
        with hist_cols[2]:
            if st.button("🔄 Clear History", key="clear_hist"):
                st.session_state.kube_shell_history = []
                st.session_state.history_index = -1
                st.session_state.current_command = ""
                st.rerun()
        with hist_cols[3]:
            if st.button("📋 Show History", key="show_hist"):
                st.session_state.show_history = not st.session_state.get("show_history", False)
                st.rerun()
    
    # Display command history if requested
    if st.session_state.get("show_history", False) and st.session_state.kube_shell_history:
        st.markdown("#### 📜 Full Command History")
        for i, cmd in enumerate(reversed(st.session_state.kube_shell_history)):
            col1, col2, col3 = st.columns([1, 4, 1])
            with col1:
                st.markdown(f"`{len(st.session_state.kube_shell_history) - i}`")
            with col2:
                st.code(cmd, language="shell")
            with col3:
                if st.button(f"▶️", key=f"hist_exec_{i}"):
                    st.session_state.current_command = cmd
                    st.rerun()
    
    # Display last command output
    if st.session_state.last_command_output:
        st.markdown("#### 📋 Last Command Output")
        output = st.session_state.last_command_output
        st.markdown(f"**Command:** `{output['command']}`")
        
        if output['stdout']:
            st.markdown("**Output:**")
            st.markdown(f'<div class="terminal-output">{output["stdout"]}</div>', unsafe_allow_html=True)
        
        if output['stderr']:
            st.markdown("**Errors:**")
            st.error(output['stderr'])
        
        if output['returncode'] != 0:
            st.warning(f"⚠️ kubectl exited with code {output['returncode']}")

def execute_kubectl_command(shell_cmd):
    """Execute kubectl command and store results"""
    # Only allow safe kubectl commands
    allowed = ["kubectl get", "kubectl describe", "kubectl logs"]
    if not any(shell_cmd.strip().startswith(a) for a in allowed):
        st.error("Only 'kubectl get', 'kubectl describe', and 'kubectl logs' commands are allowed.")
        return
    
    with st.spinner("Running kubectl..."):
        try:
            # Remove 'kubectl' prefix for backend
            raw_cmd = shell_cmd.strip()[len("kubectl "):]
            resp = requests.post(
                "http://localhost:8000/kubectl_raw",
                params={"command": raw_cmd},
                timeout=30
            )
            
            if resp.status_code == 200:
                data = resp.json()
                stdout = data.get("stdout", "")
                stderr = data.get("stderr", "")
                returncode = data.get("returncode", 0)
                
                # Store output in session state
                st.session_state.last_command_output = {
                    "stdout": stdout,
                    "stderr": stderr,
                    "returncode": returncode,
                    "command": shell_cmd
                }
                
                # Display output
                if stdout:
                    st.success("✅ Command executed successfully!")
                    # If 'get', try to parse as table
                    if shell_cmd.strip().startswith("kubectl get") and stdout.strip():
                        import pandas as pd
                        lines = stdout.strip().splitlines()
                        if len(lines) > 1:
                            header = lines[0].split()
                            rows = [l.split() for l in lines[1:] if l.strip()]
                            try:
                                df = pd.DataFrame(rows, columns=header)
                                st.dataframe(df, use_container_width=True)
                            except Exception:
                                st.code(stdout, language="shell")
                        else:
                            st.code(stdout, language="shell")
                    else:
                        st.code(stdout, language="shell")
                
                if stderr:
                    st.error(f"⚠️ stderr: {stderr}")
                
                if returncode != 0:
                    st.warning(f"⚠️ kubectl exited with code {returncode}")
                    
            else:
                st.error(f"❌ API Error: {resp.status_code} - {resp.text}")
                
        except Exception as e:
            st.error(f"❌ Error running kubectl: {e}")

# --- Sidebar navigation ---
pages = {
    "Dashboard": dashboard_page,
    "Pod Explorer & Logs": pod_explorer_page,
    "Cluster Explorer": cluster_explorer_page,
    "Kubernetes Shell": kubernetes_shell_page
}
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
    st.markdown("<div class='sidebar-nav'>", unsafe_allow_html=True)
    page = st.radio(
        "",
        [f"{sidebar_icons[p]} {p}" for p in pages.keys()],
        index=list(pages.keys()).index("Dashboard"),
        key="nav_radio"
    )
    page = page.split(' ', 1)[1]
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-section'>", unsafe_allow_html=True)
    ai_actions_section()
    retrain_model_section()
    st.markdown("</div>", unsafe_allow_html=True)

pages[page]()
# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🚀 Powered by SmartOps AI | Real-time Kubernetes Monitoring</p>
    <p>Built with ❤️ using Streamlit and AI/ML</p>
</div>
""", unsafe_allow_html=True) 