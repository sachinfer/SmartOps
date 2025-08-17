# -*- coding: utf-8 -*-
"""
Kubernetes Cluster Overview - SmartOps AI
New Relic-style monitoring dashboard
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

# New Relic-style CSS
st.markdown("""
<style>
/* New Relic-style dark theme */
.main .block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    max-width: 1400px;
    background-color: #1a1a1a;
}

/* Dark theme background */
.stApp {
    background-color: #1a1a1a;
}

/* New Relic-style header */
.dashboard-header {
    background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
    padding: 2rem;
    border-radius: 8px;
    margin-bottom: 2rem;
    border: 1px solid #4a5568;
    position: relative;
}

.dashboard-header h1 {
    font-size: 2rem;
    margin-bottom: 0.5rem;
    font-weight: 600;
    color: #f7fafc;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.dashboard-header p {
    font-size: 1rem;
    opacity: 0.8;
    margin: 0;
    color: #e2e8f0;
}

/* New Relic-style section headers */
.section-header {
    background: #2d3748;
    color: #f7fafc;
    padding: 1rem 1.5rem;
    border-radius: 6px;
    margin: 2rem 0 1rem 0;
    font-size: 1.1rem;
    font-weight: 600;
    border-left: 3px solid #3182ce;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

/* New Relic-style metric cards */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.metric-card {
    background: #2d3748;
    border: 1px solid #4a5568;
    border-radius: 8px;
    padding: 1.5rem;
    transition: all 0.2s ease;
    position: relative;
}

.metric-card:hover {
    border-color: #3182ce;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.metric-value {
    font-size: 2.5rem;
    font-weight: 700;
    color: #f7fafc;
    margin-bottom: 0.5rem;
    line-height: 1;
}

.metric-label {
    font-size: 0.875rem;
    color: #a0aec0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 500;
    margin-bottom: 0.75rem;
}

.metric-status {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    background: #38a169;
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
}

.metric-status.arrow-up::before {
    content: '↑';
    font-size: 0.8rem;
    font-weight: bold;
}

/* New Relic-style resource cards */
.resource-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.resource-card {
    background: #2d3748;
    border: 1px solid #4a5568;
    border-radius: 8px;
    padding: 1.5rem;
    transition: all 0.2s ease;
}

.resource-card:hover {
    border-color: #3182ce;
    transform: translateY(-1px);
}

.resource-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
}

.resource-icon {
    font-size: 1.25rem;
    color: #3182ce;
}

.resource-title {
    font-size: 1rem;
    font-weight: 600;
    color: #f7fafc;
    margin: 0;
}

.resource-value {
    font-size: 2rem;
    font-weight: 700;
    color: #f7fafc;
    margin-bottom: 0.5rem;
    text-align: center;
}

/* New Relic-style containers */
.chart-container {
    background: #2d3748;
    border: 1px solid #4a5568;
    border-radius: 8px;
    padding: 1.5rem;
    margin: 2rem 0;
}

.chart-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
}

.chart-icon {
    font-size: 1.25rem;
    color: #3182ce;
}

.chart-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #f7fafc;
    margin: 0;
}

/* New Relic-style time selector */
.time-selector {
    background: #2d3748;
    border: 1px solid #4a5568;
    border-radius: 8px;
    padding: 1.5rem;
    margin: 2rem 0;
}

.time-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
    font-size: 1rem;
    font-weight: 600;
    color: #f7fafc;
}

/* New Relic-style status messages */
.status-message {
    background: #2d3748;
    border: 1px solid #38a169;
    color: #f7fafc;
    padding: 1rem 1.5rem;
    border-radius: 6px;
    margin: 1.5rem 0;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.status-icon {
    font-size: 1.25rem;
    color: #38a169;
}

.status-text {
    font-size: 0.9rem;
    font-weight: 500;
    margin: 0;
    color: #e2e8f0;
}

/* New Relic-style buttons */
.stButton > button {
    background: #3182ce !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    background: #2c5aa0 !important;
    transform: translateY(-1px) !important;
}

/* New Relic-style selectboxes */
.stSelectbox > div > div {
    background: #2d3748 !important;
    border: 1px solid #4a5568 !important;
    color: #f7fafc !important;
}

.stSelectbox > div > div:hover {
    border-color: #3182ce !important;
}

/* New Relic-style number inputs */
.stNumberInput > div > div > input {
    background: #2d3748 !important;
    border: 1px solid #4a5568 !important;
    color: #f7fafc !important;
}

.stNumberInput > div > div > input:focus {
    border-color: #3182ce !important;
}

/* New Relic-style dataframes */
.dataframe {
    background: #2d3748 !important;
    color: #f7fafc !important;
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

# New Relic-style Time Selector
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
    if st.button("🔄 Refresh", use_container_width=True):
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

# New Relic-style Cluster Status
st.markdown('<div class="section-header">🏥 Cluster Status & Health</div>', unsafe_allow_html=True)
st.markdown("""
<div class="status-message">
    <div class="status-icon">✅</div>
    <div class="status-text">SmartOps AI Status: No anomalies detected. All systems are running smoothly!</div>
</div>
""", unsafe_allow_html=True)

# New Relic-style Cluster Metrics
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

# New Relic-style Resource Usage
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

# New Relic-style Pod Status
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

st.bar_chart(
    pod_data.set_index('Status'),
    use_container_width=True,
    height=300
)

st.markdown("</div>", unsafe_allow_html=True)

# New Relic-style Node Health
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

st.dataframe(
    node_data,
    use_container_width=True,
    hide_index=True,
    height=200
)

st.markdown("</div>", unsafe_allow_html=True)

# New Relic-style Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #a0aec0; padding: 2rem; font-size: 0.9rem;">
    <p style="font-weight: 600; margin-bottom: 0.5rem;">🚀 Powered by SmartOps AI | Enterprise Kubernetes Monitoring</p>
    <p style="opacity: 0.8; margin: 0;">Last updated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S IST') + """</p>
</div>
""", unsafe_allow_html=True)