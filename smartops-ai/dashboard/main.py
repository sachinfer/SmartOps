import streamlit as st
import sys
import os
import importlib.util

# Page configuration
st.set_page_config(
    page_title="SmartOps Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Comprehensive CSS fix for all alignment and overlap issues
st.markdown("""
<style>
/* Reset everything */
* {
    box-sizing: border-box !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* Force full viewport */
html, body {
    width: 100vw !important;
    max-width: 100vw !important;
    min-width: 100vw !important;
    overflow-x: hidden !important;
}

/* Dark theme */
.main {
    background-color: #0e1117 !important;
    color: #fafafa !important;
}

.stApp {
    background-color: #0e1117 !important;
    color: #fafafa !important;
}

/* NUCLEAR SIDEBAR FIX */
.sidebar .sidebar-content {
    background-color: #1e1e1e !important;
    border-right: 1px solid #333 !important;
    width: 300px !important;
    max-width: 300px !important;
    min-width: 300px !important;
    position: fixed !important;
    left: 0 !important;
    top: 0 !important;
    height: 100vh !important;
    z-index: 1000 !important;
    overflow-y: auto !important;
}

/* NUCLEAR MAIN CONTENT FIX */
.main {
    margin-left: 300px !important;
    width: calc(100vw - 300px) !important;
    max-width: calc(100vw - 300px) !important;
    min-width: calc(100vw - 300px) !important;
    position: relative !important;
    left: 0 !important;
    right: 0 !important;
    overflow-x: hidden !important;
}

.main .block-container {
    max-width: 100% !important;
    width: 100% !important;
    padding: 2rem !important;
    margin: 0 !important;
    position: relative !important;
    left: 0 !important;
    right: 0 !important;
    transform: none !important;
}

/* Force all content to start from left edge */
.main .block-container *,
.main .block-container > div,
.main .block-container > div > div,
.main .block-container > div > div > div {
    position: relative !important;
    left: 0 !important;
    margin-left: 0 !important;
    padding-left: 0 !important;
    max-width: 100% !important;
    width: 100% !important;
}

/* Modern cards */
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 15px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    color: white;
    text-align: center;
    width: 100% !important;
    max-width: 100% !important;
}

.metric-value {
    font-size: 2.5rem;
    font-weight: bold;
    margin: 0.5rem 0;
}

.metric-label {
    font-size: 1rem;
    opacity: 0.9;
}

/* Status indicators */
.status-online {
    background: #00d4aa;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-weight: 600;
    text-align: center;
    display: inline-block;
}

/* Hide Streamlit default elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Force proper spacing */
.stMarkdown {
    margin-bottom: 1rem !important;
    width: 100% !important;
    max-width: 100% !important;
}

.stMarkdown > div {
    margin-bottom: 1rem !important;
    padding: 0 !important;
    width: 100% !important;
    max-width: 100% !important;
}

.stDataFrame {
    margin: 1rem 0 !important;
    padding: 0 !important;
    width: 100% !important;
    max-width: 100% !important;
}

.stMetric {
    margin: 0.5rem 0 !important;
    padding: 0 !important;
    width: 100% !important;
    max-width: 100% !important;
}

.stColumns > div {
    margin: 0 !important;
    padding: 0.5rem !important;
    width: 100% !important;
    max-width: 100% !important;
}

.stAlert {
    margin: 1rem 0 !important;
    padding: 1rem !important;
    width: 100% !important;
    max-width: 100% !important;
}

.stButton > button {
    margin: 0.25rem 0 !important;
    padding: 0.5rem 1rem !important;
    width: 100% !important;
    max-width: 100% !important;
}

/* Force proper spacing between all elements */
.stMarkdown, .stDataFrame, .stMetric, .stColumns, .stAlert, .stButton {
    display: block !important;
    clear: both !important;
    position: relative !important;
    left: 0 !important;
    width: 100% !important;
    max-width: 100% !important;
}

/* Ensure no text overlaps */
p, h1, h2, h3, h4, h5, h6 {
    margin: 0.5rem 0 !important;
    padding: 0 !important;
    line-height: 1.4 !important;
    position: relative !important;
    left: 0 !important;
    width: 100% !important;
    max-width: 100% !important;
}

/* Fix any remaining container issues */
.block-container > div {
    margin-bottom: 1rem !important;
    position: relative !important;
    left: 0 !important;
    width: 100% !important;
    max-width: 100% !important;
}

/* Better table spacing */
.stTable {
    margin: 1rem 0 !important;
    border-spacing: 0 !important;
    position: relative !important;
    left: 0 !important;
    width: 100% !important;
    max-width: 100% !important;
}

.stTable th, .stTable td {
    padding: 0.5rem !important;
    border: 1px solid #333 !important;
}

/* Fix sidebar navigation spacing */
.sidebar .sidebar-content > div {
    margin-bottom: 0.5rem !important;
}

.sidebar .sidebar-content a {
    display: block !important;
    padding: 0.5rem 0 !important;
    margin: 0 !important;
}

/* Ensure proper page separation */
.page-content {
    min-height: 100vh !important;
    padding: 1rem !important;
    margin: 0 !important;
    position: relative !important;
    left: 0 !important;
    width: 100% !important;
    max-width: 100% !important;
}

/* NUCLEAR OVERRIDE - Force everything to proper position */
.main .block-container * {
    position: relative !important;
    left: 0 !important;
    margin-left: 0 !important;
    padding-left: 0 !important;
    max-width: 100% !important;
    width: 100% !important;
}

/* Force all Streamlit elements to full width */
[data-testid="stAppViewContainer"] {
    width: 100vw !important;
    max-width: 100vw !important;
    min-width: 100vw !important;
}

[data-testid="column"] {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 100% !important;
}

[data-testid="metric-container"] {
    width: 100% !important;
    max-width: 100% !important;
}

/* Override any remaining width constraints */
div[style*="max-width"], div[style*="width"] {
    max-width: 100% !important;
    width: 100% !important;
}

/* Force all containers to proper alignment */
.reportview-container,
.reportview-container .main,
.reportview-container .main .block-container,
.wide .block-container,
.block-container {
    max-width: 100% !important;
    width: 100% !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
    margin-left: 0 !important;
    margin-right: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# Simple sidebar
st.sidebar.title("🚀 SmartOps")
st.sidebar.markdown("**by Misi 24x7**")
st.sidebar.markdown("---")

# Clean page navigation
page = st.sidebar.selectbox(
    "📄 Select Page",
    [
        "🏠 Dashboard",
        "📊 Overview", 
        "🧭 Pod Explorer",
        "🔍 K8s Shell",
        "🔥 Anomaly Detection",
        "⚡ Auto Scaling",
        "📝 Incident Timeline",
        "💬 AI Assistant",
        "🤖 AI Actions",
        "🚀 Deployments"
    ]
)

# Page loader function
def load_page_safely(page_name, file_path):
    """Load and execute a page"""
    try:
        sys.path.append(os.path.dirname(__file__))
        spec = importlib.util.spec_from_file_location(page_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        if hasattr(module, 'show_page'):
            module.show_page()
        else:
            st.error(f"Page {page_name} not available")
            
    except Exception as e:
        st.error(f"Error loading {page_name}: {str(e)}")

# Main dashboard content
if page == "🏠 Dashboard":
    st.title("🚀 SmartOps Dashboard")
    st.markdown("**Intelligent Kubernetes Operations Platform**")
    st.markdown("---")
    
    # Key metrics in clean cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Active Pods</div>
            <div class="metric-value">24</div>
            <div style="color: #00d4aa;">↑ +2</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">CPU Usage</div>
            <div class="metric-value">68%</div>
            <div style="color: #ff6b6b;">↑ +5%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Memory Usage</div>
            <div class="metric-value">72%</div>
            <div style="color: #4ecdc4;">↑ +3%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Services</div>
            <div class="metric-value">12</div>
            <div style="color: #45b7d1;">→ 0</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick actions
    st.subheader("🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 View Overview", use_container_width=True):
            st.session_state.page = "📊 Overview"
            st.rerun()
    
    with col2:
        if st.button("⚡ Auto Scaling", use_container_width=True):
            st.session_state.page = "⚡ Auto Scaling"
            st.rerun()
    
    with col3:
        if st.button("📝 Incidents", use_container_width=True):
            st.session_state.page = "📝 Incident Timeline"
            st.rerun()
    
    # System status
    st.markdown("---")
    st.subheader("🔍 System Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="status-online">🟢 ALL SYSTEMS OPERATIONAL</div>
        """, unsafe_allow_html=True)
        st.info("🌍 **Environment:** Kubernetes")
    
    with col2:
        st.success("✅ **Auto-scaling:** Enabled for 4 apps")
        st.warning("⚠️ **Memory:** High usage on smartops-app")

elif page == "📊 Overview":
    load_page_safely("overview", "pages/1_Overview.py")
    
elif page == "🧭 Pod Explorer":
    load_page_safely("pod_explorer", "pages/2_Pod_Explorer_and_Logs.py")
    
elif page == "🔍 K8s Shell":
    load_page_safely("k8s_shell", "pages/3_Kubernetes_Shell_and_Cluster_Explorer.py")
    
elif page == "🔥 Anomaly Detection":
    load_page_safely("anomaly", "pages/4_Anomaly_Detection.py")
    
elif page == "⚡ Auto Scaling":
    load_page_safely("auto_scaling", "pages/5_Auto_Scaling_Recommendations_and_Control.py")
    
elif page == "📝 Incident Timeline":
    load_page_safely("incident", "pages/6_Incident_Timeline_and_Postmortem_Report_Generator.py")
    
elif page == "💬 AI Assistant":
    load_page_safely("ai_assistant", "pages/7_Misi_AI_Assistant.py")
    
elif page == "🤖 AI Actions":
    load_page_safely("ai_actions", "pages/8_AI_Actions.py")
    
elif page == "🚀 Deployments":
    load_page_safely("deployments", "pages/9_Deployments.py")

# Sidebar status
st.sidebar.markdown("---")
st.sidebar.markdown("### 📈 Status")
st.sidebar.success("🟢 **Online**")
st.sidebar.info("🌐 **Kubernetes**")
st.sidebar.info("✅ **Full-width**")