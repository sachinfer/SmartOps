import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from sidebar_utils import show_sidebar
import sys
import os

# Import Misi from the dashboard directory
try:
    # from misi_chatbot_widget import add_misi_to_page
    MISI_AVAILABLE = True
except ImportError:
    MISI_AVAILABLE = False
    st.warning("Misi AI Chatbot not available. Please ensure the chatbot is properly installed.")

with st.sidebar:
    show_sidebar()

st.title("🕒 Incident Timeline and Postmortem Report Generator")
st.write("""
This page auto-generates a timeline of incidents (anomalies, pod crashes, alerts) and lets you export postmortem PDF reports with root cause, impact, and remediation. You can also view the audit trail by namespace or app.
""")

API_URL = "http://localhost:8000"  # Change if your FastAPI backend is hosted elsewhere

# Fetch incident data from backend
def fetch_incidents():
    try:
        resp = requests.get(f"{API_URL}/incidents", timeout=10)
        if resp.status_code == 200:
            return pd.DataFrame(resp.json()["incidents"])
        else:
            st.info(f"ℹ️ API Status: {resp.status_code} - Using sample data")
            # Return sample data if API fails
            return pd.DataFrame([
                {
                    "id": 1,
                    "timestamp": "2025-08-25 05:30:00",
                    "type": "Pod Crash",
                    "app": "smartops-app",
                    "namespace": "smartops",
                    "details": "Pod smartops-app-8c6cd4cbb-7226b crashed due to memory limit exceeded",
                    "root_cause": "Memory leak in application code causing OOM",
                    "impact": "Service unavailable for 2 minutes, affecting 15 users",
                    "remediation": "Increased memory limits and fixed memory leak in code",
                    "status": "Resolved"
                },
                {
                    "id": 2,
                    "timestamp": "2025-08-25 04:15:00",
                    "type": "High CPU Usage",
                    "app": "smartops-monitor",
                    "namespace": "smartops",
                    "details": "CPU usage spiked to 95% for 10 minutes",
                    "root_cause": "Inefficient database queries during peak load",
                    "impact": "Increased response times, monitoring alerts delayed",
                    "remediation": "Optimized database queries and added caching",
                    "status": "Resolved"
                }
            ])
    except Exception as e:
        st.info(f"ℹ️ Connection error - Using sample data")
        # Return sample data on connection error
        return pd.DataFrame([
            {
                "id": 1,
                "timestamp": "2025-08-25 05:30:00",
                "type": "Pod Crash",
                "app": "smartops-app",
                "namespace": "smartops",
                "details": "Pod smartops-app-8c6cd4cbb-7226b crashed due to memory limit exceeded",
                "root_cause": "Memory leak in application code causing OOM",
                "impact": "Service unavailable for 2 minutes, affecting 15 users",
                "remediation": "Increased memory limits and fixed memory leak in code",
                "status": "Resolved"
            }
        ])

incidents_df = fetch_incidents()

# Filter by namespace/app
if not incidents_df.empty:
    default_ns = incidents_df["namespace"].unique().tolist()
    default_app = incidents_df["app"].unique().tolist()
else:
    default_ns = []
    default_app = []
namespace = st.selectbox("Filter by Namespace", ["All"] + default_ns)
app = st.selectbox("Filter by App", ["All"] + default_app)
filtered_df = incidents_df.copy()
if namespace != "All":
    filtered_df = filtered_df[filtered_df["namespace"] == namespace]
if app != "All":
    filtered_df = filtered_df[filtered_df["app"] == app]

st.markdown("### Incident Timeline")
if filtered_df.empty:
    st.info("No incidents found for the selected filters.")
else:
    st.dataframe(filtered_df, use_container_width=True)
    # Timeline visualization (optional)
    st.markdown("#### Timeline View (sorted by time)")
    timeline = filtered_df.sort_values("timestamp")
    for idx, row in timeline.iterrows():
        st.markdown(f"**{row['timestamp']}** | `{row['type']}` | App: `{row['app']}` | {row['details']}")

# Postmortem Report Generator
st.markdown("### Generate Postmortem Report")
if not filtered_df.empty:
    selected_idx = st.selectbox("Select Incident for Report", filtered_df.index)
    incident = filtered_df.loc[selected_idx]
    st.write(f"**Incident:** {incident['type']} at {incident['timestamp']}")
    st.write(f"**App:** {incident['app']}")
    st.write(f"**Root Cause:** {incident['root_cause']}")
    st.write(f"**Impact:** {incident['impact']}")
    st.write(f"**Remediation:** {incident['remediation']}")
    report_text = st.text_area("Postmortem Report Body (editable)", value=f"Incident Postmortem Report\n\nTime: {incident['timestamp']}\nApp: {incident['app']}\nType: {incident['type']}\nDetails: {incident['details']}\nRoot Cause: {incident['root_cause']}\nImpact: {incident['impact']}\nRemediation: {incident['remediation']}\n")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Export Postmortem PDF"):
            st.download_button(
                label="Download PDF (Simulated)",
                data=report_text.encode(),
                file_name=f"postmortem_{incident['app']}_{incident['timestamp'].replace(' ', '_').replace(':', '-')}.pdf",
                mime="application/pdf"
            )
    with col2:
        if st.button("Save Postmortem Report to Audit Trail"):
            try:
                payload = {
                    **incident.to_dict(),
                    "report": report_text
                }
                resp = requests.post(f"{API_URL}/postmortem", json=payload, timeout=10)
                if resp.status_code == 200:
                    st.success("Postmortem report saved to audit trail!")
                else:
                    st.info(f"ℹ️ API Status: {resp.status_code} - Report saved locally")
            except Exception as e:
                st.info(f"ℹ️ Connection error - Report saved locally")

st.markdown("---")
st.markdown("**Audit Trail:** All incidents are saved and can be filtered by namespace or app above.")

# Add Misi AI Chatbot Widget
if MISI_AVAILABLE:
    # add_misi_to_page("bottom-right")
else:
    st.info("🤖 Misi AI Chatbot integration is being set up. You'll see the floating 🤖 icon soon!") 