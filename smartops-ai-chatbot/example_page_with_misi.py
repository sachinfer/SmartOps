"""
Example SmartOps Page with Misi AI Chatbot Integration
This shows how to add Misi to any page with just one line of code
"""

import streamlit as st
import sys
import os

# Add the chatbot directory to Python path
sys.path.append('.')

# Import Misi integration
from misi_integration import add_misi_to_page, add_misi_to_sidebar, add_misi_quick_help

# Page configuration
st.set_page_config(
    page_title="Example Page with Misi",
    page_icon="🤖",
    layout="wide"
)

def main():
    """Main page content"""
    
    # Header
    st.title("🤖 Example SmartOps Page with Misi")
    st.markdown("This page demonstrates how to integrate Misi AI chatbot into any SmartOps page.")
    
    # Page content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## 📋 Page Content")
        st.write("This is your regular page content. Users can interact with it normally.")
        
        # Example content
        st.info("**Tip:** Misi is available in the bottom-right corner! Click the 🤖 icon to chat.")
        
        # Sample data
        st.markdown("### 📊 Sample Metrics")
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.metric("CPU Usage", "75%", "↑ 5%")
        
        with col_b:
            st.metric("Memory", "2.1 GB", "↓ 0.3 GB")
        
        with col_c:
            st.metric("Pods", "24", "↑ 2")
        
        # Sample chart
        st.markdown("### 📈 Sample Chart")
        import numpy as np
        import pandas as pd
        chart_data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=['CPU', 'Memory', 'Network']
        )
        st.line_chart(chart_data)
    
    with col2:
        st.markdown("## 🎯 Quick Actions")
        
        # Quick help with Misi
        add_misi_quick_help()
        
        # Sample buttons
        if st.button("🚀 Deploy App"):
            st.success("App deployed successfully!")
        
        if st.button("📊 View Logs"):
            st.info("Opening log viewer...")
        
        if st.button("🔍 Monitor Resources"):
            st.info("Opening resource monitor...")
    
    # Add Misi to the page (this is the magic line!)
    # It will show a floating 🤖 icon in the bottom-right corner
    add_misi_to_page()
    
    # Alternative positions (uncomment to try):
    # add_misi_to_page("top-right")      # Top-right corner
    # add_misi_to_page("bottom-left")    # Bottom-left corner
    # add_misi_to_page("top-left")       # Top-left corner

def sidebar_content():
    """Sidebar content with Misi integration"""
    
    with st.sidebar:
        st.markdown("## 🧭 Navigation")
        
        # Page navigation
        pages = ["Overview", "Pods", "Monitoring", "Settings"]
        selected_page = st.selectbox("Select Page", pages)
        
        st.markdown("---")
        
        # Misi in sidebar
        add_misi_to_sidebar()
        
        st.markdown("---")
        
        # Additional sidebar content
        st.markdown("## ⚙️ Settings")
        st.checkbox("Enable Notifications")
        st.checkbox("Auto-refresh")
        st.slider("Refresh Rate (seconds)", 5, 60, 30)

if __name__ == "__main__":
    # Add sidebar content
    sidebar_content()
    
    # Main page content
    main()
    
    # Footer
    st.markdown("---")
    st.markdown("**💡 Pro Tip:** Try asking Misi questions like:")
    st.markdown("- 'How can I check pod status?'")
    st.markdown("- 'What is anomaly detection?'")
    st.markdown("- 'How do I access the Kubernetes shell?'")
    st.markdown("- 'Tell me about auto-scaling'")
