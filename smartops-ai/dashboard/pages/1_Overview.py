import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import pytz
import requests
import numpy as np
from sidebar_utils import show_sidebar

# Timezone setup
IST = pytz.timezone('Asia/Kolkata')

# API Configuration
API_ENDPOINTS = [
    "http://localhost:8000",
    "http://34.9.232.188:8000", 
    "http://34.9.232.188"
]

# Mock data fallback
MOCK_NAMESPACES = ["default", "kube-system", "kube-public", "kube-node-lease"]

def check_data_availability(selected_date, start_time, end_time, time_preset):
    """Check if data is available for the selected time range"""
    import random
    
    # Simulate data availability based on time range
    if time_preset == "Live (Now)":
        return True  # Live data is always available
    
    # For historical data, simulate availability
    # Weekends might have less data
    if selected_date.weekday() >= 5:  # Saturday = 5, Sunday = 6
        data_chance = 0.3  # 30% chance on weekends
    else:
        data_chance = 0.7  # 70% chance on weekdays
    
    # Early morning and late night might have less data
    if start_time.hour < 6 or start_time.hour > 22:
        data_chance *= 0.5  # Reduce chance for off-hours
    
    return random.random() < data_chance

# Cached functions
@st.cache_data(ttl=30)
def fetch_namespaces():
    try:
        # Try multiple possible API endpoints
        urls = [
            "http://localhost:8000/namespaces",
            "http://34.9.232.188:8000/namespaces",
            "http://34.9.232.188/namespaces"
        ]
        
        for url in urls:
            try:
                resp = requests.get(url, timeout=5)
                if resp.status_code == 200:
                    return resp.json().get('namespaces', [])
            except:
                continue
        
        # Return mock data if no API is available
        return ["default", "kube-system", "kube-public", "kube-node-lease"]
    except Exception as e:
        return ["default", "kube-system", "kube-public", "kube-node-lease"]

@st.cache_data(ttl=30)
def load_anomalies_df():
    try:
        conn = sqlite3.connect("/app/dashboard/data/data.db")
        df = pd.read_sql_query("SELECT * FROM anomalies", conn)
        conn.close()
        return df
    except Exception as e:
        return pd.DataFrame()

@st.cache_data(ttl=30)
def fetch_cluster_metrics():
    """Fetch cluster-wide metrics"""
    try:
        # Try multiple possible API endpoints
        urls = [
            "http://localhost:8000/cluster_metrics",
            "http://34.9.232.188:8000/cluster_metrics",
            "http://34.9.232.188/cluster_metrics"
        ]
        
        for url in urls:
            try:
                resp = requests.get(url, timeout=5)
                if resp.status_code == 200:
                    return resp.json()
            except:
                continue
        
        # Mock data for demonstration
        return {
            "cpu_usage": 2.5, 
            "memory_usage": 4.2 * (1024**3), 
            "cpu_capacity": 8, 
            "memory_capacity": 16 * (1024**3),
            "node_count": 3,
            "pod_count": 12,
            "service_count": 8
        }
    except Exception as e:
        return {
            "cpu_usage": 2.5, 
            "memory_usage": 4.2 * (1024**3), 
            "cpu_capacity": 8, 
            "memory_capacity": 16 * (1024**3),
            "node_count": 3,
            "pod_count": 12,
            "service_count": 8
        }

@st.cache_data(ttl=30)
def fetch_node_metrics():
    """Fetch node-level metrics"""
    try:
        # Try multiple possible API endpoints
        urls = [
            "http://localhost:8000/node_metrics",
            "http://34.9.232.188:8000/node_metrics",
            "http://34.9.232.188/node_metrics"
        ]
        
        for url in urls:
            try:
                resp = requests.get(url, timeout=5)
                if resp.status_code == 200:
                    return resp.json().get("nodes", [])
            except:
                continue
        
        # Mock data for demonstration
        return [
            {
                "name": "gke-smartops-cluster-default-pool-897bf21e-l5gp",
                "cpu_usage": 2.5,
                "cpu_capacity": 8,
                "memory_usage": 4.2 * (1024**3),
                "memory_capacity": 16 * (1024**3),
                "status": "Ready",
                "pods": 4
            },
            {
                "name": "gke-smartops-cluster-default-pool-897bf21e-l6gp",
                "cpu_usage": 1.8,
                "cpu_capacity": 8,
                "memory_usage": 3.1 * (1024**3),
                "memory_capacity": 16 * (1024**3),
                "status": "Ready",
                "pods": 3
            },
            {
                "name": "gke-smartops-cluster-default-pool-897bf21e-l7gp",
                "cpu_usage": 3.2,
                "cpu_capacity": 8,
                "memory_usage": 5.8 * (1024**3),
                "memory_capacity": 16 * (1024**3),
                "status": "Ready",
                "pods": 5
            }
        ]
    except Exception as e:
        return [
            {
                "name": "gke-smartops-cluster-default-pool-897bf21e-l5gp",
                "cpu_usage": 2.5,
                "cpu_capacity": 8,
                "memory_usage": 4.2 * (1024**3),
                "memory_capacity": 16 * (1024**3),
                "status": "Ready",
                "pods": 4
            },
            {
                "name": "gke-smartops-cluster-default-pool-897bf21e-l6gp",
                "cpu_usage": 1.8,
                "cpu_capacity": 8,
                "memory_usage": 3.1 * (1024**3),
                "memory_capacity": 16 * (1024**3),
                "status": "Ready",
                "pods": 3
            },
            {
                "name": "gke-smartops-cluster-default-pool-897bf21e-l7gp",
                "cpu_usage": 3.2,
                "cpu_capacity": 8,
                "memory_usage": 5.8 * (1024**3),
                "memory_capacity": 16 * (1024**3),
                "status": "Ready",
                "pods": 5
            }
        ]

