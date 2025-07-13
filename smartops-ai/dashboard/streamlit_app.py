import streamlit as st
import requests
import re

st.title("SmartOps Application Status")

# Fetch anomaly score from your FastAPI app
try:
    res = requests.get("http://smartops-app-service.smartops.svc.cluster.local/metrics")
    text = res.text
    match = re.search(r"anomaly_score\s+([\d.]+)", text)
    if match:
        score = float(match.group(1))
        st.metric("Anomaly Score", score)
        if score > 0.9:
            st.error(f"⚠️ High anomaly detected! Score = {score}")
        else:
            st.success(f"✅ Normal. Score = {score}")
    else:
        st.warning("anomaly_score not found in metrics.")
except Exception as e:
    st.error(f"Error fetching metrics: {e}")

# Restart button
if st.button("🔁 Restart SmartOps App"):
    try:
        res = requests.post("http://smartops-app-service.smartops.svc.cluster.local/restart")
        st.info(res.json().get("message", "Restart triggered!"))
    except Exception as e:
        st.error(f"Error restarting app: {e}") 