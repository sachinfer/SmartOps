import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Full Width Test",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Force full width CSS
st.markdown("""
<style>
    /* Force full width */
    html, body { width: 100vw !important; max-width: 100vw !important; margin: 0 !important; padding: 0 !important; }
    .stApp { width: 100vw !important; max-width: 100vw !important; margin: 0 !important; padding: 0 !important; }
    .main { width: 100vw !important; max-width: 100vw !important; margin: 0 !important; padding: 0 !important; }
    .block-container { width: 100vw !important; max-width: 100vw !important; margin: 0 !important; padding: 0.5rem !important; }
    [data-testid="stAppViewContainer"] { width: 100vw !important; max-width: 100vw !important; margin: 0 !important; padding: 0 !important; }
    .stMarkdown, .stDataFrame, .stMetric, .stColumns, .stTable { width: 100% !important; max-width: 100% !important; }
    .stColumns > div { width: 100% !important; max-width: 100% !important; flex: 1 !important; }
    .stTable table { width: 100% !important; max-width: 100% !important; }
    :root { --main-width: 100vw !important; --max-width: 100vw !important; --content-width: 100vw !important; }
</style>
""", unsafe_allow_html=True)

st.title("Full Width Test Page")
st.write("This page should use the full width of the screen.")

# Create a wide table
import pandas as pd
import numpy as np

# Generate test data
data = {
    'Column 1': np.random.randn(10),
    'Column 2': np.random.randn(10),
    'Column 3': np.random.randn(10),
    'Column 4': np.random.randn(10),
    'Column 5': np.random.randn(10),
    'Column 6': np.random.randn(10),
    'Column 7': np.random.randn(10),
    'Column 8': np.random.randn(10),
    'Column 9': np.random.randn(10),
    'Column 10': np.random.randn(10),
}

df = pd.DataFrame(data)

st.subheader("Wide Table Test")
st.dataframe(df, use_container_width=True)

st.subheader("Columns Test")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Metric 1", "100", "10")
with col2:
    st.metric("Metric 2", "200", "20")
with col3:
    st.metric("Metric 3", "300", "30")
with col4:
    st.metric("Metric 4", "400", "40")

st.subheader("Chart Test")
import plotly.express as px
fig = px.bar(df, x='Column 1', y='Column 2', title="Test Chart")
st.plotly_chart(fig, use_container_width=True)

st.write("If you can see this text and the content above spans the full width, the fix is working!")
