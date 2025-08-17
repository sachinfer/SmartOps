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
        
        # Convert to IST
        ist = pytz.timezone('Asia/Kolkata')
        if dt.tzinfo is None:
            dt = pytz.utc.localize(dt)
        dt_ist = dt.astimezone(ist)
        
        # Return clean format: YYYY-MM-DD HH:MM:SS
        return dt_ist.strftime('%Y-%m-%d %H:%M:%S')
    except:
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

try:
    db_path = "data/deployment_events.db"
    conn = sqlite3.connect(db_path)
    events = pd.read_sql_query("SELECT * FROM deployment_events ORDER BY timestamp DESC", conn)
    conn.close()
    
    if not events.empty:
        # Count by status
        status_counts = events["status"].value_counts().to_dict()
        
        # Display summary statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Events", len(events))
        
        with col2:
            st.metric("Successful", status_counts.get('success', 0), delta=None)
        
        with col3:
            st.metric("Failed", status_counts.get('failed', 0), delta=None)
        
        with col4:
            st.metric("Started", status_counts.get('started', 0), delta=None)
        
        # Filter options
        st.markdown("### 📊 Filter Events")
        col1, col2 = st.columns(2)
        
        with col1:
            status_filter = st.multiselect(
                "Filter by Status",
                options=['success', 'failed', 'started'],
                default=['success', 'failed', 'started'],
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
            st.markdown(f"### 📋 Showing {len(filtered_events)} Events")
            
            # Create display dataframe with clean columns
            display_df = filtered_events[['timestamp_clean', 'status_indicator', 'status', 'message', 'namespace']].copy()
            display_df.columns = ['Timestamp', 'Status', 'Status Type', 'Message', 'Namespace']
            
            # Apply row styling based on status
            def highlight_rows(row):
                if row['Status Type'] == 'failed':
                    return ['background-color: rgba(220, 53, 69, 0.1)'] * len(row)
                elif row['Status Type'] == 'success':
                    return ['background-color: rgba(40, 167, 69, 0.1)'] * len(row)
                elif row['Status Type'] == 'started':
                    return ['background-color: rgba(255, 193, 7, 0.1)'] * len(row)
                else:
                    return [''] * len(row)
            
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
            
            # Recent activity
            st.markdown("#### 📈 Recent Activity")
            recent_events = filtered_events.head(10)
            for _, event in recent_events.iterrows():
                status_icon = "🟢" if event['status'] == 'success' else "🔴" if event['status'] == 'failed' else "🟡"
                st.write(f"{status_icon} **{event['timestamp_clean']}** - {event['status'].upper()}: {event['message'][:80]}...")
                
        else:
            st.info("No events match the selected filters.")
            
    else:
        st.info("No deployment events found.")
        
except Exception as e:
    st.warning(f"Could not load deployment events: {e}")

# Deployment Statistics
if 'events' in locals() and not events.empty:
    st.markdown('<div class="section-header">📊 Deployment Statistics</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_deployments = len(events)
        st.metric("Total Deployments", total_deployments)
    
    with col2:
        success_rate = (status_counts.get('success', 0) / total_deployments * 100) if total_deployments > 0 else 0
        st.metric("Success Rate", f"{success_rate:.1f}%")
    
    with col3:
        failed_rate = (status_counts.get('failed', 0) / total_deployments * 100) if total_deployments > 0 else 0
        st.metric("Failure Rate", f"{failed_rate:.1f}%")
    
    with col4:
        # Calculate last 7 days
        try:
            recent_cutoff = pd.Timestamp.now() - pd.Timedelta(days=7)
            recent_events = events[pd.to_datetime(events['timestamp']) >= recent_cutoff]
            recent_count = len(recent_events)
        except:
            recent_count = 0
        st.metric("Last 7 Days", recent_count)
    
    # Additional insights
    if 'status_counts' in locals():
        st.markdown("### 📈 Status Distribution")
        
        # Create a simple bar chart
        status_data = pd.DataFrame(list(status_counts.items()), columns=['Status', 'Count'])
        st.bar_chart(status_data.set_index('Status'))
        
        # Show top failure reasons
        if status_counts.get('failed', 0) > 0:
            st.markdown("### 🚨 Top Failure Reasons")
            failed_events = events[events['status'] == 'failed']
            failure_reasons = failed_events['message'].value_counts().head(5)
            
            for reason, count in failure_reasons.items():
                st.write(f"🔴 **{count}x** - {reason}") 