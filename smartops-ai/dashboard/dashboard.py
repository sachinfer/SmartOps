# -*- coding: utf-8 -*-
"""
SmartOps Dashboard - Main Application
This is the main entry point for the Streamlit application
"""

import streamlit as st
import sys
import os
import importlib.util

# Page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="SmartOps Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the Overview page content using importlib
def import_overview_page():
    """Import the Overview page using importlib since it starts with a number"""
    try:
        # Get the path to the Overview page
        overview_path = os.path.join(os.path.dirname(__file__), "pages", "1_Overview.py")
        
        # Load the module
        spec = importlib.util.spec_from_file_location("overview", overview_path)
        overview_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(overview_module)
        
        return overview_module.show_page
    except Exception as e:
        st.error(f"Error importing Overview page: {e}")
        # Return a fallback function
        def fallback_page():
            st.title("Overview Page")
            st.write("Error loading Overview page content")
        return fallback_page

# Get the show_page function
show_page = import_overview_page()

# Create the sidebar with navigation
def create_sidebar():
    """Create a comprehensive sidebar with navigation"""
    
    # Main title with branding
    st.sidebar.title("🚀 SmartOps Dashboard")
    st.sidebar.markdown("**by Misi 24x7**")
    st.sidebar.markdown("---")
    
    # Navigation sections
    st.sidebar.markdown("### 📊 **Core Monitoring**")
    st.sidebar.markdown("• **🟩 Overview** (Current)")
    st.sidebar.markdown("• 🧭 Pod Explorer & Logs")
    st.sidebar.markdown("• 🔍 Kubernetes Shell")
    st.sidebar.markdown("• 🔥 Anomaly Detection")
    
    st.sidebar.markdown("---")
    
    st.sidebar.markdown("### ⚡ **Operations**")
    st.sidebar.markdown("• ⚡ Auto Scaling Control")
    st.sidebar.markdown("• 📝 Incident Timeline")
    st.sidebar.markdown("• 🚀 Deployments")
    
    st.sidebar.markdown("---")
    
    st.sidebar.markdown("### 🤖 **AI & Analytics**")
    st.sidebar.markdown("• 🤖 AI Actions")
    st.sidebar.markdown("• 💬 Misi AI Assistant")
    
    st.sidebar.markdown("---")
    
    # Quick actions
    st.sidebar.markdown("### 🔄 **Quick Actions**")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("🔄 Refresh", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    with col2:
        if st.button("📊 Status", use_container_width=True):
            st.sidebar.success("✅ All systems operational")
    
    # System status
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📈 **System Status**")
    st.sidebar.success("🟢 **Online**")
    
    # Environment info
    try:
        env = os.environ.get('KUBERNETES_SERVICE_HOST', 'local')
        if env != 'local':
            st.sidebar.info(f"🌍 **Environment:** {env.upper()}")
        else:
            st.sidebar.info("🌍 **Environment:** Local")
    except:
        st.sidebar.info("🌍 **Environment:** Unknown")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**SmartOps by Misi 24x7**")
    st.sidebar.markdown("*Enterprise Kubernetes Monitoring*")

# Show the sidebar
create_sidebar()

# Show the main page content
st.markdown("---")
show_page()
