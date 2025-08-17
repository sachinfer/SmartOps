import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import pytz

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
.failed-row {
    background-color: rgba(220, 53, 69, 0.1);
}
.success-row {
    background-color: rgba(40, 167, 69, 0.1);
}
.started-row {
    background-color: rgba(255, 193, 7, 0.1);
}
</style>
""", unsafe_allow_html=True)

def format_timestamp(timestamp_str):
    """Format timestamp to show only date and time without extra symbols"""
    try:
        # Parse the timestamp string
        if 'T' in timestamp_str:
            # ISO format with T
            dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        else:
            # Try other formats
            dt = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
        
        # Convert to IST (UTC+05:30)
        ist = pytz.timezone('Asia/Kolkata')
        if dt.tzinfo is None:
            dt = pytz.utc.localize(dt)
        dt_ist = dt.astimezone(ist)
        
        # Return clean format: YYYY-MM-DD HH:MM:SS
        return dt_ist.strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        # If parsing fails, return original but clean
        return timestamp_str.split('+')[0].replace('T', ' ')

def get_status_color(status):
    """Get color for status badges"""
    if status == 'success':
        return '🟢'
    elif status == 'failed':
        return '🔴'
    elif status == 'started':
        return '🟡'
    else:
        return '⚪'

# Main content
st.markdown("""
<div class="dashboard-header">
    <h1>🚀 Deployment Workflow Events</h1>
    <p>Deployment tracking and workflow management</p>
