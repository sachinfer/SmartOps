import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import pytz
import requests
import sys
import os

# Get IST timezone
IST = pytz.timezone('Asia/Kolkata')

def get_ist_time():
    """Get current time in IST timezone"""
    return datetime.now(IST)

# Check if API service is running
def check_api_health():
    try:
        # Try the anomaly service first
        response = requests.get("http://smartops-anomaly-service.smartops.svc.cluster.local/", timeout=5)
        if response.status_code == 200:
            return True
    except Exception:
        pass
    
    try:
        # Fallback to localhost
        response = requests.get("http://localhost:8000/", timeout=5)
        return response.status_code == 200
    except Exception:
        return False

# Simple functions with better error handling
@st.cache_data(ttl=30)
def fetch_namespaces():
    try:
        # Try the anomaly service first
        url = "http://smartops-anomaly-service.smartops.svc.cluster.local/namespaces"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            namespaces = resp.json().get('namespaces', [])
            if namespaces:  # Only return if we got actual namespaces
                return namespaces
    except Exception as e:
        print(f"Error fetching namespaces from anomaly service: {e}")
    
    try:
        # Fallback to localhost
        url = "http://localhost:8000/namespaces"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            namespaces = resp.json().get('namespaces', [])
            if namespaces:  # Only return if we got actual namespaces
                return namespaces
    except Exception as e:
        print(f"Error fetching namespaces from localhost: {e}")
    
    # Final fallback - return common namespaces
    return ['smartops', 'default', 'kube-system', 'all']

@st.cache_data(ttl=30)
def load_anomalies_df():
    print("DEBUG: Starting to load anomaly data...")
    try:
        # Try to load from the real anomaly database first
        print("DEBUG: Trying to load from /app/dashboard/data/data.db")
        conn = sqlite3.connect('/app/dashboard/data/data.db')
        df = pd.read_sql_query("SELECT * FROM anomalies ORDER BY timestamp DESC LIMIT 100", conn)
        conn.close()
        
        print(f"DEBUG: Loaded {len(df)} records from data.db")
        if not df.empty:
            # Convert timestamp to datetime if it's a string
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            print("DEBUG: Successfully loaded real data from data.db")
            return df
    except Exception as e:
        print(f"DEBUG: Error loading from database: {e}")
    
    try:
        # Try to load from the old anomalies database
        print("DEBUG: Trying to load from /app/dashboard/data/anomalies.db")
        conn = sqlite3.connect('/app/dashboard/data/anomalies.db')
        df = pd.read_sql_query("SELECT * FROM anomalies ORDER BY timestamp DESC LIMIT 100", conn)
        conn.close()
        
        print(f"DEBUG: Loaded {len(df)} records from anomalies.db")
        if not df.empty:
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            print("DEBUG: Successfully loaded data from anomalies.db")
            return df
    except Exception as e:
        print(f"DEBUG: Error loading from old database: {e}")
    
    # If we get here, there's a problem - log it and return empty DataFrame
    print("WARNING: No anomaly data could be loaded from any source")
    return pd.DataFrame()

def has_namespace_column(df):
    return 'namespace' in df.columns

@st.cache_data(ttl=10)
def get_real_pod_metrics():
    """Get real-time pod metrics from the anomaly service"""
    try:
        # Try the anomaly service first
        url = "http://smartops-anomaly-service.smartops.svc.cluster.local/pods"
        resp = requests.get(url, params={"namespace": "smartops"}, timeout=5)
        if resp.status_code == 200:
            return resp.json().get('pods', [])
    except Exception:
        pass
    
    try:
        # Fallback to localhost
        url = "http://localhost:8000/pods"
        resp = requests.get(url, params={"namespace": "smartops"}, timeout=5)
        if resp.status_code == 200:
            return resp.json().get('pods', [])
    except Exception:
        pass
    
    return []

@st.cache_data(ttl=10)
def get_cluster_metrics():
    """Get real-time cluster metrics"""
    try:
        # Try the anomaly service first
        url = "http://smartops-anomaly-service.smartops.svc.cluster.local/cluster_metrics"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    
    try:
        # Fallback to localhost
        url = "http://localhost:8000/cluster_metrics"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    
    return {"cpu_usage": 0, "cpu_capacity": 1, "memory_usage": 0, "memory_capacity": 1}

