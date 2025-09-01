import streamlit as st
import pandas as pd
import requests
import sys
import os

# Import Misi from the dashboard directory
try:
    # from misi_chatbot_widget import add_misi_to_page
    MISI_AVAILABLE = True
except ImportError:
    MISI_AVAILABLE = False
    st.warning("Misi AI Chatbot not available. Please ensure the chatbot is properly installed.")

def show_page():
    """Main page function - called by the router"""
    # Note: Page config is handled by the main app, not here
    
    # Force full width for this page
    st.markdown("""
    <style>
    .main .block-container {
        max-width: 100% !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("⚖️ Auto-Scaling Recommendations and Control")
    st.write("""
    This page uses AI to analyze CPU/memory usage trends and recommend optimal Horizontal Pod Autoscaler (HPA) settings for your workloads. You can also apply recommended changes directly from the dashboard.
    """)

    API_URL = "http://localhost:8000"  # Change if your FastAPI backend is hosted elsewhere

    # Fetch real HPA/usage data from backend
    def fetch_hpa_data():
        try:
            resp = requests.get(f"{API_URL}/hpa_status", timeout=10)
            if resp.status_code == 200:
                return pd.DataFrame(resp.json()["hpa"])
            else:
                st.info(f"ℹ️ API Status: {resp.status_code} - Using sample data")
                # Return sample data if API fails
                return pd.DataFrame([
                    {
                        "pod": "smartops-app",
                        "namespace": "smartops",
                        "current_replicas": 1,
                        "min_replicas": 1,
                        "max_replicas": 5,
                        "cpu_avg": 0.65,
                        "mem_avg": 0.72,
                        "cpu_target": 0.7,
                        "mem_target": 0.8,
                        "last_scale_time": "2025-08-25 05:30:00",
                        "status": "Active"
                    },
                    {
                        "pod": "smartops-monitor",
                        "namespace": "smartops",
                        "current_replicas": 1,
                        "min_replicas": 1,
                        "max_replicas": 3,
                        "cpu_avg": 0.45,
                        "mem_avg": 0.38,
                        "cpu_target": 0.7,
                        "mem_target": 0.8,
                        "last_scale_time": "2025-08-25 04:15:00",
                        "status": "Active"
                    }
                ])
        except Exception as e:
            st.info(f"ℹ️ Connection error - Using sample data")
            # Return sample data on connection error
            return pd.DataFrame([
                {
                    "pod": "smartops-app",
                    "namespace": "smartops",
                    "current_replicas": 1,
                    "min_replicas": 1,
                    "max_replicas": 5,
                    "cpu_avg": 0.65,
                    "mem_avg": 0.72,
                    "cpu_target": 0.7,
                    "mem_target": 0.8,
                    "last_scale_time": "2025-08-25 05:30:00",
                    "status": "Active"
                }
            ])

    usage_df = fetch_hpa_data()
    if usage_df.empty:
        st.info("ℹ️ No HPA data available - Using sample data for demonstration")
        # Provide sample data for demonstration
        usage_df = pd.DataFrame([
            {
                "pod": "smartops-app",
                "namespace": "smartops",
                "current_replicas": 1,
                "min_replicas": 1,
                "max_replicas": 5,
                "cpu_avg": 0.65,
                "mem_avg": 0.72,
                "cpu_target": 0.7,
                "mem_target": 0.8,
                "last_scale_time": "2025-08-25 05:30:00",
                "status": "Active"
            }
        ])

    st.markdown("### Current Usage & HPA Settings")
    st.dataframe(usage_df, use_container_width=True)

    # Example AI recommendation logic (replace with your real model)
    def recommend_hpa(cpu_avg, mem_avg):
        # Simple rule-based logic for demo
        if cpu_avg > 0.7 or mem_avg > 0.7:
            return 2, 10  # Recommend higher min/max
        elif cpu_avg < 0.4 and mem_avg < 0.4:
            return 1, 3   # Recommend lower min/max
        else:
            return 1, 5   # Default

    st.markdown("### AI Recommendations")
    recommendations = []
    for idx, row in usage_df.iterrows():
        min_repl, max_repl = recommend_hpa(row['cpu_avg'], row['mem_avg'])
        recommendations.append({'pod': row['pod'], 'recommended_min': min_repl, 'recommended_max': max_repl})
    rec_df = pd.DataFrame(recommendations)
    st.dataframe(rec_df, use_container_width=True)

    st.markdown("### Apply Recommended HPA Settings")
    for idx, row in rec_df.iterrows():
        with st.expander(f"{row['pod']} - Set min: {row['recommended_min']}, max: {row['recommended_max']}"):
            if st.button(f"Apply to {row['pod']}"):
                try:
                    resp = requests.post(f"{API_URL}/update_hpa", json={
                        'pod': row['pod'],
                        'min_replicas': row['recommended_min'],
                        'max_replicas': row['recommended_max']
                    }, timeout=10)
                    if resp.status_code == 200:
                        st.success(f"HPA updated for {row['pod']}! Min: {row['recommended_min']}, Max: {row['recommended_max']}")
                    else:
                        st.info(f"ℹ️ API Status: {resp.status_code} - HPA update simulated")
                except Exception as e:
                    st.info(f"ℹ️ Connection error - HPA update simulated")

    # Add Misi AI Chatbot Widget
    if MISI_AVAILABLE:
        # add_misi_to_page("bottom-right")
        pass  # Placeholder for when Misi is properly integrated
    else:
        st.info("🤖 Misi AI Chatbot integration is being set up. You'll see the floating 🤖 icon soon!") 