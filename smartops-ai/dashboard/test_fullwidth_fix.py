import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Full Width Test",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Test the full width layout
st.title("🔧 Full Width Layout Test")
st.write("This page tests if the full-width layout is working properly across all elements.")

# Test metrics
st.subheader("📊 Metrics Test")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Test Metric 1", "100", "↑10")
with col2:
    st.metric("Test Metric 2", "200", "↓5")
with col3:
    st.metric("Test Metric 3", "300", "→0")
with col4:
    st.metric("Test Metric 4", "400", "↑20")

# Test columns
st.subheader("📋 Columns Test")
col1, col2 = st.columns(2)
with col1:
    st.info("This is column 1 - should use full width")
with col2:
    st.success("This is column 2 - should use full width")

# Test data display
st.subheader("📊 Data Display Test")
import pandas as pd
import numpy as np

# Create sample data
data = {
    'Name': ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5'],
    'Value': np.random.randint(1, 100, 5),
    'Status': ['Active', 'Inactive', 'Active', 'Pending', 'Active'],
    'Date': pd.date_range('2024-01-01', periods=5)
}

df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)

# Test charts
st.subheader("📈 Charts Test")
import plotly.express as px

fig = px.bar(df, x='Name', y='Value', title='Sample Bar Chart')
st.plotly_chart(fig, use_container_width=True)

# Test form elements
st.subheader("📝 Form Elements Test")
col1, col2 = st.columns(2)
with col1:
    st.text_input("Text Input", "Sample text")
    st.selectbox("Select Box", ["Option 1", "Option 2", "Option 3"])
with col2:
    st.text_area("Text Area", "Sample text area content")
    st.slider("Slider", 0, 100, 50)

# Test alerts and info boxes
st.subheader("ℹ️ Alerts Test")
st.info("This is an info alert - should span full width")
st.success("This is a success alert - should span full width")
st.warning("This is a warning alert - should span full width")
st.error("This is an error alert - should span full width")

# Test expandable content
st.subheader("📂 Expandable Content Test")
with st.expander("Click to expand - should use full width"):
    st.write("This content should use the full width when expanded.")
    st.dataframe(df, use_container_width=True)

# Layout verification
st.subheader("🔍 Layout Verification")
st.markdown("""
**If the layout is working correctly, you should see:**
- All elements spanning the full width of the screen
- No narrow columns or small content areas
- Charts and tables using the full available space
- Consistent spacing and alignment

**If you see small, narrow content areas, the layout fix needs adjustment.**
""")

# Footer
st.markdown("---")
st.markdown("**Full Width Layout Test Complete** - All elements should span the full width of the screen.")
