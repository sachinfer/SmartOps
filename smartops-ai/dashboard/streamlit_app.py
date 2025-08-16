import streamlit as st
from sidebar_utils import show_sidebar

# Page config with modern theme
st.set_page_config(
    page_title="SmartOps AI Dashboard", 
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 0.5rem;
    }
    .alert-banner {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(255,107,107,0.3);
    }
    .success-banner {
        background: linear-gradient(135deg, #00b894 0%, #00a085 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,184,148,0.3);
    }
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        cursor: pointer;
        border: 2px solid transparent;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        border-color: #667eea;
    }
    .feature-card:active {
        transform: translateY(-2px);
    }
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    .feature-title {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        color: #2c3e50;
    }
    .feature-desc {
        color: #666;
        line-height: 1.5;
    }
    .clickable-card {
        cursor: pointer;
        user-select: none;
    }
    .navigation-section {
        background: rgba(255,255,255,0.05);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 2rem 0;
        border: 1px solid rgba(255,255,255,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Main content
st.markdown("""
<div class="main-header">
    <h1>🚀 SmartOps AI Dashboard</h1>
    <p>Welcome to the SmartOps AI-Driven DevOps Automation & Monitoring Platform</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    show_sidebar()

# Main content area
st.markdown("""
## 🎯 Quick Navigation

Click on any card below to navigate to the corresponding section, or use the sidebar for navigation:

- **🔥 Anomaly Detection** - AI-powered anomaly detection and analysis
- **🤖 AI Actions** - AI recommendations and action history
- **🚀 Deployments** - Deployment workflow events and tracking
- **🛰️ Pod Explorer & Logs** - Pod management and log viewing
- **🔍 Cluster Explorer** - Cluster resource exploration
- **🖥️ Kubernetes Shell** - kubectl command interface

Each page is designed to provide focused functionality for specific aspects of Kubernetes monitoring and management.
""")

# Feature cards with HTML styling for better visual appeal
st.markdown("""
<div class="navigation-section">
    <h3 style="color: white; margin-bottom: 1rem;">📋 Feature Overview</h3>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="feature-grid">
    <div class="feature-card clickable-card" onclick="window.parent.postMessage({type: 'streamlit:setComponentValue', key: 'anomaly_click', value: true}, '*')">
        <div class="feature-icon">🔥</div>
        <div class="feature-title">Anomaly Detection</div>
        <div class="feature-desc">AI-powered anomaly detection with top anomalies by CPU usage and recent anomaly tracking.</div>
    </div>
    <div class="feature-card clickable-card" onclick="window.parent.postMessage({type: 'streamlit:setComponentValue', key: 'ai_actions_click', value: true}, '*')">
        <div class="feature-icon">🤖</div>
        <div class="feature-title">AI Actions</div>
        <div class="feature-desc">AI recommendations and action history with model retraining capabilities.</div>
    </div>
    <div class="feature-card clickable-card" onclick="window.parent.postMessage({type: 'streamlit:setComponentValue', key: 'deployments_click', value: true}, '*')">
        <div class="feature-icon">🚀</div>
        <div class="feature-title">Deployments</div>
        <div class="feature-desc">Deployment workflow events tracking with success/failure statistics and metrics.</div>
    </div>
    <div class="feature-card clickable-card" onclick="window.parent.postMessage({type: 'streamlit:setComponentValue', key: 'pod_explorer_click', value: true}, '*')">
        <div class="feature-icon">🛰️</div>
        <div class="feature-title">Pod Explorer</div>
        <div class="feature-desc">Pod management with real-time log viewing, filtering, and pod actions (restart, delete, describe).</div>
    </div>
    <div class="feature-card clickable-card" onclick="window.parent.postMessage({type: 'streamlit:setComponentValue', key: 'cluster_explorer_click', value: true}, '*')">
        <div class="feature-icon">🔍</div>
        <div class="feature-title">Cluster Explorer</div>
        <div class="feature-desc">Safe kubectl-like queries for exploring cluster resources across namespaces.</div>
    </div>
    <div class="feature-card clickable-card" onclick="window.parent.postMessage({type: 'streamlit:setComponentValue', key: 'k8s_shell_click', value: true}, '*')">
        <div class="feature-icon">🖥️</div>
        <div class="feature-title">Kubernetes Shell</div>
        <div class="feature-desc">Interactive kubectl command interface with command history and safe execution.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Handle clicks from HTML cards
if st.button("🔥 Anomaly Detection", key="anomaly_click", use_container_width=True):
    st.switch_page("pages/4_Anomaly_Detection.py")

if st.button("🤖 AI Actions", key="ai_actions_click", use_container_width=True):
    st.switch_page("pages/8_AI_Actions.py")

if st.button("🚀 Deployments", key="deployments_click", use_container_width=True):
    st.switch_page("pages/9_Deployments.py")

if st.button("🛰️ Pod Explorer & Logs", key="pod_explorer_click", use_container_width=True):
    st.switch_page("pages/2_Pod Explorer & Logs.py")

if st.button("🔍 Cluster Explorer", key="cluster_explorer_click", use_container_width=True):
    st.switch_page("pages/3_Kubernetes Shell & Cluster Explorer.py")

if st.button("🖥️ Kubernetes Shell", key="k8s_shell_click", use_container_width=True):
    st.switch_page("pages/3_Kubernetes Shell & Cluster Explorer.py")

st.markdown("---")

st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🚀 Powered by SmartOps AI | Real-time Kubernetes Monitoring</p>
    <p>Built with ❤️ using Streamlit and AI/ML</p>
</div>
""", unsafe_allow_html=True) 