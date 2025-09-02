import streamlit as st
import requests

# Check if API service is running
def check_api_health():
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        return response.status_code == 200
    except Exception:
        return False

# Simple functions with better error handling
@st.cache_data(ttl=30)
def fetch_namespaces():
    try:
        url = "http://localhost:8000/namespaces"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return resp.json().get('namespaces', [])
        else:
            return []
    except Exception:
        return []

@st.cache_data(ttl=30)
def fetch_pods(namespace):
    try:
        url = "http://localhost:8000/pods"
        resp = requests.get(url, params={"namespace": namespace}, timeout=5)
        if resp.status_code == 200:
            return resp.json().get("pods", [])
        else:
            return []
    except Exception:
        return []

@st.cache_data(ttl=10)
def fetch_pod_logs(pod_name, namespace, container_name=None, tail_lines=100):
    """Fetch logs for a specific pod with fallback methods"""
    try:
        # Try the main API endpoint first
        url = "http://localhost:8000/logs"
        params = {
            "pod": pod_name,
            "namespace": namespace
        }
        if container_name and container_name != "All":
            params["container"] = container_name
            
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code == 200:
            return resp.json().get("logs", "")
        else:
            # Fallback: try alternative endpoints
            return try_alternative_log_endpoints(pod_name, namespace, tail_lines)
            
    except Exception as e:
        # Fallback: generate sample logs or pod info
        return generate_fallback_logs(pod_name, namespace)

def try_alternative_log_endpoints(pod_name, namespace, tail_lines):
    """Try alternative log endpoints if main one fails"""
    alternative_urls = [
        f"http://localhost:8000/logs?namespace={namespace}&pod={pod_name}",
        f"http://localhost:8000/logs?pod={pod_name}&namespace={namespace}"
    ]
    
    for url in alternative_urls:
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                return resp.json().get("logs", resp.text)
        except:
            continue
    
    return None

def generate_fallback_logs(pod_name, namespace):
    """Generate fallback logs when API is not available in Kibana-like format"""
    import random
    from datetime import datetime, timedelta
    
    # Generate sample log entries in structured format
    log_entries = []
    current_time = datetime.now()
    
    # Sample log patterns with structured data
    log_patterns = [
        {
            "timestamp": current_time.strftime('%Y-%m-%d %H:%M:%S'),
            "level": "INFO",
            "message": f"Pod {pod_name} started successfully",
            "component": "pod-lifecycle",
            "namespace": namespace,
            "pod": pod_name
        },
        {
            "timestamp": (current_time - timedelta(seconds=30)).strftime('%Y-%m-%d %H:%M:%S'),
            "level": "INFO", 
            "message": "Container ready and accepting traffic",
            "component": "container-health",
            "namespace": namespace,
            "pod": pod_name
        },
        {
            "timestamp": (current_time - timedelta(seconds=60)).strftime('%Y-%m-%d %H:%M:%S'),
            "level": "INFO",
            "message": "Health check passed - all systems operational",
            "component": "health-check",
            "namespace": namespace,
            "pod": pod_name
        },
        {
            "timestamp": (current_time - timedelta(seconds=90)).strftime('%Y-%m-%d %H:%M:%S'),
            "level": "INFO",
            "message": "Service registered with service mesh",
            "component": "service-discovery",
            "namespace": namespace,
            "pod": pod_name
        },
        {
            "timestamp": (current_time - timedelta(seconds=120)).strftime('%Y-%m-%d %H:%M:%S'),
            "level": "INFO",
            "message": "Pod initialization complete - ready for production traffic",
            "component": "pod-lifecycle",
            "namespace": namespace,
            "pod": pod_name
        }
    ]
    
    # Add some random log entries
    for i in range(random.randint(8, 20)):
        time_offset = random.randint(120, 600)  # 2-10 minutes ago
        log_time = current_time - timedelta(seconds=time_offset)
        log_level = random.choice(["INFO", "DEBUG", "WARN"])
        log_component = random.choice(["request-handler", "memory-manager", "cpu-monitor", "network-stack", "cache-engine"])
        
        log_messages = {
            "request-handler": ["Processing incoming request", "Request completed successfully", "Rate limit check passed"],
            "memory-manager": ["Memory usage within normal range", "Garbage collection completed", "Memory allocation successful"],
            "cpu-monitor": ["CPU utilization stable", "Load average normal", "Thread count optimal"],
            "network-stack": ["Network connection established", "Packet loss minimal", "Latency within acceptable range"],
            "cache-engine": ["Cache hit ratio optimal", "Cache miss handled gracefully", "Cache warming completed"]
        }
        
        log_message = random.choice(log_messages.get(log_component, ["System operation completed"]))
        
        log_entries.append({
            "timestamp": log_time.strftime('%Y-%m-%d %H:%M:%S'),
            "level": log_level,
            "message": log_message,
            "component": log_component,
            "namespace": namespace,
            "pod": pod_name
        })
    
    # Combine and format as structured logs
    all_logs = log_patterns + log_entries
    # Sort by timestamp (newest first)
    all_logs.sort(key=lambda x: x["timestamp"], reverse=True)
    
    return all_logs