# Main content
st.markdown("""
<div class="dashboard-header">
    <h1>🔥 Anomaly Detection</h1>
    <p>AI-powered anomaly detection and analysis</p>
</div>
""", unsafe_allow_html=True)



# Namespace selection
st.markdown('<div class="section-header">📋 Select Namespace</div>', unsafe_allow_html=True)
namespaces = fetch_namespaces()
print(f"DEBUG: Available namespaces: {namespaces}")

if namespaces:
    selected_namespace = st.selectbox(
        "Choose a namespace to view anomalies:",
        options=namespaces,
        index=0 if 'smartops' in namespaces else 0,
        key="namespace_selector"
    )
    print(f"DEBUG: Selected namespace: {selected_namespace}")
else:
    st.error("No namespaces available. Please check the anomaly service connection.")
    selected_namespace = "smartops"

# Check if API service is running and show helpful message
api_health = check_api_health()
print(f"DEBUG: API health check result: {api_health}")

# Always show anomaly data regardless of API health
# The API health check is just for real-time metrics, not for historical anomaly data

# Real-time metrics sections removed as requested

# Load and filter data
print("DEBUG: About to load anomaly data...")
df = load_anomalies_df()
print(f"DEBUG: Loaded DataFrame with shape: {df.shape}")
print(f"DEBUG: DataFrame columns: {df.columns.tolist()}")
print(f"DEBUG: DataFrame empty: {df.empty}")

if has_namespace_column(df) and selected_namespace != 'all':
    filtered_df = df[df['namespace'] == selected_namespace].copy()
    print(f"DEBUG: Filtered DataFrame shape: {filtered_df.shape}")
else:
    filtered_df = df.copy()
    print(f"DEBUG: Using full DataFrame, shape: {filtered_df.shape}")

# Top Anomalies Section
st.markdown('<div class="section-header">🔥 Top Anomalies (CPU ≥ 50%)</div>', unsafe_allow_html=True)
if not filtered_df.empty:
    chart_df = filtered_df.copy()
    
    # Check what columns are available and create safe numeric conversions
    if 'cpu' in chart_df.columns:
        chart_df['cpu_numeric'] = pd.to_numeric(chart_df['cpu'], errors='coerce').fillna(0)
        chart_df['cpu_percent'] = chart_df['cpu_numeric'] * 100
    else:
        chart_df['cpu_percent'] = 0
    
    if 'memory' in chart_df.columns:
        chart_df['memory_numeric'] = pd.to_numeric(chart_df['memory'], errors='coerce').fillna(0)
        chart_df['memory_mb'] = chart_df['memory_numeric'] / (1024 * 1024)
    else:
        chart_df['memory_mb'] = 0
    
    # Create display dataframe with available columns
    display_cols = ['timestamp', 'pod_name']
    if 'cpu_percent' in chart_df.columns:
        display_cols.append('cpu_percent')
    if 'memory_mb' in chart_df.columns:
        display_cols.append('memory_mb')
    if 'prediction' in chart_df.columns:
        display_cols.append('prediction')
    
    # Determine the sort column - use the first available metric column
    sort_column = None
    if 'cpu_percent' in chart_df.columns:
        sort_column = 'cpu_percent'
    elif 'memory_mb' in chart_df.columns:
        sort_column = 'memory_mb'
    elif 'prediction' in chart_df.columns:
        sort_column = 'prediction'
    else:
        # If no metric columns available, just take the first 5 rows
        top_anomalies_df = chart_df.head(5)[display_cols]
        sort_column = None
    
    if sort_column:
        # Filter out entries with CPU usage under 50%
        if 'cpu_percent' in chart_df.columns:
            # Ensure cpu_percent is numeric and filter
            chart_df['cpu_percent'] = pd.to_numeric(chart_df['cpu_percent'], errors='coerce').fillna(0)
            print(f"DEBUG: Top Anomalies CPU percent values before filtering: {chart_df['cpu_percent'].tolist()}")
            chart_df = chart_df[chart_df['cpu_percent'] >= 50.0]
            print(f"DEBUG: Top Anomalies CPU percent values after filtering: {chart_df['cpu_percent'].tolist()}")
        elif 'cpu' in chart_df.columns:
            # Handle raw CPU values (decimals) - convert to percentage and filter
            chart_df['cpu_numeric'] = pd.to_numeric(chart_df['cpu'], errors='coerce').fillna(0)
            chart_df['cpu_percent'] = chart_df['cpu_numeric'] * 100
            print(f"DEBUG: Top Anomalies CPU values before filtering: {chart_df['cpu_numeric'].tolist()}")
            chart_df = chart_df[chart_df['cpu_numeric'] >= 0.5]  # 0.5 = 50% in decimal
            print(f"DEBUG: Top Anomalies CPU values after filtering: {chart_df['cpu_numeric'].tolist()}")
            if chart_df.empty:
                st.info("No anomalies found with CPU usage above 50%.")
                top_anomalies_df = pd.DataFrame()
            else:
                top_anomalies_df = chart_df.nlargest(5, sort_column)[display_cols]
        else:
            top_anomalies_df = chart_df.nlargest(5, sort_column)[display_cols]
    
    # Format the display
    if 'cpu_percent' in top_anomalies_df.columns:
        top_anomalies_df['cpu_percent'] = top_anomalies_df['cpu_percent'].round(1).astype(str) + '%'
    if 'memory_mb' in top_anomalies_df.columns:
        top_anomalies_df['memory_mb'] = top_anomalies_df['memory_mb'].round(1).astype(str) + 'MB'
    
    top_anomalies_df = top_anomalies_df.rename(columns={'timestamp': 'Timestamp', 'pod_name': 'Pod Name'})
    st.dataframe(top_anomalies_df, use_container_width=True)
