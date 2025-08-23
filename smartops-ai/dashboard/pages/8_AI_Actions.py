import streamlit as st
import pandas as pd
import requests

# Check if API service is running
def check_api_health():
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        return response.status_code == 200
    except Exception:
        return False

# Page config
st.set_page_config(
    page_title="AI Actions - SmartOps AI",
    page_icon="🤖",
    layout="wide"
)

# Modern CSS styling
st.markdown("""
<style>
.dashboard-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.1);
    text-align: center;
    color: white;
}
.dashboard-header h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    font-weight: 700;
}
.dashboard-header p {
    font-size: 1.1rem;
    opacity: 0.9;
    margin: 0;
}
.section-header {
    background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 10px;
    margin: 2rem 0 1rem 0;
    font-size: 1.3rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.stDataFrame {
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}
</style>
""", unsafe_allow_html=True)

# Main content
st.markdown("""
<div class="dashboard-header">
    <h1>🤖 AI Actions & Recommendations</h1>
    <p>AI-powered recommendations and action history</p>
</div>
""", unsafe_allow_html=True)

# Check if API service is running and show helpful message
if not check_api_health():

    
    # Show current cluster status based on what we know
    # Get real cluster status
    try:
        node_response = requests.get("http://localhost:8000/kubectl_get", params={"resource_type": "nodes", "all_namespaces": "true"}, timeout=5)
        pod_response = requests.get("http://localhost:8000/kubectl_get", params={"resource_type": "pods", "all_namespaces": "true"}, timeout=5)
        namespace_response = requests.get("http://localhost:8000/namespaces", timeout=5)
        service_response = requests.get("http://localhost:8000/kubectl_get", params={"resource_type": "services", "all_namespaces": "true"}, timeout=5)
        
        node_count = len(node_response.json().get("items", [])) if node_response.status_code == 200 else 0
        pod_count = len(pod_response.json().get("items", [])) if pod_response.status_code == 200 else 0
        namespace_count = len(namespace_response.json().get("namespaces", [])) if namespace_response.status_code == 200 else 0
        service_count = len(service_response.json().get("items", [])) if service_response.status_code == 200 else 0
        
        # Get actual node names
        node_names = []
        if node_response.status_code == 200:
            nodes = node_response.json().get("items", [])
            node_names = [node.get("name", "") for node in nodes if node.get("name")]
        
        node_info = f"{node_count} ({', '.join(node_names)})" if node_names else f"{node_count}"
        
        st.success(f"✅ **Current Cluster Status**:\n- **Nodes**: {node_info}\n- **Pods**: {pod_count}\n- **Namespaces**: {namespace_count}\n- **Services**: {service_count}")
    except Exception:
        st.info("ℹ️ Using fallback cluster data")
    
    st.warning("⚠️ **AI Actions**: AI-powered recommendations require the backend API service to be running.")

# AI Action History Section
st.markdown('<div class="section-header">📜 AI Action History</div>', unsafe_allow_html=True)
try:
    resp = requests.get("http://localhost:8000/ai_actions", params={"all": "true"}, timeout=5)
    actions = resp.json().get("actions", [])
except Exception:
    actions = []

if not actions:
    st.info("No AI actions in history.")
else:
    actions_df = pd.DataFrame(actions)
    if not actions_df.empty:
        actions_df = actions_df.rename(columns={
            "timestamp": "Timestamp",
            "pod_name": "Pod Name",
            "namespace": "Namespace",
            "reason": "Reason",
            "status": "Status"
        })
        # Summary counts
        status_counts = actions_df["Status"].value_counts().to_dict()
        st.markdown(f"**Completed:** {status_counts.get('completed', 0)} | **Pending:** {status_counts.get('pending', 0)} | **Failed:** {status_counts.get('failed', 0)} | **Not Found:** {status_counts.get('not_found', 0)}")
        
        # Color-code status
        def color_status(val):
            if val == "completed":
                return "background-color: #00b894; color: white;"
            elif val == "pending":
                return "background-color: #fdcb6e; color: black;"
            elif val == "failed":
                return "background-color: #e74c3c; color: white;"
            elif val == "not_found":
                return "background-color: #95a5a6; color: white;"
            else:
                return ""
        
        st.dataframe(actions_df.style.applymap(color_status, subset=['Status']), use_container_width=True)

# AI Recommendations Section
st.markdown('<div class="section-header">🎯 AI Recommendations (Pending Actions)</div>', unsafe_allow_html=True)
try:
    resp = requests.get("http://localhost:8000/ai_actions", timeout=5)
    actions = resp.json().get("actions", [])
except Exception:
    actions = []

if not actions:
    st.info("No pending AI actions.")
else:
    for action in actions:
        with st.expander(f"Pod: {action['pod_name']} | Namespace: {action['namespace']}"):
            st.write(f"**Reason:** {action['reason']}")
            st.write(f"**Timestamp:** {action['timestamp']}")
            col1, col2 = st.columns(2)
            with col1:
                confirm_btn = st.button(f"✅ Confirm Delete Pod {action['pod_name']}", key=f"confirm_{action['id']}")
            with col2:
                ignore_btn = st.button(f"🚫 Ignore", key=f"ignore_{action['id']}")
            if confirm_btn:
                with st.spinner("Deleting pod..."):
                    resp = requests.post("http://localhost:8000/confirm_ai_action", params={"action_id": action['id']})
                    if resp.status_code == 200:
                        st.success(f"Pod {action['pod_name']} deleted.")
                    else:
                        try:
                            data = resp.json()
                            if data.get("status") == "not_found":
                                st.info(data.get("error", "Pod not found."))
                                if st.button(f"🚫 Ignore (mark as ignored)", key=f"ignore_notfound_{action['id']}"):
                                    resp2 = requests.post("http://localhost:8000/ignore_ai_action", params={"action_id": action['id']})
                                    if resp2.status_code == 200:
                                        st.success("Action marked as ignored.")
                                    else:
                                        st.info(f"ℹ️ Ignore failed: {resp2.text}")
                            else:
                                st.info(f"ℹ️ Delete failed: {resp.text}")
                        except Exception:
                            st.info(f"ℹ️ Delete failed: {resp.text}")
            if ignore_btn:
                with st.spinner("Marking as ignored..."):
                    resp = requests.post("http://localhost:8000/ignore_ai_action", params={"action_id": action['id']})
                    if resp.status_code == 200:
                        st.success("Action marked as ignored.")
                    else:
                        st.info(f"ℹ️ Ignore failed: {resp.text}")

# Model Retraining Section
st.markdown('<div class="section-header">🧠 Retrain Anomaly Detection Model</div>', unsafe_allow_html=True)
if st.button("🔄 Retrain Model", key="retrain_model_btn"):
    with st.spinner("Retraining model... this may take a minute..."):
        try:
            resp = requests.post("http://localhost:8000/retrain_model", timeout=60)
            if resp.status_code == 200:
                st.success("Model retrained and deployed!")
            else:
                st.info(f"ℹ️ Retrain failed: {resp.text}")
        except Exception:
            st.info("ℹ️ Retrain error occurred") 