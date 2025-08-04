import streamlit as st
import pandas as pd
import sqlite3

# Page config
st.set_page_config(
    page_title="Deployments - SmartOps AI",
    page_icon="🚀",
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
.stDataFrame {
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}
</style>
""", unsafe_allow_html=True)

# Main content
st.markdown("""
<div class="dashboard-header">
    <h1>🚀 Deployment Workflow Events</h1>
    <p>Deployment tracking and workflow management</p>
</div>
""", unsafe_allow_html=True)

# Deployment Workflow Events Summary
st.markdown('<div class="section-header">🚀 Deployment Workflow Events</div>', unsafe_allow_html=True)
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
            <span style='background:#0984e3;color:white;padding:0.5rem 1.2rem;border-radius:8px;font-size:1.2rem;font-weight:bold;display:inline-block;'>Deployment Workflow Events</span>
            <span style='background:#00b894;color:white;padding:0.3rem 1rem;border-radius:8px;font-size:1rem;'>Successful: {status_counts.get('success', 0)}</span>
            <span style='background:#d63031;color:white;padding:0.3rem 1rem;border-radius:8px;font-size:1rem;'>Failed: {status_counts.get('failed', 0)}</span>
            <span style='background:#fdcb6e;color:black;padding:0.3rem 1rem;border-radius:8px;font-size:1rem;'>Started: {status_counts.get('started', 0)}</span>
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(events, use_container_width=True)
    else:
        st.info("No deployment events found.")
except Exception as e:
    st.warning(f"Could not load deployment events: {e}")

# Deployment Statistics
if 'events' in locals() and not events.empty:
    st.markdown('<div class="section-header">📊 Deployment Statistics</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_deployments = len(events)
        st.metric("Total Deployments", total_deployments)
    
    with col2:
        success_rate = (status_counts.get('success', 0) / total_deployments * 100) if total_deployments > 0 else 0
        st.metric("Success Rate", f"{success_rate:.1f}%")
    
    with col3:
        recent_deployments = len(events[events['timestamp'] >= (pd.Timestamp.now() - pd.Timedelta(days=7)).strftime('%Y-%m-%d')])
        st.metric("Last 7 Days", recent_deployments) 