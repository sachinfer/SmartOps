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

# NUCLEAR CSS FIX - This will definitely fix the horizontal overlap
st.markdown("""
<style>
/* NUCLEAR CSS RESET - Override everything */
* {
    box-sizing: border-box !important;
    margin: 0 !important;
    padding: 0 !important;
    position: relative !important;
    left: 0 !important;
}

/* FORCE FULL VIEWPORT */
html, body {
    width: 100vw !important;
    max-width: 100vw !important;
    min-width: 100vw !important;
    overflow-x: hidden !important;
    position: relative !important;
    left: 0 !important;
}

/* NUCLEAR STREAMLIT OVERRIDES */
.stApp, .stApp > div, .stApp > div > div {
    width: 100vw !important;
    max-width: 100vw !important;
    min-width: 100vw !important;
    position: relative !important;
    left: 0 !important;
}

/* FORCE SIDEBAR TO BE FIXED AND NOT INTERFERE */
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
    padding: 1rem !important;
    overflow-y: auto !important;
}

/* FORCE MAIN CONTENT TO START AFTER SIDEBAR */
.main {
    margin-left: 300px !important;
    width: calc(100vw - 300px) !important;
    max-width: calc(100vw - 300px) !important;
    min-width: calc(100vw - 300px) !important;
    position: relative !important;
    left: 0 !important;
    overflow-x: hidden !important;
}

/* FORCE MAIN CONTENT BLOCK-CONTAINER TO USE FULL AVAILABLE WIDTH */
.main .block-container {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 100% !important;
    margin-left: 0 !important;
    margin-right: 0 !important;
    padding: 2rem !important;
    position: relative !important;
    left: 0 !important;
    transform: none !important;
}

/* FORCE ALL CONTENT WITHIN BLOCK-CONTAINER TO EXPAND */
.main .block-container > div,
.main .block-container > div > div,
.main .block-container > div > div > div {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 100% !important;
    position: relative !important;
    left: 0 !important;
    margin-left: 0 !important;
    padding-left: 0 !important;
}

/* FORCE ALL STREAMLIT ELEMENTS */
[data-testid="stAppViewContainer"] {
    width: 100vw !important;
    max-width: 100vw !important;
    min-width: 100vw !important;
    position: relative !important;
    left: 0 !important;
}

/* OVERRIDE ANY REMAINING WIDTH CONSTRAINTS */
div[style*="max-width"], div[style*="width"] {
    max-width: 100vw !important;
    width: 100vw !important;
    position: relative !important;
    left: 0 !important;
}

/* FORCE ALL ELEMENTS TO START FROM LEFT EDGE */
.stMarkdown, .stDataFrame, .stMetric, .stColumns, .stAlert, .stButton {
    position: relative !important;
    left: 0 !important;
    margin-left: 0 !important;
    padding-left: 0 !important;
}

/* FORCE PROPER SPACING */
.stMarkdown > div {
    margin-bottom: 1rem !important;
    padding: 0 !important;
    position: relative !important;
    left: 0 !important;
}

.stDataFrame {
    margin: 1rem 0 !important;
    padding: 0 !important;
    position: relative !important;
    left: 0 !important;
}

.stMetric {
    margin: 0.5rem 0 !important;
    padding: 0 !important;
    position: relative !important;
    left: 0 !important;
}

.stColumns > div {
    margin: 0 !important;
    padding: 0.5rem !important;
    position: relative !important;
    left: 0 !important;
}

.stAlert {
    margin: 1rem 0 !important;
    padding: 1rem !important;
    position: relative !important;
    left: 0 !important;
}

.stButton > button {
    margin: 0.25rem 0 !important;
    padding: 0.5rem 1rem !important;
    position: relative !important;
    left: 0 !important;
}

/* FORCE PROPER SPACING BETWEEN ALL ELEMENTS */
.stMarkdown, .stDataFrame, .stMetric, .stColumns, .stAlert, .stButton {
    display: block !important;
    clear: both !important;
    position: relative !important;
    left: 0 !important;
}

/* ENSURE NO TEXT OVERLAPS */
p, h1, h2, h3, h4, h5, h6 {
    margin: 0.5rem 0 !important;
    padding: 0 !important;
    line-height: 1.4 !important;
    position: relative !important;
    left: 0 !important;
}

/* FIX ANY REMAINING CONTAINER ISSUES */
.block-container > div {
    margin-bottom: 1rem !important;
    position: relative !important;
    left: 0 !important;
}

/* BETTER TABLE SPACING */
.stTable {
    margin: 1rem 0 !important;
    border-spacing: 0 !important;
    position: relative !important;
    left: 0 !important;
}

.stTable th, .stTable td {
    padding: 0.5rem !important;
    border: 1px solid #333 !important;
}

/* FIX SIDEBAR NAVIGATION SPACING */
.sidebar .sidebar-content > div {
    margin-bottom: 0.5rem !important;
}

.sidebar .sidebar-content a {
    display: block !important;
    padding: 0.5rem 0 !important;
    margin: 0 !important;
}

/* ENSURE PROPER PAGE SEPARATION */
.page-content {
    min-height: 100vh !important;
    padding: 1rem !important;
    margin: 0 !important;
    position: relative !important;
    left: 0 !important;
}

/* FORCE COLUMNS TO EXPAND */
[data-testid="column"] {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 100% !important;
    position: relative !important;
    left: 0 !important;
}

/* FORCE METRICS TO EXPAND */
[data-testid="metric-container"] {
    width: 100% !important;
    max-width: 100% !important;
    position: relative !important;
    left: 0 !important;
}

/* FORCE BUTTONS AND CARDS TO EXPAND */
.stButton > button,
.element-container {
    width: 100% !important;
    max-width: 100% !important;
    position: relative !important;
    left: 0 !important;
}

/* OVERRIDE ANY REMAINING WIDTH CONSTRAINTS */
div[style*="max-width"], div[style*="width"] {
    max-width: 100vw !important;
    width: 100vw !important;
    position: relative !important;
    left: 0 !important;
}
</style>

<!-- NUCLEAR JAVASCRIPT TO FORCE FULL WIDTH -->
<script>
function nuclearForceFullWidth() {
    // Force all containers to full width
    const containers = document.querySelectorAll('.main .block-container, .stApp > div, [data-testid="stAppViewContainer"]');
    containers.forEach(container => {
        container.style.maxWidth = '100vw !important';
        container.style.width = '100vw !important';
        container.style.paddingLeft = '1rem !important';
        container.style.paddingRight = '1rem !important';
        container.style.marginLeft = '0 !important';
        container.style.marginRight = '0 !important';
        container.style.position = 'relative !important';
        container.style.left = '0 !important';
    });
    
    // Force main content area
    const mainContainer = document.querySelector('.main .block-container');
    if (mainContainer) {
        mainContainer.style.marginLeft = '0px !important';
        mainContainer.style.width = '100% !important';
        mainContainer.style.maxWidth = '100% !important';
        mainContainer.style.padding = '1rem !important';
        mainContainer.style.position = 'relative !important';
        mainContainer.style.left = '0px !important';
        mainContainer.style.transform = 'none !important';
    }
    
    // Force all divs to expand
    const allDivs = document.querySelectorAll('div');
    allDivs.forEach(div => {
        if (div.style.maxWidth && div.style.maxWidth !== '100vw') {
            div.style.maxWidth = '100vw !important';
        }
        if (div.style.width && div.style.width !== '100vw') {
            div.style.width = '100vw !important';
        }
        div.style.position = 'relative !important';
        div.style.left = '0px !important';
    });

    // Ensure proper page separation
    const pageElements = document.querySelectorAll('.stMarkdown, .stDataFrame, .stMetric');
    pageElements.forEach(element => {
        element.style.marginBottom = '1rem !important';
        element.style.width = '100% !important';
        element.style.maxWidth = '100% !important';
        element.style.position = 'relative !important';
        element.style.left = '0px !important';
        element.style.marginLeft = '0px !important';
    });
}

// Run immediately and continuously
nuclearForceFullWidth();
setInterval(nuclearForceFullWidth, 25);

// Also run on DOM changes
const observer = new MutationObserver(nuclearForceFullWidth);
observer.observe(document.body, { childList: true, subtree: true });

// Force on window resize
window.addEventListener('resize', nuclearForceFullWidth);

// Force on page load
window.addEventListener('load', nuclearForceFullWidth);
document.addEventListener('DOMContentLoaded', nuclearForceFullWidth);
</script>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🚀 SmartOps Dashboard")
st.sidebar.markdown("**by Misi 24x7**")
st.sidebar.markdown("---")

# Initialize session state for current page
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Main Dashboard"

# Page navigation with session state
page = st.sidebar.selectbox(
    "Select Page",
    [
        "Main Dashboard",
        "Overview",
        "Pod Explorer and Logs",
        "Kubernetes Shell",
        "Anomaly Detection",
        "Auto Scaling",
        "Incident Timeline",
        "Misi AI Assistant",
        "AI Actions",
        "Deployments"
    ],
    key="page_selector"
)

# Update session state when page changes
if page != st.session_state.current_page:
    st.session_state.current_page = page
    st.rerun()

# Page loader function with proper error handling
def load_page_safely(page_name, file_path):
    """Load and execute a page with proper error handling"""
    try:
        # Clear the page completely
        st.empty()
        
        # Add current directory to path
        sys.path.append(os.path.dirname(__file__))
        
        # Import and execute the page
        spec = importlib.util.spec_from_file_location(page_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Call show_page function
        if hasattr(module, 'show_page'):
            module.show_page()
        else:
            st.error(f"Page {page_name} does not have a show_page function")
            
    except Exception as e:
        st.error(f"Error loading {page_name}: {str(e)}")
        st.write("This page is under maintenance.")

# Page routing with clean separation
if page == "Main Dashboard":
    # Clear any previous content
    st.empty()
    
    st.title("🚀 SmartOps Dashboard")
    st.write("Welcome to SmartOps - Intelligent Kubernetes Operations Platform")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Pods", "24", "↑2")
    with col2:
        st.metric("CPU Usage", "68%", "↓5%")
    with col3:
        st.metric("Memory Usage", "72%", "↑3%")
    with col4:
        st.metric("Services", "12", "→0")
    
    st.markdown("---")
    
    # Quick access cards
    st.subheader("🚀 Quick Access")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("**📊 Overview**\nCluster status and resource monitoring")
        
    with col2:
        st.info("**⚖️ Auto Scaling**\nAI-powered scaling recommendations")
        
    with col3:
        st.info("**🕒 Incident Timeline**\nTrack and analyze incidents")
    
    # Recent activity
    st.subheader("📈 Recent Activity")
    st.success("✅ All systems operational")
    st.info("🔄 Auto-scaling enabled for 4 applications")
    st.warning("⚠️ Memory usage high on smartops-app")

elif page == "Overview":
    load_page_safely("overview", "pages/1_Overview.py")
    
elif page == "Pod Explorer and Logs":
    load_page_safely("pod_explorer", "pages/2_Pod_Explorer_and_Logs.py")
    
elif page == "Kubernetes Shell":
    load_page_safely("k8s_shell", "pages/3_Kubernetes_Shell_and_Cluster_Explorer.py")
    
elif page == "Anomaly Detection":
    load_page_safely("anomaly", "pages/4_Anomaly_Detection.py")
    
elif page == "Auto Scaling":
    load_page_safely("auto_scaling", "pages/5_Auto_Scaling_Recommendations_and_Control.py")
    
elif page == "Incident Timeline":
    load_page_safely("incident", "pages/6_Incident_Timeline_and_Postmortem_Report_Generator.py")
    
elif page == "Misi AI Assistant":
    load_page_safely("ai_assistant", "pages/7_Misi_AI_Assistant.py")
    
elif page == "AI Actions":
    load_page_safely("ai_actions", "pages/8_AI_Actions.py")
    
elif page == "Deployments":
    load_page_safely("deployments", "pages/9_Deployments.py")

else:
    st.title(f"📄 {page}")
    st.write(f"The {page} page is under development.")
    st.info("Please select another page from the sidebar.")

# Sidebar status
st.sidebar.markdown("---")
st.sidebar.success("🟢 **Status:** Online")
st.sidebar.info("🌐 **Environment:** Kubernetes")
st.sidebar.info("✅ **Full-width:** Enabled")
st.sidebar.info("🚀 **Nuclear CSS:** Active")