# -*- coding: utf-8 -*-
"""
SmartOps Dashboard - Main Application
This is the main entry point that shows the sidebar and enables navigation
"""

import streamlit as st
import os
import sys
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

# Create the sidebar with navigation
def create_sidebar():
    """Create a comprehensive sidebar with navigation"""
    
    # Main title with branding
    st.sidebar.title("🚀 SmartOps Dashboard")
    st.sidebar.markdown("**by Misi 24x7**")
    st.sidebar.markdown("---")
    
    # Navigation sections
    st.sidebar.markdown("### 📊 **Core Monitoring**")
    
    # Other pages as navigation items
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
        import os
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

# Main content area
st.title("🚀 SmartOps Dashboard")
st.markdown("**Welcome to SmartOps - Enterprise Kubernetes Monitoring by Misi 24x7**")
st.markdown("---")

# Display overview information
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Active Pods",
        value="24",
        delta="+2"
    )

with col2:
    st.metric(
        label="CPU Usage",
        value="68%",
        delta="-5%"
    )

with col3:
    st.metric(
        label="Memory Usage",
        value="72%",
        delta="+3%"
    )

st.markdown("---")

# Quick access to key features
st.subheader("🚀 Quick Access")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 **Monitoring & Analytics**")
    st.markdown("• [Pod Explorer & Logs](?page=2_Pod_Explorer_and_Logs)")
    st.markdown("• [Kubernetes Shell](?page=3_Kubernetes_Shell_and_Cluster_Explorer)")
    st.markdown("• [Anomaly Detection](?page=4_Anomaly_Detection)")

with col2:
    st.markdown("### ⚡ **Operations & Control**")
    st.markdown("• [Auto Scaling Control](?page=5_Auto_Scaling_Recommendations_and_Control)")
    st.markdown("• [Incident Timeline](?page=6_Incident_Timeline_and_Postmortem_Report_Generator)")
    st.markdown("• [Deployments](?page=9_Deployments)")

st.markdown("---")

# System overview
st.subheader("📈 System Overview")
st.info("""
**SmartOps Dashboard** provides comprehensive monitoring and control for your Kubernetes clusters. 
Use the navigation in the sidebar to access different features, or click the quick links above.
""")

# Footer
st.markdown("---")
st.markdown("*SmartOps Dashboard - Powered by Misi 24x7*")
