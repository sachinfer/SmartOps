import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import pytz
import sys
import os

# Import Misi from the dashboard directory
try:
    # from misi_chatbot_widget import add_misi_to_page
    MISI_AVAILABLE = True
except ImportError:
    MISI_AVAILABLE = False
    st.warning("Misi AI Chatbot not available. Please ensure the chatbot is properly installed.")

# Page config is handled by the main app

# Custom CSS for better styling
st.markdown("""
<style>
.section-header {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
    text-align: center;
    font-size: 1.5rem;
    font-weight: bold;
}

.dashboard-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem;
    border-radius: 15px;
    margin: 1rem 0;
    text-align: center;
}

.dashboard-header h1 {
    margin: 0;
    font-size: 2.5rem;
    font-weight: bold;
}

.dashboard-header p {
    margin: 0.5rem 0 0 0;
    font-size: 1.2rem;
    opacity: 0.9;
}
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
        <p>Deployment tracking, workflow management, and Git commit history</p>
    </div>
    """, unsafe_allow_html=True)

    # Create tabs for different views
    tab1, tab2 = st.tabs(["🚀 Deployment Events", "📝 Git Commits"])
    
    with tab1:
        # Real-time updates
        st.markdown("### 🔄 Real-time Updates")
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

        # Live status indicator
        if 'last_event_count' not in st.session_state:
            st.session_state.last_event_count = 0

        # Show live status
        st.markdown("### 📊 Live Status")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("🔄 Auto-refresh", "ON" if auto_refresh else "OFF")
            
        with col2:
            if 'last_event_count' in st.session_state:
                st.metric("📈 Events Monitored", st.session_state.last_event_count)
                
        with col3:
            # Get current time in IST
            ist_tz = pytz.timezone('Asia/Kolkata')
            current_time = datetime.now(ist_tz).strftime('%I:%M:%S %p')
            st.metric("🕐 Current Time (IST)", current_time)

        st.markdown("---")

        # Deployment Workflow Events Summary
        st.markdown('<div class="section-header">🚀 Deployment Workflow Events</div>', unsafe_allow_html=True)

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
                    st.info(f"ℹ️ Missing required columns: {missing_columns}")
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
                
        except Exception:
            st.info("Please check if the deployment events database is accessible")

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
                
                # Show recent successful deployments (only if filtered_events exists and has timestamp_clean)
                if 'filtered_events' in locals() and not filtered_events.empty and 'timestamp_clean' in filtered_events.columns:
                    st.markdown("### ✅ Recent Successful Deployments")
                    success_events = filtered_events[filtered_events['status'] == 'success'].head(3)
                    for _, event in success_events.iterrows():
                        st.write(f"🟢 **{event['timestamp_clean']}** - {event['message'][:60]}...")

    with tab2:
        # Git Commits Section
        st.markdown('<div class="section-header">📝 Git Commit History</div>', unsafe_allow_html=True)
        
        # Git commit controls
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            git_refresh = st.checkbox("🔄 Auto-refresh Git commits", value=True, key="git_auto_refresh")
        
        with col2:
            if st.button("🔄 Refresh Git", key="git_manual_refresh"):
                st.rerun()
        
        with col3:
            commit_limit = st.selectbox("Show commits", [10, 25, 50, 100], index=0)
        
        st.markdown("---")
        
        # Git commit data - Sample data for demonstration
        # In a real implementation, this would fetch from Git API or database
        sample_git_commits = [
            {
                "hash": "a1b2c3d4e5f6",
                "author": "Sachin Kumar",
                "email": "sachin@misi24x7.com",
                "timestamp": "2025-08-30 12:30:00 PM",
                "message": "feat: Add auto-scaling recommendations and control panel",
                "branch": "main",
                "files_changed": 15,
                "insertions": 234,
                "deletions": 45
            },
            {
                "hash": "b2c3d4e5f6a1",
                "author": "DevOps Team",
                "email": "devops@misi24x7.com",
                "timestamp": "2025-08-30 11:15:00 AM",
                "message": "fix: Resolve deployment pipeline issues in staging",
                "branch": "develop",
                "files_changed": 8,
                "insertions": 67,
                "deletions": 23
            },
            {
                "hash": "c3d4e5f6a1b2",
                "author": "Sachin Kumar",
                "email": "sachin@misi24x7.com",
                "timestamp": "2025-08-30 10:45:00 AM",
                "message": "docs: Update API documentation and deployment guides",
                "branch": "main",
                "files_changed": 12,
                "insertions": 89,
                "deletions": 12
            },
            {
                "hash": "d4e5f6a1b2c3",
                "author": "AI Team",
                "email": "ai@misi24x7.com",
                "timestamp": "2025-08-30 09:30:00 AM",
                "message": "feat: Implement anomaly detection algorithm improvements",
                "branch": "feature/anomaly-detection",
                "files_changed": 25,
                "insertions": 456,
                "deletions": 78
            },
            {
                "hash": "e5f6a1b2c3d4",
                "author": "DevOps Team",
                "email": "devops@misi24x7.com",
                "timestamp": "2025-08-30 08:15:00 AM",
                "message": "fix: Kubernetes deployment configuration updates",
                "branch": "main",
                "files_changed": 6,
                "insertions": 34,
                "deletions": 15
            },
            {
                "hash": "f6a1b2c3d4e5",
                "author": "Sachin Kumar",
                "email": "sachin@misi24x7.com",
                "timestamp": "2025-08-30 07:00:00 AM",
                "message": "feat: Add incident timeline and postmortem report generator",
                "branch": "main",
                "files_changed": 18,
                "insertions": 298,
                "deletions": 56
            },
            {
                "hash": "a1b2c3d4e5f7",
                "author": "AI Team",
                "email": "ai@misi24x7.com",
                "timestamp": "2025-08-29 06:45:00 PM",
                "message": "perf: Optimize dashboard performance and reduce load times",
                "branch": "main",
                "files_changed": 22,
                "insertions": 167,
                "deletions": 89
            },
            {
                "hash": "b2c3d4e5f6a2",
                "author": "DevOps Team",
                "email": "devops@misi24x7.com",
                "timestamp": "2025-08-29 05:30:00 PM",
                "message": "fix: Resolve database connection issues in production",
                "branch": "hotfix/db-connection",
                "files_changed": 4,
                "insertions": 23,
                "deletions": 8
            },
            {
                "hash": "c3d4e5f6a1b3",
                "author": "Sachin Kumar",
                "email": "sachin@misi24x7.com",
                "timestamp": "2025-08-29 04:15:00 PM",
                "message": "feat: Implement real-time monitoring dashboard",
                "branch": "main",
                "files_changed": 31,
                "insertions": 567,
                "deletions": 123
            },
            {
                "hash": "d4e5f6a1b2c4",
                "author": "AI Team",
                "email": "ai@misi24x7.com",
                "timestamp": "2025-08-29 03:00:00 PM",
                "message": "refactor: Clean up code structure and improve maintainability",
                "branch": "refactor/cleanup",
                "files_changed": 45,
                "insertions": 234,
                "deletions": 156
            }
        ]
        
        # Git commit filtering
        st.markdown("### 🔍 Filter Git Commits")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            author_filter = st.multiselect(
                "Filter by Author",
                options=list(set([commit['author'] for commit in sample_git_commits])),
                default=list(set([commit['author'] for commit in sample_git_commits])),
                help="Select which authors to display"
            )
        
        with col2:
            branch_filter = st.multiselect(
                "Filter by Branch",
                options=list(set([commit['branch'] for commit in sample_git_commits])),
                default=list(set([commit['branch'] for commit in sample_git_commits])),
                help="Select which branches to display"
            )
        
        with col3:
            git_search = st.text_input(
                "Search in Commit Messages",
                placeholder="Enter search term...",
                help="Search for specific text in commit messages"
            )
        
        # Filter commits based on selection
        filtered_commits = [
            commit for commit in sample_git_commits
            if commit['author'] in author_filter
            and commit['branch'] in branch_filter
            and (not git_search or git_search.lower() in commit['message'].lower())
        ]
        
        # Display git commits
        if filtered_commits:
            st.markdown(f"### 📋 Showing {len(filtered_commits)} Git Commits")
            
            # Create display dataframe for git commits
            git_display_data = []
            for commit in filtered_commits[:commit_limit]:
                git_display_data.append({
                    'Hash': commit['hash'][:8],
                    'Author': commit['author'],
                    'Timestamp': commit['timestamp'],
                    'Message': commit['message'],
                    'Branch': commit['branch'],
                    'Files': commit['files_changed'],
                    'Changes': f"+{commit['insertions']} -{commit['deletions']}"
                })
            
            git_df = pd.DataFrame(git_display_data)
            
            # Display the git commits dataframe with styling
            st.dataframe(
                git_df,
                use_container_width=True,
                hide_index=True
            )
            
            # Show detailed commit information
            st.markdown("### 🔍 Detailed Commit Information")
            
            for commit in filtered_commits[:5]:  # Show details for first 5 commits
                with st.expander(f"📝 {commit['hash'][:8]} - {commit['message'][:60]}..."):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Commit Hash:** `{commit['hash']}`")
                        st.write(f"**Author:** {commit['author']} ({commit['email']})")
                        st.write(f"**Timestamp:** {commit['timestamp']}")
                        st.write(f"**Branch:** `{commit['branch']}`")
                    
                    with col2:
                        st.write(f"**Files Changed:** {commit['files_changed']}")
                        st.write(f"**Insertions:** +{commit['insertions']}")
                        st.write(f"**Deletions:** -{commit['deletions']}")
                        st.write(f"**Net Change:** +{commit['insertions'] - commit['deletions']}")
                    
                    st.write(f"**Commit Message:** {commit['message']}")
            
            # Git statistics
            st.markdown("### 📊 Git Statistics")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_commits = len(filtered_commits)
                st.metric("Total Commits", total_commits)
            
            with col2:
                unique_authors = len(set([commit['author'] for commit in filtered_commits]))
                st.metric("Unique Authors", unique_authors)
            
            with col3:
                total_changes = sum([commit['insertions'] + commit['deletions'] for commit in filtered_commits])
                st.metric("Total Changes", total_changes)
            
            # Recent activity timeline
            st.markdown("### 📈 Recent Git Activity")
            recent_commits = filtered_commits[:10]
            for commit in recent_commits:
                branch_icon = "🌿" if commit['branch'] == 'main' else "🌱"
                st.write(f"{branch_icon} **{commit['timestamp']}** - `{commit['hash'][:8]}` by **{commit['author']}** on `{commit['branch']}`")
                st.write(f"   📝 {commit['message']}")
                st.write("---")
        
        else:
            st.info("No commits match the selected filters.")
        
        # Git integration note
        st.markdown("---")
        st.info("""
        **💡 Git Integration Note:** This page currently shows sample git commit data for demonstration. 
        In a production environment, this would be connected to your actual Git repository (GitHub, GitLab, etc.) 
        to show real-time commit information.
        """)

except Exception:
    st.info("ℹ️ An unexpected error occurred while loading the page")
    st.info("🔄 Please refresh the page or contact support if the issue persists")

# Add Misi AI Chatbot Widget
if MISI_AVAILABLE:
    # add_misi_to_page("bottom-right")
    pass  # Placeholder for when Misi is properly integrated
else:
    st.info("🤖 Misi AI Chatbot integration is being set up. You'll see the floating 🤖 icon soon!") 