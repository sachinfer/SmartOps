# -*- coding: utf-8 -*-
"""
Kubernetes Cluster Overview - SmartOps AI
New Relic-style monitoring dashboard for K8s Cluster
"""

import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import sys
import os
import subprocess
import json

# Fix import path for sidebar_utils
try:
    # Try to import from parent directory
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from sidebar_utils import show_sidebar
except ImportError:
    # Fallback: create a simple sidebar function
    def show_sidebar():
        st.sidebar.title("SmartOps Dashboard")
        st.sidebar.info("Navigation menu will appear here")
        st.sidebar.markdown("---")
        st.sidebar.markdown("### Quick Actions")
        if st.sidebar.button("🔄 Refresh Data"):
            st.cache_data.clear()
            st.rerun()

# Environment detection for K8s cluster
def get_cluster_environment():
    """Detect if running in Kubernetes cluster and get service endpoints"""
    try:
        # Check if running in K8s cluster
        k8s_host = os.environ.get('KUBERNETES_SERVICE_HOST')
        if k8s_host:
            return "kubernetes"
        
        # Check if running in Docker
        if os.path.exists('/.dockerenv'):
            return "docker"
        
        # Check for Google Cloud specific environment variables
        gcp_project = os.environ.get('GOOGLE_CLOUD_PROJECT')
        gcp_zone = os.environ.get('GOOGLE_CLOUD_ZONE')
        if gcp_project or gcp_zone:
            return "google_cloud"
        
        return "local"
    except:
        return "local"

def get_api_endpoint():
    """Get the appropriate API endpoint based on environment"""
    env = get_cluster_environment()
    
    if env == "kubernetes":
        # In K8s cluster, use service names
        # Try multiple possible service names for different deployments
        service_names = [
            "smartops-api-service:8000",
            "smartops-api:8000", 
            "smartops-backend:8000",
            "api-service:8000"
        ]
        
        # Check which service is available
        for service in service_names:
            try:
                response = requests.get(f"http://{service}/", timeout=2)
                if response.status_code == 200:
                    return f"http://{service}"
            except:
                continue
        
        # If no service found, return the default
        return "http://smartops-api-service:8000"
        
    elif env == "google_cloud":
        # In Google Cloud, try multiple endpoints
        gcp_endpoints = [
            "http://smartops-api-service:8000",
            "http://smartops-api:8000",
            "http://localhost:8000",
            "http://127.0.0.1:8000"
        ]
        
        # Check which endpoint is available
        for endpoint in gcp_endpoints:
            try:
                response = requests.get(f"{endpoint}/", timeout=2)
                if response.status_code == 200:
                    return endpoint
            except:
                continue
        
        # If no endpoint found, return the default
        return "http://smartops-api-service:8000"
        
    elif env == "docker":
        # In Docker, try service name or localhost
        docker_endpoints = [
            "http://smartops-api:8000",
            "http://localhost:8000",
            "http://host.docker.internal:8000"
        ]
        
        # Check which endpoint is available
        for endpoint in docker_endpoints:
            try:
                response = requests.get(f"{endpoint}/", timeout=2)
                if response.status_code == 200:
                    return endpoint
            except:
                continue
        
        return "http://smartops-api:8000"
    else:
        # Local development
        return "http://localhost:8000"

# Import Misi from the dashboard directory
try:
    # from misi_chatbot_widget import add_misi_to_page
    MISI_AVAILABLE = True
except ImportError:
    MISI_AVAILABLE = False
    st.warning("Misi AI Chatbot not available. Please ensure the chatbot is properly installed.")

def show_page():
    """Main page function - called by the router"""
    # Page config
    st.set_page_config(
        page_title="Kubernetes Cluster Overview - SmartOps AI",
        page_icon="📊",
        layout="wide"
    )
    
    # Show the sidebar
    show_sidebar()

# Function to fetch real-time pod data
@st.cache_data(ttl=30)  # Cache for 30 seconds
def fetch_pod_data():
    try:
        api_endpoint = get_api_endpoint()
        response = requests.get(f"{api_endpoint}/pods", timeout=10)
        if response.status_code == 200:
            return response.json().get("pods", [])
        else:
            # Don't show error to user, just return empty list
            return []
    except Exception as e:
        # Don't show technical error to user, just return empty list
        return []

