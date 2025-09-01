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

# Nuclear HTML injection to force full width immediately
st.markdown("""
<div style="
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: -1;
    pointer-events: none;
"></div>

<!-- Nuclear CSS that overrides everything -->
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

/* Nuclear Streamlit overrides */
.stApp, .stApp > div, .stApp > div > div {
    width: 100vw !important;
    max-width: 100vw !important;
    min-width: 100vw !important;
}

/* Force main container to use full available width */
.main .block-container {
    width: calc(100vw - 300px) !important;
    max-width: calc(100vw - 300px) !important;
    min-width: calc(100vw - 300px) !important;
    margin-left: 300px !important;
    margin-right: 0 !important;
    padding: 1rem !important;
}

/* Force all content to expand */
.main .block-container > div,
.main .block-container > div > div,
.main .block-container > div > div > div {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 100% !important;
}

/* Force columns to expand */
[data-testid="column"] {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 100% !important;
}

/* Force metrics to expand */
[data-testid="metric-container"] {
    width: 100% !important;
    max-width: 100% !important;
}

/* Force buttons and cards to expand */
.stButton > button,
.element-container {
    width: 100% !important;
    max-width: 100% !important;
}

/* Force all Streamlit elements */
[data-testid="stAppViewContainer"] {
    width: 100vw !important;
    max-width: 100vw !important;
    min-width: 100vw !important;
}

/* Override any remaining width constraints */
div[style*="max-width"], div[style*="width"] {
    max-width: 100vw !important;
    width: 100vw !important;
}

/* Page content styling */
.page-content {
    padding: 1rem !important;
    margin: 0 !important;
    width: 100% !important;
    max-width: 100% !important;
}

/* Better spacing between elements */
.stMarkdown {
    margin-bottom: 1rem !important;
}

/* Force sidebar width */
.sidebar .sidebar-content {
    width: 300px !important;
    max-width: 300px !important;
}

/* Ensure no horizontal scrolling */
.main {
    overflow-x: hidden !important;
}

/* Better table alignment */
.stTable {
    width: 100% !important;
    max-width: 100% !important;
}

/* Force all containers to proper alignment */
.block-container {
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    margin-left: 0 !important;
    margin-right: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# Nuclear JavaScript to force full width
st.markdown("""
<script>
function forceFullWidth() {
    // Force all containers to full width
    const containers = document.querySelectorAll('.main .block-container, .stApp > div, [data-testid="stAppViewContainer"]');
    containers.forEach(container => {
        container.style.maxWidth = '100vw !important';
        container.style.width = '100vw !important';
        container.style.paddingLeft = '1rem !important';
        container.style.paddingRight = '1rem !important';
        container.style.marginLeft = '0 !important';
        container.style.marginRight = '0 !important';
    });
    
    // Force main content area
    const mainContainer = document.querySelector('.main .block-container');
    if (mainContainer) {
        mainContainer.style.marginLeft = '300px !important';
        mainContainer.style.width = 'calc(100vw - 300px) !important';
        mainContainer.style.maxWidth = 'calc(100vw - 300px) !important';
        mainContainer.style.padding = '1rem !important';
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
    });
    
    // Ensure proper page separation
    const pageElements = document.querySelectorAll('.stMarkdown, .stDataFrame, .stMetric');
    pageElements.forEach(element => {
        element.style.marginBottom = '1rem !important';
        element.style.width = '100% !important';
        element.style.maxWidth = '100% !important';
    });
}

// Run immediately and continuously
forceFullWidth();
setInterval(forceFullWidth, 100);

// Also run on DOM changes
const observer = new MutationObserver(forceFullWidth);
observer.observe(document.body, { childList: true, subtree: true });

// Force on window resize
window.addEventListener('resize', forceFullWidth);
</script>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🚀 SmartOps Dashboard")
st.sidebar.markdown("**by Misi 24x7**")
st.sidebar.markdown("---")

# Page navigation
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
    ]
)

# Simple page loader function
def load_page(page_name, file_path):
    """Load and execute a page"""
    try:
        # Clear any previous content
        st.markdown("---")
        
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

# Page routing with proper separation
if page == "Main Dashboard":
    # Clear any previous content
    st.markdown("---")
    
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
    load_page("overview", "pages/1_Overview.py")
    
elif page == "Pod Explorer and Logs":
    load_page("pod_explorer", "pages/2_Pod_Explorer_and_Logs.py")
    
elif page == "Kubernetes Shell":
    load_page("k8s_shell", "pages/3_Kubernetes_Shell_and_Cluster_Explorer.py")
    
elif page == "Anomaly Detection":
    load_page("anomaly", "pages/4_Anomaly_Detection.py")
    
elif page == "Auto Scaling":
    load_page("auto_scaling", "pages/5_Auto_Scaling_Recommendations_and_Control.py")
    
elif page == "Incident Timeline":
    load_page("incident", "pages/6_Incident_Timeline_and_Postmortem_Report_Generator.py")
    
elif page == "Misi AI Assistant":
    load_page("ai_assistant", "pages/7_Misi_AI_Assistant.py")
    
elif page == "AI Actions":
    load_page("ai_actions", "pages/8_AI_Actions.py")
    
elif page == "Deployments":
    load_page("deployments", "pages/9_Deployments.py")

else:
    st.title(f"📄 {page}")
    st.write(f"The {page} page is under development.")
    st.info("Please select another page from the sidebar.")

# Sidebar status
st.sidebar.markdown("---")
st.sidebar.success("🟢 **Status:** Online")
st.sidebar.info("🌐 **Environment:** Kubernetes")
st.sidebar.info("✅ **Full-width:** Enabled")