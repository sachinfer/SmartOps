import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import pytz
from sidebar_utils import show_sidebar

# Page configuration
st.set_page_config(
    page_title="Deployments - SmartOps AI",
    page_icon="🚀",
    layout="wide"
)

# Sidebar
with st.sidebar:
    show_sidebar()

# Custom CSS for better styling - matching Pod Explorer
st.markdown("""
<style>
.main .block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    max-width: 1200px;
}

.stApp {
    background-color: #f8f9fa;
}

.dashboard-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 12px;
    margin-bottom: 2rem;
    color: white;
    text-align: center;
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

.section-box {
    background: white;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.section-title {
    font-size: 1.3rem;
    font-weight: 600;
    color: #495057;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
    margin: 1rem 0;
}

.metric-card {
    background: white;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    padding: 1rem;
    text-align: center;
}

.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: #667eea;
    margin-bottom: 0.25rem;
}

.metric-label {
    font-size: 0.8rem;
    color: #6c757d;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.event-card {
    background: white;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 1rem;
    margin: 0.5rem 0;
    transition: all 0.2s ease;
}

.event-card:hover {
    border-color: #667eea;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.event-status {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.status-success {
    background: #d4edda;
    color: #155724;
}

.status-failed {
    background: #f8d7da;
    color: #721c24;
}

.status-started {
    background: #fff3cd;
    color: #856404;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Helper functions
def format_timestamp(timestamp_str):
    """Format timestamp to IST with AM/PM"""
    try:
        # Try to parse the timestamp
        if isinstance(timestamp_str, str):
            # Handle different timestamp formats
            if 'T' in timestamp_str:
                # ISO format: 2024-01-15T10:30:00Z
                dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            elif ' ' in timestamp_str:
                # Standard format: 2024-01-15 10:30:00
                dt = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
            else:
                # Unix timestamp
                dt = datetime.fromtimestamp(float(timestamp_str))
        else:
            dt = timestamp_str
            
        # Convert to IST (UTC+05:30)
        ist_tz = pytz.timezone('Asia/Kolkata')
        if dt.tzinfo is None:
            dt = pytz.utc.localize(dt)
        ist_time = dt.astimezone(ist_tz)
        
        # Format as YYYY-MM-DD HH:MM:SS AM/PM
        return ist_time.strftime('%Y-%m-%d %I:%M:%S %p')
    except Exception as e:
        return str(timestamp_str)

def get_status_color(status):
    """Get status indicator emoji"""
    if status == 'success':
        return '🟢'
    elif status == 'failed':
        return '🔴'
    else:
        return '⚪'

# Main page content with error handling
try:
    st.markdown("""
    <div class="dashboard-header">
        <h1>🚀 Deployment Workflow Events</h1>
        <p>Deployment tracking and workflow management</p>
    </div>
    """, unsafe_allow_html=True)

    # Real-time updates section
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔄 Real-time Updates</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])

    with col1:
        auto_refresh = st.checkbox("🔄 Auto-refresh every 30 seconds", value=True, key="auto_refresh")

    with col2:
        if st.button("🔄 Manual Refresh", key="manual_refresh"):
            st.rerun()

    # Auto-refresh logic
    if auto_refresh:
        import time
        if 'last_refresh' not in st.session_state:
            st.session_state.last_refresh = time.time()
        
        if time.time() - st.session_state.last_refresh > 30:
            st.session_state.last_refresh = time.time()
            st.rerun()

    # Show last refresh time
    if 'last_refresh' in st.session_state:
        st.info(f"🕐 Last updated: {datetime.fromtimestamp(st.session_state.last_refresh).strftime('%I:%M:%S %p')}")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Live status section
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Live Status</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{'ON' if auto_refresh else 'OFF'}</div>
            <div class="metric-label">Auto-refresh</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        if 'last_event_count' in st.session_state:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{st.session_state.last_event_count}</div>
                <div class="metric-label">Events Monitored</div>
            </div>
            """, unsafe_allow_html=True)
            
    with col3:
        current_time = datetime.now().strftime('%I:%M:%S %p')
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{current_time.split()[0]}</div>
            <div class="metric-label">Current Time</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Deployment Workflow Events Summary
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🚀 Deployment Workflow Events</div>', unsafe_allow_html=True)

    # Load and process events
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
            # Ensure we have the required columns
            required_columns = ['timestamp', 'status', 'message', 'namespace']
            missing_columns = [col for col in required_columns if col not in events.columns]
            
            if missing_columns:
                st.error(f"❌ Missing required columns: {missing_columns}")
                st.write("Available columns:", list(events.columns))
                events = None
            else:
                # Filter out "started" events, keep only success and failed
                events = events[events['status'].isin(['success', 'failed'])]
                
                # Update event count for live tracking
                current_event_count = len(events)
                if 'last_event_count' not in st.session_state:
                    st.session_state.last_event_count = current_event_count
                
                # Check if new events were added
                new_events = current_event_count - st.session_state.last_event_count
                st.session_state.last_event_count = current_event_count
                
                # Show new events indicator
                if new_events > 0:
                    st.success(f"🆕 **{new_events} new events** detected since last refresh!")
                elif new_events == 0:
                    st.info("📊 No new events since last refresh")
                
                # Count by status
                status_counts = events["status"].value_counts().to_dict()
                
                # Display summary statistics (only success and failed)
                st.markdown("""
                <div class="metric-grid">
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{len(events)}</div>
                        <div class="metric-label">Total Deployments</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{status_counts.get('success', 0)}</div>
                        <div class="metric-label">Successful</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{status_counts.get('failed', 0)}</div>
                        <div class="metric-label">Failed</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
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
                
                # Format timestamps and add status indicators (only if we have data)
                if not filtered_events.empty:
                    filtered_events = filtered_events.copy()
                    filtered_events['timestamp_clean'] = filtered_events['timestamp'].apply(format_timestamp)
                    filtered_events['status_indicator'] = filtered_events['status'].apply(get_status_color)
                    
                    # Display filtered events
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
            
    except Exception as e:
        st.warning(f"Could not load deployment events: {e}")
        st.info("Please check if the deployment events database is accessible")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Deployment Statistics
    if 'events' in locals() and not events.empty:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📊 Deployment Statistics</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_deployments = len(events)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_deployments}</div>
                <div class="metric-label">Total Deployments</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            success_rate = (status_counts.get('success', 0) / total_deployments * 100) if total_deployments > 0 else 0
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{success_rate:.1f}%</div>
                <div class="metric-label">Success Rate</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            failed_rate = (status_counts.get('failed', 0) / total_deployments * 100) if total_deployments > 0 else 0
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{failed_rate:.1f}%</div>
                <div class="metric-label">Failure Rate</div>
            </div>
            """, unsafe_allow_html=True)
        
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
            
            # Show recent successful deployments (only if filtered_events exists and has timestamp_clean)
            if 'filtered_events' in locals() and not filtered_events.empty and 'timestamp_clean' in filtered_events.columns:
                st.markdown("### ✅ Recent Successful Deployments")
                success_events = filtered_events[filtered_events['status'] == 'success'].head(3)
                for _, event in success_events.iterrows():
                    st.write(f"🟢 **{event['timestamp_clean']}** - {event['message'][:60]}...")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; padding: 2rem; font-size: 0.9rem;">
        <p style="font-weight: 600; margin-bottom: 0.5rem;">🚀 SmartOps AI - Deployment Workflow Events</p>
        <p style="opacity: 0.8; margin: 0;">Last updated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
    </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error("❌ An unexpected error occurred while loading the page")
    st.error(f"Error: {str(e)}")
    import traceback
    st.code(traceback.format_exc())
    st.info("🔄 Please refresh the page or contact support if the issue persists") 