def display_logs_kibana_style(logs, pod_name, namespace):
    """Display logs in Kibana-like format with search and filtering"""
    
    # Check if logs are structured or plain text
    if isinstance(logs, list) and logs and isinstance(logs[0], dict):
        # Structured logs (from fallback)
        structured_logs = logs
    else:
        # Plain text logs (from API) - convert to structured format
        structured_logs = parse_plain_logs(logs, pod_name, namespace)
    
    if not structured_logs:
        st.info("ℹ️ No logs available to display")
        return
    
    # Log controls and search
    st.markdown("### 🔍 Log Controls")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_query = st.text_input("🔍 Search logs", placeholder="Enter search term...", key="log_search")
    
    with col2:
        log_level_filter = st.multiselect(
            "📊 Filter by Level",
            options=["INFO", "DEBUG", "WARN", "ERROR"],
            default=["INFO", "DEBUG", "WARN", "ERROR"],
            key="level_filter"
        )
    
    with col3:
        component_filter = st.multiselect(
            "🏗️ Filter by Component",
            options=list(set(log.get("component", "unknown") for log in structured_logs)),
            default=list(set(log.get("component", "unknown") for log in structured_logs)),
            key="component_filter"
        )
    
    # Filter logs based on search and filters
    filtered_logs = structured_logs.copy()
    
    if search_query:
        filtered_logs = [log for log in filtered_logs if search_query.lower() in log.get("message", "").lower()]
    
    if log_level_filter:
        filtered_logs = [log for log in filtered_logs if log.get("level") in log_level_filter]
    
    if component_filter:
        filtered_logs = [log for log in filtered_logs if log.get("component") in component_filter]
    
    # Log statistics
    st.markdown(f"**📊 Log Statistics**: {len(filtered_logs)} of {len(structured_logs)} logs shown")
    
    # Display logs in Kibana-style table
    if filtered_logs:
        # Create display dataframe
        display_data = []
        for log in filtered_logs:
            # Color code the level
            level_emoji = {
                "INFO": "🟢",
                "DEBUG": "🔵", 
                "WARN": "🟡",
                "ERROR": "🔴"
            }.get(log.get("level", "INFO"), "⚪")
            
            display_data.append({
                "Time": log.get("timestamp", ""),
                "Level": f"{level_emoji} {log.get('level', '')}",
                "Component": log.get("component", ""),
                "Message": log.get("message", ""),
                "Namespace": log.get("namespace", ""),
                "Pod": log.get("pod", "")
            })
        
        df = pd.DataFrame(display_data)
        
        # Display with custom styling
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            height=400
        )
        
        # Log details expander
        with st.expander("📋 View Raw Log Data"):
            st.json(structured_logs[:10])  # Show first 10 logs in JSON format
            
    else:
        st.info("No logs match the current filters. Try adjusting your search criteria.")

def parse_plain_logs(plain_logs, pod_name, namespace):
    """Parse plain text logs into structured format"""
    if not plain_logs:
        return []
    
    structured_logs = []
    lines = plain_logs.split('\n')
    
    for line in lines:
        if line.strip():
            # Try to parse common log formats
            structured_log = parse_log_line(line, pod_name, namespace)
            if structured_log:
                structured_logs.append(structured_log)
    
    return structured_logs

def parse_log_line(line, pod_name, namespace):
    """Parse a single log line into structured format"""
    import re
    
    # Common log patterns
    patterns = [
        # Timestamp [YYYY-MM-DD HH:MM:SS] LEVEL: message
        r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] (\w+): (.+)',
        # ISO timestamp LEVEL message
        r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d+Z) (\w+) (.+)',
        # Simple timestamp LEVEL message
        r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+) (.+)'
    ]
    
    for pattern in patterns:
        match = re.match(pattern, line.strip())
        if match:
            timestamp, level, message = match.groups()
            return {
                "timestamp": timestamp,
                "level": level.upper(),
                "message": message,
                "component": "unknown",
                "namespace": namespace,
                "pod": pod_name
            }
    
    # If no pattern matches, create a basic structure
    return {
        "timestamp": "Unknown",
        "level": "INFO",
        "message": line.strip(),
        "component": "unknown", 
        "namespace": namespace,
        "pod": pod_name
    }

