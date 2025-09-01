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

# Full-width CSS
st.markdown("""
<style>
.main .block-container {
    max-width: 100% !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}
.stApp > div {
    max-width: 100% !important;
}
</style>
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