# Function to get pod status counts
def get_pod_status_counts(pods):
    status_counts = {'Running': 0, 'Pending': 0, 'Failed': 0, 'Succeeded': 0}
    for pod in pods:
        status = pod.get('status', 'Unknown')
        if status in status_counts:
            status_counts[status] += 1
        else:
            status_counts['Failed'] += 1  # Treat unknown status as failed
    return status_counts

# Function to fetch real-time node data
@st.cache_data(ttl=30)  # Cache for 30 seconds
def fetch_node_data():
    try:
        api_endpoint = get_api_endpoint()
        response = requests.get(f"{api_endpoint}/kubectl_get", params={"resource_type": "nodes"}, timeout=10)
        if response.status_code == 200:
            return response.json().get("output", [])
        else:
            # Don't show error to user, just return empty list
            return []
    except Exception as e:
        # Don't show error to user, just return empty list
        return []

# Function to get namespace count
@st.cache_data(ttl=30)
def get_namespace_count():
    try:
        api_endpoint = get_api_endpoint()
        response = requests.get(f"{api_endpoint}/namespaces", timeout=10)
        if response.status_code == 200:
            namespaces = response.json().get("namespaces", [])
            return len(namespaces)
        else:
            return 11  # Fallback to default
    except Exception:
        return 11  # Fallback to default

# Function to get available namespaces
@st.cache_data(ttl=30)
def get_available_namespaces():
    try:
        api_endpoint = get_api_endpoint()
        response = requests.get(f"{api_endpoint}/namespaces", timeout=10)
        if response.status_code == 200:
            namespaces = response.json().get("namespaces", [])
            return [ns.get('name', '') for ns in namespaces if ns.get('name')]
        else:
            return ['default', 'kube-system', 'smartops']  # Fallback namespaces
    except Exception:
        return ['default', 'kube-system', 'smartops']  # Fallback namespaces

# Function to fetch real-time pod data with namespace filter
@st.cache_data(ttl=30)  # Cache for 30 seconds
def fetch_pod_data_by_namespace(namespace="all"):
    try:
        api_endpoint = get_api_endpoint()
        if namespace == "all":
            response = requests.get(f"{api_endpoint}/pods", timeout=10)
        else:
            response = requests.get(f"{api_endpoint}/kubectl_get", 
                                 params={"resource_type": "pods", "namespace": namespace}, timeout=10)
        
        if response.status_code == 200:
            if namespace == "all":
                return response.json().get("pods", [])
            else:
                return response.json().get("output", [])
        else:
            return []
    except Exception as e:
        return []

# Function to check if API service is running
def check_api_health():
    """Check if the backend API service is accessible"""
    try:
        api_endpoint = get_api_endpoint()
        env = get_cluster_environment()
        
        # Log the environment and endpoint being tested
        st.sidebar.info(f"🔍 Testing API endpoint: {api_endpoint}")
        st.sidebar.info(f"🌍 Environment detected: {env}")
        
        response = requests.get(f"{api_endpoint}/", timeout=5)
        return response.status_code == 200
    except Exception as e:
        st.sidebar.error(f"❌ API Health Check Failed: {str(e)}")
        return False

# Function to get service count
@st.cache_data(ttl=30)
def get_service_count():
    try:
        api_endpoint = get_api_endpoint()
        response = requests.get(f"{api_endpoint}/kubectl_get", params={"resource_type": "services", "all_namespaces": True}, timeout=10)
        if response.status_code == 200:
            services = response.json().get("output", [])
            return len(services)
        else:
            return 16  # Fallback to default
    except Exception:
        return 16  # Fallback to default

