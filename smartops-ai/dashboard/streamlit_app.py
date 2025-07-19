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

# Helper to fetch namespaces from FastAPI backend
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
    # Main header with gradient
    st.markdown("""
    <div class="main-header">
        <h1>🚀 SmartOps AI Anomaly Detection Dashboard</h1>
        <p>Real-time Kubernetes monitoring with AI-powered anomaly detection</p>
    </div>
    """, unsafe_allow_html=True)

    # Connect to DB
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

    # Fetch namespaces for dropdown
    namespace_options = ['all'] + fetch_namespaces()
    selected_ns = st.selectbox('Select Namespace', namespace_options, index=0)

    # Namespace stats (pods/services count)
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
    ns_stats = fetch_namespace_stats(selected_ns)
    st.markdown(f"""
    <div style='display: flex; gap: 1.5rem; margin-bottom: 1.5rem;'>
        <span style='background:#00b894; color:white; border-radius:8px; padding:0.4em 1.2em; font-size:1.2rem; font-weight:bold;'>Pods: {ns_stats['pod_count']}</span>
        <span style='background:#0984e3; color:white; border-radius:8px; padding:0.4em 1.2em; font-size:1.2rem; font-weight:bold;'>Services: {ns_stats['service_count']}</span>
    </div>
    """, unsafe_allow_html=True)

    # Filter dataframe by namespace if applicable
    if has_namespace_column(df) and selected_ns != 'all':
        filtered_df = df[df['namespace'] == selected_ns].copy()
    else:
        filtered_df = df.copy()

    # Top Anomalies by CPU Usage
    st.markdown("## 🔥 Top Anomalies by CPU Usage")
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

    # Recent Anomalies
    st.markdown("## 🕒 Recent Anomalies")
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

        # Charts section
        st.markdown("## 📈 Analytics Dashboard")
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
        fig.update_layout(height=600, showlegend=False, title_text="Resource Usage Analytics")
        st.plotly_chart(fig, use_container_width=True)

    # --- AI Action History (now in main dashboard) ---
    st.markdown("## 📜 AI Action History")
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
        df = pd.DataFrame(actions)
        if not df.empty:
            df = df.rename(columns={
                "timestamp": "Timestamp",
                "pod_name": "Pod Name",
                "namespace": "Namespace",
                "reason": "Reason",
                "status": "Status"
            })
            # Summary counts
            status_counts = df["Status"].value_counts().to_dict()
            st.markdown(f"**Completed:** {status_counts.get('completed', 0)} | **Pending:** {status_counts.get('pending', 0)} | **Failed:** {status_counts.get('failed', 0)} | **Not Found:** {status_counts.get('not_found', 0)}")
            # Color-code status
            def color_status(val):
                if val == "completed":
                    return "background-color: #00b894; color: white;"
                elif val == "pending":
                    return "background-color: #fdcb6e; color: black;"
                elif val == "failed":
                    return "background-color: #d63031; color: white;"
                elif val == "not_found":
                    return "background-color: #636e72; color: white;"
                elif val == "ignored":
                    return "background-color: #b2bec3; color: black;"
                return ""
            st.dataframe(
                df[["Timestamp", "Pod Name", "Namespace", "Reason", "Status"]]
                .style.applymap(color_status, subset=["Status"]),
                use_container_width=True
            )

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

    namespaces = fetch_namespaces()
    if not namespaces:
        st.warning("No namespaces found.")
        return
    namespace = st.selectbox("Select Namespace", namespaces)

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
    anomalies_df = load_anomalies_df()
    pod_resource_df = pd.DataFrame()
    if not anomalies_df.empty and pod:
        if 'pod_name' in anomalies_df.columns:
            pod_resource_df = anomalies_df[anomalies_df['pod_name'] == pod].copy()
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
    @st.cache_data(ttl=30)
    def fetch_resource_types():
        try:
            resp = requests.get("http://localhost:8000/kubectl_resource_types", timeout=5)
            return resp.json().get("resource_types", [])
        except Exception:
            return ["pods", "services", "deployments", "nodes", "events"]
    @st.cache_data(ttl=30)
    def fetch_namespaces():
        try:
            resp = requests.get("http://localhost:8000/kubectl_namespaces", timeout=5)
            return resp.json().get("namespaces", [])
        except Exception:
            return ["default", "smartops"]
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

    st.markdown("---")
    st.markdown("### ⚠️ Raw Kubectl Command (Dev Only)")
    st.warning("This feature is for dev environments only. Use with caution! Only 'get', 'describe', 'logs' are allowed.")
    if "kubectl_history" not in st.session_state:
        st.session_state.kubectl_history = []
    raw_cmd = st.text_input("kubectl command (after 'kubectl')", "get pods -A")
    if st.button("Run kubectl command"):
        # Restrict to safe commands
        allowed = ["get", "describe", "logs"]
        if not any(raw_cmd.strip().startswith(a) for a in allowed):
            st.error("Only 'get', 'describe', 'logs' commands are allowed.")
        else:
            st.session_state.kubectl_history.insert(0, raw_cmd)
            with st.spinner("Running kubectl..."):
                try:
                    resp = requests.post(
                        "http://localhost:8000/kubectl_raw",
                        params={"command": raw_cmd},
                        timeout=30
                    )
                    data = resp.json()
                    # If 'get', try to parse as table
                    if raw_cmd.strip().startswith("get") and data.get("stdout"):
                        import pandas as pd
                        lines = data["stdout"].strip().splitlines()
                        if len(lines) > 1:
                            header = lines[0].split()
                            rows = [l.split() for l in lines[1:] if l.strip()]
                            try:
                                df = pd.DataFrame(rows, columns=header)
                                st.dataframe(df, use_container_width=True)
                            except Exception:
                                st.code(data["stdout"], language="shell")
                        else:
                            st.code(data["stdout"], language="shell")
                    else:
                        st.code(data.get("stdout", ""), language="shell")
                    if data.get("stderr"):
                        st.error(data["stderr"])
                    if data.get("returncode", 0) != 0:
                        st.warning(f"kubectl exited with code {data.get('returncode')}")
                except Exception as e:
                    st.error(f"Error running kubectl: {e}")
    # Command history
    if st.session_state.kubectl_history:
        st.markdown("#### Command History")
        for cmd in st.session_state.kubectl_history[:10]:
            if st.button(f"▶️ {cmd}", key=f"history_{cmd}"):
                st.session_state["raw_cmd"] = cmd
                st.experimental_rerun()

# --- Sidebar navigation ---
pages = {
    "Dashboard": dashboard_page,
    "Pod Explorer & Logs": pod_explorer_page,
    "Cluster Explorer": cluster_explorer_page
}
page = st.sidebar.radio("Navigate", list(pages.keys()))

# Show AI actions and retrain button in sidebar for all pages
with st.sidebar:
    ai_actions_section()
    retrain_model_section()

pages[page]()
# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🚀 Powered by SmartOps AI | Real-time Kubernetes Monitoring</p>
    <p>Built with ❤️ using Streamlit and AI/ML</p>
</div>
""", unsafe_allow_html=True) 