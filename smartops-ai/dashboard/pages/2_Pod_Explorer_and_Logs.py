import streamlit as st
import pandas as pd
import requests
import pytz
import time
import sqlite3
import json
from sidebar_utils import show_sidebar

with st.sidebar:
    show_sidebar()

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

st.title("🛰️ Pod Explorer and Logs")
st.write("Explore pods and view their logs in real time.")

namespaces = fetch_namespaces()
if not namespaces:
    st.warning("No namespaces found.")
    st.stop()

# Simple star mark for favorites
st.markdown("### 📁 Select Namespace")
col1, col2 = st.columns([4, 1])

with col1:
    # Sort namespaces: favorites first, then others
    favorite_namespaces = [ns for ns in namespaces if ns in st.session_state.favorite_namespaces]
    other_namespaces = [ns for ns in namespaces if ns not in st.session_state.favorite_namespaces]
    sorted_namespaces = favorite_namespaces + other_namespaces
    
    # Add star marks to favorite namespaces
    display_namespaces = []
    for ns in sorted_namespaces:
        if ns in st.session_state.favorite_namespaces:
            display_namespaces.append(f"⭐ {ns}")
        else:
            display_namespaces.append(ns)
    
    namespace = st.selectbox(
        "Choose namespace", 
        sorted_namespaces,
        format_func=lambda x: f"⭐ {x}" if x in st.session_state.favorite_namespaces else x,
        key="namespace_selector"
    )

with col2:
    # Simple star toggle button
    if namespace in st.session_state.favorite_namespaces:
        if st.button("💔", key="remove_star", help=f"Remove {namespace} from favorites"):
            remove_favorite_namespace(namespace)
            st.success(f"Removed {namespace} from favorites!")
            st.rerun()
    else:
        if st.button("⭐", key="add_star", help=f"Add {namespace} to favorites"):
            add_favorite_namespace(namespace)
            st.success(f"Added {namespace} to favorites!")
            st.rerun()

# Show current namespace info
if namespace:
    st.info(f"**Current Namespace:** {namespace}")

pods = fetch_pods(namespace)
if not pods:
    st.warning("No pods found in this namespace.")
    st.stop()

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
auto_refresh_checkbox = st.checkbox("Live Log Streaming (auto-refresh every 5s)", value=False)
if auto_refresh_checkbox:
    def log_auto_refresh(interval_sec=5):
        if "log_last_refresh" not in st.session_state:
            st.session_state["log_last_refresh"] = time.time()
        if time.time() - st.session_state["log_last_refresh"] > interval_sec:
            st.session_state["log_last_refresh"] = time.time()
            st.rerun()
    log_auto_refresh(5)

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
            confirm = st.radio(
                "Are you sure you want to restart this pod? It will be deleted and recreated by the deployment.",
                ["No", "Yes"],
                key="confirm_restart"
            )
            if confirm == "Yes":
                resp = requests.post("http://localhost:8000/restart_pod", params={"namespace": namespace, "pod": pod})
                if resp.status_code == 200:
                    pod_action_result.success("Pod restart requested.")
                else:
                    pod_action_result.error(f"Restart failed: {resp.text}")
    with action_col2:
        if st.button("🗑️ Delete Pod", key="delete_pod"):
            confirm = st.radio(
                "Are you sure you want to delete this pod? It may not be recreated if not managed by a controller.",
                ["No", "Yes"],
                key="confirm_delete"
            )
            if confirm == "Yes":
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