@st.cache_data(ttl=30)
def fetch_pod_status_summary():
    """Fetch pod status summary"""
    try:
        # Try multiple possible API endpoints
        urls = [
            "http://localhost:8000/pod_status_summary",
            "http://34.9.232.188:8000/pod_status_summary",
            "http://34.9.232.188/pod_status_summary"
        ]
        
        for url in urls:
            try:
                resp = requests.get(url, timeout=5)
                if resp.status_code == 200:
                    return resp.json()
            except:
                continue
        
        return {
            "running": 10,
            "pending": 1,
            "failed": 0,
            "succeeded": 1,
            "total": 12
        }
    except Exception as e:
        return {
            "running": 10,
            "pending": 1,
            "failed": 0,
            "succeeded": 1,
            "total": 12
        }

def generate_time_series_data(time_range="current"):
    """Generate mock time series data for charts based on time range"""
    now = datetime.now()
    
    if time_range == "current" or time_range == "5min_ago":
        # Last 5 minutes with 10-second intervals
        timestamps = [now - timedelta(seconds=i*10) for i in range(30, 0, -1)]
        intervals = 30
    elif time_range == "15min_ago":
        # Last 15 minutes with 1-minute intervals
        timestamps = [now - timedelta(minutes=i) for i in range(15, 0, -1)]
        intervals = 15
    elif time_range == "1hour_ago":
        # Last hour with 5-minute intervals
        timestamps = [now - timedelta(minutes=i*5) for i in range(12, 0, -1)]
        intervals = 12
    elif time_range == "6hours_ago":
        # Last 6 hours with 30-minute intervals
        timestamps = [now - timedelta(minutes=i*30) for i in range(12, 0, -1)]
        intervals = 12
    else:  # 24hours_ago
        # Last 24 hours with 2-hour intervals
        timestamps = [now - timedelta(hours=i*2) for i in range(12, 0, -1)]
        intervals = 12
    
    # CPU usage with some variation based on time
    cpu_base = 65
    cpu_data = [cpu_base + np.random.normal(0, 5) for _ in range(intervals)]
    cpu_data = [max(0, min(100, x)) for x in cpu_data]
    
    # Memory usage with some variation based on time
    memory_base = 72
    memory_data = [memory_base + np.random.normal(0, 3) for _ in range(intervals)]
    memory_data = [max(0, min(100, x)) for x in memory_data]
    
    return timestamps, cpu_data, memory_data

def get_historical_metrics(time_range):
    """Get historical cluster metrics based on time range"""
    # Simulate data availability - some time ranges might not have data
    import random
    
    # Randomly determine if data is available for this time range
    data_available = random.choice([True, False, False])  # 33% chance of data being available
    
    if not data_available:
        return None  # No data available
    
    if time_range == "current":
        return {
            "cpu_usage": 2.5,
            "memory_usage": 4.2 * (1024**3),
            "cpu_capacity": 8,
            "memory_capacity": 16 * (1024**3),
            "node_count": 3,
            "pod_count": 12,
            "service_count": 8
        }
    elif time_range == "5min_ago":
        return {
            "cpu_usage": 2.8,
            "memory_usage": 4.5 * (1024**3),
            "cpu_capacity": 8,
            "memory_capacity": 16 * (1024**3),
            "node_count": 3,
            "pod_count": 11,
            "service_count": 8
        }
    elif time_range == "15min_ago":
        return {
            "cpu_usage": 3.1,
            "memory_usage": 4.8 * (1024**3),
            "cpu_capacity": 8,
            "memory_capacity": 16 * (1024**3),
            "node_count": 3,
            "pod_count": 10,
            "service_count": 8
        }
    elif time_range == "1hour_ago":
        return {
            "cpu_usage": 2.2,
            "memory_usage": 3.9 * (1024**3),
            "cpu_capacity": 8,
            "memory_capacity": 16 * (1024**3),
            "node_count": 3,
            "pod_count": 13,
            "service_count": 8
        }
    elif time_range == "6hours_ago":
        return {
            "cpu_usage": 1.8,
            "memory_usage": 3.5 * (1024**3),
            "cpu_capacity": 8,
            "memory_capacity": 16 * (1024**3),
            "node_count": 3,
            "pod_count": 15,
            "service_count": 8
        }
    else:  # 24hours_ago
        return {
            "cpu_usage": 1.5,
            "memory_usage": 3.2 * (1024**3),
            "cpu_capacity": 8,
            "memory_capacity": 16 * (1024**3),
            "node_count": 3,
            "pod_count": 18,
            "service_count": 8
        }

