import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def show_page():
    # Nuclear full-width CSS for maximum aggression
    st.markdown("""
    <style>
    /* Nuclear option - override EVERYTHING */
    * {
        max-width: 100% !important;
        width: auto !important;
    }
    
    /* Streamlit specific overrides - maximum aggression */
    .main .block-container,
    .block-container,
    .stApp > div,
    [data-testid="stAppViewContainer"],
    .stApp > div > div,
    .stApp > div > div > div,
    .stApp > div > div > div > div,
    .stApp > div > div > div > div > div,
    .stApp > div > div > div > div > div > div {
        max-width: 100% !important;
        width: 100% !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
        min-width: 100% !important;
    }
    
    /* Force full width on ALL possible containers */
    .main .block-container > div,
    .main .block-container > div > div,
    .main .block-container > div > div > div,
    .main .block-container > div > div > div > div {
        max-width: 100% !important;
        width: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Override any remaining constraints with extreme prejudice */
    div[data-testid="stAppViewContainer"] > div,
    div[data-testid="stAppViewContainer"] > div > div,
    div[data-testid="stAppViewContainer"] > div > div > div {
        max-width: 100% !important;
        width: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Force sidebar to not interfere */
    .sidebar .sidebar-content {
        width: 250px !important;
        max-width: 250px !important;
    }
    
    /* Force main content to use remaining space */
    .main .block-container {
        margin-left: 250px !important;
        margin-right: 0 !important;
        padding: 0 !important;
        width: calc(100vw - 250px) !important;
        max-width: calc(100vw - 250px) !important;
    }
    </style>
    
    
    """, unsafe_allow_html=True)

    st.title("⚖️ Auto-Scaling Recommendations and Control")
    st.write("AI-powered auto-scaling recommendations for your Kubernetes workloads")
    
    # Sample HPA data
    st.subheader("📊 Current HPA Settings")
    hpa_data = {
        "Application": ["smartops-app", "smartops-dashboard", "smartops-monitor", "smartops-anomaly"],
        "Current Replicas": [3, 2, 1, 2],
        "Min Replicas": [2, 1, 1, 1],
        "Max Replicas": [10, 5, 3, 5],
        "CPU Target": ["70%", "80%", "75%", "65%"],
        "Memory Target": ["80%", "85%", "80%", "75%"],
        "Status": ["Scaling", "Stable", "Stable", "Scaling"]
    }
    
    df = pd.DataFrame(hpa_data)
    st.dataframe(df, use_container_width=True)
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Apps", "4", "0")
    with col2:
        st.metric("Active HPAs", "4", "+1")
    with col3:
        st.metric("Total Replicas", "8", "+2")
    with col4:
        st.metric("Avg CPU Target", "72.5%", "-5%")
    
    # AI Recommendations
    st.subheader("🤖 AI Recommendations")
    
    recommendations = [
        {"app": "smartops-app", "current_max": 10, "recommended_max": 8, "reason": "Peak usage only reaches 6 replicas", "savings": "20%"},
        {"app": "smartops-dashboard", "current_max": 5, "recommended_max": 3, "reason": "Low traffic pattern", "savings": "40%"},
        {"app": "smartops-monitor", "current_max": 3, "recommended_max": 3, "reason": "Optimal settings", "savings": "0%"},
        {"app": "smartops-anomaly", "current_max": 5, "recommended_max": 4, "reason": "Consistent load pattern", "savings": "20%"}
    ]
    
    for rec in recommendations:
        with st.expander(f"📊 {rec['app']} - Potential Savings: {rec['savings']}"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Current Max:** {rec['current_max']}")
            with col2:
                st.write(f"**Recommended Max:** {rec['recommended_max']}")
            with col3:
                st.write(f"**Savings:** {rec['savings']}")
            
            st.write(f"**Reason:** {rec['reason']}")
            
            if st.button(f"Apply for {rec['app']}", key=f"apply_{rec['app']}"):
                st.success(f"✅ HPA updated for {rec['app']}")
    
    # Usage Charts
    st.subheader("📈 Resource Usage Trends")
    
    # Sample usage data
    dates = pd.date_range(start='2025-01-25', end='2025-01-31', freq='D')
    usage_data = {
        'Date': dates,
        'smartops-app': [65, 70, 68, 72, 75, 73, 69],
        'smartops-dashboard': [45, 50, 48, 52, 55, 53, 49],
        'smartops-monitor': [30, 35, 33, 37, 40, 38, 34],
        'smartops-anomaly': [55, 60, 58, 62, 65, 63, 59]
    }
    
    usage_df = pd.DataFrame(usage_data)
    usage_df_melted = usage_df.melt(id_vars=['Date'], var_name='Application', value_name='CPU Usage %')
    
    fig = px.line(usage_df_melted, x='Date', y='CPU Usage %', color='Application', 
                  title='7-Day CPU Usage Trend')
    st.plotly_chart(fig, use_container_width=True)
    
    # Apply Settings
    st.subheader("⚙️ Apply HPA Settings")
    
    col1, col2 = st.columns(2)
    with col1:
        selected_app = st.selectbox("Select Application", 
                                   ["smartops-app", "smartops-dashboard", "smartops-monitor", "smartops-anomaly"])
    with col2:
        action = st.selectbox("Action", ["Apply AI Recommendation", "Custom Settings"])
    
    if action == "Custom Settings":
        col1, col2 = st.columns(2)
        with col1:
            min_replicas = st.number_input("Min Replicas", min_value=1, max_value=10, value=2)
        with col2:
            max_replicas = st.number_input("Max Replicas", min_value=1, max_value=20, value=5)
    
    if st.button("🚀 Apply Settings", type="primary"):
        st.success(f"✅ HPA settings applied for {selected_app}!")
        st.balloons()

if __name__ == "__main__":
    show_page()