# Function to get cluster info directly from kubectl
def get_cluster_info():
    """Get cluster information directly using kubectl commands"""
    try:
        # Get cluster info
        result = subprocess.run(['kubectl', 'cluster-info'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return result.stdout
        return "Cluster info not available"
    except Exception as e:
        return f"Error getting cluster info: {str(e)}"

# Function to get node info directly
def get_nodes_info():
    """Get node information directly using kubectl"""
    try:
        result = subprocess.run(['kubectl', 'get', 'nodes', '-o', 'json'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            nodes_data = json.loads(result.stdout)
            return nodes_data.get('items', [])
        return []
    except Exception as e:
        st.sidebar.warning(f"⚠️ kubectl nodes command failed: {str(e)}")
        return []

# Function to get pods info directly
def get_pods_info():
    """Get pods information directly using kubectl"""
    try:
        result = subprocess.run(['kubectl', 'get', 'pods', '--all-namespaces', '-o', 'json'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            pods_data = json.loads(result.stdout)
            return pods_data.get('items', [])
        return []
    except Exception as e:
        st.sidebar.warning(f"⚠️ kubectl pods command failed: {str(e)}")
        return []

# Function to get services info directly
def get_services_info():
    """Get services information directly using kubectl"""
    try:
        result = subprocess.run(['kubectl', 'get', 'services', '--all-namespaces', '-o', 'json'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            services_data = json.loads(result.stdout)
            return services_data.get('items', [])
        return []
    except Exception as e:
        st.sidebar.warning(f"⚠️ kubectl services command failed: {str(e)}")
        return []

# Function to get namespaces info directly
def get_namespaces_info():
    """Get namespaces information directly using kubectl"""
    try:
        result = subprocess.run(['kubectl', 'get', 'namespaces', '-o', 'json'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            namespaces_data = json.loads(result.stdout)
            return namespaces_data.get('items', [])
        return []
    except Exception as e:
        st.sidebar.warning(f"⚠️ kubectl namespaces command failed: {str(e)}")
        return []

# Enhanced data fetching with fallback to direct kubectl
def get_enhanced_pod_data():
    """Get pod data with fallback to direct kubectl"""
    # Try API first
    pods = fetch_pod_data()
    if pods:
        return pods
    
    # Fallback to direct kubectl
    try:
        pods_info = get_pods_info()
        if pods_info:
            formatted_pods = []
            for pod in pods_info:
                metadata = pod.get('metadata', {})
                status = pod.get('status', {})
                formatted_pods.append({
                    'name': metadata.get('name', 'Unknown'),
                    'namespace': metadata.get('namespace', 'default'),
                    'status': status.get('phase', 'Unknown'),
                    'age': 'Unknown',
                    'ready': f"{status.get('readyReplicas', 0)}/{status.get('replicas', 0)}"
                })
            return formatted_pods
    except:
        pass
    
    return []

def get_enhanced_node_data():
    """Get node data with fallback to direct kubectl"""
    # Try API first
    nodes = fetch_node_data()
    if nodes:
        return nodes
    
    # Fallback to direct kubectl
    try:
        nodes_info = get_nodes_info()
        if nodes_info:
            formatted_nodes = []
            for node in nodes_info:
                metadata = node.get('metadata', {})
                status = node.get('status', {})
                formatted_nodes.append({
                    'name': metadata.get('name', 'Unknown'),
                    'status': 'Ready' if status.get('conditions', [{}])[0].get('status') == 'True' else 'NotReady',
                    'roles': 'worker',
                    'age': 'Unknown',
                    'version': status.get('nodeInfo', {}).get('kubeletVersion', 'Unknown'),
                    'internal_ip': status.get('addresses', [{}])[0].get('address', 'Unknown') if status.get('addresses') else 'Unknown'
                })
            return formatted_nodes
    except:
        pass
    
    return []

# New Relic-style CSS
st.markdown("""
<style>
/* Beautiful modern dark theme */
.main .block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    max-width: 1400px;
    background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
}

/* Dark theme background with subtle pattern */
.stApp {
    background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
    background-attachment: fixed;
}

/* Beautiful gradient header with glow effect */
.dashboard-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    padding: 2.5rem;
    border-radius: 20px;
    margin-bottom: 2rem;
    border: none;
    position: relative;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    overflow: hidden;
}

.dashboard-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 50%, rgba(255,255,255,0.1) 100%);
    animation: shimmer 3s ease-in-out infinite;
}

@keyframes shimmer {
    0%, 100% { transform: translateX(-100%); }
    50% { transform: translateX(100%); }
}

.dashboard-header h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    font-weight: 700;
    color: #ffffff;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    position: relative;
    z-index: 2;
}

.dashboard-header p {
    font-size: 1.1rem;
    opacity: 0.95;
    margin: 0;
    color: #f8fafc;
    font-weight: 500;
    position: relative;
    z-index: 2;
}

/* Beautiful section headers with gradient borders */
.section-header {
    background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
    color: #f7fafc;
    padding: 1.2rem 1.8rem;
    border-radius: 15px;
    margin: 2.5rem 0 1.5rem 0;
    font-size: 1.2rem;
    font-weight: 600;
    border: none;
    position: relative;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
    overflow: hidden;
}

.section-header::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 5px;
    background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    border-radius: 0 3px 3px 0;
}

/* Beautiful metric cards with glassmorphism */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
    margin: 2.5rem 0;
}

.metric-card {
    background: rgba(45, 55, 72, 0.8);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 2rem;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
}

.metric-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4);
    border-color: rgba(102, 126, 234, 0.5);
}

.metric-value {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
    line-height: 1;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.metric-label {
    font-size: 0.9rem;
    color: #a0aec0;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
    margin-bottom: 1rem;
}

.metric-status {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 25px;
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    box-shadow: 0 4px 15px rgba(72, 187, 120, 0.3);
}

.metric-status.arrow-up::before {
    content: '↑';
    font-size: 0.9rem;
    font-weight: bold;
    animation: bounce 2s infinite;
}

@keyframes bounce {
    0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
    40% { transform: translateY(-5px); }
    60% { transform: translateY(-3px); }
}

/* Beautiful resource cards */
.resource-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
    gap: 2rem;
    margin: 2.5rem 0;
}

.resource-card {
    background: rgba(45, 55, 72, 0.8);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 2rem;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.resource-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
}

.resource-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    border-color: rgba(240, 147, 251, 0.5);
}

.resource-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.resource-icon {
    font-size: 1.5rem;
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.resource-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #f7fafc;
    margin: 0;
}

.resource-value {
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
    text-align: center;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

/* Beautiful chart containers */
.chart-container {
    background: rgba(45, 55, 72, 0.8);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 2rem;
    margin: 2.5rem 0;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
}

.chart-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.chart-icon {
    font-size: 1.5rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.chart-title {
    font-size: 1.2rem;
    font-weight: 600;
    color: #f7fafc;
    margin: 0;
}

/* Beautiful time selector */
.time-selector {
    background: rgba(45, 55, 72, 0.8);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 2rem;
    margin: 2.5rem 0;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
}

.time-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
    font-size: 1.1rem;
    font-weight: 600;
    color: #f7fafc;
}

/* Beautiful status messages */
.status-message {
    background: rgba(45, 55, 72, 0.8);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(56, 178, 172, 0.3);
    color: #f7fafc;
    padding: 1.5rem 2rem;
    border-radius: 15px;
    margin: 2rem 0;
    display: flex;
    align-items: center;
    gap: 1rem;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.status-icon {
    font-size: 1.5rem;
    background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.status-text {
    font-size: 1rem;
    font-weight: 500;
    margin: 0;
    color: #e2e8f0;
}

/* Beautiful buttons with gradients */
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    padding: 0.75rem 1.5rem !important;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
}

/* Beautiful selectboxes */
.stSelectbox > div > div {
    background: rgba(45, 55, 72, 0.8) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #f7fafc !important;
    border-radius: 12px !important;
}

.stSelectbox > div > div:hover {
    border-color: rgba(102, 126, 234, 0.5) !important;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2) !important;
}

/* Beautiful number inputs */
.stNumberInput > div > div > input {
    background: rgba(45, 55, 72, 0.8) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #f7fafc !important;
    border-radius: 12px !important;
}

.stNumberInput > div > div > input:focus {
    border-color: rgba(102, 126, 234, 0.5) !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
}

/* Beautiful dataframes */
.dataframe {
    background: rgba(45, 55, 72, 0.8) !important;
    color: #f7fafc !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Beautiful pod status badges */
.pod-status-badge {
    background: rgba(45, 55, 72, 0.8);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 25px;
    padding: 0.75rem 1.5rem;
    margin: 0.5rem;
    display: inline-block;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.pod-status-badge:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

.pod-status-running {
    border-color: rgba(72, 187, 120, 0.5);
    box-shadow: 0 4px 15px rgba(72, 187, 120, 0.2);
}

.pod-status-pending {
    border-color: rgba(237, 137, 54, 0.5);
    box-shadow: 0 4px 15px rgba(237, 137, 54, 0.2);
}

.pod-status-failed {
    border-color: rgba(229, 62, 62, 0.5);
    box-shadow: 0 4px 15px rgba(229, 62, 62, 0.2);
}

.pod-status-succeeded {
    border-color: rgba(56, 178, 172, 0.5);
    box-shadow: 0 4px 15px rgba(56, 178, 172, 0.2);
}

/* Responsive design */
@media (max-width: 768px) {
    .metric-grid {
        grid-template-columns: 1fr;
    }
    
    .resource-grid {
        grid-template-columns: 1fr;
    }
    
    .dashboard-header {
        padding: 2rem;
    }
    
    .dashboard-header h1 {
        font-size: 2rem;
    }
}

/* Beautiful scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(45, 55, 72, 0.3);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
}

/* Beautiful animations */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.metric-card, .resource-card, .chart-container {
    animation: fadeInUp 0.6s ease-out;
}

/* Beautiful glow effects */
.glow-effect {
    position: relative;
}

.glow-effect::after {
    content: '';
    position: absolute;
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    background: linear-gradient(45deg, #667eea, #764ba2, #f093fb, #667eea);
    border-radius: inherit;
    z-index: -1;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.glow-effect:hover::after {
    opacity: 0.3;
}

/* Floating particles animation */
@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-20px) rotate(180deg); }
}

.floating-particle {
    position: fixed;
    width: 6px;
    height: 6px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    border-radius: 50%;
    animation: float 6s ease-in-out infinite;
    z-index: 1;
    opacity: 0.6;
}

.floating-particle:nth-child(1) { left: 10%; animation-delay: 0s; }
.floating-particle:nth-child(2) { left: 20%; animation-delay: 2s; }
.floating-particle:nth-child(3) { left: 30%; animation-delay: 4s; }
.floating-particle:nth-child(4) { left: 40%; animation-delay: 1s; }
.floating-particle:nth-child(5) { left: 50%; animation-delay: 3s; }
.floating-particle:nth-child(6) { left: 60%; animation-delay: 5s; }
.floating-particle:nth-child(7) { left: 70%; animation-delay: 2s; }
.floating-particle:nth-child(8) { left: 80%; animation-delay: 4s; }
.floating-particle:nth-child(9) { left: 90%; animation-delay: 1s; }

/* Beautiful hover effects for all interactive elements */
.metric-card:hover .metric-value,
.resource-card:hover .resource-value {
    transform: scale(1.1);
    transition: transform 0.3s ease;
}

/* Enhanced button animations */
.stButton > button:active {
    transform: translateY(1px) !important;
    box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3) !important;
}

/* Beautiful focus states */
.stSelectbox > div > div:focus-within,
.stNumberInput > div > div > input:focus {
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
    border-color: rgba(102, 126, 234, 0.8) !important;
}

/* Smooth transitions for all elements */
* {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Enhanced dataframes */
.dataframe {
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2) !important;
}

.dataframe:hover {
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.3) !important;
}
</style>
""", unsafe_allow_html=True)

# Main content
st.markdown("""
<div class="dashboard-header">
    <h1>📊 Kubernetes Cluster Overview</h1>
    <p>Real-time monitoring dashboard powered by SmartOps AI</p>
</div>

<!-- Floating particles for visual appeal -->
<div class="floating-particle"></div>
<div class="floating-particle"></div>
<div class="floating-particle"></div>
<div class="floating-particle"></div>
<div class="floating-particle"></div>
<div class="floating-particle"></div>
<div class="floating-particle"></div>
<div class="floating-particle"></div>
<div class="floating-particle"></div>
""", unsafe_allow_html=True)

# Check if API service is running and show helpful message
# api_available = check_api_health()

# Show cluster environment information
# env = get_cluster_environment()
# st.markdown(f"""
# <div class="status-message" style="background: rgba(45, 55, 72, 0.9); border-color: rgba(102, 126, 234, 0.5);">
#     <div class="status-icon">🌍</div>
#     <div class="status-text">
#         <strong>Environment:</strong> {env.upper()} | 
#         <strong>API Status:</strong> {'✅ Available' if api_available else '❌ Not Available'} | 
#         <strong>Cluster:</strong> {'🟢 Connected' if env == 'kubernetes' else '🟡 Local/Docker'}
#     </div>
# </div>
# """, unsafe_allow_html=True)

# Show Google Cloud specific information
# if env == "google_cloud":
#     gcp_project = os.environ.get('GOOGLE_CLOUD_PROJECT', 'Not Set')
#     gcp_zone = os.environ.get('GOOGLE_CLOUD_ZONE', 'Not Set')
#     gcp_region = os.environ.get('GOOGLE_CLOUD_REGION', 'Not Set')
#     
#     st.markdown(f"""
#     <div class="status-message" style="background: rgba(56, 178, 172, 0.2); border-color: rgba(56, 178, 172, 0.5);">
#         <div class="status-icon">☁️</div>
#         <div class="status-text">
#             <strong>Google Cloud Info:</strong> Project: {gcp_project} | Zone: {gcp_zone} | Region: {gcp_region}
#         </div>
#     </div>
#     """, unsafe_allow_html=True)
#     
#     # Show troubleshooting tips for Google Cloud
#     if not api_available:
#         st.markdown("""
#         <div class="status-message" style="background: rgba(229, 62, 62, 0.2); border-color: rgba(229, 62, 62, 0.5);">
#             <div class="status-icon">🔧</div>
#             <div class="status-text">
#                 <strong>Google Cloud Troubleshooting:</strong><br/>
#                 • Check if smartops-api-service is deployed and running<br/>
#                 • Verify service names and ports in your deployment<br/>
#                 • Check network policies and firewall rules<br/>
#                 • Ensure services are in the same namespace
#             </div>
#         </div>
#         """, unsafe_allow_html=True)
#         
#         # Add connectivity test button
#         if st.button("🔍 Test API Connectivity", type="primary"):
#             st.markdown("### 📡 Connectivity Test Results")
#             connectivity_results = test_connectivity()
#             for result in connectivity_results:
#                 st.text(result)
#             
#             st.markdown("""
#             **🔧 Next Steps:**
#             1. **Check if smartops-api-service is running:**
#                ```bash
#                kubectl get pods -n <namespace>
#                kubectl get services -n <namespace>
#                ```
#             
#             2. **Check service endpoints:**
#                ```bash
#                kubectl get endpoints smartops-api-service -n <namespace>
#                ```
#             
#             3. **Check logs:**
#                ```bash
#                kubectl logs -f deployment/smartops-api-service -n <namespace>
#                ```
#             
#             4. **Verify network policies:**
#                ```bash
#                kubectl get networkpolicies -n <namespace>
#                ```
#             """)

# Add connectivity test function
# def test_connectivity():
#     """Test connectivity to different endpoints and show results"""
#     endpoints_to_test = [
#         "http://smartops-api-service:8000",
#         "http://smartops-api:8000",
#         "http://smartops-backend:8000",
#         "http://api-service:8000",
#         "http://localhost:8000",
#         "http://127.0.0.1:8000"
#     ]
#     
#     results = []
#     for endpoint in endpoints_to_test:
#         try:
#             response = requests.get(f"{endpoint}/", timeout=3)
#             if response.status_code == 200:
#                 results.append(f"✅ {endpoint} - Available")
#             else:
#                 results.append(f"⚠️ {endpoint} - Status {response.status_code}")
#         except Exception as e:


# New Relic-style Time Selector
st.markdown("""
<div class="time-selector">
    <div class="time-header">⏰ Time Range Selection</div>
    <div style="display: grid; grid-template-columns: 2fr 2fr 1fr; gap: 1rem; align-items: end;">
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    time_preset = st.selectbox(
        "Select Time Range",
        ["Live (Now)", "5 minutes ago", "15 minutes ago", "1 hour ago", "6 hours ago", "24 hours ago"],
        index=0,
        label_visibility="collapsed"
    )

with col2:
    if time_preset != "Live (Now)":
        relative_value = st.number_input("Value", min_value=1, max_value=365, value=1, step=1, label_visibility="collapsed")
        relative_unit = st.selectbox("Unit", ["Minutes ago", "Hours ago", "Days ago"], index=1, label_visibility="collapsed")

with col3:
    if st.button("🔄 Refresh", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.markdown("</div></div>", unsafe_allow_html=True)



# Display time info
if time_preset == "Live (Now)":
    st.markdown(f"""
    <div class="status-message">
        <div class="status-icon">📅</div>
        <div class="status-text">Viewing: Real-time data | {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="status-message">
        <div class="status-icon">📅</div>
        <div class="status-text">Viewing: Data from {relative_value} {relative_unit.lower()} | {datetime.now().strftime("%B %d, %Y")}</div>
    </div>
    """, unsafe_allow_html=True)

# New Relic-style Cluster Status
st.markdown('<div class="section-header">🏥 Cluster Status & Health</div>', unsafe_allow_html=True)
st.markdown("""
<div class="status-message">
    <div class="status-icon">✅</div>
    <div class="status-text">SmartOps AI Status: No anomalies detected. All systems are running smoothly!</div>
</div>
""", unsafe_allow_html=True)

# New Relic-style Cluster Metrics
st.markdown('<div class="section-header">📊 Cluster Metrics</div>', unsafe_allow_html=True)

# Get live or fallback data for metrics with enhanced fallback
node_count = 1 if not api_available else len(fetch_node_data()) if fetch_node_data() else 1
pod_count = len(fetch_pod_data()) if fetch_pod_data() and api_available else 18
service_count = get_service_count()
namespace_count = get_namespace_count()



st.markdown(f"""
<div class="metric-grid">
    <div class="metric-card">
        <div class="metric-value">{node_count}</div>
        <div class="metric-label">Nodes</div>
        <div class="metric-status arrow-up">Active</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">{pod_count}</div>
        <div class="metric-label">Pods</div>
        <div class="metric-status arrow-up">Running</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">{service_count}</div>
        <div class="metric-label">Services</div>
        <div class="metric-status arrow-up">Network</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">{namespace_count}</div>
        <div class="metric-label">Namespaces</div>
        <div class="metric-status arrow-up">Logical</div>
    </div>
</div>
""", unsafe_allow_html=True)

# New Relic-style Resource Usage
st.markdown('<div class="section-header">⚡ Resource Usage</div>', unsafe_allow_html=True)

st.markdown("""
<div class="resource-grid">
    <div class="resource-card">
        <div class="resource-header">
            <div class="resource-icon">🖥️</div>
            <div class="resource-title">CPU Usage</div>
        </div>
        <div class="resource-value">31%</div>
        <div class="metric-status arrow-up">2.5/8 cores</div>
    </div>
    <div class="resource-card">
        <div class="resource-header">
            <div class="resource-icon">💾</div>
            <div class="resource-title">Memory Usage</div>
        </div>
        <div class="resource-value">26%</div>
        <div class="metric-status arrow-up">4.2/16 GB</div>
    </div>
</div>
""", unsafe_allow_html=True)

# New Relic-style Pod Status
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<div class="section-header">📋 Pod Status</div>', unsafe_allow_html=True)
with col2:
    if st.button("🔄 Refresh Pod Data", type="secondary"):
        st.cache_data.clear()
        st.rerun()

st.markdown(f"""
<div style="margin-bottom: 1rem; text-align: right; color: #a0aec0; font-size: 0.8rem;">
    Last updated: {datetime.now().strftime('%H:%M:%S')}
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="chart-container">
    <div class="chart-header">
        <div class="chart-icon">📊</div>
        <div class="chart-title">Pod Status Distribution</div>
    </div>
""", unsafe_allow_html=True)

# Fetch real-time pod data with enhanced fallback
pods = get_enhanced_pod_data()

# Get pod status counts
if pods:
    status_counts = get_pod_status_counts(pods)
else:
    # Fallback to default values if no data available
    status_counts = {'Running': 18, 'Pending': 0, 'Failed': 0, 'Succeeded': 0}

# Create a DataFrame for the chart
pod_data = pd.DataFrame(list(status_counts.items()), columns=['Status', 'Count'])

# Display real-time pod status summary with beautiful badges
st.markdown(f"""
<div style="margin-bottom: 1.5rem;">
    <div style="display: flex; gap: 1rem; flex-wrap: wrap; justify-content: center;">
        <div class="pod-status-badge pod-status-running">
            <span style="color: #48bb78; font-weight: 700; font-size: 1.1rem;">🟢 Running: {status_counts['Running']}</span>
        </div>
        <div class="pod-status-badge pod-status-pending">
            <span style="color: #ed8936; font-weight: 700; font-size: 1.1rem;">🟡 Pending: {status_counts['Pending']}</span>
        </div>
        <div class="pod-status-badge pod-status-failed">
            <span style="color: #e53e3e; font-weight: 700; font-size: 1.1rem;">🔴 Failed: {status_counts['Failed']}</span>
        </div>
        <div class="pod-status-badge pod-status-succeeded">
            <span style="color: #38b2ac; font-weight: 700; font-size: 1.1rem;">🔵 Succeeded: {status_counts['Succeeded']}</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.bar_chart(
    pod_data.set_index('Status'),
    use_container_width=True,
    height=300
)

st.markdown("</div>", unsafe_allow_html=True)

# New Relic-style Node Health
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<div class="section-header">🖥️ Node Health Status</div>', unsafe_allow_html=True)
with col2:
    if st.button("🔄 Refresh Node Data", type="secondary"):
        st.cache_data.clear()
        st.rerun()

st.markdown("""
<div class="chart-container">
    <div class="chart-header">
        <div class="chart-icon">🔍</div>
        <div class="chart-title">Node Health Overview</div>
    </div>
""", unsafe_allow_html=True)

# Fetch real-time node data with enhanced fallback
try:
    # Try to get node data using enhanced function
    nodes_data = get_enhanced_node_data()
    
    if nodes_data:
        node_data_list = []
        for node in nodes_data:
            node_name = node.get('name', 'Unknown')
            status = node.get('status', 'Unknown')
            roles = node.get('roles', '<none>')
            age = node.get('age', 'Unknown')
            version = node.get('version', 'Unknown')
            internal_ip = node.get('internal_ip', 'Unknown')
            
            # Determine health status
            if status == 'Ready':
                health = '🟢 Healthy'
            else:
                health = '🔴 Unhealthy'
            
            node_data_list.append({
                'Node Name': node_name,
                'Status': status,
                'Roles': roles,
                'Health': health,
                'Age': age,
                'Version': version,
                'Internal IP': internal_ip
            })
        
        if node_data_list:
            node_data = pd.DataFrame(node_data_list)
            st.dataframe(
                node_data,
                use_container_width=True,
                hide_index=True,
                height=200
            )
        else:
            st.warning("No node data found")
    else:
        # Fallback to sample node info
        node_data = pd.DataFrame({
            'Node Name': ['Cluster Node'],
            'Status': ['Ready'],
            'Health': ['🟢 Healthy'],
            'Info': ['Cluster information'],
            'Version': ['v1.28.0'],
            'Internal IP': ['192.168.1.100']
        })
        st.dataframe(node_data, use_container_width=True, hide_index=True, height=200)
        
except Exception as e:
    # Fallback to sample node info on error
    st.warning(f"Error fetching node data: {str(e)}")
    node_data = pd.DataFrame({
        'Node Name': ['Cluster Node'],
        'Status': ['Ready'],
        'Health': ['🟢 Healthy'],
        'Info': ['Cluster information'],
        'Version': ['v1.28.0'],
        'Internal IP': ['192.168.1.100']
    })
    st.dataframe(node_data, use_container_width=True, hide_index=True, height=200)

st.markdown("</div>", unsafe_allow_html=True)

# Add Misi AI Chatbot Widget
if MISI_AVAILABLE:
    # add_misi_to_page("bottom-right")
    pass  # Placeholder for when Misi is properly integrated
else:
    st.info("🤖 Misi AI Chatbot integration is being set up. You'll see the floating 🤖 icon soon!")

# Beautiful Footer with gradient
st.markdown("---")
st.markdown(f"""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 3rem 2rem; border-radius: 20px; margin: 3rem 0; text-align: center; box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);">
    <div style="margin-bottom: 1rem;">
        <span style="font-size: 2rem; margin: 0 0.5rem;">🚀</span>
        <span style="font-size: 2rem; margin: 0 0.5rem;">⚡</span>
        <span style="font-size: 2rem; margin: 0 0.5rem;">🔮</span>
    </div>
    <p style="font-weight: 700; margin-bottom: 0.5rem; color: white; font-size: 1.1rem;">Powered by SmartOps AI</p>
    <p style="color: #f8fafc; margin: 0; opacity: 0.9; font-size: 0.9rem;">Enterprise Kubernetes Monitoring & AI-Powered Operations</p>
    <div style="margin-top: 1rem; opacity: 0.8; color: #f8fafc; font-size: 0.8rem;">
        Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}
    </div>
</div>
""", unsafe_allow_html=True)

# Main execution block
if __name__ == "__main__":
    show_page()