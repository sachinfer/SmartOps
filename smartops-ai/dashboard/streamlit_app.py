import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
from typing import Tuple

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

st.set_page_config(page_title="SmartOps Dashboard", layout="wide")
st.title("🔍 SmartOps Anomaly Detection Dashboard")

# Connect to DB
conn = sqlite3.connect("/app/dashboard/data/data.db")
conn.execute("""
    CREATE TABLE IF NOT EXISTS anomalies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        cpu TEXT,
        memory TEXT,
        prediction TEXT
    )
""")
conn.commit()
df = pd.read_sql_query("SELECT * FROM anomalies", conn)
conn.close()

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

# Check if 'namespace' column exists in the anomalies table
def has_namespace_column(df):
    return 'namespace' in df.columns

# Namespace selection UI
namespace_options = ['all']
if has_namespace_column(df):
    ns_list = df['namespace'].dropna().unique().tolist()
    namespace_options += sorted(ns_list)
selected_ns = st.selectbox('Select Namespace', namespace_options, index=0)

# Filter dataframe by namespace if applicable
if has_namespace_column(df) and selected_ns != 'all':
    filtered_df = df[df['namespace'] == selected_ns].copy()
else:
    filtered_df = df.copy()

if filtered_df.empty:
    st.warning("No data available for the selected namespace.")
else:
    filtered_df['timestamp'] = pd.to_datetime(filtered_df['timestamp'])
    latest = filtered_df.iloc[-1]
    # Try to parse CPU/memory as float, fallback to 0
    try:
        cpu_val = float(latest['cpu'])
    except:
        cpu_val = 0.0
    try:
        mem_val = float(latest['memory'])
    except:
        mem_val = 0.0
    status, advice, banner_type, latest_action = get_status_and_advice(latest['prediction'], cpu_val, mem_val)
    st.markdown(f"<div style='padding:1em; border-radius:8px; background-color:{'#d4edda' if banner_type=='success' else '#f8d7da'}; color:{'#155724' if banner_type=='success' else '#721c24'}; font-size:1.2em; margin-bottom:1em;'><b>{status}</b><br>{advice}</div>", unsafe_allow_html=True)

    # Table of recent predictions
    st.subheader("🕒 Recent Predictions")
    # Add pod_name and labels columns if present
    display_cols = ['timestamp', 'cpu', 'memory', 'prediction']
    if 'pod_name' in filtered_df.columns:
        display_cols.append('pod_name')
    if 'labels' in filtered_df.columns:
        display_cols.append('labels')
    show_df = filtered_df[display_cols].copy()
    show_df = show_df.sort_values('timestamp', ascending=False).head(20)
    def rec_action(row):
        pred = row['prediction']
        try:
            cpu_val = float(row['cpu'])
        except:
            cpu_val = 0.0
        try:
            mem_val = float(row['memory'])
        except:
            mem_val = 0.0
        if pred.lower() == "normal":
            return "No action needed"
        elif cpu_val > 0.8:
            return "High CPU: Consider scaling CPU"
        elif mem_val > 0.8 * 1024*1024*1024:
            return "High Memory: Consider scaling memory"
        else:
            return "Check logs and recent deployments"
    show_df['Recommended Action'] = show_df.apply(rec_action, axis=1)
    show_df = show_df.rename(columns={
        'timestamp': 'Timestamp',
        'cpu': 'CPU Usage',
        'memory': 'Memory Usage',
        'prediction': 'Prediction',
        'pod_name': 'Pod Name',
        'labels': 'Labels'
    })
    st.dataframe(show_df, use_container_width=True)

    # Plain English summary
    st.subheader("📢 System Summary")
    anomaly_count = (filtered_df['prediction'].str.lower() != 'normal').sum()
    total = len(filtered_df)
    st.info(f"Out of {total} recent checks, {anomaly_count} anomalies were detected.")
    if anomaly_count == 0:
        st.success("Everything looks good! No anomalies detected in the recent data.")
    else:
        st.error(f"{anomaly_count} anomalies detected. Please review the recommended actions above.")

# Deployment events summary
st.header("Deployment Workflow Events")
try:
    db_path = "data/deployment_events.db"
    conn = sqlite3.connect(db_path)
    events = pd.read_sql_query("SELECT * FROM deployment_events ORDER BY timestamp DESC", conn)
    conn.close()
    # Add namespace filter for deployment events
    ns_options = ['all'] + sorted([ns for ns in events['namespace'].dropna().unique() if ns]) if 'namespace' in events.columns else ['all']
    selected_ns = st.selectbox('Select Deployment Namespace', ns_options, index=0, key='deploy_ns')
    if selected_ns != 'all' and 'namespace' in events.columns:
        events = events[events['namespace'] == selected_ns]
    if not events.empty:
        latest = events.iloc[0]
        if latest["status"] == "success":
            st.success(f"✅ Deployment Success at {latest['timestamp']}: {latest['message']}")
        elif latest["status"] == "failed":
            st.error(f"❌ Deployment Failed at {latest['timestamp']}: {latest['message']}")
        elif latest["status"] == "started":
            st.info(f"🚀 Deployment Started at {latest['timestamp']}: {latest['message']}")
    else:
        st.info("No deployment events recorded yet.")
    st.metric("Deployments Started", (events["status"] == "started").sum())
    st.metric("Deployments Successful", (events["status"] == "success").sum())
    st.metric("Deployments Failed", (events["status"] == "failed").sum())
    st.write("### Recent Deployment Events")
    st.dataframe(events.head(10))
except Exception as e:
    st.warning(f"Could not load deployment events: {e}") 