</div>
""", unsafe_allow_html=True)

# Deployment Workflow Events Summary
st.markdown('<div class="section-header">🚀 Deployment Workflow Events</div>', unsafe_allow_html=True)

# Manual event logging test
st.markdown("### 🧪 Test Event Logging")
col1, col2, col3 = st.columns(3)

with col1:
    test_status = st.selectbox("Test Status", ["success", "failed"], key="test_status")
    
with col2:
    test_message = st.text_input("Test Message", "Test deployment event", key="test_message")
    
with col3:
    if st.button("📝 Log Test Event", key="log_test"):
        try:
            import requests
            test_event = {
                "status": test_status,
                "message": test_message,
                "namespace": "smartops"
            }
            response = requests.post("http://localhost:8000/log_event", json=test_event, timeout=5)
            if response.status_code == 200:
                st.success("✅ Test event logged successfully!")
                st.rerun()
            else:
                st.error(f"❌ Failed to log test event: {response.status_code}")
        except Exception as e:
            st.error(f"❌ Error logging test event: {str(e)}")

st.markdown("---")

try:
    # Try multiple possible database paths
    db_paths = [
        "data/deployment_events.db",
        "/app/dashboard/data/deployment_events.db",
        "smartops-ai/dashboard/data/deployment_events.db"
    ]
    
    events = None
    used_path = None
    
    for db_path in db_paths:
        try:
            conn = sqlite3.connect(db_path)
            events = pd.read_sql_query("SELECT * FROM deployment_events ORDER BY timestamp DESC", conn)
            conn.close()
            used_path = db_path
            break
        except Exception as e:
            continue
    
    if events is not None and not events.empty:
        # Filter out "started" events, keep only success and failed
        events = events[events['status'].isin(['success', 'failed'])]
        
        # Debug: Show raw data
        st.markdown("### 🔍 Debug: Raw Events Data")
        st.write(f"Database path used: {used_path}")
        st.write(f"Total events found: {len(events)} (success + failed only)")
        st.write(f"Status distribution: {events['status'].value_counts().to_dict()}")
        
        # Count by status
        status_counts = events["status"].value_counts().to_dict()
        
        # Display summary statistics (only success and failed)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Deployments", len(events))
        
        with col2:
            st.metric("Successful", status_counts.get('success', 0), delta=None)
        
        with col3:
            st.metric("Failed", status_counts.get('failed', 0), delta=None)
        
        # Filter options (only success and failed)
        st.markdown("### 📊 Filter Events")
        col1, col2 = st.columns(2)
        
        with col1:
            status_filter = st.multiselect(
                "Filter by Status",
                options=['success', 'failed'],
                default=['success', 'failed'],
                help="Select which status types to display"
            )
        
        with col2:
            search_term = st.text_input(
                "Search in Messages",
                placeholder="Enter search term...",
                help="Search for specific text in deployment messages"
            )
        
        # Filter events based on selection
        filtered_events = events[events['status'].isin(status_filter)]
        
        if search_term:
            filtered_events = filtered_events[
                filtered_events['message'].str.contains(search_term, case=False, na=False)
            ]
        
        # Format timestamps and add status indicators
        filtered_events = filtered_events.copy()
        filtered_events['timestamp_clean'] = filtered_events['timestamp'].apply(format_timestamp)
        filtered_events['status_indicator'] = filtered_events['status'].apply(get_status_color)
        
        # Display filtered events
        if not filtered_events.empty:
            st.markdown(f"### 📋 Showing {len(filtered_events)} Events (Success + Failed Only)")
            
            # Create display dataframe with clean columns
            display_df = filtered_events[['timestamp_clean', 'status_indicator', 'status', 'message', 'namespace']].copy()
            display_df.columns = ['Timestamp', 'Status', 'Status Type', 'Message', 'Namespace']
            
            # Display the dataframe with styling
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )
            
            # Show detailed analysis
            st.markdown("### 🔍 Event Analysis")
            
            # Failed deployments analysis
            failed_events = filtered_events[filtered_events['status'] == 'failed']
            if not failed_events.empty:
                st.markdown("#### ❌ Failed Deployments")
                for _, event in failed_events.iterrows():
                    with st.expander(f"🔴 {event['timestamp_clean']} - {event['message'][:50]}..."):
                        st.write(f"**Timestamp:** {event['timestamp_clean']}")
                        st.write(f"**Status:** {event['status']}")
                        st.write(f"**Message:** {event['message']}")
                        st.write(f"**Namespace:** {event['namespace']}")
            
            # Successful deployments analysis
            success_events = filtered_events[filtered_events['status'] == 'success']
            if not success_events.empty:
                st.markdown("#### ✅ Successful Deployments")
                for _, event in success_events.head(5).iterrows():  # Show last 5 successful
                    with st.expander(f"🟢 {event['timestamp_clean']} - {event['message'][:50]}..."):
                        st.write(f"**Timestamp:** {event['timestamp_clean']}")
                        st.write(f"**Status:** {event['status']}")
                        st.write(f"**Message:** {event['message']}")
                        st.write(f"**Namespace:** {event['namespace']}")
            
            # Recent activity (only success and failed)
            st.markdown("#### 📈 Recent Activity (Success + Failed)")
            recent_events = filtered_events.head(10)
            for _, event in recent_events.iterrows():
                status_icon = "🟢" if event['status'] == 'success' else "🔴"
                st.write(f"{status_icon} **{event['timestamp_clean']}** - {event['status'].upper()}: {event['message'][:80]}...")
                
        else:
            st.info("No events match the selected filters.")
            
    else:
        st.info("No deployment events found in any database location.")
        st.write("Tried these paths:")
        for path in db_paths:
            st.write(f"- {path}")
        
except Exception as e:
    st.warning(f"Could not load deployment events: {e}")
    st.error(f"Error details: {str(e)}")
    import traceback
    st.code(traceback.format_exc())

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
        failed_rate = (status_counts.get('failed', 0) / total_deployments * 100) if total_deployments > 0 else 0
        st.metric("Failure Rate", f"{failed_rate:.1f}%")
    
    # Additional insights
    if 'status_counts' in locals():
        st.markdown("### 📈 Status Distribution")
        
        # Create a simple bar chart (only success and failed)
        status_data = pd.DataFrame(list(status_counts.items()), columns=['Status', 'Count'])
        st.bar_chart(status_data.set_index('Status'))
        
        # Show top failure reasons
        if status_counts.get('failed', 0) > 0:
            st.markdown("### 🚨 Top Failure Reasons")
            failed_events = events[events['status'] == 'failed']
            failure_reasons = failed_events['message'].value_counts().head(5)
            
            for reason, count in failure_reasons.items():
                st.write(f"🔴 **{count}x** - {reason}")
        
        # Show recent successful deployments
        if status_counts.get('success', 0) > 0:
            st.markdown("### ✅ Recent Successful Deployments")
            success_events = events[events['status'] == 'success'].head(3)
            for _, event in success_events.iterrows():
                st.write(f"🟢 **{event['timestamp_clean']}** - {event['message'][:60]}...") 