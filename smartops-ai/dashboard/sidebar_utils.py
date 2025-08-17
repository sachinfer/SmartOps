import streamlit as st

def show_sidebar():
    # ---------- Hide everything except the sidebar ----------
    st.markdown(
        """
        <style>
        /* Hide main content + default chrome */
        .block-container { display: none !important; }
        #MainMenu, header, footer { visibility: hidden; }

        /* Sidebar sizing */
        section[data-testid="stSidebar"]{
            min-width: 320px !important;
            width: 320px !important;
        }

        /* ---------- Sidebar look (matches screenshot) ---------- */
        section[data-testid="stSidebar"] > div:first-child{
            background: linear-gradient(180deg,#6b6eea 0%, #8356b1 55%, #7a59b5 100%);
            height: 100vh;
            padding: 1.2rem 1rem 2rem 1rem;
            border-top-right-radius: 20px;
            border-bottom-right-radius: 20px;
            box-shadow: 2px 0 16px rgba(102,126,234,0.10);
        }

        /* hide default sidebar header space */
        section[data-testid="stSidebar"] [data-testid="stSidebarHeader"],
        section[data-testid="stSidebar"] > div:first-child > div:first-child{
            display:none !important;
        }

        /* Titles, labels, dividers */
        .sb-title{
            font-size: 1.1rem; font-weight: 700; color: #ffffff; letter-spacing: .6px;
            margin: .3rem 0 .2rem 0; display:flex; align-items:center; gap:.5rem;
        }
        .sb-sub{
            color:#dfe6e9; font-size:.9rem; margin:.7rem 0 .5rem 0; display:flex; align-items:center; gap:.45rem;
            opacity:.95;
        }
        .sb-divider{
            border-top: 1px solid rgba(255,255,255,.25);
            margin: 1.1rem 0 1.1rem 0;
        }
        .sb-section{ margin: .3rem 0 1rem 0; }

        /* Pill buttons (exact feel) */
        .stButton > button {
            width: 100% !important;
            text-align: left !important;
            font-weight: 600 !important;
            color: #ffffff !important;
            background: rgba(0,0,0,.28) !important;
            border: 1px solid rgba(255,255,255,.18) !important;
            border-radius: 10px !important;
            padding: .65rem .9rem !important;
            line-height: 1.1rem !important;
            box-shadow: inset 0 1px 0 rgba(255,255,255,.06);
        }
        .stButton > button:hover{
            background: rgba(255,255,255,.22) !important;
            transform: translateX(5px);
            transition: all .18s ease;
        }
        .stButton > button:active{
            transform: translateX(2px);
        }

        /* Make emojis align nicely inside buttons */
        .stButton > button p { margin: 0; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ---------- Sidebar content ----------
    st.markdown(
        """
        <div style="text-align:center; margin: .2rem 0 1.2rem 0;">
            <div style="font-size:2.2rem;">🚀</div>
            <div style="font-size:1.35rem; font-weight:800; color:#fff; letter-spacing:.6px;">SmartOps</div>
            <div style="font-size:.92rem; color:#dfe6e9; opacity:.95;">AI Kubernetes Platform</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="sb-title">🧭 Navigation</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

    # ---- Core Monitoring
    st.markdown('<div class="sb-section">', unsafe_allow_html=True)
    st.markdown('<div class="sb-sub">📊 Core Monitoring</div>', unsafe_allow_html=True)
    if st.button("🟩  Overview Dashboard", key="nav_overview", use_container_width=True):
        st.switch_page("pages/1_Overview.py")
    if st.button("🔥  Anomaly Detection", key="nav_anomaly", use_container_width=True):
        st.switch_page("pages/4_Anomaly_Detection.py")
    st.markdown('</div>', unsafe_allow_html=True)

    # ---- Pod & Cluster
    st.markdown('<div class="sb-section">', unsafe_allow_html=True)
    st.markdown('<div class="sb-sub">🛰️ Pod & Cluster</div>', unsafe_allow_html=True)
    if st.button("🧭  Pod Explorer & Logs", key="nav_pod", use_container_width=True):
        st.switch_page("pages/2_Pod_Explorer_and_Logs.py")
    if st.button("🔍  Cluster Explorer", key="nav_cluster", use_container_width=True):
        st.switch_page("pages/3_Kubernetes_Shell_and_Cluster_Explorer.py")
    if st.button("🖥️  Kubernetes Shell", key="nav_shell", use_container_width=True):
        st.switch_page("pages/3_Kubernetes_Shell_and_Cluster_Explorer.py")
    st.markdown('</div>', unsafe_allow_html=True)

    # ---- Operations
    st.markdown('<div class="sb-section">', unsafe_allow_html=True)
    st.markdown('<div class="sb-sub">⚡ Operations</div>', unsafe_allow_html=True)
    if st.button("⚡  Auto Scaling Control", key="nav_scale", use_container_width=True):
        st.switch_page("pages/5_Auto_Scaling_Recommendations_and_Control.py")
    if st.button("🚀  Deployments", key="nav_deploy", use_container_width=True):
        st.switch_page("pages/9_Deployments.py")
    st.markdown('</div>', unsafe_allow_html=True)

    # ---- AI & Analytics
    st.markdown('<div class="sb-section">', unsafe_allow_html=True)
    st.markdown('<div class="sb-sub">🤖 AI & Analytics</div>', unsafe_allow_html=True)
    if st.button("🤖  AI Actions", key="nav_actions", use_container_width=True):
        st.switch_page("pages/8_AI_Actions.py")
    if st.button("📝  Incident Timeline", key="nav_incident", use_container_width=True):
        st.switch_page("pages/6_Incident_Timeline_and_Postmortem_Report_Generator.py")
    st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-title">🤖 AI Controls</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        "<div style='color:#dfe6e9; font-size:.84rem; text-align:center; opacity:.95;'>SmartOps v1.0<br/>© 2024 Your Company</div>",
        unsafe_allow_html=True
    )

# Run
show_sidebar()
