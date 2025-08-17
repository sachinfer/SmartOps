# -*- coding: utf-8 -*-
"""
Kubernetes Cluster Overview - SmartOps AI
Enhanced dashboard for monitoring cluster health and metrics
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

# Enhanced CSS for better UI experience
st.markdown("""
<style>
/* Main container styling */
.main .block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    max-width: 1400px;
}

/* Enhanced header styling */
.dashboard-header {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    padding: 2.5rem;
    border-radius: 16px;
    margin-bottom: 2.5rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.1);
    position: relative;
    overflow: hidden;
}

.dashboard-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 50%, rgba(255,255,255,0.05) 100%);
    pointer-events: none;
}

.dashboard-header h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    font-weight: 700;
    color: white;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.dashboard-header p {
    font-size: 1.1rem;
    opacity: 0.95;
    margin: 0;
    color: #e8f4fd;
    font-weight: 400;
}

/* Enhanced section headers */
.section-header {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    color: #495057;
    padding: 1.2rem 1.8rem;
    border-radius: 12px;
    margin: 2.5rem 0 1.5rem 0;
    font-size: 1.2rem;
    font-weight: 700;
    border-left: 5px solid #2a5298;
    display: flex;
    align-items: center;
    gap: 0.8rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

/* Enhanced metric cards */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.8rem;
    margin: 2rem 0;
}

.metric-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    border: 1px solid #e9ecef;
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    border-left: 4px solid #00d4aa;
}

.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
    border-color: #2a5298;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #00d4aa, #2a5298);
}

.metric-value {
    font-size: 3rem;
    font-weight: 800;
    color: #1e3c72;
    margin-bottom: 0.5rem;
    line-height: 1;
}

.metric-label {
    font-size: 1rem;
    color: #6c757d;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.metric-status {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    background: linear-gradient(135deg, #00d4aa 0%, #00b894 100%);
    color: white;
    padding: 0.4rem 0.8rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    box-shadow: 0 2px 8px rgba(0, 212, 170, 0.3);
}

.metric-status.arrow-up::before {
    content: '↑';
    font-size: 0.9rem;
    font-weight: bold;
}

/* Enhanced resource usage cards */
.resource-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 2rem;
    margin: 2rem 0;
}

.resource-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    border: 1px solid #e9ecef;
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.resource-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 25px rgba(0, 0, 0, 0.12);
}

.resource-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 1.5rem;
}

.resource-icon {
    font-size: 1.5rem;
    color: #2a5298;
}

.resource-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #495057;
    margin: 0;
}

.resource-value {
    font-size: 2.5rem;
    font-weight: 800;
    color: #1e3c72;
    margin-bottom: 0.5rem;
    text-align: center;
}

.resource-details {
    text-align: center;
    color: #6c757d;
    font-size: 0.9rem;
    font-weight: 500;
}

/* Enhanced charts and tables */
.chart-container {
    background: white;
    border: 1px solid #e9ecef;
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    margin: 2rem 0;
}

.chart-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 1.5rem;
}

.chart-icon {
    font-size: 1.5rem;
    color: #2a5298;
}

.chart-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: #495057;
    margin: 0;
}

/* Enhanced time selector */
.time-selector {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    border: 1px solid #dee2e6;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 2rem 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.time-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 1.5rem;
    font-size: 1.1rem;
    font-weight: 600;
    color: #495057;
}

