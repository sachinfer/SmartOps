import streamlit as st
import sys
import os

# Simple page configuration
st.set_page_config(
    page_title="SmartOps Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simple full-width CSS
st.markdown("""
<style>
.main .block-container {
    max-width: 100%;
    padding-left: 1rem;
    padding-right: 1rem;
}
</style>
""", unsafe_allow_html=True)

# Simple sidebar
st.sidebar.title("🚀 SmartOps Dashboard")
st.sidebar.markdown("**by Misi 24x7**")
st.sidebar.markdown("---")

# Page selection
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
        "AI Assistant",
        "AI Actions",
        "Deployments"
    ]
)

# Simple page routing
if page == "Main Dashboard":
    st.title("🚀 SmartOps Dashboard")
    st.write("Welcome to SmartOps!")
    
    # Simple metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Pods", "24", "2")
    with col2:
        st.metric("CPU Usage", "68%", "-5%")
    with col3:
        st.metric("Memory Usage", "72%", "3%") 
    with col4:
        st.metric("Services", "12", "0")
    
    st.markdown("---")
    st.subheader("Quick Access")
    st.info("Select a page from the sidebar to continue.")

elif page == "Overview":
    try:
        from pages import overview_page
        overview_page.show_page()
    except Exception as e:
        st.error(f"Error loading Overview: {e}")
        st.title("📊 Overview")
        st.write("This page is being fixed...")

elif page == "Auto Scaling":
    try:
        sys.path.append(os.path.dirname(__file__))
        import importlib.util
        spec = importlib.util.spec_from_file_location("auto_scaling", "pages/5_Auto_Scaling_Recommendations_and_Control.py")
        auto_scaling = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(auto_scaling)
        auto_scaling.show_page()
    except Exception as e:
        st.error(f"Error loading Auto Scaling: {e}")
        st.title("⚡ Auto Scaling")
        st.write("This page is being fixed...")
        st.code(str(e))

elif page == "Incident Timeline":
    try:
        sys.path.append(os.path.dirname(__file__))
        import importlib.util
        spec = importlib.util.spec_from_file_location("incident", "pages/6_Incident_Timeline_and_Postmortem_Report_Generator.py")
        incident = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(incident)
        incident.show_page()
    except Exception as e:
        st.error(f"Error loading Incident Timeline: {e}")
        st.title("📝 Incident Timeline")
        st.write("This page is being fixed...")
        st.code(str(e))

else:
    st.title(f"📄 {page}")
    st.write(f"This page ({page}) is under development.")
    st.info("Please select another page from the sidebar.")

st.sidebar.markdown("---")
st.sidebar.info("**Environment:** Local Development")
st.sidebar.success("🟢 **Status:** Online")
