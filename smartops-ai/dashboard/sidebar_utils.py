import streamlit as st

def show_sidebar():
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        height: 100vh;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        border-top-right-radius: 20px;
        border-bottom-right-radius: 20px;
        box-shadow: 2px 0 16px rgba(102,126,234,0.08);
    }
    .sidebar-section-title {
        font-size: 1.1rem;
        font-weight: bold;
        color: #fff;
        margin: 1.5rem 0 0.5rem 0;
        letter-spacing: 1px;
    }
    .sidebar-divider {
        border-top: 1px solid #dfe6e9;
        margin: 1.2rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Logo and project
    st.markdown("""
    <div class='sidebar-logo' style='text-align:center; margin-bottom:1.5rem;'>
        <span style='font-size:2.2rem;'>🚀</span>
        <span class='project' style='font-size:1.3rem;font-weight:bold;color:#fff;letter-spacing:1px;display:block;'>SmartOps</span>
        <div class='subtitle' style='font-size:0.9rem;color:#dfe6e9;'>AI Kubernetes Platform</div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation section (Streamlit handles the links)
    st.markdown("<div class='sidebar-section-title'>🧭 Navigation</div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)

    # AI Controls section (these are your custom controls)
    st.markdown("<div class='sidebar-section-title'>🤖 AI Controls</div>", unsafe_allow_html=True)

    # The following will be rendered by your main/page code:
    # - AI Recommendations (Pending Actions)
    # - Retrain Anomaly Detection Model

    # Optional: Add a footer or version
    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)
    st.markdown("<div style='color:#dfe6e9; font-size:0.85rem; text-align:center;'>SmartOps v1.0<br/>© 2024 Your Company</div>", unsafe_allow_html=True) 