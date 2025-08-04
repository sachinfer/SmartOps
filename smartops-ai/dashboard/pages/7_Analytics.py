import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import pytz
import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Timezone setup
IST = pytz.timezone('Asia/Kolkata')

# Cached functions
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

@st.cache_data(ttl=60)
def load_analytics_data(filtered_df):
    chart_df = filtered_df.copy()
    chart_df['cpu_numeric'] = pd.to_numeric(chart_df['cpu'], errors='coerce').fillna(0)
    chart_df['cpu_percent'] = chart_df['cpu_numeric'] * 100
    chart_df['memory_numeric'] = pd.to_numeric(chart_df['memory'], errors='coerce').fillna(0)
    chart_df['memory_mb'] = chart_df['memory_numeric'] / (1024 * 1024)
    return chart_df

def has_namespace_column(df):
    return 'namespace' in df.columns

# Page config
st.set_page_config(
    page_title="Analytics - SmartOps AI",
    page_icon="📈",
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
.charts-container {
    border-radius: 15px;
    padding: 2rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    margin: 2rem 0;
}
</style>
""", unsafe_allow_html=True)

# Main content
st.markdown("""
<div class="dashboard-header">
    <h1>📈 Analytics Dashboard</h1>
    <p>Resource usage analytics and trends</p>
</div>
""", unsafe_allow_html=True)

# Namespace selection
namespace_options = ['all'] + fetch_namespaces()
selected_ns = st.selectbox('Select Namespace', namespace_options, index=0, key="analytics_ns")

# Load and filter data
df = load_anomalies_df()
if has_namespace_column(df) and selected_ns != 'all':
    filtered_df = df[df['namespace'] == selected_ns].copy()
else:
    filtered_df = df.copy()

if not filtered_df.empty:
    chart_df = load_analytics_data(filtered_df)
    
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
else:
    st.info('No analytics data available for the selected namespace.') 