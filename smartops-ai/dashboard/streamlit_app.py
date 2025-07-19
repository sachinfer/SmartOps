import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
from typing import Tuple
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pytz

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

# Metrics cards row
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
    # Make the card clickable using Streamlit's button
    if st.button('🟦 Available Pods', key='show_pods'):
        st.session_state['show_pods'] = not st.session_state.get('show_pods', False)
    available_pods_count = 23  # Placeholder, replace with real count from backend/API
    st.markdown(f"""
    <div class="metric-card">
        <h3>🟦 Available Pods</h3>
        <h2>{available_pods_count}</h2>
    </div>
    """, unsafe_allow_html=True)

# Show all pods table if the card is clicked
if st.session_state.get('show_pods', False):
    st.markdown('### 🟦 All Available Pods')
    # Mocked pod data; replace with real API/backend call
    pod_data = [
        {'name': 'smartops-app-123', 'namespace': 'smartops', 'status': 'Running'},
        {'name': 'smartops-dashboard-456', 'namespace': 'smartops', 'status': 'Running'},
        {'name': 'nginx-789', 'namespace': 'default', 'status': 'Pending'},
        # ... add more or fetch from backend ...
    ]
    pods_df = pd.DataFrame(pod_data)
    # Filter by selected namespace if not 'all'
    if selected_ns != 'all':
        pods_df = pods_df[pods_df['namespace'] == selected_ns]
    st.dataframe(pods_df, use_container_width=True)

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
    # Get CPU and memory values (convert to numeric if needed)
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
    
    # Prepare data for charts
    chart_df = filtered_df.copy()
    chart_df['cpu_numeric'] = pd.to_numeric(chart_df['cpu'], errors='coerce').fillna(0)
    chart_df['memory_numeric'] = pd.to_numeric(chart_df['memory'], errors='coerce').fillna(0)
    chart_df['cpu_percent'] = chart_df['cpu_numeric'] * 100
    chart_df['memory_mb'] = chart_df['memory_numeric'] / (1024 * 1024)
    
    # Convert timestamps to IST for charts with robust parsing
    def parse_anomaly_timestamp(ts):
        try:
            if pd.isna(ts):
                return ts
            if isinstance(ts, str):
                # Handle ISO format without timezone
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
                # Already a datetime object
                if ts.tzinfo is None:
                    ts = pytz.utc.localize(ts)
                return ts.astimezone(IST)
        except Exception:
            return ts
    
    chart_df['timestamp_ist'] = chart_df['timestamp'].apply(parse_anomaly_timestamp)
    
    # Create subplots for CPU and Memory trends
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('CPU Usage Over Time (IST)', 'Memory Usage Over Time (IST)', 'CPU Distribution', 'Memory Distribution'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # CPU over time
    fig.add_trace(
        go.Scatter(x=chart_df['timestamp_ist'], y=chart_df['cpu_percent'], 
                  mode='lines+markers', name='CPU %', line=dict(color='#667eea')),
        row=1, col=1
    )
    
    # Memory over time
    fig.add_trace(
        go.Scatter(x=chart_df['timestamp_ist'], y=chart_df['memory_mb'], 
                  mode='lines+markers', name='Memory MB', line=dict(color='#764ba2')),
        row=1, col=2
    )
    
    # CPU histogram
    fig.add_trace(
        go.Histogram(x=chart_df['cpu_percent'], name='CPU Distribution', 
                    marker_color='#667eea', opacity=0.7),
        row=2, col=1
    )
    
    # Memory histogram
    fig.add_trace(
        go.Histogram(x=chart_df['memory_mb'], name='Memory Distribution', 
                    marker_color='#764ba2', opacity=0.7),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=False, title_text="Resource Usage Analytics")
    st.plotly_chart(fig, use_container_width=True)
    
    # Top anomalies by CPU usage
    st.markdown("## 🔥 Top Anomalies by CPU Usage")
    top_cpu_df = chart_df.nlargest(5, 'cpu_percent')[['timestamp_ist', 'pod_name', 'cpu_percent', 'memory_mb', 'prediction']]
    top_cpu_df['timestamp_ist'] = top_cpu_df['timestamp_ist'].dt.strftime('%Y-%m-%d %H:%M:%S IST')
    top_cpu_df['cpu_percent'] = top_cpu_df['cpu_percent'].round(1).astype(str) + '%'
    top_cpu_df['memory_mb'] = top_cpu_df['memory_mb'].round(1).astype(str) + 'MB'
    top_cpu_df = top_cpu_df.rename(columns={'timestamp_ist': 'Timestamp (IST)'})
    st.dataframe(top_cpu_df, use_container_width=True)

    # Recent anomalies table with enhanced styling
    st.markdown("## 🕒 Recent Anomalies")
    # Prepare data for display
    display_cols = ['timestamp', 'cpu', 'memory', 'prediction']
    if 'pod_name' in filtered_df.columns:
        display_cols.append('pod_name')
    if 'labels' in filtered_df.columns:
        display_cols.append('labels')
    show_df = filtered_df[display_cols].copy()
    show_df = show_df.sort_values('timestamp', ascending=False).head(20)
    
    # Convert timestamps to IST
    def parse_recent_timestamp(ts):
        try:
            if pd.isna(ts):
                return ts
            if isinstance(ts, str):
                # Handle ISO format without timezone
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
                # Already a datetime object
                if ts.tzinfo is None:
                    ts = pytz.utc.localize(ts)
                return ts.astimezone(IST)
        except Exception:
            return ts
    
    show_df['timestamp_ist'] = show_df['timestamp'].apply(parse_recent_timestamp)
    show_df['timestamp_ist'] = show_df['timestamp_ist'].dt.strftime('%Y-%m-%d %H:%M:%S IST')
    
    # Format the display
    if not show_df.empty:
        # Convert CPU and memory to numeric, handling any non-numeric values
        show_df['cpu_numeric'] = pd.to_numeric(show_df['cpu'], errors='coerce').fillna(0)
        show_df['memory_numeric'] = pd.to_numeric(show_df['memory'], errors='coerce').fillna(0)
        
        # Convert CPU to percentage and memory to MB for display
        show_df['cpu_display'] = (show_df['cpu_numeric'] * 100).round(1).astype(str) + '%'
        show_df['memory_display'] = (show_df['memory_numeric'] / (1024 * 1024)).round(1).astype(str) + 'MB'
        
        # Create display dataframe with formatted columns
        display_df = show_df[['timestamp_ist', 'cpu_display', 'memory_display', 'prediction']].copy()
        if 'pod_name' in show_df.columns:
            display_df['pod_name'] = show_df['pod_name']
        if 'labels' in show_df.columns:
            display_df['labels'] = show_df['labels']
        
        # Rename columns for display
        display_df = display_df.rename(columns={
            'timestamp_ist': 'Timestamp (IST)',
            'cpu_display': 'CPU',
            'memory_display': 'Memory',
            'pod_name': 'Pod Name',
            'labels': 'Labels'
        })
        
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("No anomalies detected in the recent data.")

    # Plain English summary
    st.markdown("## 📢 System Summary")
    anomaly_count = (filtered_df['prediction'].str.lower() != 'normal').sum()
    total = len(filtered_df)
    st.info(f"Out of {total} recent checks, {anomaly_count} anomalies were detected.")
    if anomaly_count == 0:
        st.success("Everything looks good! No anomalies detected in the recent data.")
    else:
        st.error(f"{anomaly_count} anomalies detected. Please review the recommended actions above.")

# Deployment events summary with enhanced styling
st.markdown("## 🚀 Deployment Workflow Events")
try:
    db_path = "data/deployment_events.db"
    conn = sqlite3.connect(db_path)
    
    # Check if namespace column exists, if not add it
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(deployment_events)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'namespace' not in columns:
        # Add namespace column to existing table
        cursor.execute("ALTER TABLE deployment_events ADD COLUMN namespace TEXT DEFAULT 'smartops'")
        conn.commit()
        st.info("Updated deployment events table to include namespace column.")
    
    events = pd.read_sql_query("SELECT * FROM deployment_events ORDER BY timestamp DESC", conn)
    conn.close()
    
    # Convert timestamps to IST
    if not events.empty:
        # Handle different timestamp formats
        def parse_deployment_timestamp(ts_str):
            try:
                if pd.isna(ts_str):
                    return ts_str
                if isinstance(ts_str, str):
                    # Handle ISO format without timezone
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
                    # Already a datetime object
                    if ts_str.tzinfo is None:
                        ts_str = pytz.utc.localize(ts_str)
                    return ts_str
            except Exception:
                # Fallback to simple parsing
                return pd.to_datetime(ts_str)
        
        events['timestamp'] = events['timestamp'].apply(parse_deployment_timestamp)
        events['timestamp_ist'] = events['timestamp'].apply(lambda x: 
            x.astimezone(IST) if x.tzinfo else pytz.utc.localize(x).astimezone(IST)
        )
        events['timestamp_ist'] = events['timestamp_ist'].dt.strftime('%Y-%m-%d %H:%M:%S IST')
    
    # Add namespace filter for deployment events
    if 'namespace' in events.columns and not events.empty:
        # Get unique namespaces, excluding None/NaN values
        unique_namespaces = events['namespace'].dropna().unique().tolist()
        ns_options = ['all'] + sorted([ns for ns in unique_namespaces if ns and ns.strip()])
    else:
        ns_options = ['all']
    
    selected_ns = st.selectbox('Select Deployment Namespace', ns_options, index=0, key='deploy_ns')
    
    if selected_ns != 'all' and 'namespace' in events.columns:
        events = events[events['namespace'] == selected_ns]
    
    if not events.empty:
        latest = events.iloc[0]
        if latest["status"] == "success":
            st.markdown(f"""
            <div class="success-banner">
                <h3>✅ Deployment Success at {latest['timestamp_ist']}</h3>
                <p>{latest['message']}</p>
            </div>
            """, unsafe_allow_html=True)
        elif latest["status"] == "failed":
            st.markdown(f"""
            <div class="alert-banner">
                <h3>❌ Deployment Failed at {latest['timestamp_ist']}</h3>
                <p>{latest['message']}</p>
            </div>
            """, unsafe_allow_html=True)
        elif latest["status"] == "started":
            st.markdown(f"""
            <div class="metric-card">
                <h3>🚀 Deployment Started at {latest['timestamp_ist']}</h3>
                <p>{latest['message']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No deployment events recorded yet.")
    
    # Deployment metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🚀 Deployments Started", (events["status"] == "started").sum())
    with col2:
        st.metric("✅ Deployments Successful", (events["status"] == "success").sum())
    with col3:
        st.metric("❌ Deployments Failed", (events["status"] == "failed").sum())
    
    st.markdown("### 📋 Recent Deployment Events")
    if not events.empty:
        display_events = events[['timestamp_ist', 'status', 'message']].copy()
        display_events = display_events.rename(columns={'timestamp_ist': 'Timestamp (IST)'})
        st.dataframe(display_events.head(10), use_container_width=True)
    else:
        st.info("No deployment events to display.")
except Exception as e:
    st.warning(f"Could not load deployment events: {e}")
    st.error(f"Error details: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🚀 Powered by SmartOps AI | Real-time Kubernetes Monitoring</p>
    <p>Built with ❤️ using Streamlit and AI/ML</p>
</div>
""", unsafe_allow_html=True) 