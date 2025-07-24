import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import requests
from sidebar_utils import show_sidebar

with st.sidebar:
    show_sidebar()

st.title("🔗 Service Dependency Map (Real-Time)")
st.write("""
Automatically visualize service-to-service communication using Kubernetes network flows or service mesh (e.g., Istio, Linkerd).

This dynamic dependency graph helps identify cascading failures or bottlenecks in your cluster.
""")

API_URL = "http://localhost:8000"  # Change if your backend is hosted elsewhere

def fetch_service_edges():
    try:
        resp = requests.get(f"{API_URL}/service_dependencies", timeout=10)
        if resp.status_code == 200:
            return resp.json().get("edges", [])
        else:
            st.error(f"Failed to fetch service dependencies: {resp.text}")
            return []
    except Exception as e:
        st.warning(f"Falling back to simulated data. Error: {e}")
        # Simulated fallback
        return [
            ("frontend", "backend"),
            ("backend", "database"),
            ("frontend", "auth"),
            ("auth", "database"),
            ("worker", "database"),
            ("worker", "cache"),
            ("frontend", "worker"),
        ]

service_edges = fetch_service_edges()
services = set([s for s, _ in service_edges] + [t for _, t in service_edges])

# Build the graph
g = nx.DiGraph()
g.add_edges_from(service_edges)

# Draw the graph (static fallback)
st.markdown("### Service Dependency Graph (Static)")
fig, ax = plt.subplots(figsize=(6, 4))
pos = nx.spring_layout(g, seed=42)
nx.draw(g, pos, with_labels=True, node_color="#667eea", edge_color="#764ba2", node_size=2000, font_size=12, font_color="white", arrowsize=20, ax=ax)
st.pyplot(fig)

# Optionally, use pyvis for interactive visualization if available
try:
    from pyvis.network import Network
    import streamlit.components.v1 as components
    net = Network(height="500px", width="100%", directed=True)
    for node in services:
        net.add_node(node, label=node)
    for src, dst in service_edges:
        net.add_edge(src, dst)
    net.repulsion(node_distance=200, central_gravity=0.33, spring_length=100, spring_strength=0.10, damping=0.95)
    net.show_buttons(filter_=['physics'])
    net.save_graph("service_dep_map.html")
    st.markdown("### Interactive Dependency Graph (Pyvis)")
    with open("service_dep_map.html", "r", encoding="utf-8") as f:
        html = f.read()
    components.html(html, height=550, scrolling=True)
except Exception as e:
    st.info("Install pyvis for interactive visualization: pip install pyvis")

st.markdown("---")
st.markdown("**Why:** This map helps you quickly spot cascading failures, bottlenecks, and critical dependencies in your microservices architecture.") 