else:
    st.info("No anomaly data available for the selected namespace.")

# Pod Actions Section
st.markdown('<div class="section-header">🎯 Recent Pod Actions</div>', unsafe_allow_html=True)
try:
    conn = sqlite3.connect('/app/dashboard/data/data.db')
    
    # First check if the table exists
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='pod_actions'")
    table_exists = cursor.fetchone() is not None
    
    if table_exists:
        actions_df = pd.read_sql_query("""
            SELECT timestamp, action, pod_name, reason, user_action
            FROM pod_actions 
            ORDER BY timestamp DESC 
            LIMIT 10
        """, conn)
        
        if not actions_df.empty:
            # Format the display with robust timestamp parsing
            print(f"DEBUG: Sample timestamp values: {actions_df['timestamp'].head(3).tolist()}")
            try:
                # Try multiple timestamp formats
                actions_df['timestamp'] = pd.to_datetime(actions_df['timestamp'], format='mixed', errors='coerce')
                print(f"DEBUG: After mixed format parsing: {actions_df['timestamp'].head(3).tolist()}")
                # If that fails, try ISO8601
                if actions_df['timestamp'].isna().any():
                    actions_df['timestamp'] = pd.to_datetime(actions_df['timestamp'], format='ISO8601', errors='coerce')
                    print(f"DEBUG: After ISO8601 format parsing: {actions_df['timestamp'].head(3).tolist()}")
                # If still failing, try infer_datetime_format
                if actions_df['timestamp'].isna().any():
                    actions_df['timestamp'] = pd.to_datetime(actions_df['timestamp'], infer_datetime_format=True, errors='coerce')
                    print(f"DEBUG: After infer_datetime_format parsing: {actions_df['timestamp'].head(3).tolist()}")
            except Exception as e:
                print(f"DEBUG: Timestamp parsing error: {e}")
                # Fallback: create a dummy timestamp
                actions_df['timestamp'] = pd.to_datetime('2025-01-01 00:00:00')
            
            actions_df['Time'] = actions_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S IST')
            actions_df['Action'] = actions_df['action'].apply(lambda x: '🔴 KILLED' if x == 'kill' else '🚫 IGNORED')
            actions_df['Pod'] = actions_df['pod_name']
            actions_df['Reason'] = actions_df['reason']
            actions_df['User Action'] = actions_df['user_action'].apply(lambda x: '👤 Manual' if x else '🤖 Auto')
            
            display_actions = actions_df[['Time', 'Action', 'Pod', 'Reason', 'User Action']]
            st.dataframe(display_actions, use_container_width=True)
        else:
            st.info("No pod actions recorded yet. Try killing or ignoring a pod from the Pod Management page.")
    else:
        st.info("Pod actions table not created yet. Try killing or ignoring a pod from the Pod Management page to create the table.")
    
    conn.close()