def get_historical_node_metrics(time_range):
    """Get historical node metrics based on time range"""
    if time_range == "current":
        return [
            {
                "name": "gke-smartops-cluster-default-pool-897bf21e-l5gp",
                "cpu_usage": 2.5,
                "cpu_capacity": 8,
                "memory_usage": 4.2 * (1024**3),
                "memory_capacity": 16 * (1024**3),
                "status": "Ready",
                "pods": 4
            },
            {
                "name": "gke-smartops-cluster-default-pool-897bf21e-l6gp",
                "cpu_usage": 1.8,
                "cpu_capacity": 8,
                "memory_usage": 3.1 * (1024**3),
                "memory_capacity": 16 * (1024**3),
                "status": "Ready",
                "pods": 3
            },
            {
                "name": "gke-smartops-cluster-default-pool-897bf21e-l7gp",
                "cpu_usage": 3.2,
                "cpu_capacity": 8,
                "memory_usage": 5.8 * (1024**3),
                "memory_capacity": 16 * (1024**3),
                "status": "Ready",
                "pods": 5
            }
        ]
    elif time_range == "5min_ago":
        return [
            {
                "name": "gke-smartops-cluster-default-pool-897bf21e-l5gp",
                "cpu_usage": 2.8,
                "cpu_capacity": 8,
                "memory_usage": 4.5 * (1024**3),
                "memory_capacity": 16 * (1024**3),
                "status": "Ready",
                "pods": 4
            },
            {
                "name": "gke-smartops-cluster-default-pool-897bf21e-l6gp",
                "cpu_usage": 2.1,
                "cpu_capacity": 8,
                "memory_usage": 3.3 * (1024**3),
                "memory_capacity": 16 * (1024**3),
                "status": "Ready",
                "pods": 3
            },
            {
                "name": "gke-smartops-cluster-default-pool-897bf21e-l7gp",
                "cpu_usage": 3.5,
                "cpu_capacity": 8,
                "memory_usage": 6.0 * (1024**3),
                "memory_capacity": 16 * (1024**3),
                "status": "Ready",
                "pods": 5
            }
        ]
    elif time_range == "15min_ago":
        return [
            {
                "name": "gke-smartops-cluster-default-pool-897bf21e-l5gp",
                "cpu_usage": 3.1,
                "cpu_capacity": 8,
                "memory_usage": 4.8 * (1024**3),
                "memory_capacity": 16 * (1024**3),
                "status": "Ready",
                "pods": 4
            },
            {
                "name": "gke-smartops-cluster-default-pool-897bf21e-l6gp",
                "cpu_usage": 2.4,
                "cpu_capacity": 8,
                "memory_usage": 3.5 * (1024**3),
                "memory_capacity": 16 * (1024**3),
                "status": "Ready",
                "pods": 3
            },
            {
                "name": "gke-smartops-cluster-default-pool-897bf21e-l7gp",
                "cpu_usage": 3.8,
                "cpu_capacity": 8,
                "memory_usage": 6.2 * (1024**3),
                "memory_capacity": 16 * (1024**3),
                "status": "Ready",
                "pods": 5
            }
        ]
    elif time_range == "1hour_ago":
        return [
            {
                "name": "gke-smartops-cluster-default-pool-897bf21e-l5gp",
                "cpu_usage": 2.2,
                "cpu_capacity": 8,
                "memory_usage": 3.9 * (1024**3),
                "memory_capacity": 16 * (1024**3),
                "status": "Ready",
                "pods": 4
            },
            {
                "name": "gke-smartops-cluster-default-pool-897bf21e-l6gp",
                "cpu_usage": 1.5,
                "cpu_capacity": 8,
                "memory_usage": 2.9 * (1024**3),
                "memory_capacity": 16 * (1024**3),
                "status": "Ready",
                "pods": 3
            },
            {
                "name": "gke-smartops-cluster-default-pool-897bf21e-l7gp",
                "cpu_usage": 2.9,
                "cpu_capacity": 8,
                "memory_usage": 5.5 * (1024**3),
                "memory_capacity": 16 * (1024**3),
                "status": "Ready",
                "pods": 5
            }
        ]
    elif time_range == "6hours_ago":
        return [
            {
                "name": "gke-smartops-cluster-default-pool-897bf21e-l5gp",
                "cpu_usage": 1.8,
                "cpu_capacity": 8,
                "memory_usage": 3.5 * (1024**3),
                "memory_capacity": 16 * (1024**3),
                "status": "Ready",
                "pods": 4
            },
            {
                "name": "gke-smartops-cluster-default-pool-897bf21e-l6gp",
                "cpu_usage": 1.2,
                "cpu_capacity": 8,
                "memory_usage": 2.7 * (1024**3),
                "memory_capacity": 16 * (1024**3),
                "status": "Ready",
                "pods": 3
            },
            {
                "name": "gke-smartops-cluster-default-pool-897bf21e-l7gp",
                "cpu_usage": 2.5,
                "cpu_capacity": 8,
                "memory_usage": 5.2 * (1024**3),
                "memory_capacity": 16 * (1024**3),
                "status": "Ready",
                "pods": 5
            }
        ]
    else:  # 24hours_ago
        return [
            {
                "name": "gke-smartops-cluster-default-pool-897bf21e-l5gp",
                "cpu_usage": 1.5,
                "cpu_capacity": 8,
                "memory_usage": 3.2 * (1024**3),
                "memory_capacity": 16 * (1024**3),
                "status": "Ready",
                "pods": 4
            },
            {
                "name": "gke-smartops-cluster-default-pool-897bf21e-l6gp",
                "cpu_usage": 1.0,
                "cpu_capacity": 8,
                "memory_usage": 2.5 * (1024**3),
                "memory_capacity": 16 * (1024**3),
                "status": "Ready",
                "pods": 3
            },
            {
                "name": "gke-smartops-cluster-default-pool-897bf21e-l7gp",
                "cpu_usage": 2.2,
                "cpu_capacity": 8,
                "memory_usage": 4.9 * (1024**3),
                "memory_capacity": 16 * (1024**3),
                "status": "Ready",
                "pods": 5
            }
        ]