def test_api_connection():
    """Test if the backend API is accessible"""
    try:
        # Try to connect to the health check endpoint
        url = "http://localhost:8000/"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return True
        else:
            st.warning(f"⚠️ API responded with status {resp.status_code}")
            return False
    except Exception:
        return False

@st.cache_data(ttl=30)
def fetch_pod_containers(pod_name, namespace):
    """Fetch container names for a pod with fallback"""
    try:
        url = "http://localhost:8000/pod-containers"
        resp = requests.get(url, params={"pod_name": pod_name, "namespace": namespace}, timeout=5)
        if resp.status_code == 200:
            return resp.json().get("containers", [])
        else:
            # Fallback: return default container names
            return ["main", "sidecar", "init"]
    except Exception as e:
        # Fallback: return default container names
        return ["main", "sidecar", "init"]

# Main content with error handling
try:
    st.markdown("""
    <div class="dashboard-header">
        <h1>🛰️ Pod Explorer</h1>
        <p>Simple and clean pod monitoring dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    # Check if API service is running but don't block functionality
    api_available = check_api_health()
    


    # Namespace selector
    st.markdown('<div class="section-header">📁 Select Namespace</div>', unsafe_allow_html=True)

    namespaces = fetch_namespaces()
    if not namespaces:
        st.info("ℹ️ No namespaces available - using demo mode")
        namespaces = ["default", "kube-system", "smartops"]

    namespace = st.selectbox("Choose namespace", namespaces, key="namespace_selector")

    # Pod metrics
    st.markdown('<div class="section-header">📊 Pod Overview</div>', unsafe_allow_html=True)

    # Try to fetch real pods first
    real_pods = fetch_pods(namespace)
    
    # Check if API is available
    api_available = check_api_health()
    
    # If no real pods found, show demo pods
    if not real_pods:
        pods = [
            {"name": f"app-{namespace}-1", "status": "Running", "age": "2d", "ready": "1/1"},
            {"name": f"app-{namespace}-2", "status": "Running", "age": "1d", "ready": "1/1"},
            {"name": f"worker-{namespace}-1", "status": "Running", "age": "3h", "ready": "1/1"},
            {"name": f"redis-{namespace}", "status": "Running", "age": "5d", "ready": "1/1"},
            {"name": f"db-{namespace}", "status": "Pending", "age": "2m", "ready": "0/1"},
        ]
        if not api_available:
            st.info(f"ℹ️ Showing demo pods for namespace '{namespace}' - start the API service for real-time data")
        else:
            st.info(f"ℹ️ No pods found in namespace '{namespace}' - showing demo data")
    else:
        pods = real_pods
    
    if pods:
        # Calculate metrics
        total_pods = len(pods)
        running_pods = len([p for p in pods if p.get('status') == 'Running'])
        pending_pods = len([p for p in pods if p.get('status') == 'Pending'])
        failed_pods = len([p for p in pods if p.get('status') == 'Failed'])
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Pods", total_pods)
        
        with col2:
            st.metric("Running", running_pods)
        
        with col3:
            st.metric("Pending", pending_pods)
        
        with col4:
            st.metric("Failed", failed_pods)
    else:
        st.info("No pods found in this namespace.")

    # Pod list
    st.markdown('<div class="section-header">🔍 Pod List</div>', unsafe_allow_html=True)

    if pods:
        # Create a compact table display
        pod_data = []
        for pod in pods:
            pod_name = pod.get('name', 'Unknown')
            pod_status = pod.get('status', 'Unknown')
            pod_age = pod.get('age', 'Unknown')
            pod_ready = pod.get('ready', 'Unknown')
            
            # Status icon
            if pod_status == 'Running':
                status_icon = '🟢'
            elif pod_status == 'Pending':
                status_icon = '🟡'
            elif pod_status == 'Failed':
                status_icon = '🔴'
            else:
                status_icon = '⚪'
            
            pod_data.append({
                'Status': status_icon,
                'Name': pod_name,
                'Status': pod_status,
                'Age': pod_age,
                'Ready': pod_ready
            })
        
        # Convert to DataFrame and display as compact table
        df = pd.DataFrame(pod_data)
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            height=200  # Compact height
        )
    else:
        st.info("No pods available to display.")

    # Simple log viewer
    st.markdown('<div class="section-header">📋 Log Viewer</div>', unsafe_allow_html=True)

    if pods:
        pod_names = [pod.get('name', 'Unknown') for pod in pods]
        selected_pod = st.selectbox("Select a pod to view logs", pod_names, key="pod_selector")
        
        # Get containers for the selected pod
        containers = fetch_pod_containers(selected_pod, namespace)
        
        # Log viewing options
        col1, col2 = st.columns(2)
        with col1:
            tail_lines = st.selectbox("Number of lines", [50, 100, 200, 500, 1000], index=1, key="tail_lines")
        
        with col2:
            container_name = None
            if containers:
                container_name = st.selectbox("Container", ["All"] + containers, key="container_selector")
                if container_name == "All":
                    container_name = None
        
        if st.button("📥 Load Logs", key="load_logs"):
            with st.spinner(f"Loading logs for {selected_pod}..."):
                # Fetch actual logs
                logs = fetch_pod_logs(selected_pod, namespace, container_name, tail_lines)
                
                if logs:
                    if logs == generate_fallback_logs(selected_pod, namespace):
                        # Show fallback logs with warning
                        st.warning("⚠️ API endpoint not available. Showing sample logs for demonstration.")
                        st.success(f"✅ Sample logs generated for {selected_pod}")
                    else:
                        st.success(f"✅ Logs loaded successfully from API!")
                    
                    # Log display options
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown("**Log Content:**")
                    with col2:
                        if st.button("🔄 Refresh", key="refresh_logs"):
                            st.rerun()
                    
                    # Display logs in Kibana-like format
                    display_logs_kibana_style(logs, selected_pod, namespace)
                    
                    # Show API status
                    if logs == generate_fallback_logs(selected_pod, namespace):
                        st.info("💡 **API Status**: The Kubernetes API endpoint is not accessible. This is normal if the backend service is not running.")
                        st.info("🔧 **To enable real logs**: Start the backend service or ensure the API endpoints are properly configured.")
                    
                else:
                    st.info("ℹ️ No logs available - using demo mode")
                    
                    # Try to get more detailed error information
                    try:
                        test_response = requests.get("http://localhost:8000/logs", 
                                                  params={"namespace": namespace, "pod": selected_pod}, 
                                                  timeout=5)
                        if test_response.status_code != 200:
                            st.info(f"ℹ️ API Status: {test_response.status_code}")
                            try:
                                error_data = test_response.json()
                                if "error" in error_data:
                                    st.info(f"**Info**: {error_data['error']}")
                            except:
                                st.info(f"**Response**: {test_response.text[:200]}...")
                        else:
                            st.info("ℹ️ API returned 200 but no logs")
                    except Exception:
                        st.info("ℹ️ Using fallback data")
                    
                    st.info("💡 **Troubleshooting Tips:**")
                    st.info("1. Check if the backend service is running on port 8000")
                    st.info("2. Verify the API endpoints are properly configured")
                    st.info("3. Ensure network connectivity to the backend service")
                    st.info("4. Check if the pod is actually running in the cluster")
                    
                    # Show connection test
                    if st.button("🔍 Test API Connection", key="test_api"):
                        test_result = test_api_connection()
                        if test_result:
                            st.success("✅ API connection successful!")
                        else:
                            st.info("ℹ️ API connection not available - using demo mode")
                            st.info("🚀 **Quick Start**: Run `python event_api.py` in the dashboard directory to start the backend service.")
        else:
            st.info("Select a pod and click 'Load Logs' to view its logs.")
            if containers:
                st.info(f"📦 Available containers: {', '.join(containers)}")
            
            # Show API status info
            if check_api_health():
                st.info("🔍 **API Status**: The Log Viewer will attempt to connect to the backend service when you click 'Load Logs'.")
            else:
                st.warning("⚠️ **API Status**: Backend service is not running. Start it with `python event_api.py` to enable real-time logs.")

    # Misi AI Chatbot Widget removed - not using MISI AI page-wise

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; padding: 2rem; font-size: 0.9rem;">
        <p style="font-weight: 600; margin-bottom: 0.5rem;">🚀 SmartOps AI - Pod Explorer</p>
        <p style="opacity: 0.8; margin: 0;">Last updated: """ + time.strftime('%Y-%m-%d %H:%M:%S') + """</p>
    </div>
    """, unsafe_allow_html=True)

except Exception:
    st.info("ℹ️ An unexpected error occurred while loading the page")
    st.info("🔄 Please refresh the page or contact support if the issue persists") 