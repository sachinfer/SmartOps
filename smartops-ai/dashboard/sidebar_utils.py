import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import subprocess
import json

def get_anomaly_data():
    """Fetch recent actionable anomalies from the database"""
    try:
        # Try multiple possible database paths
        db_paths = [
            '/app/dashboard/data/data.db',  # Production path
            'smartops-ai/dashboard/data/data.db',  # Local development
            'data/data.db',  # Relative path
            'dashboard/data/data.db'  # Another relative path
        ]
        
        conn = None
        for db_path in db_paths:
            try:
                conn = sqlite3.connect(db_path)
                # Test if the table exists
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='anomalies'")
                if cursor.fetchone():
                    break
                conn.close()
                conn = None
            except:
                if conn:
                    conn.close()
                conn = None
                continue
        
        if not conn:
            st.error("Could not connect to anomalies database")
            return pd.DataFrame()
        
        # Query for recent anomalies (last 24 hours) with high CPU usage
        query = """
        SELECT timestamp, pod_name, cpu, memory, prediction, labels
        FROM anomalies 
        WHERE timestamp >= datetime('now', '-24 hours')
        AND cpu > 0.5  -- CPU usage > 50%
        AND prediction = 'Anomaly detected'
        ORDER BY timestamp DESC
        LIMIT 10
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        # Convert CPU to percentage and memory to MB
        if not df.empty:
            df['cpu_percent'] = (df['cpu'] * 100).round(1)
            df['memory_mb'] = (df['memory'] / (1024 * 1024)).round(1)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['time_ago'] = df['timestamp'].apply(lambda x: get_time_ago(x))
        
        return df
    except Exception as e:
        st.error(f"Error fetching anomaly data: {e}")
        return pd.DataFrame()

def get_time_ago(timestamp):
    """Convert timestamp to human readable time ago"""
    now = datetime.now()
    diff = now - timestamp
    
    if diff.days > 0:
        return f"{diff.days}d ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours}h ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes}m ago"
    else:
        return "Just now"

def kill_pod(pod_name, namespace="smartops"):
    """Kill a problematic pod permanently"""
    try:
        # Delete the pod
        result = subprocess.run([
            'kubectl', 'delete', 'pod', pod_name, 
            '-n', namespace, '--force', '--grace-period=0'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            return True, f"Successfully killed pod {pod_name}"
        else:
            return False, f"Failed to kill pod: {result.stderr}"
    except Exception as e:
        return False, f"Error killing pod: {str(e)}"

def ignore_anomaly(pod_name):
    """Mark an anomaly as ignored (store in session state)"""
    if 'ignored_anomalies' not in st.session_state:
        st.session_state.ignored_anomalies = set()
    
    st.session_state.ignored_anomalies.add(pod_name)
    st.rerun()

def show_anomaly_notifications():
    """Display anomaly notifications in the sidebar"""
    # Add refresh button
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<div class="sb-title">🚨 Active Anomalies</div>', unsafe_allow_html=True)
    with col2:
        if st.button("🔄", key="refresh_anomalies", help="Refresh anomalies"):
            st.rerun()
    
    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    
    # Get anomaly data
    anomalies_df = get_anomaly_data()
    
    if anomalies_df.empty:
        st.markdown(
            '<div style="color: #dfe6e9; font-size: 0.9rem; text-align: center; padding: 1rem;">✅ No active anomalies</div>',
            unsafe_allow_html=True
        )
        return
    
    # Filter out ignored anomalies
    ignored = st.session_state.get('ignored_anomalies', set())
    active_anomalies = anomalies_df[~anomalies_df['pod_name'].isin(ignored)]
    
    if active_anomalies.empty:
        st.markdown(
            '<div style="color: #dfe6e9; font-size: 0.9rem; text-align: center; padding: 1rem;">✅ All anomalies handled</div>',
            unsafe_allow_html=True
        )
        return
    
    # Show anomaly count with notification badge
    anomaly_count = len(active_anomalies)
    st.markdown(
        f'<div style="color: #ff6b6b; font-size: 0.9rem; text-align: center; padding: 0.5rem; background: rgba(255,107,107,0.1); border-radius: 8px; margin-bottom: 1rem;">🚨 {anomaly_count} Active Anomaly{"s" if anomaly_count > 1 else ""}</div>',
        unsafe_allow_html=True
    )
    
    # Display each anomaly
    for _, row in active_anomalies.iterrows():
        pod_name = row['pod_name']
        cpu_percent = row['cpu_percent']
        memory_mb = row['memory_mb']
        time_ago = row['time_ago']
        
        # Anomaly severity based on CPU usage
        if cpu_percent > 90:
            severity_icon = "🔴"
            severity_color = "#ff6b6b"
            severity_text = "CRITICAL"
        elif cpu_percent > 70:
            severity_icon = "🟠"
            severity_color = "#ffa726"
            severity_text = "HIGH"
        else:
            severity_icon = "🟡"
            severity_color = "#ffd54f"
            severity_text = "MEDIUM"
        
        # Anomaly card
        st.markdown(
            f"""
            <div style="
                background: rgba(0,0,0,0.2); 
                border: 1px solid {severity_color}; 
                border-radius: 10px; 
                padding: 1rem; 
                margin: 0.5rem 0;
                backdrop-filter: blur(10px);
            ">
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                    <span style="font-size: 1.2rem;">{severity_icon}</span>
                    <span style="color: {severity_color}; font-weight: bold;">{pod_name}</span>
                    <span style="color: {severity_color}; font-size: 0.7rem; background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px;">{severity_text}</span>
                </div>
                <div style="color: #dfe6e9; font-size: 0.85rem; margin-bottom: 0.5rem;">
                    CPU: <strong>{cpu_percent}%</strong> | Memory: <strong>{memory_mb}MB</strong>
                </div>
                <div style="color: #bdc3c7; font-size: 0.8rem; margin-bottom: 0.8rem;">
                    {time_ago}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Action buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(f"🗑️ Kill", key=f"kill_{pod_name}", use_container_width=True):
                success, message = kill_pod(pod_name)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        
        with col2:
            if st.button(f"👁️ Ignore", key=f"ignore_{pod_name}", use_container_width=True):
                ignore_anomaly(pod_name)
    
    # Show ignored anomalies count
    if ignored:
        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
        st.markdown(
            f'<div style="color: #bdc3c7; font-size: 0.8rem; text-align: center;">👁️ {len(ignored)} anomalies ignored</div>',
            unsafe_allow_html=True
        )

