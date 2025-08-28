#!/usr/bin/env python3
"""
SmartOps Dashboard - Main Application
Simple dashboard with static sidebar
"""

import streamlit as st
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import sidebar utilities
from sidebar_utils import show_sidebar

# Page configuration
st.set_page_config(
    page_title="SmartOps AI Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for the main app
st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 3rem 2rem;
    border-radius: 20px;
    margin: 2rem 0;
    text-align: center;
    color: white;
    box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
}

.main-header h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
    font-weight: 800;
    text-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.main-header p {
    font-size: 1.3rem;
    opacity: 0.95;
    margin: 0;
    font-weight: 500;
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin: 3rem 0;
}

.feature-card {
    background: rgba(45, 55, 72, 0.8);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.feature-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
}

.feature-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4);
    border-color: rgba(102, 126, 234, 0.5);
}

.feature-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    display: block;
}

.feature-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #f7fafc;
    margin-bottom: 1rem;
}

.feature-description {
    color: #a0aec0;
    line-height: 1.6;
    margin-bottom: 1.5rem;
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Show static sidebar (never changes)
    show_sidebar()
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 SmartOps AI Dashboard</h1>
        <p>Enterprise Kubernetes Monitoring & AI-Powered Operations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message
    st.success("🎉 Welcome to SmartOps AI! Your Kubernetes cluster monitoring dashboard is ready.")
    
    # Feature overview
    st.markdown("## 🎯 Dashboard Features")
    
    # Feature grid
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Core Monitoring</div>
            <div class="feature-description">
                Real-time cluster overview, pod status, and resource monitoring with beautiful visualizations.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔥</div>
            <div class="feature-title">Anomaly Detection</div>
            <div class="feature-description">
                AI-powered anomaly detection for pods, services, and cluster resources with actionable insights.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🛰️</div>
            <div class="feature-title">Pod Management</div>
            <div class="feature-description">
                Advanced pod explorer, log viewer, and cluster shell for comprehensive cluster management.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick start guide
    st.markdown("## 🚀 Quick Start Guide")
    
    st.info("""
    **Getting Started:**
    1. **Use the sidebar navigation** to explore different dashboard sections
    2. **Start with Overview Dashboard** to see your cluster status
    3. **Check Anomaly Detection** for any issues
    4. **Use Pod Explorer** to manage your workloads
    5. **Access AI Actions** for automated operations
    """)
    
    # System status
    st.markdown("## 🔧 System Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Dashboard Status", "🟢 Online", "Ready")
    
    with col2:
        st.metric("API Status", "🟢 Connected", "Port 8000")
    
    with col3:
        st.metric("Database", "🟢 Active", "SQLite")
    
    with col4:
        st.metric("AI Engine", "🟢 Ready", "SmartOps AI")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #a0aec0; padding: 2rem;">
        <p>🚀 Powered by SmartOps AI - Enterprise Kubernetes Operations</p>
        <p style="font-size: 0.9rem; opacity: 0.8;">© 2024 SmartOps AI. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
