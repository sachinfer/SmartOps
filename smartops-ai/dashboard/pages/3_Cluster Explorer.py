import streamlit as st
import pandas as pd
import requests

@st.cache_data(ttl=30)
def fetch_resource_types():
    try:
        resp = requests.get("http://localhost:8000/kubectl_resource_types", timeout=5)
        return resp.json().get("resource_types", [])
    except Exception:
        return ["pods", "services", "deployments", "nodes", "events"]

@st.cache_data(ttl=30)
def fetch_namespaces():
    try:
        url = f"http://localhost:8000/namespaces"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return resp.json().get('namespaces', [])
        else:
            return []
    except Exception as e:
        st.warning(f"Could not fetch namespaces: {e}")
        return []

st.title("🔍 Cluster Explorer")
st.write("Run safe kubectl-like queries on your cluster.")

# Fetch resource types and namespaces for autocomplete
resource_types = fetch_resource_types()
namespaces = fetch_namespaces()

# UI for resource type and namespace
resource = st.selectbox("Resource Type", resource_types, index=0)
ns = st.selectbox("Namespace", ["All"] + namespaces, index=0)
all_ns = ns == "All"
if st.button("Fetch"):
    with st.spinner("Fetching data..."):
        try:
            params = {"resource_type": resource, "all_namespaces": str(all_ns).lower()}
            resp = requests.get("http://localhost:8000/kubectl_get", params=params, timeout=15)
            items = resp.json().get("items", [])
            if not items:
                st.info("No results found.")
            else:
                df = pd.DataFrame(items)
                st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Error fetching data: {e}") 