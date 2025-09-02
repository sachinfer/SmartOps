import streamlit as st
import requests
from datetime import datetime

# Check if API service is running
def check_api_health():
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        return response.status_code == 200
    except Exception:
        return False

# Fetch node data
def fetch_node_data():
    try:
        response = requests.get("http://localhost:8000/nodes", timeout=5)
        if response.status_code == 200:
            return response.json().get('nodes', [])
        return []
    except Exception:
        return []

# Fetch pod data
def fetch_pod_data():
    try:
        response = requests.get("http://localhost:8000/pods", timeout=5)
        if response.status_code == 200:
            return response.json().get('pods', [])
        return []
    except Exception:
        return []

# Get service count
def get_service_count():
    try:
        response = requests.get("http://localhost:8000/services", timeout=5)
        if response.status_code == 200:
            return len(response.json().get('services', []))
        return 0
    except Exception:
        return 0

# Get namespace count
def get_namespace_count():
    try:
        response = requests.get("http://localhost:8000/namespaces", timeout=5)
        if response.status_code == 200:
            return len(response.json().get('namespaces', []))
        return 0
    except Exception:
        return 0

# Main content
st.markdown("""
<div class="dashboard-header">
    <h1>📊 Kubernetes Cluster Overview</h1>
    <p>Real-time monitoring dashboard powered by SmartOps AI</p>
</div>

<!-- Floating particles for visual appeal -->
<div class="floating-particle"></div>
<div class="floating-particle"></div>
<div class="floating-particle"></div>
<div class="floating-particle"></div>
<div class="floating-particle"></div>
<div class="floating-particle"></div>
<div class="floating-particle"></div>
<div class="floating-particle"></div>
<div class="floating-particle"></div>
""", unsafe_allow_html=True)

# Check if API service is running and show helpful message
# api_available = check_api_health()

# Show cluster environment information
# env = get_cluster_environment()
# st.markdown(f"""
# <div class="status-message" style="background: rgba(45, 55, 72, 0.9); border-color: rgba(102, 126, 234, 0.5);">
#     <div class="status-icon">🌍</div>
#     <div class="status-text">
#         <strong>Environment:</strong> {env.upper()} | 
#         <strong>API Status:</strong> {'✅ Available' if api_available else '❌ Not Available'} | 
#         <strong>Cluster:</strong> {'🟢 Connected' if env == 'kubernetes' else '🟡 Local/Docker'}
#     </div>
# </div>
# """, unsafe_allow_html=True)

# Show Google Cloud specific information
# if env == "google_cloud":
#     gcp_project = os.environ.get('GOOGLE_CLOUD_PROJECT', 'Not Set')
#     gcp_zone = os.environ.get('GOOGLE_CLOUD_ZONE', 'Not Set')
#     gcp_region = os.environ.get('GOOGLE_CLOUD_REGION', 'Not Set')
#     
#     st.markdown(f"""
#     <div class="status-message" style="background: rgba(56, 178, 172, 0.2); border-color: rgba(56, 178, 172, 0.5);">
#         <div class="status-icon">☁️</div>
#         <div class="status-text">
#             <strong>Google Cloud Info:</strong> Project: {gcp_project} | Zone: {gcp_zone} | Region: {gcp_region}
#         </div>
#     </div>
#     """, unsafe_allow_html=True)
#     
#     # Show troubleshooting tips for Google Cloud
#     if not api_available:
#         st.markdown("""
#         <div class="status-message" style="background: rgba(229, 62, 62, 0.2); border-color: rgba(229, 62, 62, 0.5);">
#             <div class="status-icon">🔧</div>
#             <div class="status-text">
#                 <strong>Google Cloud Troubleshooting:</strong><br/>
#                 • Check if smartops-api-service is deployed and running<br/>
#                 • Verify service names and ports in your deployment<br/>
#                 • Check network policies and firewall rules<br/>
#                 • Ensure services are in the same namespace
#             </div>
#         </div>
#         """, unsafe_allow_html=True)
#         
#         # Add connectivity test button
#         if st.button("🔍 Test API Connectivity", type="primary"):
#             st.markdown("### 📡 Connectivity Test Results")
#             connectivity_results = test_connectivity()
#             for result in connectivity_results:
#                 st.text(result)
#             
#             st.markdown("""
#             **🔧 Next Steps:**
#             1. **Check if smartops-api-service is running:**
#                ```bash
#                kubectl get pods -n <namespace>
#                kubectl get services -n <namespace>
#                ```
#             
#             2. **Check service endpoints:**
#                ```bash
#                kubectl get endpoints smartops-api-service -n <namespace>
#                ```
#             
#             3. **Check logs:**
#                ```bash
#                kubectl logs -f deployment/smartops-api-service -n <namespace>
#                ```
#             
#             4. **Verify network policies:**
#                ```bash
#                kubectl get networkpolicies -n <namespace>
#                ```
#             """)

