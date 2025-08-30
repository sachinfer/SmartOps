# -*- coding: utf-8 -*-
"""
SmartOps Dashboard - Main Entry Point
This file serves as the main entry point for the Streamlit multi-page app
"""

import streamlit as st

# Page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="SmartOps Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    st.markdown("• **Pod Explorer & Logs** - Explore pods and view logs")
    st.markdown("• **Kubernetes Shell** - Interactive cluster exploration")
    st.markdown("• **Anomaly Detection** - AI-powered anomaly detection")

with col2:
    st.markdown("### ⚡ **Operations & Control**")
    st.markdown("• **Auto Scaling Control** - Manage HPA and scaling")
    st.markdown("• **Incident Timeline** - Track incidents and generate reports")
    st.markdown("• **Deployments** - Monitor deployment status")

st.markdown("---")

# System overview
st.subheader("📈 System Overview")
st.info("""
**SmartOps Dashboard** provides comprehensive monitoring and control for your Kubernetes clusters. 
Use the navigation in the sidebar to access different features and pages.
""")

# Current status
st.subheader("🔍 Current Status")
status_col1, status_col2 = st.columns(2)

with status_col1:
    st.success("✅ **System Status: Operational**")
    st.info("🌍 **Environment: Local**")
    st.warning("⚠️ **Alerts: 2 active**")

with status_col2:
    st.metric("📊 **Pods Running**", "24/25")
    st.metric("🔗 **Services**", "12")
    st.metric("📦 **Deployments**", "8")

# Footer
st.markdown("---")
st.markdown("*SmartOps Dashboard - Powered by Misi 24x7*")
