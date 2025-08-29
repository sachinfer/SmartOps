import streamlit as st

# Page config
st.set_page_config(
    page_title="Test Sidebar",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simple sidebar
st.sidebar.title("🚀 Test Sidebar")
st.sidebar.markdown("This is a test sidebar")
st.sidebar.button("Test Button")

# Main content
st.title("Test Page")
st.write("If you can see this and a sidebar on the left, the sidebar is working!")
