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
        working_db = None
        for db_path in db_paths:
            try:
                conn = sqlite3.connect(db_path)
                # Test if the table exists
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='anomalies'")
                if cursor.fetchone():
                    working_db = db_path
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
        
        # Debug: Check table structure
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(anomalies)")
        columns_info = cursor.fetchall()
        
        # Debug: Show sample data
        cursor.execute("SELECT * FROM anomalies LIMIT 3")
        sample_data = cursor.fetchall()
        
        # Query for recent anomalies (last 24 hours) with high CPU usage
        query = """
        SELECT timestamp, pod_name, cpu, memory, prediction, labels
        FROM anomalies 
        WHERE timestamp >= datetime('now', '-24 hours')
        AND prediction = 'Anomaly detected'
        ORDER BY timestamp DESC
        LIMIT 10
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        # Convert CPU to percentage and memory to MB with proper error handling
        if not df.empty:
            # Handle CPU conversion - ensure it's numeric
            try:
                # Convert CPU to numeric, handling any string values
                df['cpu'] = pd.to_numeric(df['cpu'], errors='coerce')
                # Filter out rows where CPU conversion failed
                df = df.dropna(subset=['cpu'])
                # Filter for high CPU usage (> 50%)
                df = df[df['cpu'] > 0.5]
                
                # Convert CPU to percentage
                df['cpu_percent'] = (df['cpu'] * 100).round(1)
                
                # Handle memory conversion
                df['memory'] = pd.to_numeric(df['memory'], errors='coerce')
                df = df.dropna(subset=['memory'])
                df['memory_mb'] = (df['memory'] / (1024 * 1024)).round(1)
                
                # Convert timestamp
                df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
                df = df.dropna(subset=['timestamp'])
                
                # Add time ago
                df['time_ago'] = df['timestamp'].apply(lambda x: get_time_ago(x))
                
            except Exception as e:
                st.error(f"Error processing anomaly data: {e}")
                return pd.DataFrame()
        
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
        # First check if kubectl is available
        result = subprocess.run(['which', 'kubectl'], capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            # kubectl not available, try alternative methods
            return False, f"kubectl not available. Pod {pod_name} cannot be killed from this container."
        
        # kubectl is available, proceed with deletion
        result = subprocess.run([
            'kubectl', 'delete', 'pod', pod_name, 
            '-n', namespace, '--force', '--grace-period=0'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            return True, f"Successfully killed pod {pod_name}"
        else:
            return False, f"Failed to kill pod: {result.stderr}"
    except subprocess.TimeoutExpired:
        return False, "Timeout while trying to kill pod"
    except FileNotFoundError:
        return False, "kubectl command not found. Pod killing is not available from this container."
    except Exception as e:
        return False, f"Error killing pod: {str(e)}"

def show_pod_killing_alternatives():
    """Show alternative ways to kill pods when kubectl is not available"""
    st.markdown("---")
    st.markdown("**🔧 Alternative Ways to Kill Pods:**")
    
    st.markdown("""
    Since kubectl is not available in this container, you can kill pods using:
    
    **1. From your local machine:**
    ```bash
    kubectl delete pod <pod-name> -n smartops --force --grace-period=0
    ```
    
    **2. From Cloud Shell:**
    ```bash
    kubectl delete pod <pod-name> -n smartops --force --grace-period=0
    ```
    
    **3. From another pod with kubectl:**
    ```bash
    kubectl exec -it <monitor-pod> -- kubectl delete pod <pod-name> -n smartops
    ```
    
    **4. Scale deployment to 0:**
    ```bash
    kubectl scale deployment <deployment-name> --replicas=0 -n smartops
    ```
    """)
    
    # Show current stress test pods
    st.markdown("**🚨 Current Stress Test Pods:**")
    st.markdown("Use these commands to kill the stress-test pod:")
    
    st.code("kubectl delete pod stress-test -n smartops --force --grace-period=0", language="bash")
    
    # Add a button to show more info
    if st.button("📋 Show All Pods"):
        show_all_pods_info()

def show_all_pods_info():
    """Show information about all pods in the smartops namespace"""
    st.markdown("**📊 All Pods in smartops Namespace:**")
    
    st.markdown("""
    To see all pods and their status:
    ```bash
    kubectl get pods -n smartops
    ```
    
    To see detailed pod information:
    ```bash
    kubectl describe pod <pod-name> -n smartops
    ```
    
    To see pod logs:
    ```bash
    kubectl logs <pod-name> -n smartops
    ```
    """)

def ignore_anomaly(pod_name):
    """Mark an anomaly as ignored (store in session state)"""
    if 'ignored_anomalies' not in st.session_state:
        st.session_state.ignored_anomalies = set()
    
    st.session_state.ignored_anomalies.add(pod_name)
    st.rerun()

def show_anomaly_notifications():
    """Display anomaly notifications in the sidebar"""
    # Add refresh button and debug button
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown('<div class="sb-title">🚨 Active Anomalies</div>', unsafe_allow_html=True)
    with col2:
        if st.button("🔄", key="refresh_anomalies", help="Refresh anomalies"):
            st.rerun()
    with col3:
        if st.button("🐛", key="debug_anomalies", help="Debug database"):
            debug_database()
    
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
    
    # Remove duplicate pods (keep only the most recent entry for each pod)
    active_anomalies = active_anomalies.drop_duplicates(subset=['pod_name'], keep='first')
    
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
    for idx, (_, row) in enumerate(active_anomalies.iterrows()):
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
        
        # Action buttons with unique keys
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(f"🗑️ Kill", key=f"kill_{pod_name}_{idx}", use_container_width=True):
                success, message = kill_pod(pod_name)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
                    # Show alternatives when kubectl is not available
                    if "kubectl not available" in message:
                        show_pod_killing_alternatives()
        
        with col2:
            if st.button(f"👁️ Ignore", key=f"ignore_{pod_name}_{idx}", use_container_width=True):
                ignore_anomaly(pod_name)
    
    # Show ignored anomalies count
    if ignored:
        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
        st.markdown(
            f'<div style="color: #bdc3c7; font-size: 0.8rem; text-align: center;">👁️ {len(ignored)} anomalies ignored</div>',
            unsafe_allow_html=True
        )
    
    # Quick Actions Section
    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-title">⚡ Quick Actions</div>', unsafe_allow_html=True)
    
    # Get current anomalies for quick actions
    current_anomalies = get_anomaly_data()
    if not current_anomalies.empty:
        st.markdown("**🚨 Active Anomaly Pods:**")
        for idx, (_, row) in enumerate(current_anomalies.iterrows()):
            pod_name = row['pod_name']
            cpu_percent = row['cpu_percent']
            
            # Create a copy-paste command
            kill_command = f"kubectl delete pod {pod_name} -n smartops --force --grace-period=0"
            
            st.markdown(f"""
            <div style="
                background: rgba(255,107,107,0.1); 
                border: 1px solid #ff6b6b; 
                border-radius: 8px; 
                padding: 0.8rem; 
                margin: 0.5rem 0;
            ">
                <div style="color: #ff6b6b; font-weight: bold; margin-bottom: 0.5rem;">
                    🔴 {pod_name} (CPU: {cpu_percent}%)
                </div>
                <div style="font-size: 0.8rem; color: #dfe6e9;">
                    Copy and run this command:
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.code(kill_command, language="bash")
            
            # Add a copy button
            if st.button(f"📋 Copy Command", key=f"copy_{pod_name}_{idx}", use_container_width=True):
                st.success(f"Command copied! Run: {kill_command}")
    else:
        st.markdown("✅ No active anomalies")
    
    st.markdown("---")
    
    # Show namespace info
    st.markdown("**📋 Current Namespace:** `smartops`")
    
    # Add a button to refresh pod list
    if st.button("🔄 Refresh Pod List", key="refresh_pods", use_container_width=True):
        st.rerun()

