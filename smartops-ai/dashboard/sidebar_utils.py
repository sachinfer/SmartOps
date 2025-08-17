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
    
    /* Hide the default Streamlit sidebar header */
    section[data-testid="stSidebar"] [data-testid="stSidebarHeader"] {
        display: none !important;
    }
    
    /* Alternative way to hide the header if the above doesn't work */
    section[data-testid="stSidebar"] > div:first-child > div:first-child {
        display: none !important;
    }
    
    .sidebar-section-title {
        font-size: 1.1rem;
        font-weight: bold;
        color: #fff;
        margin: 1.5rem 0 0.5rem 0;
        letter-spacing: 1px;
    }
    .sidebar-divider {
        border-top: 1px solid rgba(255,255,255,0.2);
        margin: 1.2rem 0;
    }
    .sidebar-nav-item {
        background: rgba(255,255,255,0.1);
        border-radius: 8px;
        padding: 0.8rem;
        margin: 0.3rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .sidebar-nav-item:hover {
        background: rgba(255,255,255,0.2);
        transform: translateX(5px);
    }
    .sidebar-nav-item:active {
        transform: translateX(2px);
    }
    .sidebar-nav-icon {
        margin-right: 0.5rem;
        font-size: 1.1rem;
    }
    .sidebar-nav-text {
        color: #fff;
        font-weight: 500;
        font-size: 0.95rem;
    }
    .sidebar-category {
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Navigation section
    st.markdown("<div class='sidebar-section-title'>🧭 Navigation</div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)
    
    # Pod & Cluster Management
    st.markdown("<div class='sidebar-category'>", unsafe_allow_html=True)
    st.markdown("<div style='color:#dfe6e9; font-size:0.9rem; margin-bottom:0.5rem;'>🛰️ Pod & Cluster</div>", unsafe_allow_html=True)
    
    if st.button("🛰️ Pod Explorer & Logs", key="sidebar_pod_explorer", use_container_width=True):
        st.switch_page("pages/2_Pod_Explorer_and_Logs.py")
    
    if st.button("🔍 Cluster Explorer", key="sidebar_cluster_explorer", use_container_width=True):
        st.switch_page("pages/3_Kubernetes_Shell_and_Cluster_Explorer.py")
    
    if st.button("🖥️ Kubernetes Shell", key="sidebar_k8s_shell", use_container_width=True):
        st.switch_page("pages/3_Kubernetes_Shell_and_Cluster_Explorer.py")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Operations & Control
    st.markdown("<div class='sidebar-category'>", unsafe_allow_html=True)
    st.markdown("<div style='color:#dfe6e9; font-size:0.9rem; margin-bottom:0.5rem;'>⚡ Operations</div>", unsafe_allow_html=True)
    
    if st.button("⚡ Auto Scaling Control", key="sidebar_auto_scaling", use_container_width=True):
        st.switch_page("pages/5_Auto_Scaling_Recommendations_and_Control.py")
    
    if st.button("🚀 Deployments", key="sidebar_deployments", use_container_width=True):
        st.switch_page("pages/9_Deployments.py")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # AI & Analytics
    st.markdown("<div class='sidebar-category'>", unsafe_allow_html=True)
    st.markdown("<div style='color:#dfe6e9; font-size:0.9rem; margin-bottom:0.5rem;'>🤖 AI & Analytics</div>", unsafe_allow_html=True)
    
    if st.button("🤖 AI Actions", key="sidebar_ai_actions", use_container_width=True):
        st.switch_page("pages/8_AI_Actions.py")
    
    if st.button("📋 Incident Timeline", key="sidebar_incident_timeline", use_container_width=True):
        st.switch_page("pages/6_Incident_Timeline_and_Postmortem_Report_Generator.py")
    
    st.markdown("</div>", unsafe_allow_html=True) 