except Exception as e:
    st.info(f"Pod actions not available: {str(e)}")

# Recent Anomalies Section
st.markdown('<div class="section-header">🕒 Recent Anomalies (CPU ≥ 50%)</div>', unsafe_allow_html=True)
if not filtered_df.empty:
    # Build display columns dynamically based on what's available
    display_cols = ['timestamp']
    
    # Add metric columns if they exist
    if 'cpu' in filtered_df.columns:
        display_cols.append('cpu')
    if 'memory' in filtered_df.columns:
        display_cols.append('memory')
    if 'prediction' in filtered_df.columns:
        display_cols.append('prediction')
    if 'cpu_percent' in filtered_df.columns:
        display_cols.append('cpu_percent')
    if 'memory_mb' in filtered_df.columns:
        display_cols.append('memory_mb')
    
    # Add metadata columns if they exist
    if 'pod_name' in filtered_df.columns:
        display_cols.append('pod_name')
    if 'labels' in filtered_df.columns:
        display_cols.append('labels')
    
    # Only select columns that actually exist
    available_cols = [col for col in display_cols if col in filtered_df.columns]
    show_df = filtered_df[available_cols].copy()
    
    # Filter out entries with CPU usage under 50%
    if 'cpu' in show_df.columns:
        show_df['cpu_numeric'] = pd.to_numeric(show_df['cpu'], errors='coerce').fillna(0)
        print(f"DEBUG: CPU values before filtering: {show_df['cpu_numeric'].tolist()}")
        show_df = show_df[show_df['cpu_numeric'] >= 0.5]  # 0.5 = 50% in decimal
        print(f"DEBUG: CPU values after filtering: {show_df['cpu_numeric'].tolist()}")
        show_df['cpu_display'] = (show_df['cpu_numeric'] * 100).round(1).astype(str) + '%'
    elif 'cpu_percent' in show_df.columns:
        # Ensure cpu_percent is numeric and filter
        show_df['cpu_percent'] = pd.to_numeric(show_df['cpu_percent'], errors='coerce').fillna(0)
        print(f"DEBUG: CPU percent values before filtering: {show_df['cpu_percent'].tolist()}")
        show_df = show_df[show_df['cpu_percent'] >= 50.0]
        print(f"DEBUG: CPU percent values after filtering: {show_df['cpu_percent'].tolist()}")
        show_df['cpu_display'] = show_df['cpu_percent'].astype(str) + '%'
    
    show_df = show_df.sort_values('timestamp', ascending=False).head(20)
    
    # Check if any data remains after filtering
    if show_df.empty:
        st.info("No recent anomalies found with CPU usage above 50%.")
        display_df = pd.DataFrame()
    else:
        # Format Memory column if it exists
        if 'memory' in show_df.columns:
            show_df['memory_numeric'] = pd.to_numeric(show_df['memory'], errors='coerce').fillna(0)
            show_df['memory_display'] = (show_df['memory_numeric'] / (1024 * 1024)).round(1).astype(str) + 'MB'
        elif 'memory_mb' in show_df.columns:
            show_df['memory_display'] = show_df['memory_mb'].astype(str) + 'MB'
        
        # Create final display dataframe with available formatted columns
        final_display_cols = ['timestamp']
        
        if 'cpu_display' in show_df.columns:
            final_display_cols.append('cpu_display')
        if 'memory_display' in show_df.columns:
            final_display_cols.append('memory_display')
        if 'prediction' in show_df.columns:
            final_display_cols.append('prediction')
        if 'pod_name' in show_df.columns:
            final_display_cols.append('pod_name')
        if 'labels' in show_df.columns:
            final_display_cols.append('labels')
        
        # Only select columns that actually exist
        available_final_cols = [col for col in final_display_cols if col in show_df.columns]
        display_df = show_df[available_final_cols].copy()
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

# Misi AI Chatbot Widget removed - not using MISI AI page-wise 