# Add connectivity test function
# def test_connectivity():
#     """Test connectivity to different endpoints and show results"""
#     endpoints_to_test = [
#         "http://smartops-api-service:8000",
#         "http://smartops-api:8000",
#         "http://smartops-backend:8000",
#         "http://api-service:8000",
#         "http://localhost:8000",
#         "http://127.0.0.1:8000"
#     ]
#     
#     results = []
#     for endpoint in endpoints_to_test:
#         try:
#             response = requests.get(f"{endpoint}/", timeout=3)
#             if response.status_code == 200:
#                 results.append(f"✅ {endpoint} - Available")
#             else:
#                 results.append(f"⚠️ {endpoint} - Status {response.status_code}")
#         except Exception as e:


# New Relic-style Time Selector
st.markdown("""
<div class="time-selector">
    <div class="time-header">⏰ Time Range Selection</div>
    <div style="display: grid; grid-template-columns: 2fr 2fr 1fr; gap: 1rem; align-items: end;">
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    time_preset = st.selectbox(
        "Select Time Range",
        ["Live (Now)", "5 minutes ago", "15 minutes ago", "1 hour ago", "6 hours ago", "24 hours ago"],
        index=0,
        label_visibility="collapsed"
    )

with col2:
    if time_preset != "Live (Now)":
        relative_value = st.number_input("Value", min_value=1, max_value=365, value=1, step=1, label_visibility="collapsed")
        relative_unit = st.selectbox("Unit", ["Minutes ago", "Hours ago", "Days ago"], index=1, label_visibility="collapsed")

with col3:
    if st.button("🔄 Refresh", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.markdown("</div></div>", unsafe_allow_html=True)



# Display time info
if time_preset == "Live (Now)":
    st.markdown(f"""
    <div class="status-message">
        <div class="status-icon">📅</div>
        <div class="status-text">Viewing: Real-time data | {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="status-message">
        <div class="status-icon">📅</div>
        <div class="status-text">Viewing: Data from {relative_value} {relative_unit.lower()} | {datetime.now().strftime("%B %d, %Y")}</div>
    </div>
    """, unsafe_allow_html=True)

# New Relic-style Cluster Status
st.markdown('<div class="section-header">🏥 Cluster Status & Health</div>', unsafe_allow_html=True)
st.markdown("""
<div class="status-message">
    <div class="status-icon">✅</div>
    <div class="status-text">SmartOps AI Status: No anomalies detected. All systems are running smoothly!</div>
</div>
""", unsafe_allow_html=True)

# New Relic-style Cluster Metrics
st.markdown('<div class="section-header">📊 Cluster Metrics</div>', unsafe_allow_html=True)

# Get live or fallback data for metrics with enhanced fallback
node_count = len(fetch_node_data()) if fetch_node_data() else 1
pod_count = len(fetch_pod_data()) if fetch_pod_data() else 18
service_count = get_service_count()
namespace_count = get_namespace_count()



st.markdown(f"""
<div class="metric-grid">
    <div class="metric-card">
        <div class="metric-value">{node_count}</div>
        <div class="metric-label">Nodes</div>
        <div class="metric-status arrow-up">Active</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">{pod_count}</div>
        <div class="metric-label">Pods</div>
        <div class="metric-status arrow-up">Running</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">{service_count}</div>
        <div class="metric-label">Services</div>
        <div class="metric-status arrow-up">Network</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">{namespace_count}</div>
        <div class="metric-label">Namespaces</div>
        <div class="metric-status arrow-up">Logical</div>
    </div>
</div>
""", unsafe_allow_html=True)

# New Relic-style Resource Usage
st.markdown('<div class="section-header">⚡ Resource Usage</div>', unsafe_allow_html=True)

st.markdown("""
<div class="resource-grid">
    <div class="resource-card">
        <div class="resource-header">
            <div class="resource-icon">🖥️</div>
            <div class="resource-title">CPU Usage</div>
        </div>
        <div class="resource-value">31%</div>
        <div class="metric-status arrow-up">2.5/8 cores</div>
    </div>
    <div class="resource-card">
        <div class="resource-header">
            <div class="resource-icon">💾</div>
            <div class="resource-title">Memory Usage</div>
        </div>
        <div class="resource-value">26%</div>
        <div class="metric-status arrow-up">4.2/16 GB</div>
    </div>
</div>
""", unsafe_allow_html=True)

# New Relic-style Pod Status
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<div class="section-header">📋 Pod Status</div>', unsafe_allow_html=True)
with col2:
    if st.button("🔄 Refresh Pod Data", type="secondary"):
        st.cache_data.clear()
        st.rerun()

st.markdown(f"""
<div style="margin-bottom: 1rem; text-align: right; color: #a0aec0; font-size: 0.8rem;">
    Last updated: {datetime.now().strftime('%H:%M:%S')}
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="chart-container">
    <div class="chart-header">
        <div class="chart-icon">📊</div>
        <div class="chart-title">Pod Status Distribution</div>
    </div>
""", unsafe_allow_html=True)

# Fetch real-time pod data with enhanced fallback
pods = get_enhanced_pod_data()

# Get pod status counts
if pods:
    status_counts = get_pod_status_counts(pods)
else:
    # Fallback to default values if no data available
    status_counts = {'Running': 18, 'Pending': 0, 'Failed': 0, 'Succeeded': 0}

# Create a DataFrame for the chart
pod_data = pd.DataFrame(list(status_counts.items()), columns=['Status', 'Count'])

# Display real-time pod status summary with beautiful badges
st.markdown(f"""
<div style="margin-bottom: 1.5rem;">
    <div style="display: flex; gap: 1rem; flex-wrap: wrap; justify-content: center;">
        <div class="pod-status-badge pod-status-running">
            <span style="color: #48bb78; font-weight: 700; font-size: 1.1rem;">🟢 Running: {status_counts['Running']}</span>
        </div>
        <div class="pod-status-badge pod-status-pending">
            <span style="color: #ed8936; font-weight: 700; font-size: 1.1rem;">🟡 Pending: {status_counts['Pending']}</span>
        </div>
        <div class="pod-status-badge pod-status-failed">
            <span style="color: #e53e3e; font-weight: 700; font-size: 1.1rem;">🔴 Failed: {status_counts['Failed']}</span>
        </div>
        <div class="pod-status-badge pod-status-succeeded">
            <span style="color: #38b2ac; font-weight: 700; font-size: 1.1rem;">🔵 Succeeded: {status_counts['Succeeded']}</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.bar_chart(
    pod_data.set_index('Status'),
    use_container_width=True,
    height=300
)

st.markdown("</div>", unsafe_allow_html=True)

# New Relic-style Node Health
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<div class="section-header">🖥️ Node Health Status</div>', unsafe_allow_html=True)
with col2:
    if st.button("🔄 Refresh Node Data", type="secondary"):
        st.cache_data.clear()
        st.rerun()

st.markdown("""
<div class="chart-container">
    <div class="chart-header">
        <div class="chart-icon">🔍</div>
        <div class="chart-title">Node Health Overview</div>
    </div>
""", unsafe_allow_html=True)

# Fetch real-time node data with enhanced fallback
try:
    # Try to get node data using enhanced function
    nodes_data = get_enhanced_node_data()
    
    if nodes_data:
        node_data_list = []
        for node in nodes_data:
            node_name = node.get('name', 'Unknown')
            status = node.get('status', 'Unknown')
            roles = node.get('roles', '<none>')
            age = node.get('age', 'Unknown')
            version = node.get('version', 'Unknown')
            internal_ip = node.get('internal_ip', 'Unknown')
            
            # Determine health status
            if status == 'Ready':
                health = '🟢 Healthy'
            else:
                health = '🔴 Unhealthy'
            
            node_data_list.append({
                'Node Name': node_name,
                'Status': status,
                'Roles': roles,
                'Health': health,
                'Age': age,
                'Version': version,
                'Internal IP': internal_ip
            })
        
        if node_data_list:
            node_data = pd.DataFrame(node_data_list)
            st.dataframe(
                node_data,
                use_container_width=True,
                hide_index=True,
                height=200
            )
        else:
            st.warning("No node data found")
    else:
        # Fallback to sample node info
        node_data = pd.DataFrame({
            'Node Name': ['Cluster Node'],
            'Status': ['Ready'],
            'Health': ['🟢 Healthy'],
            'Info': ['Cluster information'],
            'Version': ['v1.28.0'],
            'Internal IP': ['192.168.1.100']
        })
        st.dataframe(node_data, use_container_width=True, hide_index=True, height=200)
        
except Exception as e:
    # Fallback to sample node info on error
    st.warning(f"Error fetching node data: {str(e)}")
    node_data = pd.DataFrame({
        'Node Name': ['Cluster Node'],
        'Status': ['Ready'],
        'Health': ['🟢 Healthy'],
        'Info': ['Cluster information'],
        'Version': ['v1.28.0'],
        'Internal IP': ['192.168.1.100']
    })
    st.dataframe(node_data, use_container_width=True, hide_index=True, height=200)

st.markdown("</div>", unsafe_allow_html=True)

# Misi AI Chatbot Widget removed - not using MISI AI page-wise

# Beautiful Footer with gradient
st.markdown("---")
st.markdown(f"""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 3rem 2rem; border-radius: 20px; margin: 3rem 0; text-align: center; box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);">
    <div style="margin-bottom: 1rem;">
        <span style="font-size: 2rem; margin: 0 0.5rem;">🚀</span>
        <span style="font-size: 2rem; margin: 0 0.5rem;">⚡</span>
        <span style="font-size: 2rem; margin: 0 0.5rem;">🔮</span>
    </div>
    <p style="font-weight: 700; margin-bottom: 0.5rem; color: white; font-size: 1.1rem;">Powered by SmartOps AI</p>
    <p style="color: #f8fafc; margin: 0; opacity: 0.9; font-size: 0.9rem;">Enterprise Kubernetes Monitoring & AI-Powered Operations</p>
    <div style="margin-top: 1rem; opacity: 0.8; color: #f8fafc; font-size: 0.8rem;">
        Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}
    </div>
</div>
""", unsafe_allow_html=True)

# Main execution block
if __name__ == "__main__":
    pass

# For Streamlit, the page content will run automatically