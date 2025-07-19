import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
from typing import Tuple
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pytz
import requests

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="SmartOps AI Dashboard", 
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- TIMEZONE ---
IST = pytz.timezone('Asia/Kolkata')

# --- STATE INIT ---
if 'show_pods' not in st.session_state:
    st.session_state['show_pods'] = False

def toggle_show_pods():
    st.session_state['show_pods'] = not st.session_state['show_pods']

# --- CONVERT TO IST ---
def convert_to_ist(timestamp_str):
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
    except Exception:
        return timestamp_str

# --- CSS ---
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
</style>
""", unsafe_allow_html=True)

# --- AUTO REFRESH ---
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=60000)
except ImportError:
    pass

# --- HEADER ---
st.markdown("""
<div class="main-header">
    <h1>🚀 SmartOps AI Anomaly Detection Dashboard</h1>
    <p>Real-time Kubernetes monitoring with AI-powered anomaly detection</p>
</div>
""", unsafe_allow_html=True)

# --- DATABASE CONNECTION ---
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

# --- STATUS ADVICE LOGIC ---
def get_status_and_advice(latest_pred: str, cpu: float, memory: float) -> Tuple[str, str, str, str]:
    if latest_pred.lower() == "normal":
        return ("✅ All systems healthy!",
                "The system is operating normally. No action needed.",
                "success", "No action needed")
    cpu_val = float(cpu)
    mem_val = float(memory)
    mem_gi = 1024*1024*1024
    if cpu_val > 0.8:
        action = "High CPU usage detected. Consider scaling up CPU resources for the affected pod."
    elif mem_val > 0.8 * mem_gi:
        action = "High memory usage detected. Consider scaling up memory resources for the affected pod."
    else:
        action = "Unusual resource usage detected. Check pod logs and recent deployments."
    return ("🚨 SmartOps Anomaly Detected!",
            "Anomaly detected in pod resource usage. " + action,
            "error", action)

# --- FETCH NAMESPACES ---
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

# --- FETCH PODS ---
@st.cache_data(ttl=30)
def fetch_pods(namespace: str):
    try:
        url = f"http://localhost:8000/pods"
        if namespace != "all":
            url += f"?namespace={namespace}"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return resp.json().get('pods', [])
        else:
            return []
    except Exception as e:
        st.warning(f"Failed to fetch pods: {e}")
        return []

# --- FILTER NAMESPACE ---
namespace_options = ['all'] + fetch_namespaces()
selected_ns = st.selectbox('Select Namespace', namespace_options, index=0)

def has_namespace_column(df):
    return 'namespace' in df.columns

if has_namespace_column(df) and selected_ns != 'all':
    filtered_df = df[df['namespace'] == selected_ns].copy()
else:
    filtered_df = df.copy()

# --- METRIC CARDS SECTION ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>📊 Total Anomalies</h3>
        <h2>{len(filtered_df)}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    anomaly_count = (filtered_df['prediction'].str.lower() != 'normal').sum() if not filtered_df.empty else 0
    st.markdown(f"""
    <div class="metric-card">
        <h3>🎉 Active Anomalies</h3>
        <h2>{anomaly_count}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    if not filtered_df.empty:
        filtered_df['timestamp'] = pd.to_datetime(filtered_df['timestamp'])
        latest_time = filtered_df['timestamp'].max()
        if latest_time.tzinfo is None:
            latest_time = pytz.utc.localize(latest_time)
        ist_latest_time = latest_time.astimezone(IST)
        current_ist = datetime.now(IST)
        time_ago = current_ist - ist_latest_time
        minutes_ago = int(time_ago.total_seconds() / 60)
        st.markdown(f"""
        <div class="metric-card">
            <h3>⏰ Last Update</h3>
            <h2>{minutes_ago}m ago</h2>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="metric-card">
            <h3>⏰ Last Update</h3>
            <h2>N/A</h2>
        </div>
        """, unsafe_allow_html=True)

with col4:
    pods_data = fetch_pods(selected_ns)
    available_pods_count = len(pods_data)
    card_style = (
        "background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); "
        "padding: 1.5rem; border-radius: 15px; color: white; text-align: center; "
        "box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 0.5rem; cursor: pointer;"
    )
    card_html = f"""
    <button style='{card_style} border: none; width: 100%; font-size: 1.2em;' onclick="window.parent.postMessage('togglePods', '*');">
        <h3 style='margin-bottom:0.5em;'>🛰️ Available Pods</h3>
        <h2 style='margin:0;'>{available_pods_count}</h2>
        <div style='font-size:0.9em; color:#fff; margin-top:0.5em;'>Click to show/hide pods table</div>
    </button>
    """
    st.markdown(card_html, unsafe_allow_html=True)
    if st.button("", key="hidden_show_pods", help="Show pods table"):
        toggle_show_pods()

if st.session_state.get('show_pods', False):
    st.markdown('### 🛰️ All Available Pods')
    pods_df = pd.DataFrame(pods_data)
    if not pods_df.empty:
        display_cols = ['name', 'namespace', 'status', 'node', 'start_time', 'restarts', 'images']
        display_cols = [col for col in display_cols if col in pods_df.columns]
        st.dataframe(pods_df[display_cols], use_container_width=True)
    else:
        st.info("No pods available for the selected namespace.")

# You can continue the rest of your dashboard from here, including:
# - Anomaly tables
# - Trend charts
# - Deployment events summary
# - System summary messages
# - Footer etc.

