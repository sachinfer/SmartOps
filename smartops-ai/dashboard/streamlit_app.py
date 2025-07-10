import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

st.title("🔍 SmartOps Anomaly Detection Dashboard")

# Connect to DB
conn = sqlite3.connect("/app/dashboard/data/data.db")
df = pd.read_sql_query("SELECT * FROM anomalies", conn)
conn.close()

if df.empty:
    st.warning("No data available.")
else:
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Real-time stats
    st.subheader("📈 Real-Time Prediction")
    latest = df.iloc[-1]
    st.metric("Latest CPU", latest['cpu'])
    st.metric("Latest Memory", latest['memory'])
    st.metric("Prediction", latest['prediction'])

    # Heatmap
    st.subheader("🗺️ Anomaly Heatmap")
    df['date'] = df['timestamp'].dt.date
    anomaly_counts = df[df['prediction'].str.lower().str.contains('anomaly')].groupby('date').size()
    if not anomaly_counts.empty:
        fig, ax = plt.subplots()
        sns.heatmap(anomaly_counts.values.reshape(-1, 1), annot=True, fmt="d", cmap="Reds", ax=ax, yticklabels=anomaly_counts.index)
        st.pyplot(fig)
    else:
        st.info("No anomalies detected yet.")

    # ROC curve placeholder
    st.subheader("📉 Model Evaluation (Placeholder)")
    st.text("Once you test with labeled data, show Precision/Recall/ROC here.") 