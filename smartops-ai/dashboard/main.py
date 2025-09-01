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

# Direct HTML injection to force full width immediately
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

<!-- Force viewport width -->
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
html, body {
    width: 100vw !important;
    max-width: 100vw !important;
    overflow-x: hidden !important;
}
</style>
""", unsafe_allow_html=True)

# Ultra-aggressive full-width CSS
st.markdown("""
<style>
/* CSS Reset and Nuclear option - override EVERYTHING */
html, body {
    width: 100vw !important;
    max-width: 100vw !important;
    overflow-x: hidden !important;
    margin: 0 !important;
    padding: 0 !important;
}

* {
    max-width: 100vw !important;
    width: auto !important;
    box-sizing: border-box !important;
}

/* Reset all margins and padding */
* {
    margin: 0 !important;
    padding: 0 !important;
}

/* Streamlit specific overrides - maximum aggression */
.main .block-container,
.block-container,
.stApp > div,
[data-testid="stAppViewContainer"],
.stApp > div > div,
.stApp > div > div > div,
.stApp > div > div > div > div,
.stApp > div > div > div > div > div,
.stApp > div > div > div > div > div > div {
    max-width: 100vw !important;
    width: 100vw !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
    margin-left: 0 !important;
    margin-right: 0 !important;
    min-width: 100vw !important;
}

/* Force full width on ALL possible containers */
.main .block-container > div,
.main .block-container > div > div,
.main .block-container > div > div > div,
.main .block-container > div > div > div > div {
    max-width: 100vw !important;
    width: 100vw !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* Override any remaining constraints with extreme prejudice */
div[data-testid="stAppViewContainer"] > div,
div[data-testid="stAppViewContainer"] > div > div,
div[data-testid="stAppViewContainer"] > div > div > div {
    max-width: 100vw !important;
    width: 100vw !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* Force sidebar to not interfere */
.sidebar .sidebar-content {
    width: 250px !important;
    max-width: 250px !important;
}

/* Force main content to use remaining space */
.main .block-container {
    margin-left: 250px !important;
    margin-right: 0 !important;
    padding: 0 !important;
    width: calc(100vw - 250px) !important;
    max-width: calc(100vw - 250px) !important;
}

/* Additional aggressive overrides */
[data-testid="stAppViewContainer"] {
    width: 100vw !important;
    max-width: 100vw !important;
    min-width: 100vw !important;
}

[data-testid="stAppViewContainer"] > div {
    width: 100vw !important;
    max-width: 100vw !important;
    min-width: 100vw !important;
}

/* Force all Streamlit elements */
.stApp, .stApp > div, .stApp > div > div {
    width: 100vw !important;
    max-width: 100vw !important;
    min-width: 100vw !important;
}

/* Override any remaining width constraints */
div[style*="max-width"], div[style*="width"] {
    max-width: 100vw !important;
    width: 100vw !important;
}

/* Continuous animation to force full width */
@keyframes forceFullWidth {
    0%, 100% { max-width: 100vw !important; width: 100vw !important; }
    50% { max-width: 100vw !important; width: 100vw !important; }
}

.main .block-container,
.stApp > div,
[data-testid="stAppViewContainer"] {
    animation: forceFullWidth 0.1s infinite !important;
}
</style>
""", unsafe_allow_html=True)

# Nuclear JavaScript to force full width
st.markdown("""
<script>
function forceFullWidth() {
    // Nuclear option - override EVERYTHING
    const allElements = document.querySelectorAll('*');
    allElements.forEach(element => {
        if (element.style.maxWidth && element.style.maxWidth !== '100vw') {
            element.style.maxWidth = '100vw !important';
        }
        if (element.style.width && element.style.width !== '100vw') {
            element.style.width = '100vw !important';
        }
    });
    
    // Force all containers to full width
    const containers = document.querySelectorAll('.main .block-container, .block-container, .stApp > div, [data-testid="stAppViewContainer"]');
    containers.forEach(container => {
        container.style.maxWidth = '100vw !important';
        container.style.width = '100vw !important';
        container.style.paddingLeft = '0 !important';
        container.style.paddingRight = '0 !important';
        container.style.marginLeft = '0 !important';
        container.style.marginRight = '0 !important';
        container.style.minWidth = '100vw !important';
    });
    
    // Force main content area
    const mainContainer = document.querySelector('.main .block-container');
    if (mainContainer) {
        mainContainer.style.marginLeft = '250px !important';
        mainContainer.style.marginRight = '0 !important';
        mainContainer.style.width = 'calc(100vw - 250px) !important';
        mainContainer.style.maxWidth = 'calc(100vw - 250px) !important';
    }
    
    // Override any remaining constraints with extreme prejudice
    const allDivs = document.querySelectorAll('div');
    allDivs.forEach(div => {
        if (div.style.maxWidth && div.style.maxWidth !== '100vw') {
            div.style.maxWidth = '100vw !important';
        }
        if (div.style.width && div.style.width !== '100vw') {
            div.style.width = '100vw !important';
        }
        // Force remove any inline width constraints
        if (div.style.maxWidth) div.style.removeProperty('max-width');
        if (div.style.width) div.style.removeProperty('width');
        div.style.maxWidth = '100vw !important';
        div.style.width = '100vw !important';
    });
    
    // Force all elements with any width-related styles
    const allElements = document.querySelectorAll('*');
    allElements.forEach(element => {
        const computedStyle = window.getComputedStyle(element);
        if (computedStyle.maxWidth !== 'none' || computedStyle.width !== 'auto') {
            element.style.maxWidth = '100vw !important';
            element.style.width = '100vw !important';
        }
    });
}

// Run immediately and continuously
forceFullWidth();
setInterval(forceFullWidth, 100); // Ultra-frequent updates
setInterval(forceFullWidth, 500); // Backup frequency

// Also run on DOM changes
const observer = new MutationObserver(forceFullWidth);
observer.observe(document.body, { childList: true, subtree: true });

// Force on window resize
window.addEventListener('resize', forceFullWidth);

// Force on page load
window.addEventListener('load', forceFullWidth);
document.addEventListener('DOMContentLoaded', forceFullWidth);

// Force on any scroll or interaction
document.addEventListener('scroll', forceFullWidth);
document.addEventListener('click', forceFullWidth);
document.addEventListener('keydown', forceFullWidth);

// Force on any CSS changes
const styleObserver = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        if (mutation.type === 'attributes' && mutation.attributeName === 'style') {
            forceFullWidth();
        }
    });
});
styleObserver.observe(document.body, { attributes: true, subtree: true });
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

# Page routing
if page == "Main Dashboard":
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