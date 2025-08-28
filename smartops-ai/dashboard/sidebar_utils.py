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
    try:
        now = datetime.now()
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        
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
    except Exception as e:
        return "Unknown time"

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

def show_sidebar():
    # Static sidebar - never changes, no session state needed
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
            margin: 0 !important; 
            padding: 0 !important; 
            line-height: 1.2rem !important;
        }

        /* Status indicator animation */
        .status-indicator {
            width: 8px;
            height: 8px;
            background: #4ade80;
            border-radius: 50%;
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
            background: rgba(255,255,255,0.3);
            border-radius: 3px;
        }
        section[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar-thumb:hover {
            background: rgba(255,255,255,0.5);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # ---------- Static Sidebar Content (Never Changes) ----------
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

    st.markdown('<div class="sb-title">🧭 Navigation</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

    # ---- Core Monitoring (Static)
    st.markdown('<div class="sb-section">', unsafe_allow_html=True)
    st.markdown('<div class="sb-sub">📊 Core Monitoring</div>', unsafe_allow_html=True)
    st.info("🟩 Overview Dashboard")
    st.info("🔥 Anomaly Detection")
    st.markdown('</div>', unsafe_allow_html=True)

    # ---- Pod & Cluster Management (Static)
    st.markdown('<div class="sb-section">', unsafe_allow_html=True)
    st.markdown('<div class="sb-sub">🛰️ Pod & Cluster</div>', unsafe_allow_html=True)
    st.info("🧭 Pod Explorer & Logs")
    st.info("🔍 Kubernetes Shell & Explorer")
    st.markdown('</div>', unsafe_allow_html=True)

    # ---- Operations & Scaling (Static)
    st.markdown('<div class="sb-section">', unsafe_allow_html=True)
    st.markdown('<div class="sb-sub">⚡ Operations</div>', unsafe_allow_html=True)
    st.info("⚡ Auto Scaling Control")
    st.info("🚀 Deployments")
    st.markdown('</div>', unsafe_allow_html=True)

    # ---- AI & Analytics (Static)
    st.markdown('<div class="sb-section">', unsafe_allow_html=True)
    st.markdown('<div class="sb-sub">🤖 AI & Analytics</div>', unsafe_allow_html=True)
    st.info("🤖 AI Actions")
    st.info("📝 Incident Timeline")
    st.info("💬 Misi AI")
    st.markdown('</div>', unsafe_allow_html=True)

    # ---- Quick Actions (Static)
    st.markdown('<div class="sb-section">', unsafe_allow_html=True)
    st.markdown('<div class="sb-sub">⚡ Quick Actions</div>', unsafe_allow_html=True)
    st.info("🔄 Refresh All Data")
    st.info("📊 System Status")
    st.markdown('</div>', unsafe_allow_html=True)

    # Footer (Static)
    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-title">🔧 System Info</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    
    # Static system status info
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

def get_current_page():
    """Get the current page from session state"""
    return st.session_state.get('current_page', 'overview')

def set_current_page(page_name):
    """Set the current page in session state"""
    st.session_state.current_page = page_name
