import streamlit as st

# ---- Page config ----
st.set_page_config(
    page_title="SmartOps",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

def show_sidebar_only():
    # ---- Hide everything except the sidebar ----
    st.markdown(
        """
        <style>
        /* Hide Streamlit main content area */
        .block-container { display: none !important; }

        /* Hide Streamlit default menu, header & footer */
        #MainMenu { visibility: hidden; }
        header { visibility: hidden; }
        footer { visibility: hidden; }

        /* Make the sidebar fill the height nicely */
        section[data-testid="stSidebar"] {
            min-width: 320px;
            width: 320px;
        }

        /* --- Your Sidebar Styling --- */
        section[data-testid="stSidebar"] > div:first-child {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            border-top-right-radius: 20px;
            border-bottom-right-radius: 20px;
            box-shadow: 2px 0 16px rgba(102,126,234,0.08);
        }

        /* Hide default Streamlit sidebar header */
        section[data-testid="stSidebar"] [data-testid="stSidebarHeader"] { display: none !important; }
        section[data-testid="stSidebar"] > div:first-child > div:first-child { display: none !important; }

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
        .sidebar-category { margin: 1rem 0; }

        /* Optional: make Streamlit buttons look like pill nav items */
        button[kind="secondary"] {
            background: rgba(255,255,255,0.1) !important;
            border: 1px solid rgba(255,255,255,0.12) !important;
            border-radius: 10px !important;
            color: #fff !important;
            padding: 0.6rem 0.9rem !important;
        }
        button[kind="secondary"]:hover {
            background: rgba(255,255,255,0.2) !important;
            transform: translateX(5px);
            transition: all .2s ease;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ---- Sidebar content ----
    st.markdown(
        """
        <div class='sidebar-logo' style='text-align:center; margin-bottom:1.5rem;'>
            <span style='font-size:2.2rem;'>🚀</span>
            <span class='project' style='font-size:1.3rem;font-weight:bold;color:#fff;letter-spacing:1px;display:block;'>SmartOps</span>
            <div class='subtitle' style='font-size:0.9rem;color:#dfe6e9;'>AI Kubernetes Platform</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='sidebar-section-title'>🧭 Navigation</div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)

    # --- Core Monitoring ---
    st.markdown("<div class='sidebar-category'>", unsafe_allow_html=True)
    st.markdown("<div style='color:#dfe6e9; font-size:0.9rem; margin-bottom:0.5rem;'>📊 Core Monitoring</div>", unsafe_allow_html=True)
    if st.button("📊 Overview Dashboard", key="sidebar_overview", use_container_width=True):
        st.switch_page("pages/1_Overview.py")
    if st.button("🔥 Anomaly Detection", key="sidebar_anomaly", use_container_width=True):
        st.switch_page("pages/4_Anomaly_Detection.py")
    st.markdown("</div>", unsafe_allow_html=True)

    # --- Pod & Cluster ---
    st.markdown("<div class='sidebar-category'>", unsafe_allow_html=True)
    st.markdown("<div style='color:#dfe6e9; font-size:0.9rem; margin-bottom:0.5rem;'>🛰️ Pod & Cluster</div>", unsafe_allow_html=True)
    if st.button("🛰️ Pod Explorer & Logs", key="sidebar_pod_explorer", use_container_width=True):
        st.switch_page("pages/2_Pod_Explorer_and_Logs.py")
    if st.button("🔍 Cluster Explorer", key="sidebar_cluster_explorer", use_container_width=True):
        st.switch_page("pages/3_Kubernetes_Shell_and_Cluster_Explorer.py")
    if st.button("💻 Kubernetes Shell", key="sidebar_k8s_shell", use_container_width=True):
        st.switch_page("pages/3_Kubernetes_Shell_and_Cluster_Explorer.py")
    st.markdown("</div>", unsafe_allow_html=True)

    # --- Operations ---
    st.markdown("<div class='sidebar-category'>", unsafe_allow_html=True)
    st.markdown("<div style='color:#dfe6e9; font-size:0.9rem; margin-bottom:0.5rem;'>⚡ Operations</div>", unsafe_allow_html=True)
    if st.button("⚡ Auto Scaling Control", key="sidebar_auto_scaling", use_container_width=True):
        st.switch_page("pages/5_Auto_Scaling_Recommendations_and_Control.py")
    if st.button("🚀 Deployments", key="sidebar_deployments", use_container_width=True):
        st.switch_page("pages/9_Deployments.py")
    st.markdown("</div>", unsafe_allow_html=True)

    # --- AI & Analytics ---
    st.markdown("<div class='sidebar-category'>", unsafe_allow_html=True)
    st.markdown("<div style='color:#dfe6e9; font-size:0.9rem; margin-bottom:0.5rem;'>🤖 AI & Analytics</div>", unsafe_allow_html=True)
    if st.button("🤖 AI Actions", key="sidebar_ai_actions", use_container_width=True):
        st.switch_page("pages/8_AI_Actions.py")
    if st.button("📄 Incident Timeline", key="sidebar_incident_timeline", use_container_width=True):
        st.switch_page("pages/6_Incident_Timeline_and_Postmortem_Report_Generator.py")
    st.markdown("</div>", unsafe_allow_html=True)

    # --- Footer ---
    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-section-title'>🤖 AI Controls</div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)
    st.markdown("<div style='color:#dfe6e9; font-size:0.85rem; text-align:center;'>SmartOps v1.0<br/>© 2024 Your Company</div>", unsafe_allow_html=True)

# Run the sidebar-only view
show_sidebar_only()
