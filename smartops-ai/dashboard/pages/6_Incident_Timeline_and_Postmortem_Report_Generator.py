import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import pytz

def show_page():
    # Ultra-aggressive full-width CSS
    st.markdown("""
    <style>
    /* Force full width on ALL elements */
    * {
        max-width: 100vw !important;
    }
    
    /* Streamlit specific overrides */
    .main .block-container,
    .block-container,
    .stApp > div,
    [data-testid="stAppViewContainer"],
    .stApp > div > div,
    .stApp > div > div > div {
        max-width: 100vw !important;
        width: 100vw !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
    }
    
    /* Force full width on all containers */
    .stApp > div > div > div > div,
    .stApp > div > div > div > div > div,
    .stApp > div > div > div > div > div > div {
        max-width: 100vw !important;
        width: 100vw !important;
    }
    
    /* Override any remaining constraints */
    .main .block-container > div,
    .main .block-container > div > div {
        max-width: 100vw !important;
        width: 100vw !important;
    }
    
    /* Force full width on page content */
    .main .block-container > div > div {
        max-width: 100vw !important;
        width: 100vw !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🕒 Incident Timeline and Postmortem Report Generator")
    st.write("Track incidents, generate timeline reports, and create postmortem documentation")
    
    # Sample incident data with IST timezone
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist)
    
    incidents_data = [
        {
            "timestamp": current_time - timedelta(hours=2),
            "type": "Pod Crash",
            "app": "smartops-app",
            "namespace": "default",
            "description": "Pod crashed due to memory limit exceeded",
            "severity": "High",
            "status": "Resolved",
            "duration": "5m"
        },
        {
            "timestamp": current_time - timedelta(hours=8),
            "type": "High CPU",
            "app": "smartops-dashboard",
            "namespace": "default", 
            "description": "CPU usage above 90% for 10 minutes",
            "severity": "Medium",
            "status": "Resolved",
            "duration": "15m"
        },
        {
            "timestamp": current_time - timedelta(days=1),
            "type": "Network Issue",
            "app": "smartops-monitor",
            "namespace": "monitoring",
            "description": "Service unreachable from external network",
            "severity": "High",
            "status": "Resolved", 
            "duration": "30m"
        },
        {
            "timestamp": current_time - timedelta(days=2),
            "type": "Storage Alert",
            "app": "smartops-anomaly",
            "namespace": "default",
            "description": "Disk usage above 85%",
            "severity": "Low",
            "status": "Resolved",
            "duration": "2h"
        }
    ]
    
    # Convert to DataFrame
    df = pd.DataFrame(incidents_data)
    df['timestamp_str'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S IST')
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Incidents", len(df), "+1")
    with col2:
        st.metric("Resolved", len(df[df['status'] == 'Resolved']), "+1")
    with col3:
        st.metric("High Severity", len(df[df['severity'] == 'High']), "0")
    with col4:
        st.metric("Avg Resolution", "17.5m", "-5m")
    
    # Filters
    st.subheader("🔍 Filter Incidents")
    col1, col2 = st.columns(2)
    
    with col1:
        namespace_filter = st.selectbox("Filter by Namespace", 
                                       ["All"] + list(df['namespace'].unique()))
    with col2:
        app_filter = st.selectbox("Filter by App",
                                 ["All"] + list(df['app'].unique()))
    
    # Apply filters
    filtered_df = df.copy()
    if namespace_filter != "All":
        filtered_df = filtered_df[filtered_df['namespace'] == namespace_filter]
    if app_filter != "All":
        filtered_df = filtered_df[filtered_df['app'] == app_filter]
    
    # Incident Timeline
    st.subheader("📋 Incident Timeline")
    
    # Display incidents
    for _, incident in filtered_df.iterrows():
        severity_color = {
            "High": "🔴",
            "Medium": "🟡", 
            "Low": "🟢"
        }
        
        with st.expander(f"{severity_color[incident['severity']]} {incident['timestamp_str']} | {incident['type']} | {incident['app']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**App:** {incident['app']}")
                st.write(f"**Namespace:** {incident['namespace']}")
                st.write(f"**Type:** {incident['type']}")
                st.write(f"**Severity:** {incident['severity']}")
            with col2:
                st.write(f"**Status:** {incident['status']}")
                st.write(f"**Duration:** {incident['duration']}")
                st.write(f"**Time (IST):** {incident['timestamp_str']}")
            
            st.write(f"**Description:** {incident['description']}")
    
    # Incident Analytics
    st.subheader("📊 Incident Analytics")
    
    # Incidents by type
    col1, col2 = st.columns(2)
    
    with col1:
        incident_counts = df['type'].value_counts()
        fig1 = px.pie(values=incident_counts.values, names=incident_counts.index, 
                     title="Incidents by Type")
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        severity_counts = df['severity'].value_counts()
        fig2 = px.bar(x=severity_counts.index, y=severity_counts.values,
                     title="Incidents by Severity",
                     color=severity_counts.index,
                     color_discrete_map={"High": "red", "Medium": "orange", "Low": "green"})
        st.plotly_chart(fig2, use_container_width=True)
    
    # Postmortem Report Generator
    st.subheader("📝 Generate Postmortem Report")
    
    # Select incident for report
    incident_options = [f"{row['timestamp_str']} - {row['type']} - {row['app']}" 
                       for _, row in df.iterrows()]
    
    selected_incident_str = st.selectbox("Select Incident for Report", incident_options)
    
    if selected_incident_str:
        # Find selected incident
        selected_idx = incident_options.index(selected_incident_str)
        selected_incident = df.iloc[selected_idx]
        
        # Report details
        col1, col2 = st.columns(2)
        with col1:
            impact = st.text_area("Impact Description", 
                                value=f"Service {selected_incident['app']} was affected for {selected_incident['duration']}")
        with col2:
            root_cause = st.text_area("Root Cause Analysis",
                                    value="Resource limits exceeded due to memory leak in application code")
        
        remediation = st.text_area("Remediation Steps",
                                 value="1. Increased memory limits\n2. Fixed memory leak in code\n3. Added monitoring alerts")
        
        # Generate report
        if st.button("📄 Generate Postmortem Report", type="primary"):
            st.success("✅ Postmortem report generated!")
            
            report_content = f"""
# Incident Postmortem Report

**Incident ID:** {selected_incident['type']}-{selected_incident['timestamp'].strftime('%Y%m%d-%H%M')}
**Date:** {selected_incident['timestamp_str']}
**Application:** {selected_incident['app']}
**Namespace:** {selected_incident['namespace']}
**Severity:** {selected_incident['severity']}
**Duration:** {selected_incident['duration']}

## Summary
{selected_incident['description']}

## Impact
{impact}

## Root Cause
{root_cause}

## Remediation
{remediation}

## Timeline
- **{selected_incident['timestamp_str']}**: Incident detected
- **{(selected_incident['timestamp'] + timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M:%S IST')}**: Investigation started
- **{(selected_incident['timestamp'] + timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S IST')}**: Root cause identified
- **{(selected_incident['timestamp'] + pd.Timedelta(selected_incident['duration'])).strftime('%Y-%m-%d %H:%M:%S IST')}**: Incident resolved

## Action Items
- [ ] Review monitoring thresholds
- [ ] Update runbooks
- [ ] Schedule post-incident review
            """
            
            st.code(report_content, language="markdown")
            
            # Download button
            st.download_button(
                label="📥 Download Report",
                data=report_content,
                file_name=f"postmortem_{selected_incident['app']}_{selected_incident['timestamp'].strftime('%Y%m%d_%H%M')}.md",
                mime="text/markdown"
            )

if __name__ == "__main__":
    show_page()