def show_sidebar():
    # ---------- Hide everything except the sidebar ----------
    st.markdown(
        """
        <style>
        /* Hide default chrome but keep main content visible */
        #MainMenu, header, footer { visibility: hidden; }

        /* Sidebar sizing */
        section[data-testid="stSidebar"]{
            min-width: 320px !important;
            width: 320px !important;
        }

        /* ---------- Sidebar look (matches screenshot) ---------- */
        section[data-testid="stSidebar"] > div:first-child{
            background: linear-gradient(180deg,#6b6eea 0%, #8356b1 55%, #7a59b5 100%);
            height: 100vh;
            padding: 1.2rem 1rem 2rem 1rem;
            border-top-right-radius: 20px;
            border-bottom-right-radius: 20px;
            box-shadow: 2px 0 16px rgba(102,126,234,0.10);
        }

        /* hide default sidebar header space */
        section[data-testid="stSidebar"] [data-testid="stSidebarHeader"],
        section[data-testid="stSidebar"] > div:first-child > div:first-child{
            display:none !important;
        }

        /* Titles, labels, dividers */
        .sb-title{
            font-size: 1.1rem; font-weight: 700; color: #ffffff; letter-spacing: .6px;
            margin: .3rem 0 .2rem 0; display:flex; align-items:center; gap:.5rem;
        }
        .sb-sub{
            color:#dfe6e9; font-size:.9rem; margin:.7rem 0 .5rem 0; display:flex; align-items:center; gap:.45rem;
            opacity:.95;
        }
        .sb-divider{
            border-top: 1px solid rgba(255,255,255,.25);
            margin: 1.1rem 0 1.1rem 0;
        }
        .sb-section{ margin: .3rem 0 1rem 0; }

        /* Pill buttons (exact feel) */
        .stButton > button {
            width: 100% !important;
            text-align: left !important;
            font-weight: 600 !important;
            color: #ffffff !important;
            background: rgba(0,0,0,.28) !important;
            border: 1px solid rgba(255,255,255,.18) !important;
            border-radius: 10px !important;
            padding: .65rem .9rem !important;
            line-height: 1.1rem !important;
            box-shadow: inset 0 1px 0 rgba(255,255,255,.06);
        }
        .stButton > button:hover{
            background: rgba(255,255,255,.22) !important;
            transform: translateX(5px);
            transition: all .18s ease;
        }
        .stButton > button:active{
            transform: translateX(2px);
        }

        /* Make emojis align nicely inside buttons */
        .stButton > button p { margin: 0; }
        
        /* Anomaly notification styles */
        .anomaly-card {
            background: rgba(0,0,0,0.2);
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
            backdrop-filter: blur(10px);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ---------- Sidebar content ----------
    st.markdown(
        """
        <div style="text-align:center; margin: .2rem 0 1.2rem 0;">
            <div style="font-size:2.2rem;">🚀</div>
            <div style="font-size:1.35rem; font-weight:800; color:#fff; letter-spacing:.6px;">SmartOps</div>
            <div style="font-size:.92rem; color:#dfe6e9; opacity:.95;">AI Kubernetes Platform</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Show anomaly notifications at the top
    show_anomaly_notifications()
    
    st.markdown('<div class="sb-title">🧭 Navigation</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

    # ---- Core Monitoring
    st.markdown('<div class="sb-section">', unsafe_allow_html=True)
    st.markdown('<div class="sb-sub">📊 Core Monitoring</div>', unsafe_allow_html=True)
    if st.button("🟩  Overview Dashboard", key="nav_overview", use_container_width=True):
        st.switch_page("pages/1_Overview.py")
    if st.button("🔥  Anomaly Detection", key="nav_anomaly", use_container_width=True):
        st.switch_page("pages/4_Anomaly_Detection.py")
    st.markdown('</div>', unsafe_allow_html=True)

    # ---- Testing & Development
    st.markdown('<div class="sb-section">', unsafe_allow_html=True)
    st.markdown('<div class="sb-sub">🧪 Testing & Development</div>', unsafe_allow_html=True)
    if st.button("🧪  Sidebar Test", key="nav_test", use_container_width=True):
        st.switch_page("test_sidebar.py")
    st.markdown('</div>', unsafe_allow_html=True)

    # ---- Pod & Cluster
    st.markdown('<div class="sb-section">', unsafe_allow_html=True)
    st.markdown('<div class="sb-sub">🛰️ Pod & Cluster</div>', unsafe_allow_html=True)
    if st.button("🧭  Pod Explorer & Logs", key="nav_pod", use_container_width=True):
        st.switch_page("pages/2_Pod_Explorer_and_Logs.py")
    if st.button("🔍  Cluster Explorer", key="nav_cluster", use_container_width=True):
        st.switch_page("pages/3_Kubernetes_Shell_and_Cluster_Explorer.py")
    if st.button("🖥️  Kubernetes Shell", key="nav_shell", use_container_width=True):
        st.switch_page("pages/3_Kubernetes_Shell_and_Cluster_Explorer.py")
    st.markdown('</div>', unsafe_allow_html=True)

    # ---- Operations
    st.markdown('<div class="sb-section">', unsafe_allow_html=True)
    st.markdown('<div class="sb-sub">⚡ Operations</div>', unsafe_allow_html=True)
    if st.button("⚡  Auto Scaling Control", key="nav_scale", use_container_width=True):
        st.switch_page("pages/5_Auto_Scaling_Recommendations_and_Control.py")
    if st.button("🚀  Deployments", key="nav_deploy", use_container_width=True):
        st.switch_page("pages/9_Deployments.py")
    st.markdown('</div>', unsafe_allow_html=True)

    # ---- AI & Analytics
    st.markdown('<div class="sb-section">', unsafe_allow_html=True)
    st.markdown('<div class="sb-sub">🤖 AI & Analytics</div>', unsafe_allow_html=True)
    if st.button("🤖  AI Actions", key="nav_actions", use_container_width=True):
        st.switch_page("pages/8_AI_Actions.py")
    if st.button("📝  Incident Timeline", key="nav_incident", use_container_width=True):
        st.switch_page("pages/6_Incident_Timeline_and_Postmortem_Report_Generator.py")
    st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-title">🤖 AI Controls</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        "<div style='color:#dfe6e9; font-size:.84rem; text-align:center; opacity:.95;'>SmartOps v1.0<br/>© 2024 Your Company</div>",
        unsafe_allow_html=True
    )

# Note: This function should be called from individual pages, not run here
# show_sidebar()