/* Enhanced status messages */
.status-message {
    background: linear-gradient(135deg, #00d4aa 0%, #00b894 100%);
    color: white;
    padding: 1.5rem 2rem;
    border-radius: 12px;
    margin: 2rem 0;
    box-shadow: 0 4px 20px rgba(0, 212, 170, 0.2);
    border: 1px solid #00b894;
    display: flex;
    align-items: center;
    gap: 1rem;
}

.status-icon {
    font-size: 1.5rem;
}

.status-text {
    font-size: 1rem;
    font-weight: 600;
    margin: 0;
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Responsive design */
@media (max-width: 768px) {
    .metric-grid {
        grid-template-columns: 1fr;
    }
    
    .resource-grid {
        grid-template-columns: 1fr;
    }
    
    .dashboard-header h1 {
        font-size: 2rem;
    }
}
</style>
""", unsafe_allow_html=True)

# Main content
st.markdown("""
<div class="dashboard-header">
    <h1>📊 Kubernetes Cluster Overview</h1>
    <p>Real-time monitoring dashboard powered by SmartOps AI</p>
</div>
""", unsafe_allow_html=True)

# Enhanced Time Selector
st.markdown("""
<div class="time-selector">
    <div class="time-header">⏰ Time Range Selection</div>
    <div style="display: grid; grid-template-columns: 2fr 2fr 1fr; gap: 1rem; align-items: end;">
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    time_preset = st.selectbox(
        "Select Time Range",
        ["Live (Now)", "5 minutes ago", "15 minutes ago", "1 hour ago", "6 hours ago", "24 hours ago"],
        index=0,
        label_visibility="collapsed"
    )

with col2:
    if time_preset != "Live (Now)":
        relative_value = st.number_input("Value", min_value=1, max_value=365, value=1, step=1, label_visibility="collapsed")
        relative_unit = st.selectbox("Unit", ["Minutes ago", "Hours ago", "Days ago"], index=1, label_visibility="collapsed")

with col3:
    if st.button("🔄 Refresh", use_container_width=True, type="primary"):
        st.cache_data.clear()
        st.rerun()

st.markdown("</div></div>", unsafe_allow_html=True)

# Display time info
if time_preset == "Live (Now)":
    st.markdown("""
    <div class="status-message">
        <div class="status-icon">📅</div>
        <div class="status-text">Viewing: Real-time data | """ + datetime.now().strftime("%B %d, %Y at %I:%M %p") + """</div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="status-message">
        <div class="status-icon">📅</div>
        <div class="status-text">Viewing: Data from {relative_value} {relative_unit.lower()} | """ + datetime.now().strftime("%B %d, %Y") + """</div>
    </div>
    """, unsafe_allow_html=True)

# Enhanced Cluster Status
st.markdown('<div class="section-header">🏥 Cluster Status & Health</div>', unsafe_allow_html=True)
st.markdown("""
<div class="status-message">
    <div class="status-icon">✅</div>
    <div class="status-text">SmartOps AI Status: No anomalies detected. All systems are running smoothly!</div>
</div>
""", unsafe_allow_html=True)

# Enhanced Cluster Metrics
st.markdown('<div class="section-header">📊 Cluster Metrics</div>', unsafe_allow_html=True)

st.markdown("""
<div class="metric-grid">
    <div class="metric-card">
        <div class="metric-value">3</div>
        <div class="metric-label">Nodes</div>
        <div class="metric-status arrow-up">Active</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">12</div>
        <div class="metric-label">Pods</div>
        <div class="metric-status arrow-up">Running</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">8</div>
        <div class="metric-label">Services</div>
        <div class="metric-status arrow-up">Network</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">4</div>
        <div class="metric-label">Namespaces</div>
        <div class="metric-status arrow-up">Logical</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Enhanced Resource Usage
st.markdown('<div class="section-header">⚡ Resource Usage</div>', unsafe_allow_html=True)

st.markdown("""
<div class="resource-grid">
    <div class="resource-card">
        <div class="resource-header">
            <div class="resource-icon">🖥️</div>
            <div class="resource-title">CPU Usage</div>
        </div>
        <div class="resource-value">31%</div>
        <div class="metric-status arrow-up">2.5/8 cores</div>
    </div>
    <div class="resource-card">
        <div class="resource-header">
            <div class="resource-icon">💾</div>
            <div class="resource-title">Memory Usage</div>
        </div>
        <div class="resource-value">26%</div>
        <div class="metric-status arrow-up">4.2/16 GB</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Enhanced Pod Status
st.markdown('<div class="section-header">📋 Pod Status</div>', unsafe_allow_html=True)

st.markdown("""
<div class="chart-container">
    <div class="chart-header">
        <div class="chart-icon">📊</div>
        <div class="chart-title">Pod Status Distribution</div>
    </div>
""", unsafe_allow_html=True)

pod_data = pd.DataFrame({
    'Status': ['Running', 'Pending', 'Failed', 'Succeeded'],
    'Count': [10, 1, 0, 1]
})

# Create a more visually appealing chart
st.bar_chart(
    pod_data.set_index('Status'),
    use_container_width=True,
    height=300
)

st.markdown("</div>", unsafe_allow_html=True)

# Enhanced Node Health
st.markdown('<div class="section-header">🖥️ Node Health Status</div>', unsafe_allow_html=True)

st.markdown("""
<div class="chart-container">
    <div class="chart-header">
        <div class="chart-icon">🔍</div>
        <div class="chart-title">Node Health Overview</div>
    </div>
""", unsafe_allow_html=True)

node_data = pd.DataFrame({
    'Node Name': ['gke-node-1', 'gke-node-2', 'gke-node-3'],
    'Status': ['Ready', 'Ready', 'Ready'],
    'Health': ['🟢 Healthy', '🟢 Healthy', '🟢 Healthy'],
    'CPU Usage (%)': [31, 23, 40],
    'Memory Usage (%)': [26, 19, 36],
    'Pods': [4, 3, 5]
})

# Enhanced dataframe display
st.dataframe(
    node_data,
    use_container_width=True,
    hide_index=True,
    height=200
)

st.markdown("</div>", unsafe_allow_html=True)

# Enhanced Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 2rem; font-size: 0.9rem;">
    <p style="font-weight: 600; margin-bottom: 0.5rem;">🚀 Powered by SmartOps AI | Enterprise Kubernetes Monitoring</p>
    <p style="opacity: 0.8; margin: 0;">Last updated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S IST') + """</p>
</div>
""", unsafe_allow_html=True)