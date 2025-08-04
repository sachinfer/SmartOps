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
        transition: transform 0.3s ease;
    }
    .feature-card:hover {
        transform: translateY(-5px);
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

Use the sidebar to navigate between different sections of the SmartOps AI platform:

- **🏠 Overview** - System overview and basic statistics
- **🔥 Anomaly Detection** - AI-powered anomaly detection and analysis
- **📈 Analytics** - Resource usage analytics and trends
- **🤖 AI Actions** - AI recommendations and action history
- **🚀 Deployments** - Deployment workflow events and tracking
- **🛰️ Pod Explorer & Logs** - Pod management and log viewing
- **🔍 Cluster Explorer** - Cluster resource exploration
- **🖥️ Kubernetes Shell** - kubectl command interface

Each page is designed to provide focused functionality for specific aspects of Kubernetes monitoring and management.
""")

# Feature cards
st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <div class="feature-icon">🏠</div>
        <div class="feature-title">Overview Dashboard</div>
        <div class="feature-desc">Real-time system overview with pod and service statistics, namespace monitoring, and system health status.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🔥</div>
        <div class="feature-title">Anomaly Detection</div>
        <div class="feature-desc">AI-powered anomaly detection with top anomalies by CPU usage and recent anomaly tracking.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">📈</div>
        <div class="feature-title">Analytics</div>
        <div class="feature-desc">Resource usage analytics with interactive charts showing CPU and memory trends over time.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <div class="feature-title">AI Actions</div>
        <div class="feature-desc">AI recommendations and action history with model retraining capabilities.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🚀</div>
        <div class="feature-title">Deployments</div>
        <div class="feature-desc">Deployment workflow events tracking with success/failure statistics and metrics.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🛰️</div>
        <div class="feature-title">Pod Explorer</div>
        <div class="feature-desc">Pod management with real-time log viewing, filtering, and pod actions (restart, delete, describe).</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🔍</div>
        <div class="feature-title">Cluster Explorer</div>
        <div class="feature-desc">Safe kubectl-like queries for exploring cluster resources across namespaces.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🖥️</div>
        <div class="feature-title">Kubernetes Shell</div>
        <div class="feature-desc">Interactive kubectl command interface with command history and safe execution.</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🚀 Powered by SmartOps AI | Real-time Kubernetes Monitoring</p>
    <p>Built with ❤️ using Streamlit and AI/ML</p>
</div>
""", unsafe_allow_html=True) 