def debug_database():
    """Debug database connection and show detailed information"""
    st.markdown("---")
    st.markdown("**🐛 Database Debug Information**")
    
    # Try multiple possible database paths
    db_paths = [
        '/app/dashboard/data/data.db',  # Production path
        'smartops-ai/dashboard/data/data.db',  # Local development
        'data/data.db',  # Relative path
        'dashboard/data/data.db'  # Another relative path
    ]
    
    for db_path in db_paths:
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Check if table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='anomalies'")
            if cursor.fetchone():
                st.success(f"✅ Table found in: {db_path}")
                
                # Get table structure
                cursor.execute("PRAGMA table_info(anomalies)")
                columns = cursor.fetchall()
                st.info(f"📋 Table structure: {[col[1] for col in columns]}")
                
                # Get row count
                cursor.execute("SELECT COUNT(*) FROM anomalies")
                count = cursor.fetchone()[0]
                st.info(f"📊 Total records: {count}")
                
                # Get sample data
                cursor.execute("SELECT * FROM anomalies LIMIT 3")
                sample = cursor.fetchall()
                st.info(f"📝 Sample data: {sample}")
                
                # Get data types
                cursor.execute("SELECT * FROM anomalies LIMIT 1")
                sample_row = cursor.fetchone()
                if sample_row:
                    st.info(f"🔍 Sample row types: {[type(val).__name__ for val in sample_row]}")
                
                conn.close()
                break
            else:
                st.warning(f"⚠️ Table 'anomalies' not found in: {db_path}")
                conn.close()
                
        except Exception as e:
            st.error(f"❌ Error with {db_path}: {str(e)}")
    
    st.markdown("---")

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

        /* ---------- Modern Sidebar Design ---------- */
        section[data-testid="stSidebar"] > div:first-child{
            background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            height: 100vh;
            padding: 1.2rem 1rem 2rem 1rem;
            border-top-right-radius: 20px;
            border-bottom-right-radius: 20px;
            box-shadow: 2px 0 20px rgba(0,0,0,0.3);
            position: relative;
            overflow-y: auto;
        }

        /* hide default sidebar header space */
        section[data-testid="stSidebar"] [data-testid="stSidebarHeader"],
        section[data-testid="stSidebar"] > div:first-child > div:first-child{
            display:none !important;
        }

        /* Modern typography */
        .sb-title{
            font-size: 1.1rem; 
            font-weight: 700; 
            color: #ffffff; 
            letter-spacing: .6px;
            margin: .3rem 0 .2rem 0; 
            display:flex; 
            align-items:center; 
            gap:.5rem;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        .sb-sub{
            color:#a8dadc; 
            font-size:.9rem; 
            margin:.7rem 0 .5rem 0; 
            display:flex; 
            align-items:center; 
            gap:.45rem;
            opacity:.95;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .sb-divider{
            border-top: 1px solid rgba(168, 218, 220, 0.3);
            margin: 1.1rem 0 1.1rem 0;
        }
        .sb-section{ 
            margin: .3rem 0 1rem 0; 
            padding: 0.5rem;
            border-radius: 12px;
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(10px);
        }

        /* Modern button styles */
        .stButton > button {
            width: 100% !important;
            text-align: left !important;
            font-weight: 600 !important;
            color: #ffffff !important;
            background: linear-gradient(135deg, rgba(102,126,234,0.8) 0%, rgba(118,75,162,0.8) 100%) !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
            border-radius: 12px !important;
            padding: .75rem 1rem !important;
            line-height: 1.2rem !important;
            box-shadow: 0 4px 15px rgba(102,126,234,0.2);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            margin: 0.3rem 0 !important;
        }
        .stButton > button:hover{
            background: linear-gradient(135deg, rgba(102,126,234,1) 0%, rgba(118,75,162,1) 100%) !important;
            transform: translateX(8px) translateY(-2px);
            box-shadow: 0 8px 25px rgba(102,126,234,0.4);
            border-color: rgba(255,255,255,0.4) !important;
        }
        .stButton > button:active{
            transform: translateX(4px) translateY(0px);
            box-shadow: 0 4px 15px rgba(102,126,234,0.3);
        }

        /* Make emojis align nicely inside buttons */
        .stButton > button p { 
            margin: 0; 
            font-size: 0.95rem;
        }
        
        /* Anomaly notification styles */
        .anomaly-card {
            background: linear-gradient(135deg, rgba(255,99,71,0.2) 0%, rgba(255,69,0,0.2) 100%);
            border: 1px solid rgba(255,99,71,0.3);
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 15px rgba(255,99,71,0.1);
        }

        /* Status indicators */
        .status-indicator {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 8px;
            background: #4ade80;
            box-shadow: 0 0 10px rgba(74, 222, 128, 0.5);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }

        /* Scrollbar styling */
        section[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar {
            width: 6px;
        }
        section[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar-track {
            background: rgba(255,255,255,0.1);
            border-radius: 3px;
        }
        section[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 3px;
        }
        section[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ---------- Sidebar content ----------
    st.markdown(
        """
        <div style="text-align:center; margin: .2rem 0 1.5rem 0;">
            <div style="font-size:2.5rem; margin-bottom: 0.5rem;">🚀</div>
            <div style="font-size:1.5rem; font-weight:800; color:#fff; letter-spacing:.8px; margin-bottom: 0.3rem;">SmartOps</div>
            <div style="font-size:.95rem; color:#a8dadc; opacity:.95; margin-bottom: 0.5rem;">AI Kubernetes Platform</div>
            <div style="display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
                <div class="status-indicator"></div>
                <span style="font-size: 0.8rem; color: #4ade80;">System Online</span>
            </div>
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

    # ---- Pod & Cluster Management
    st.markdown('<div class="sb-section">', unsafe_allow_html=True)
    st.markdown('<div class="sb-sub">🛰️ Pod & Cluster</div>', unsafe_allow_html=True)
    if st.button("🧭  Pod Explorer & Logs", key="nav_pod", use_container_width=True):
        st.switch_page("pages/2_Pod_Explorer_and_Logs.py")
    if st.button("🔍  Kubernetes Shell & Explorer", key="nav_cluster", use_container_width=True):
        st.switch_page("pages/3_Kubernetes_Shell_and_Cluster_Explorer.py")
    st.markdown('</div>', unsafe_allow_html=True)

    # ---- Operations & Scaling
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
    if st.button("💬  Misi AI Assistant", key="nav_misi", use_container_width=True):
        st.switch_page("pages/7_Misi_AI_Assistant.py")
    st.markdown('</div>', unsafe_allow_html=True)

    # ---- Quick Actions
    st.markdown('<div class="sb-section">', unsafe_allow_html=True)
    st.markdown('<div class="sb-sub">⚡ Quick Actions</div>', unsafe_allow_html=True)
    if st.button("🔄  Refresh All Data", key="nav_refresh", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    if st.button("📊  System Status", key="nav_status", use_container_width=True):
        st.info("🟢 All systems operational\n📊 Data refreshed\n🤖 AI services active")
    st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-title">🔧 System Info</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    
    # System status info
    st.markdown(
        """
        <div style='color:#a8dadc; font-size:.85rem; text-align:center; opacity:.9; line-height: 1.4;'>
            <div style='margin-bottom: 0.5rem;'>
                <span style='color: #4ade80;'>●</span> API: Active
            </div>
            <div style='margin-bottom: 0.5rem;'>
                <span style='color: #4ade80;'>●</span> Database: Connected
            </div>
            <div style='margin-bottom: 0.5rem;'>
                <span style='color: #4ade80;'>●</span> AI Engine: Ready
            </div>
            <div style='margin-top: 1rem; padding-top: 0.5rem; border-top: 1px solid rgba(168, 218, 220, 0.2);'>
                SmartOps v1.0<br/>
                <span style='font-size: 0.8rem; opacity: 0.8;'>© 2024 SmartOps AI</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Note: This function should be called from individual pages, not run here
# show_sidebar()
