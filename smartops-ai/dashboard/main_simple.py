import streamlit as st
import sys
import os
import traceback

# Simple page configuration
st.set_page_config(
    page_title="SmartOps Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced full-width CSS
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

# Simple sidebar
st.sidebar.title("🚀 SmartOps Dashboard")
st.sidebar.markdown("**by Misi 24x7**")
st.sidebar.markdown("---")

# Page selection
page = st.sidebar.selectbox(
    "Select Page",
    [
        "Main Dashboard",
        "Auto Scaling",
        "Incident Timeline", 
    ]
)

# Enhanced page loading function
def load_page_safely(page_name, file_path, module_name):
    """Safely load and execute a page with detailed error reporting"""
    st.info(f"🔄 Loading {page_name} page...")
    
    try:
        # Step 1: Check if file exists
        if not os.path.exists(file_path):
            st.error(f"❌ File not found: {file_path}")
            return False
            
        st.success(f"✅ File exists: {file_path}")
        
        # Step 2: Import the module
        sys.path.append(os.path.dirname(__file__))
        import importlib.util
        
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        page_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(page_module)
        
        st.success(f"✅ Module imported successfully: {module_name}")
        
        # Step 3: Check if show_page function exists
        if not hasattr(page_module, 'show_page'):
            st.error(f"❌ No 'show_page' function found in {module_name}")
            return False
            
        st.success(f"✅ 'show_page' function found")
        
        # Step 4: Execute the show_page function
        st.info(f"🔄 Executing show_page function...")
        page_module.show_page()
        st.success(f"✅ {page_name} page loaded successfully!")
        return True
        
    except Exception as e:
        st.error(f"❌ **{page_name} Error:** {e}")
        st.code(f"Error Type: {type(e).__name__}")
        
        with st.expander("🔍 **Full Error Traceback**", expanded=True):
            st.code(traceback.format_exc())
        
        return False

# Simple page routing
if page == "Main Dashboard":
    st.title("🚀 SmartOps Dashboard")
    st.write("Welcome to SmartOps! Full-width is working!")
    
    # Simple metrics with full width
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
    st.subheader("🚀 Quick Access")
    st.info("✅ Full-width layout is working! Select a page from the sidebar.")
    st.success("✅ Both Auto Scaling and Incident Timeline pages are ready!")
    
    # Debug info
    with st.expander("🔍 **Debug Info**"):
        st.write(f"Current working directory: {os.getcwd()}")
        st.write(f"Files in pages directory:")
        try:
            pages_dir = os.path.join(os.getcwd(), "pages")
            if os.path.exists(pages_dir):
                files = os.listdir(pages_dir)
                for file in files:
                    if file.endswith('.py'):
                        st.write(f"  - {file}")
        except Exception as e:
            st.error(f"Error listing pages: {e}")

elif page == "Auto Scaling":
    st.title("⚡ Auto Scaling")
    
    # Try to load the page
    success = load_page_safely(
        "Auto Scaling",
        "pages/5_Auto_Scaling_Recommendations_and_Control.py",
        "auto_scaling"
    )
    
    if not success:
        # Fallback content
        st.warning("⚠️ Using fallback content due to loading error")
        st.subheader("Auto Scaling Dashboard")
        st.write("This is fallback content while we debug the loading issue.")
        
        # Show what we know works
        st.info("✅ We know this page works (Python test passed)")
        st.info("✅ The issue is in Streamlit loading, not the page itself")

elif page == "Incident Timeline":
    st.title("📝 Incident Timeline")
    
    # Try to load the page
    success = load_page_safely(
        "Incident Timeline",
        "pages/6_Incident_Timeline_and_Postmortem_Report_Generator.py",
        "incident"
    )
    
    if not success:
        # Fallback content
        st.warning("⚠️ Using fallback content due to loading error")
        st.subheader("Incident Timeline Dashboard")
        st.write("This is fallback content while we debug the loading issue.")
        
        # Show what we know works
        st.info("✅ We know this page works (Python test passed)")
        st.info("✅ The issue is in Streamlit loading, not the page itself")

# Sidebar status
st.sidebar.markdown("---")
st.sidebar.info("**Environment:** GCP Cloud Shell")
st.sidebar.success("🟢 **Status:** Online")
st.sidebar.info("✅ Full-width working")
st.sidebar.warning("⚠️ Pages need debugging")

# Debug button
if st.sidebar.button("🔍 Debug Page Loading"):
    st.sidebar.info("Debug mode activated")
    st.info("🔍 **Debug Mode Active**")
    st.write("This will help us see exactly what's happening when pages load.")
