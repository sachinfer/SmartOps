import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from sidebar_utils import show_sidebar

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
            st.error(f"Failed to fetch incidents: {resp.text}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching incidents: {e}")
        return pd.DataFrame()

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
                    st.error(f"Failed to save postmortem: {resp.text}")
            except Exception as e:
                st.error(f"Error saving postmortem: {e}")

st.markdown("---")
st.markdown("**Audit Trail:** All incidents are saved and can be filtered by namespace or app above.") 