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

# COLLAPSIBLE SIDEBAR CSS - Toggle navigation visibility
st.markdown("""
<style>
/* BASE LAYOUT */
* {
    box-sizing: border-box !important;
}

/* MAIN APP CONTAINER - FULL WIDTH */
.stApp {
    display: flex !important;
    width: 100vw !important;
    height: 100vh !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
    position: relative !important;
    max-width: 100vw !important;
    min-width: 100vw !important;
}

/* SIDEBAR - COLLAPSIBLE */
.sidebar {
    width: 300px !important;
    min-width: 300px !important;
    max-width: 300px !important;
    background-color: #1e1e1e !important;
    border-right: 1px solid #333 !important;
    overflow-y: auto !important;
    position: fixed !important;
    left: 0 !important;
    top: 0 !important;
    height: 100vh !important;
    z-index: 1000 !important;
    padding: 1rem !important;
    transition: transform 0.3s ease-in-out !important;
}

/* SIDEBAR HIDDEN STATE */
.sidebar.hidden {
    transform: translateX(-100%) !important;
}

.sidebar .sidebar-content {
    width: 100% !important;
    height: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* MAIN CONTENT - RESPONSIVE TO SIDEBAR STATE - FULL WIDTH */
.main {
    margin-left: 300px !important;
    width: calc(100vw - 300px) !important;
    max-width: calc(100vw - 300px) !important;
    min-width: calc(100vw - 300px) !important;
    height: 100vh !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    position: relative !important;
    background-color: #0e1117 !important;
    left: 0 !important;
    transition: margin-left 0.3s ease-in-out, width 0.3s ease-in-out !important;
    flex: 1 !important;
}

/* MAIN CONTENT WHEN SIDEBAR IS HIDDEN - FULL WIDTH */
.main.sidebar-hidden {
    margin-left: 0 !important;
    width: 100vw !important;
    max-width: 100vw !important;
    min-width: 100vw !important;
    flex: 1 !important;
}

/* MAIN CONTENT BLOCK CONTAINER */
.main .block-container {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 100% !important;
    margin: 0 !important;
    padding: 2rem !important;
    position: relative !important;
    left: 0 !important;
    transform: none !important;
}

/* TOGGLE BUTTON */
.sidebar-toggle {
    position: fixed !important;
    top: 20px !important;
    left: 20px !important;
    z-index: 1001 !important;
    background-color: #667eea !important;
    color: white !important;
    border: none !important;
    border-radius: 50% !important;
    width: 50px !important;
    height: 50px !important;
    font-size: 18px !important;
    cursor: pointer !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
    transition: all 0.3s ease !important;
}

.sidebar-toggle:hover {
    background-color: #5a6fd8 !important;
    transform: scale(1.1) !important;
}

/* TOGGLE BUTTON WHEN SIDEBAR IS HIDDEN */
.sidebar-toggle.sidebar-hidden {
    left: 20px !important;
}

/* CONTENT ELEMENTS */
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

/* STREAMLIT ELEMENTS */
.stMarkdown, .stDataFrame, .stMetric, .stColumns, .stAlert, .stButton {
    position: relative !important;
    left: 0 !important;
    margin-left: 0 !important;
    padding-left: 0 !important;
    width: 100% !important;
    max-width: 100% !important;
}

/* OVERRIDE ANY REMAINING WIDTH CONSTRAINTS */
div[style*="max-width"], div[style*="width"] {
    max-width: 100% !important;
    width: 100% !important;
    position: relative !important;
    left: 0 !important;
}

/* CONTENT ELEMENTS WITHIN MAIN AREA */
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

/* STREAMLIT APP VIEW CONTAINER */
[data-testid="stAppViewContainer"] {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 100% !important;
    position: relative !important;
    left: 0 !important;
    margin-left: 0 !important;
}

/* STREAMLIT ELEMENTS PROPER POSITIONING */
.stMarkdown, .stDataFrame, .stMetric, .stColumns, .stAlert, .stButton {
    position: relative !important;
    left: 0 !important;
    margin-left: 0 !important;
    padding-left: 0 !important;
    width: 100% !important;
    max-width: 100% !important;
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

/* OVERRIDE ANY REMAINING WIDTH CONSTRAINTS - FORCE FULL WIDTH */
div[style*="max-width"], div[style*="width"] {
    max-width: 100% !important;
    width: 100% !important;
    position: relative !important;
    left: 0 !important;
}

/* FORCE ALL STREAMLIT CONTAINERS TO USE FULL WIDTH */
.stApp > div,
.stApp > div > div,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > div,
[data-testid="stAppViewContainer"] > div > div {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 100% !important;
    position: relative !important;
    left: 0 !important;
    margin-left: 0 !important;
    padding-left: 0 !important;
}

/* FORCE ALL CONTENT ELEMENTS TO EXPAND */
.stMarkdown,
.stDataFrame,
.stMetric,
.stColumns,
.stAlert,
.stButton,
.stSelectbox,
.stTextInput,
.stTextArea,
.stSlider,
.stCheckbox,
.stRadio,
.stExpander,
.stTabs,
.stContainer,
.element-container {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 100% !important;
    position: relative !important;
    left: 0 !important;
    margin-left: 0 !important;
    padding-left: 0 !important;
}

/* FORCE PLOTLY CHARTS TO USE FULL WIDTH */
.stPlotlyChart,
.stAltairChart,
.stVegaLiteChart,
.stPydeckChart {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 100% !important;
}

/* FORCE TABLES TO USE FULL WIDTH */
.stDataFrame,
.stTable,
.stDataEditor {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 100% !important;
}

/* FORCE COLUMNS TO USE FULL WIDTH */
[data-testid="column"] {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 100% !important;
    flex: 1 !important;
}

/* FORCE METRICS TO USE FULL WIDTH */
[data-testid="metric-container"] {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 100% !important;
    flex: 1 !important;
}
</style>

<!-- COLLAPSIBLE SIDEBAR JAVASCRIPT -->
<script>
// Initialize sidebar state
let sidebarHidden = false;

// Create toggle button
function createToggleButton() {
    const toggleButton = document.createElement('button');
    toggleButton.className = 'sidebar-toggle';
    toggleButton.innerHTML = '☰';
    toggleButton.title = 'Toggle Sidebar';
    toggleButton.onclick = toggleSidebar;
    document.body.appendChild(toggleButton);
}

// Toggle sidebar function
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.main');
    const toggleButton = document.querySelector('.sidebar-toggle');
    
    if (sidebar && mainContent && toggleButton) {
        sidebarHidden = !sidebarHidden;
        
        if (sidebarHidden) {
            // Hide sidebar
            sidebar.classList.add('hidden');
            mainContent.classList.add('sidebar-hidden');
            toggleButton.innerHTML = '☰';
            toggleButton.title = 'Show Sidebar';
        } else {
            // Show sidebar
            sidebar.classList.remove('hidden');
            mainContent.classList.remove('sidebar-hidden');
            toggleButton.innerHTML = '✕';
            toggleButton.title = 'Hide Sidebar';
        }
        
        // Store state in localStorage
        localStorage.setItem('sidebarHidden', sidebarHidden);
    }
}

// Initialize sidebar state from localStorage
function initializeSidebarState() {
    const savedState = localStorage.getItem('sidebarHidden');
    if (savedState === 'true') {
        sidebarHidden = true;
        const sidebar = document.querySelector('.sidebar');
        const mainContent = document.querySelector('.main');
        const toggleButton = document.querySelector('.sidebar-toggle');
        
        if (sidebar && mainContent && toggleButton) {
            sidebar.classList.add('hidden');
            mainContent.classList.add('sidebar-hidden');
            toggleButton.innerHTML = '☰';
            toggleButton.title = 'Show Sidebar';
        }
    }
}

// Layout fix function - Enhanced for full width
function fixLayout() {
    // Ensure proper layout
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.main');
    
    if (sidebar && mainContent) {
        if (sidebarHidden) {
            sidebar.classList.add('hidden');
            mainContent.classList.add('sidebar-hidden');
        } else {
            sidebar.classList.remove('hidden');
            mainContent.classList.remove('sidebar-hidden');
        }
    }
    
    // Force all content elements to use full width
    const allContentElements = document.querySelectorAll('.main .stMarkdown, .main .stDataFrame, .main .stMetric, .main .stAlert, .main .stButton, .main .stSelectbox, .main .stTextInput, .main .stTextArea, .main .stSlider, .main .stCheckbox, .main .stRadio, .main .stExpander, .main .stTabs, .main .stContainer, .main .element-container, .main [data-testid="column"], .main [data-testid="metric-container"]');
    
    allContentElements.forEach(element => {
        element.style.position = 'relative !important';
        element.style.left = '0 !important';
        element.style.marginLeft = '0 !important';
        element.style.paddingLeft = '0 !important';
        element.style.width = '100% !important';
        element.style.maxWidth = '100% !important';
        element.style.minWidth = '100% !important';
        element.style.flex = '1 !important';
    });
    
    // Force all containers to use full width
    const containers = document.querySelectorAll('.main .block-container, .main [data-testid="stAppViewContainer"], .main [data-testid="stAppViewContainer"] > div, .main [data-testid="stAppViewContainer"] > div > div');
    containers.forEach(container => {
        container.style.width = '100% !important';
        container.style.maxWidth = '100% !important';
        container.style.minWidth = '100% !important';
        container.style.position = 'relative !important';
        container.style.left = '0 !important';
        container.style.marginLeft = '0 !important';
        container.style.paddingLeft = '0 !important';
    });
    
    // Force charts to use full width
    const charts = document.querySelectorAll('.main .stPlotlyChart, .main .stAltairChart, .main .stVegaLiteChart, .main .stPydeckChart');
    charts.forEach(chart => {
        chart.style.width = '100% !important';
        chart.style.maxWidth = '100% !important';
        chart.style.minWidth = '100% !important';
    });
    
    // Force tables to use full width
    const tables = document.querySelectorAll('.main .stDataFrame, .main .stTable, .main .stDataEditor');
    tables.forEach(table => {
        table.style.width = '100% !important';
        table.style.maxWidth = '100% !important';
        table.style.minWidth = '100% !important';
    });
}

// Initialize everything when DOM is ready
function initialize() {
    createToggleButton();
    initializeSidebarState();
    fixLayout();
}

// Run on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize);
} else {
    initialize();
}

// Run on window load
window.addEventListener('load', initialize);

// Run on DOM changes
const observer = new MutationObserver(fixLayout);
observer.observe(document.body, { childList: true, subtree: true });

// Run on window resize
window.addEventListener('resize', fixLayout);
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
st.sidebar.info("🔄 **Sidebar:** Collapsible")
st.sidebar.info("🚀 **Layout:** Full-width Toggle")