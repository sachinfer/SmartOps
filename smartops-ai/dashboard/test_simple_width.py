import streamlit as st
import pandas as pd
import numpy as np

# Configure page for wide layout
st.set_page_config(
    page_title="Simple Width Test",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simple CSS injection
st.markdown("""
<style>
.main .block-container {
    max-width: 100%;
    padding-left: 1rem;
    padding-right: 1rem;
}
</style>
""", unsafe_allow_html=True)

st.title("Simple Full Width Test")

# Create test data
data = pd.DataFrame({
    'A': np.random.randn(20),
    'B': np.random.randn(20),
    'C': np.random.randn(20),
    'D': np.random.randn(20),
    'E': np.random.randn(20),
    'F': np.random.randn(20),
    'G': np.random.randn(20),
    'H': np.random.randn(20),
    'I': np.random.randn(20),
    'J': np.random.randn(20),
})

st.subheader("Table with use_container_width=True")
st.dataframe(data, use_container_width=True)

st.subheader("Columns Test")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Metric 1", "100")
with col2:
    st.metric("Metric 2", "200")
with col3:
    st.metric("Metric 3", "300")
with col4:
    st.metric("Metric 4", "400")
with col5:
    st.metric("Metric 5", "500")

st.markdown("---")
st.markdown("**If this content spans the full width, the basic approach is working.**")
st.markdown("**If not, the issue is more fundamental with Streamlit configuration.**")