def get_historical_pod_status(time_range):
    """Get historical pod status based on time range"""
    if time_range == "current":
        return {
            "running": 10,
            "pending": 1,
            "failed": 0,
            "succeeded": 1,
            "total": 12
        }
    elif time_range == "5min_ago":
        return {
            "running": 11,
            "pending": 0,
            "failed": 0,
            "succeeded": 1,
            "total": 12
        }
    elif time_range == "15min_ago":
        return {
            "running": 10,
            "pending": 1,
            "failed": 0,
            "succeeded": 1,
            "total": 12
        }
    elif time_range == "1hour_ago":
        return {
            "running": 13,
            "pending": 0,
            "failed": 0,
            "succeeded": 0,
            "total": 13
        }
    elif time_range == "6hours_ago":
        return {
            "running": 15,
            "pending": 0,
            "failed": 0,
            "succeeded": 0,
            "total": 15
        }
    else:  # 24hours_ago
        return {
            "running": 18,
            "pending": 0,
            "failed": 0,
            "succeeded": 0,
            "total": 18
        }

# Page config
st.set_page_config(
    page_title="Kubernetes Cluster Overview - SmartOps AI",
    page_icon="📊",
    layout="wide"
)

# Sidebar
with st.sidebar:
    show_sidebar()

# Professional Grafana-style CSS
st.markdown("""
<style>
/* Reset and base styles */
* {
    box-sizing: border-box;
}

/* Main container */
.main .block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    max-width: 1400px;
}

/* Header styling */
.dashboard-header {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    padding: 2rem;
    border-radius: 8px;
    margin-bottom: 2rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    border: 1px solid #e1e5e9;
}

.dashboard-header h1 {
    font-size: 2.2rem;
    margin-bottom: 0.5rem;
    font-weight: 600;
    color: white;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.dashboard-header p {
    font-size: 1rem;
    opacity: 0.9;
    margin: 0;
    color: #e8f4fd;
}

/* Status cards */
.status-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.status-card {
    background: white;
    border: 1px solid #e1e5e9;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.status-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    border-color: #2a5298;
}

.status-card.healthy {
    border-left: 4px solid #00d4aa;
}

.status-card.warning {
    border-left: 4px solid #ffa726;
}

.status-card.critical {
    border-left: 4px solid #ef5350;
}

.status-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #1e3c72, #2a5298);
}

.status-number {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: #1e3c72;
}

.status-label {
    font-size: 0.9rem;
    color: #6c757d;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 500;
}

.status-description {
    font-size: 0.85rem;
    color: #495057;
    margin-top: 0.5rem;
}

/* Section headers */
.section-header {
    background: #f8f9fa;
    color: #495057;
    padding: 1rem 1.5rem;
    border-radius: 6px;
    margin: 2rem 0 1rem 0;
    font-size: 1.1rem;
    font-weight: 600;
    border-left: 4px solid #2a5298;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

/* Alert banners */
.alert-banner {
    background: linear-gradient(135deg, #ef5350 0%, #e53935 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 8px;
    margin: 1rem 0;
    box-shadow: 0 4px 15px rgba(239, 83, 80, 0.2);
    border: 1px solid #e53935;
}

.success-banner {
    background: linear-gradient(135deg, #00d4aa 0%, #00b894 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 8px;
    margin: 1rem 0;
    box-shadow: 0 4px 15px rgba(0, 212, 170, 0.2);
    border: 1px solid #00b894;
}

.warning-banner {
    background: linear-gradient(135deg, #ffa726 0%, #ff9800 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 8px;
    margin: 1rem 0;
    box-shadow: 0 4px 15px rgba(255, 167, 38, 0.2);
    border: 1px solid #ff9800;
}

/* Metric cards */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin: 1.5rem 0;
}

.metric-card {
    background: white;
    border: 1px solid #e1e5e9;
    border-radius: 6px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.metric-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: #1e3c72;
    margin-bottom: 0.25rem;
}

.metric-label {
    font-size: 0.8rem;
    color: #6c757d;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Node table styling */
.node-table {
    background: white;
    border: 1px solid #e1e5e9;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

/* Grafana-style time selector */
.grafana-time-selector {
    background: #f8f9fa;
    border: 1px solid #e1e5e9;
    border-radius: 8px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

/* Time tabs styling */
.time-tabs {
    display: flex;
    border-bottom: 2px solid #e1e5e9;
    margin: 1rem 0;
}

.tab {
    padding: 0.75rem 1.5rem;
    cursor: pointer;
    border-bottom: 3px solid transparent;
    transition: all 0.3s ease;
    font-weight: 500;
    color: #6c757d;
    background: transparent;
}

.tab:hover {
    color: #2a5298;
    background: rgba(42, 82, 152, 0.05);
}

.tab.active {
    color: #2a5298;
    border-bottom-color: #2a5298;
    background: rgba(42, 82, 152, 0.1);
}

/* Tab content */
.tab-content {
    display: none;
    padding: 1rem 0;
}

.tab-content.active {
    display: block;
}

/* Time input styling */
.time-input-label {
    font-weight: 600;
    color: #495057;
    margin-bottom: 0.5rem;
    display: block;
}

.date-input-label {
    font-weight: 600;
    color: #495057;
    margin-bottom: 0.5rem;
    display: block;
}

/* Quick actions CSS removed */

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Main content
st.markdown("""
<div class="dashboard-header">
    <h1>📊 Kubernetes Cluster Overview</h1>
    <p>Real-time monitoring dashboard powered by SmartOps AI</p>
</div>
""", unsafe_allow_html=True)

# Time Selector for Historical Data
st.markdown('<div class="section-header">⏰ Time Range Selector</div>', unsafe_allow_html=True)

# Grafana-style time range selector
st.markdown('<div class="grafana-time-selector">', unsafe_allow_html=True)

# Header bar with current selection and refresh button
col_header1, col_header2, col_header3 = st.columns([3, 1, 1])

with col_header1:
    # Display current time range selection
    st.markdown("**~ Now → Now**")

with col_header2:
    # Quick time presets dropdown
    time_preset = st.selectbox(
        "Quick Presets",
        ["Live (Now)", "5 minutes ago", "15 minutes ago", "1 hour ago", "6 hours ago", "24 hours ago"],
        index=0,
        label_visibility="collapsed"
    )

with col_header3:
    # Refresh button
    if st.button("🔄 Refresh", use_container_width=True, key="refresh_main"):
        st.cache_data.clear()
        st.rerun()

# Tab-style time selection
st.markdown("""
<div class="time-tabs">
    <div class="tab active" id="relative-tab" onclick="switchTab('relative')">Relative</div>
    <div class="tab" id="absolute-tab" onclick="switchTab('absolute')">Absolute</div>
    <div class="tab" id="now-tab" onclick="switchTab('now')">Now</div>
</div>

<script>
function switchTab(tabName) {
    // Hide all tab contents
    var contents = document.querySelectorAll('.tab-content');
    for (var i = 0; i < contents.length; i++) {
        contents[i].classList.remove('active');
    }
    
    // Remove active class from all tabs
    var tabs = document.querySelectorAll('.tab');
    for (var i = 0; i < tabs.length; i++) {
        tabs[i].classList.remove('active');
    }
    
    // Show selected tab content and activate tab
    document.getElementById(tabName + '-content').classList.add('active');
    document.getElementById(tabName + '-tab').classList.add('active');
}
</script>
""", unsafe_allow_html=True)

# Relative time selection (default active tab)
st.markdown('<div class="tab-content active" id="relative-content">', unsafe_allow_html=True)

col_rel1, col_rel2, col_rel3 = st.columns([1, 2, 1])

with col_rel1:
    # Number input for relative time
    relative_value = st.number_input(
        "Value",
        min_value=1,
        max_value=365,
        value=1,
        step=1,
        key="relative_value"
    )

with col_rel2:
    # Unit selection
    relative_unit = st.selectbox(
        "Unit",
        ["Minutes ago", "Hours ago", "Days ago", "Weeks ago"],
        index=1,  # Default to "Hours ago"
        key="relative_unit"
    )

with col_rel3:
    # Calculate and display start date
    if relative_unit == "Minutes ago":
        start_datetime = datetime.now() - timedelta(minutes=relative_value)
    elif relative_unit == "Hours ago":
        start_datetime = datetime.now() - timedelta(hours=relative_value)
    elif relative_unit == "Days ago":
        start_datetime = datetime.now() - timedelta(days=relative_value)
    else:  # Weeks ago
        start_datetime = datetime.now() - timedelta(weeks=relative_value)
    
    st.markdown(f"**Start date:** {start_datetime.strftime('%b %d, %Y @ %H:%M:%S')}")

# Round to day toggle
round_to_day = st.checkbox("Round to the day", value=True, key="round_to_day")

st.markdown('</div>', unsafe_allow_html=True)

# Absolute time selection
st.markdown('<div class="tab-content" id="absolute-content">', unsafe_allow_html=True)

col_abs1, col_abs2, col_abs3, col_abs4 = st.columns([1, 1, 1, 1])

with col_abs1:
    # Start date
    start_date = st.date_input(
        "Start Date",
        value=datetime.now().date(),
        key="start_date_abs"
    )

with col_abs2:
    # Start time
    start_time_abs = st.time_input(
        "Start Time",
        value=datetime.strptime("00:00", "%H:%M").time(),
        key="start_time_abs"
    )

with col_abs3:
    # End date
    end_date = st.date_input(
        "End Date",
        value=datetime.now().date(),
        key="end_date_abs"
    )

with col_abs4:
    # End time
    end_time_abs = st.time_input(
        "End Time",
        value=datetime.now().time(),
        key="end_time_abs"
    )

st.markdown('</div>', unsafe_allow_html=True)

# Now tab (instant current time)
st.markdown('<div class="tab-content" id="now-content">', unsafe_allow_html=True)

st.info("🕐 **Current Time:** " + datetime.now().strftime("%B %d, %Y at %I:%M:%S %p"))

if st.button("Set to Current Time", key="set_now"):
    time_preset = "Live (Now)"
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Apply the selected time range
if time_preset == "Live (Now)":
    selected_time = "Current"
    time_description = "Real-time data"
    display_date = datetime.now().strftime("%B %d, %Y")
    display_time = f"{datetime.now().strftime('%I:%M %p')}"
    start_time = datetime.now().time()
    end_time = datetime.now().time()
    selected_date = datetime.now().date()
else:
    # For relative time, use the calculated start time
    if relative_unit == "Minutes ago":
        start_datetime = datetime.now() - timedelta(minutes=relative_value)
    elif relative_unit == "Hours ago":
        start_datetime = datetime.now() - timedelta(hours=relative_value)
    elif relative_unit == "Days ago":
        start_datetime = datetime.now() - timedelta(days=relative_value)
    else:  # Weeks ago
        start_datetime = datetime.now() - timedelta(weeks=relative_value)
    
    if round_to_day:
        start_datetime = start_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
    
    selected_date = start_datetime.date()
    start_time = start_datetime.time()
    end_time = datetime.now().time()
    
    # Map to our internal time format
    if relative_unit == "Minutes ago" and relative_value <= 5:
        selected_time = "5min_ago"
        time_description = f"Data from {relative_value} minutes ago"
    elif relative_unit == "Minutes ago" and relative_value <= 15:
        selected_time = "15min_ago"
        time_description = f"Data from {relative_value} minutes ago"
    elif relative_unit == "Hours ago" and relative_value <= 1:
        selected_time = "1hour_ago"
        time_description = f"Data from {relative_value} hour ago"
    elif relative_unit == "Hours ago" and relative_value <= 6:
        selected_time = "6hours_ago"
        time_description = f"Data from {relative_value} hours ago"
    elif relative_unit == "Days ago" and relative_value <= 1:
        selected_time = "24hours_ago"
        time_description = f"Data from {relative_value} day ago"
    else:
        selected_time = "24hours_ago"
        time_description = f"Data from {relative_value} {relative_unit.lower()}"
    
    # Format for display
    display_date = selected_date.strftime("%B %d, %Y")
    start_time_12hr = start_time.strftime("%I:%M %p")
    end_time_12hr = end_time.strftime("%I:%M %p")



# Display selected time info and refresh button
col1, col2 = st.columns([3, 1])

with col1:
    if time_preset == "Live (Now)":
        st.info(f"📅 **Viewing:** {time_description} | {display_date} at {display_time}")
    else:
        st.info(f"📅 **Viewing:** {time_description} | {display_date} from {start_time_12hr} to {end_time_12hr}")

with col2:
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# Check data availability for the selected time range FIRST
data_available = check_data_availability(selected_date, start_time, end_time, time_preset)

# Data Availability Summary
st.markdown('<div class="section-header">📊 Data Availability Summary</div>', unsafe_allow_html=True)

if data_available:
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.success(f"✅ **Data Available:** Successfully loaded {time_description} for {display_date} from {start_time_12hr} to {end_time_12hr}")
    
    with col2:
        st.metric("Data Status", "Available", delta="✅")
    
    with col3:
        st.metric("Time Range", f"{start_time_12hr} - {end_time_12hr}")
else:
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.error(f"❌ **Data Not Available:** No historical data found for {time_description} | {display_date} from {start_time_12hr} to {end_time_12hr}")
        st.warning("💡 **Tip:** Try selecting a different time range or use 'Live (Now)' for current data.")
    
    with col2:
        st.metric("Data Status", "Unavailable", delta="❌")
    
    with col3:
        st.metric("Time Range", f"{start_time_12hr} - {end_time_12hr}")

# API Connection Status
st.info("🔌 **API Status:** Using mock data for demonstration. Real-time metrics will be available once the API endpoints are configured.")

# Fetch all data based on selected time range
if selected_time == "Current":
    cluster_metrics = fetch_cluster_metrics()
    node_metrics = fetch_node_metrics()
    pod_status = fetch_pod_status_summary()
else:
    if data_available:
        cluster_metrics = get_historical_metrics(selected_time)
        node_metrics = get_historical_node_metrics(selected_time)
        pod_status = get_historical_pod_status(selected_time)
    else:
        cluster_metrics = None
        node_metrics = None
        pod_status = None

df = load_anomalies_df()

# Overall Cluster Health Status
if data_available and cluster_metrics and node_metrics and pod_status:
    st.markdown(f'<div class="section-header">🏥 Cluster Health Status - {time_description}</div>', unsafe_allow_html=True)
    
    # Show time context
    if time_preset != "Live (Now)":
        st.info(f"📅 **Time Context:** Showing health status for {display_date} from {start_time_12hr} to {end_time_12hr}")

    # Calculate overall health score
    health_score = 0
    total_checks = 0
    
    # CPU health check
    cpu_usage_percent = (cluster_metrics['cpu_usage'] / cluster_metrics['cpu_capacity']) * 100 if cluster_metrics['cpu_capacity'] > 0 else 0
    if cpu_usage_percent < 70:
        health_score += 1
    total_checks += 1

    # Memory health check
    memory_usage_percent = (cluster_metrics['memory_usage'] / cluster_metrics['memory_capacity']) * 100 if cluster_metrics['memory_capacity'] > 0 else 0
    if memory_usage_percent < 70:
        health_score += 1
    total_checks += 1

    # Pod health check
    if pod_status['failed'] == 0:
        health_score += 1
    total_checks += 1

    # Node health check
    healthy_nodes = sum(1 for node in node_metrics if node.get('status') == 'Ready')
    if healthy_nodes == len(node_metrics):
        health_score += 1
    total_checks += 1
else:
    st.markdown('<div class="section-header">🏥 Cluster Health Status</div>', unsafe_allow_html=True)
    st.warning("⚠️ **Health Status Unavailable:** Cannot calculate cluster health without historical data.")
    st.info("Please select a time range with available data to view cluster health metrics.")
    
    # Set default values for display
    health_score = 0
    total_checks = 1
    cpu_usage_percent = 0
    memory_usage_percent = 0
    healthy_nodes = 0

# Anomaly health check
if df.empty or df.iloc[-1]['prediction'].lower() == 'normal':
    health_score += 1
total_checks += 1

overall_health_percent = (health_score / total_checks) * 100

# Display health status
if overall_health_percent >= 80:
    health_status = "Excellent"
    health_color = "success"
    health_icon = "🟢"
elif overall_health_percent >= 60:
    health_status = "Good"
    health_color = "warning"
    health_icon = "🟡"
else:
    health_status = "Needs Attention"
    health_color = "error"
    health_icon = "🔴"

# Health status display
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    if health_color == "success":
        st.markdown(f"""
        <div class="success-banner">
            <h3>{health_icon} Cluster Health: {overall_health_percent:.0f}% - {health_status}</h3>
            <p>Your Kubernetes cluster is operating at optimal performance. All systems are healthy and running smoothly.</p>
        </div>
        """, unsafe_allow_html=True)
    elif health_color == "warning":
        st.markdown(f"""
        <div class="warning-banner">
            <h3>{health_icon} Cluster Health: {overall_health_percent:.0f}% - {health_status}</h3>
            <p>Your cluster is generally healthy but some areas need attention. Monitor resource usage closely.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="alert-banner">
            <h3>{health_icon} Cluster Health: {overall_health_percent:.0f}% - {health_status}</h3>
            <p>Your cluster requires immediate attention. Check resource usage, pod status, and node health.</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{overall_health_percent:.0f}%</div>
        <div class="metric-label">Health Score</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    if node_metrics:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{healthy_nodes}/{len(node_metrics)}</div>
            <div class="metric-label">Healthy Nodes</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">0/0</div>
            <div class="metric-label">Healthy Nodes</div>
        </div>
        """, unsafe_allow_html=True)

# SmartOps AI Status
if not df.empty:
    latest = df.iloc[-1]
    if latest['prediction'].lower() == 'normal':
        st.markdown("""
        <div class="success-banner">
            <h3>✅ SmartOps AI Status</h3>
            <p>No anomalies detected. All systems are running smoothly!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="alert-banner">
            <h3>🚨 SmartOps AI Alert</h3>
            <p>Anomaly detected in pod resource usage. Check the Anomaly Detection page for details.</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="success-banner">
        <h3>✅ SmartOps AI Status</h3>
        <p>No anomalies detected. All systems are running smoothly!</p>
    </div>
    """, unsafe_allow_html=True)

# Cluster Statistics
if data_available:
    st.markdown(f'<div class="section-header">📊 Cluster Statistics - {time_description}</div>', unsafe_allow_html=True)
    
    # Show time context
    if time_preset != "Live (Now)":
        st.info(f"📅 **Time Context:** Showing statistics for {display_date} from {start_time_12hr} to {end_time_12hr}")
else:
    st.markdown('<div class="section-header">📊 Cluster Statistics</div>', unsafe_allow_html=True)

if data_available:
    # Stats cards in a grid
    st.markdown(f"""
    <div class="status-grid">
        <div class="status-card healthy">
            <div class="status-number">{cluster_metrics.get('node_count', 3)}</div>
            <div class="status-label">Nodes</div>
            <div class="status-description">Active cluster nodes</div>
        </div>
        <div class="status-card healthy">
            <div class="status-number">{cluster_metrics.get('pod_count', 12)}</div>
            <div class="status-label">Pods</div>
            <div class="status-description">Running containers</div>
        </div>
        <div class="status-card healthy">
            <div class="status-number">{cluster_metrics.get('service_count', 8)}</div>
            <div class="status-label">Services</div>
            <div class="status-description">Network services</div>
        </div>
        <div class="status-card healthy">
            <div class="status-number">{len(fetch_namespaces())}</div>
            <div class="status-label">Namespaces</div>
            <div class="status-description">Logical partitions</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.warning("⚠️ **Statistics Unavailable:** Cannot display cluster statistics without historical data.")
    st.info("Please select a time range with available data to view cluster statistics.")

# Pod Status Summary
st.markdown('<div class="section-header">📋 Pod Status Summary</div>', unsafe_allow_html=True)

if data_available and pod_status:
    # Create pod status visualization
    pod_data = {
        'Status': ['Running', 'Pending', 'Failed', 'Succeeded'],
        'Count': [pod_status['running'], pod_status['pending'], pod_status['failed'], pod_status['succeeded']],
        'Color': ['#00d4aa', '#ffa726', '#ef5350', '#42a5f5']
    }

    fig_pods = px.bar(
        x=pod_data['Status'],
        y=pod_data['Count'],
        color=pod_data['Status'],
        color_discrete_map=dict(zip(pod_data['Status'], pod_data['Color'])),
        title=f"Pod Status Distribution - {time_description}"
    )

    fig_pods.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    fig_pods.update_xaxes(showgrid=False)
    fig_pods.update_yaxes(showgrid=True, gridcolor='#e9ecef')

    st.plotly_chart(fig_pods, use_container_width=True)
else:
    st.warning("⚠️ **Pod Status Unavailable:** Cannot display pod status without historical data.")
    st.info("Please select a time range with available data to view pod status information.")

# Resource Usage Visualization
if data_available:
    st.markdown(f'<div class="section-header">⚡ Resource Usage Overview - {time_description}</div>', unsafe_allow_html=True)
    
    # Show time context
    if time_preset != "Live (Now)":
        st.info(f"📅 **Time Context:** Showing resource usage for {display_date} from {start_time_12hr} to {end_time_12hr}")
else:
    st.markdown('<div class="section-header">⚡ Resource Usage Overview</div>', unsafe_allow_html=True)

if data_available:
    # Show notice about mock data
    st.info("📊 **Note:** Currently showing demonstration data. Real-time metrics will be available once the API is fully deployed.")

    # Create two columns for cluster overview
    col1, col2 = st.columns(2)
else:
    st.warning("⚠️ **Resource Usage Unavailable:** Cannot display resource usage metrics without historical data.")
    st.info("Please select a time range with available data to view resource usage information.")

with col1:
    # Cluster CPU Usage Gauge
    fig_cpu = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = cpu_usage_percent,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Cluster CPU Usage (%)", 'font': {'size': 16}},
        delta = {'reference': 80},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#2a5298"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': "#00d4aa"},
                {'range': [50, 80], 'color': "#ffa726"},
                {'range': [80, 100], 'color': "#ef5350"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig_cpu.update_layout(
        height=300, 
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_cpu, use_container_width=True)

with col2:
    # Cluster RAM Usage Gauge
    fig_memory = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = memory_usage_percent,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Cluster RAM Usage (%)", 'font': {'size': 16}},
        delta = {'reference': 80},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkgreen"},
            'bar': {'color': "#2a5298"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': "#00d4aa"},
                {'range': [50, 80], 'color': "#ffa726"},
                {'range': [80, 100], 'color': "#ef5350"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig_memory.update_layout(
        height=300, 
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_memory, use_container_width=True)

# Time Series Charts
if data_available:
    st.markdown(f'<div class="section-header">⏰ Resource Usage Trends - {time_description}</div>', unsafe_allow_html=True)
    
    # Show time context
    if time_preset != "Live (Now)":
        st.info(f"📅 **Time Context:** Showing trends for {display_date} from {start_time_12hr} to {end_time_12hr}")
else:
    st.markdown('<div class="section-header">⏰ Resource Usage Trends</div>', unsafe_allow_html=True)

if data_available:
    # Generate mock time series data based on selected time range
    timestamps, cpu_data, memory_data = generate_time_series_data(selected_time)

    # Create time series charts
    col1, col2 = st.columns(2)
else:
    st.warning("⚠️ **Trend Data Unavailable:** Cannot display resource usage trends without historical data.")
    st.info("Please select a time range with available data to view trend information.")

with col1:
    fig_cpu_trend = go.Figure()
    fig_cpu_trend.add_trace(go.Scatter(
        x=timestamps,
        y=cpu_data,
        mode='lines+markers',
        name='CPU Usage %',
        line=dict(color='#2a5298', width=3),
        marker=dict(size=4)
    ))
    # Update title based on time range
    if selected_time == "Current":
        title_text = "CPU Usage Trend (Live)"
    elif selected_time == "5min_ago":
        title_text = "CPU Usage Trend (Last 5 Minutes)"
    elif selected_time == "15min_ago":
        title_text = "CPU Usage Trend (Last 15 Minutes)"
    elif selected_time == "1hour_ago":
        title_text = "CPU Usage Trend (Last Hour)"
    elif selected_time == "6hours_ago":
        title_text = "CPU Usage Trend (Last 6 Hours)"
    else:
        title_text = "CPU Usage Trend (Last 24 Hours)"
    
    fig_cpu_trend.update_layout(
        title=title_text,
        xaxis_title="Time",
        yaxis_title="CPU Usage (%)",
        height=300,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='#e9ecef'),
        yaxis=dict(showgrid=True, gridcolor='#e9ecef', range=[0, 100])
    )
    st.plotly_chart(fig_cpu_trend, use_container_width=True)

with col2:
    fig_memory_trend = go.Figure()
    fig_memory_trend.add_trace(go.Scatter(
        x=timestamps,
        y=memory_data,
        mode='lines+markers',
        name='Memory Usage %',
        line=dict(color='#00d4aa', width=3),
        marker=dict(size=4)
    ))
    # Update title based on time range
    if selected_time == "Current":
        title_text = "Memory Usage Trend (Live)"
    elif selected_time == "5min_ago":
        title_text = "Memory Usage Trend (Last 5 Minutes)"
    elif selected_time == "15min_ago":
        title_text = "Memory Usage Trend (Last 15 Minutes)"
    elif selected_time == "1hour_ago":
        title_text = "Memory Usage Trend (Last Hour)"
    elif selected_time == "6hours_ago":
        title_text = "Memory Usage Trend (Last 6 Hours)"
    else:
        title_text = "Memory Usage Trend (Last 24 Hours)"
    
    fig_memory_trend.update_layout(
        title=title_text,
        xaxis_title="Time",
        yaxis_title="Memory Usage (%)",
        height=300,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='#e9ecef'),
        yaxis=dict(showgrid=True, gridcolor='#e9ecef', range=[0, 100])
    )
    st.plotly_chart(fig_memory_trend, use_container_width=True)

# Node Health Table
if data_available:
    st.markdown(f'<div class="section-header">🖥️ Node Health Status - {time_description}</div>', unsafe_allow_html=True)
    
    # Show time context
    if time_preset != "Live (Now)":
        st.info(f"📅 **Time Context:** Showing node health for {display_date} from {start_time_12hr} to {end_time_12hr}")
else:
    st.markdown('<div class="section-header">🖥️ Node Health Status</div>', unsafe_allow_html=True)

if data_available and node_metrics:
    # Create node metrics dataframe
    node_data = []
    for node in node_metrics:
        cpu_percent = (node.get('cpu_usage', 0) / node.get('cpu_capacity', 1)) * 100
        memory_percent = (node.get('memory_usage', 0) / node.get('memory_capacity', 1)) * 100
        
        # Determine health status
        if cpu_percent < 70 and memory_percent < 70 and node.get('status') == 'Ready':
            health_status = "🟢 Healthy"
        elif cpu_percent > 80 or memory_percent > 80:
            health_status = "🔴 Critical"
        else:
            health_status = "🟡 Warning"
        
        node_data.append({
            'Node Name': node.get('name', 'Unknown'),
            'Status': node.get('status', 'Unknown'),
            'Health': health_status,
            'CPU Usage (%)': round(cpu_percent, 1),
            'Memory Usage (%)': round(memory_percent, 1),
            'CPU Cores': node.get('cpu_capacity', 0),
            'Memory (GB)': round(node.get('memory_capacity', 0) / (1024**3), 1),
            'Pods': node.get('pods', 0)
        })
    
    node_df = pd.DataFrame(node_data)
    
    # Display node table with better styling
    st.markdown('<div class="node-table">', unsafe_allow_html=True)
    st.dataframe(
        node_df,
        use_container_width=True,
        hide_index=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.warning("⚠️ **Node Health Unavailable:** Cannot display node health without historical data.")
    st.info("Please select a time range with available data to view node health information.")

# Quick Actions section removed

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 2rem; font-size: 0.9rem;">
    <p>🚀 Powered by SmartOps AI | Enterprise Kubernetes Monitoring</p>
    <p>Last updated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S IST') + """</p>
</div>
""", unsafe_allow_html=True)
