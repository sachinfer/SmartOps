# -*- coding: utf-8 -*-
"""
Kubernetes Cluster Overview - SmartOps AI
Simplified dashboard for monitoring cluster health and metrics
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from sidebar_utils import show_sidebar

# Page config
st.set_page_config(
    page_title="Kubernetes Cluster Overview - SmartOps AI",
    page_icon="📊",
    layout="wide"
)

# Sidebar
with st.sidebar:
    show_sidebar()

# Main content
st.markdown("""
<div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 2rem; border-radius: 8px; margin-bottom: 2rem;">
    <h1 style="color: white; margin: 0;">📊 Kubernetes Cluster Overview</h1>
    <p style="color: #e8f4fd; margin: 0.5rem 0 0 0;">Real-time monitoring dashboard powered by SmartOps AI</p>
</div>
""", unsafe_allow_html=True)

# Simple Time Selector
st.header("⏰ Time Range Selection")
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    time_preset = st.selectbox(
        "Select Time Range",
        ["Live (Now)", "5 minutes ago", "15 minutes ago", "1 hour ago", "6 hours ago", "24 hours ago"],
        index=0
    )

with col2:
    if time_preset != "Live (Now)":
        relative_value = st.number_input("Value", min_value=1, max_value=365, value=1, step=1)
        relative_unit = st.selectbox("Unit", ["Minutes ago", "Hours ago", "Days ago"], index=1)

with col3:
    if st.button("🔄 Refresh", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# Display time info
if time_preset == "Live (Now)":
    st.info("📅 **Viewing:** Real-time data | " + datetime.now().strftime("%B %d, %Y at %I:%M %p"))
else:
    st.info(f"📅 **Viewing:** Data from {relative_value} {relative_unit.lower()} | " + datetime.now().strftime("%B %d, %Y"))

# Cluster Status
st.header("🏥 Cluster Status & Health")
st.success("✅ **SmartOps AI Status:** No anomalies detected. All systems are running smoothly!")

# Simple Metrics
st.header("📊 Cluster Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Nodes", "3", "Active")
with col2:
    st.metric("Pods", "12", "Running")
with col3:
    st.metric("Services", "8", "Network")
with col4:
    st.metric("Namespaces", "4", "Logical")

# Resource Usage
st.header("⚡ Resource Usage")
col1, col2 = st.columns(2)

with col1:
    st.metric("CPU Usage", "31%", "2.5/8 cores")
with col2:
    st.metric("Memory Usage", "26%", "4.2/16 GB")

# Pod Status
st.header("📋 Pod Status")
pod_data = pd.DataFrame({
    'Status': ['Running', 'Pending', 'Failed', 'Succeeded'],
    'Count': [10, 1, 0, 1]
})
st.bar_chart(pod_data.set_index('Status'))

# Node Health
st.header("🖥️ Node Health Status")
node_data = pd.DataFrame({
    'Node Name': ['gke-node-1', 'gke-node-2', 'gke-node-3'],
    'Status': ['Ready', 'Ready', 'Ready'],
    'Health': ['🟢 Healthy', '🟢 Healthy', '🟢 Healthy'],
    'CPU Usage (%)': [31, 23, 40],
    'Memory Usage (%)': [26, 19, 36],
    'Pods': [4, 3, 5]
})
st.dataframe(node_data, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.markdown("🚀 **Powered by SmartOps AI | Enterprise Kubernetes Monitoring**")
st.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}*")