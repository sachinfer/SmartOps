import streamlit as st
import sys
import os
import traceback

st.set_page_config(page_title="Debug Test", layout="wide")

st.title("🔍 Debug Test - Page Loading")

# Test 1: Basic Streamlit functionality
st.success("✅ Basic Streamlit is working")

# Test 2: Check current directory
st.write(f"Current directory: {os.getcwd()}")

# Test 3: List pages directory
pages_dir = "pages"
if os.path.exists(pages_dir):
    st.success(f"✅ Pages directory exists: {pages_dir}")
    files = os.listdir(pages_dir)
    st.write("Files in pages directory:")
    for file in files:
        if file.endswith('.py'):
            st.write(f"  - {file}")
else:
    st.error(f"❌ Pages directory not found: {pages_dir}")

# Test 4: Try to import Auto Scaling page
st.markdown("---")
st.subheader("🔄 Testing Auto Scaling Page Import")

try:
    # Add current directory to path
    sys.path.append(os.path.dirname(__file__))
    
    # Import the module
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "auto_scaling", 
        "pages/5_Auto_Scaling_Recommendations_and_Control.py"
    )
    auto_scaling = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(auto_scaling)
    
    st.success("✅ Module imported successfully")
    
    # Check if show_page function exists
    if hasattr(auto_scaling, 'show_page'):
        st.success("✅ 'show_page' function found")
        
        # Try to execute show_page
        st.info("🔄 Attempting to execute show_page...")
        auto_scaling.show_page()
        st.success("✅ show_page executed successfully!")
        
    else:
        st.error("❌ No 'show_page' function found")
        
except Exception as e:
    st.error(f"❌ **Import Error:** {e}")
    st.code(f"Error Type: {type(e).__name__}")
    
    with st.expander("🔍 **Full Error Traceback**", expanded=True):
        st.code(traceback.format_exc())

# Test 5: Try to import Incident Timeline page
st.markdown("---")
st.subheader("🔄 Testing Incident Timeline Page Import")

try:
    spec = importlib.util.spec_from_file_location(
        "incident", 
        "pages/6_Incident_Timeline_and_Postmortem_Report_Generator.py"
    )
    incident = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(incident)
    
    st.success("✅ Module imported successfully")
    
    if hasattr(incident, 'show_page'):
        st.success("✅ 'show_page' function found")
        
        st.info("🔄 Attempting to execute show_page...")
        incident.show_page()
        st.success("✅ show_page executed successfully!")
        
    else:
        st.error("❌ No 'show_page' function found")
        
except Exception as e:
    st.error(f"❌ **Import Error:** {e}")
    st.code(f"Error Type: {type(e).__name__}")
    
    with st.expander("🔍 **Full Error Traceback**", expanded=True):
        st.code(traceback.format_exc())

st.markdown("---")
st.info("🔍 This debug test will show exactly where the page loading fails")
