import streamlit as st
import pandas as pd
import requests
from sidebar_utils import show_sidebar

with st.sidebar:
    show_sidebar()

st.title("⚖️ Auto-Scaling Recommendations & Control")
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
            st.error(f"Failed to fetch HPA data: {resp.text}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching HPA data: {e}")
        return pd.DataFrame()

usage_df = fetch_hpa_data()
if usage_df.empty:
    st.warning("No HPA data available.")
    st.stop()

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
                    st.error(f"Failed to update HPA: {resp.text}")
            except Exception as e:
                st.error(f"Error updating HPA: {e}") 