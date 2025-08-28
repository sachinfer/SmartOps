#!/usr/bin/env python3
"""
SmartOps Dashboard - Main Application
Centralized navigation system for consistent sidebar behavior
"""

import streamlit as st
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sidebar_utils import show_sidebar, get_current_page, set_current_page

def route_to_page():
    """Route to the appropriate page based on sidebar selection"""
    current_page = get_current_page()
    
    # Show sidebar first (this will be consistent across all pages)
    show_sidebar()
    
    # Route to the appropriate page based on current_page
    if current_page == "overview":
        from pages import page_1_Overview
        page_1_Overview.show_page()
    elif current_page == "anomaly":
        from pages import page_4_Anomaly_Detection
        page_4_Anomaly_Detection.show_page()
    elif current_page == "pod_explorer":
        from pages import page_2_Pod_Explorer_and_Logs
        page_2_Pod_Explorer_and_Logs.show_page()
    elif current_page == "kubernetes_shell":
        from pages import page_3_Kubernetes_Shell_and_Cluster_Explorer
        page_3_Kubernetes_Shell_and_Cluster_Explorer.show_page()
    elif current_page == "auto_scaling":
        from pages import page_5_Auto_Scaling_Recommendations_and_Control
        page_5_Auto_Scaling_Recommendations_and_Control.show_page()
    elif current_page == "deployments":
        from pages import page_9_Deployments
        page_9_Deployments.show_page()
    elif current_page == "ai_actions":
        from pages import page_8_AI_Actions
        page_8_AI_Actions.show_page()
    elif current_page == "incident_timeline":
        from pages import page_6_Incident_Timeline_and_Postmortem_Report_Generator
        page_6_Incident_Timeline_and_Postmortem_Report_Generator.show_page()
    elif current_page == "misi_ai":
        from pages import page_7_Misi_AI_Assistant
        page_7_Misi_AI_Assistant.show_page()
    else:
        # Default to overview page
        set_current_page("overview")
        from pages import page_1_Overview
        page_1_Overview.show_page()

def main():
    """Main application entry point"""
    # Page configuration
    st.set_page_config(
        page_title="SmartOps AI Dashboard",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Route to the appropriate page
    route_to_page()

if __name__ == "__main__":
    main()
