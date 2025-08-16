import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import requests
import json
from datetime import datetime, timedelta
import pytz
import kubernetes
from kubernetes import client, config
import os
import sqlite3
import io
import base64

# Import page modules
from pages.overview import create_overview_page
from pages.anomaly_detection import create_anomaly_detection_page
from pages.ai_actions import create_ai_actions_page
from pages.deployments import create_deployments_page
from pages.pod_explorer import create_pod_explorer_page
from pages.argocd_management import create_argocd_management_page

# Initialize Dash app with Bootstrap theme
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True,
    title="SmartOps AI Dashboard",
    update_title=None
)

# App configuration
app.config.suppress_callback_exceptions = True

# Custom CSS for stunning dark theme
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533483 100%);
                color: #ffffff;
                min-height: 100vh;
                overflow-x: hidden;
                position: relative;
            }
            
            body::before {
                content: '';
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: 
                    radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
                    radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
                    radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.2) 0%, transparent 50%);
                pointer-events: none;
                z-index: -1;
            }
            
            /* Stunning Header */
            .main-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
                padding: 4rem 3rem;
                border-radius: 30px;
                margin: 2rem 0;
                text-align: center;
                color: white;
                box-shadow: 
                    0 25px 80px rgba(102, 126, 234, 0.4),
                    0 0 0 1px rgba(255, 255, 255, 0.1);
                position: relative;
                overflow: hidden;
                backdrop-filter: blur(20px);
                width: 100%;
            }
            
            .main-header::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: 
                    url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="25" cy="25" r="0.5" fill="rgba(255,255,255,0.05)"/><circle cx="75" cy="75" r="0.5" fill="rgba(255,255,255,0.05)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
                opacity: 0.4;
                animation: float 20s ease-in-out infinite;
            }
            
            @keyframes float {
                0%, 100% { transform: translateY(0px) rotate(0deg); }
                50% { transform: translateY(-20px) rotate(180deg); }
            }
            
            .main-header h1 {
                font-size: 4rem;
                font-weight: 900;
                margin-bottom: 1.5rem;
                text-shadow: 0 8px 32px rgba(0,0,0,0.5);
                position: relative;
                z-index: 1;
                background: linear-gradient(45deg, #fff, #f0f0f0, #fff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                animation: glow 3s ease-in-out infinite alternate;
            }
            
            @keyframes glow {
                from { filter: drop-shadow(0 0 20px rgba(255,255,255,0.8)); }
                to { filter: drop-shadow(0 0 30px rgba(255,255,255,1)); }
            }
            
            .main-header p {
                font-size: 1.4rem;
                opacity: 0.95;
                position: relative;
                z-index: 1;
                font-weight: 300;
                letter-spacing: 0.5px;
            }
            
            /* Modern Cards */
            .metric-card {
                background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.05) 100%);
                backdrop-filter: blur(25px);
                border: 1px solid rgba(255,255,255,0.2);
                padding: 2.5rem 2rem;
                border-radius: 25px;
                color: white;
                text-align: center;
                box-shadow: 
                    0 15px 50px rgba(0,0,0,0.4),
                    0 0 0 1px rgba(255,255,255,0.1);
                margin: 1rem;
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
                overflow: hidden;
                cursor: pointer;
                height: 100%;
                min-height: 200px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            }
            
            .metric-card:hover {
                transform: translateY(-15px) scale(1.05);
                box-shadow: 
                    0 30px 80px rgba(0,0,0,0.5),
                    0 0 0 2px rgba(102, 126, 234, 0.8);
                border-color: rgba(102, 126, 234, 0.8);
            }
            
            .metric-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
                transition: left 0.8s;
            }
            
            .metric-card:hover::before {
                left: 100%;
            }
            
            .metric-card::after {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
                opacity: 0;
                transition: opacity 0.4s ease;
                pointer-events: none;
            }
            
            .metric-card:hover::after {
                opacity: 1;
            }
            
            .metric-card h3 {
                font-size: 3.5rem;
                font-weight: 800;
                margin-bottom: 0.5rem;
                background: linear-gradient(45deg, #667eea, #764ba2, #f093fb);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            .metric-card p {
                font-size: 1.1rem;
                opacity: 0.8;
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            /* Chart Containers */
            .chart-container {
                background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
                backdrop-filter: blur(25px);
                border: 1px solid rgba(255,255,255,0.2);
                padding: 2.5rem;
                border-radius: 25px;
                color: white;
                box-shadow: 
                    0 15px 50px rgba(0,0,0,0.4),
                    0 0 0 1px rgba(255,255,255,0.1);
                margin-bottom: 2rem;
                width: 100%;
                min-height: 400px;
            }
            
            /* Ensure full width for all columns */
            .row {
                width: 100%;
                margin-left: 0;
                margin-right: 0;
            }
            
            .col, .col-12 {
                padding-left: 0;
                padding-right: 0;
            }
            
            /* Animations */
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(40px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .fade-in-up {
                animation: fadeInUp 0.8s cubic-bezier(0.4, 0, 0.2, 1);
            }
            
            /* Chart container enhancements */
            .chart-container h3 {
                font-size: 1.8rem;
                font-weight: 700;
                margin-bottom: 1.5rem;
                color: #fff;
                text-align: center;
                position: relative;
            }
            
            .chart-container h3::after {
                content: '';
                position: absolute;
                bottom: -10px;
                left: 50%;
                transform: translateX(-50%);
                width: 60px;
                height: 3px;
                background: linear-gradient(90deg, #667eea, #764ba2);
                border-radius: 2px;
            }
            
            /* Responsive adjustments */
            @media (max-width: 1200px) {
                .content-area {
                    margin-left: 250px;
                    width: calc(100vw - 250px);
                    padding: 2rem;
                }
            }
            
            @media (max-width: 768px) {
                .sidebar {
                    width: 100%;
                    height: auto;
                    position: relative;
                }
                .content-area {
                    margin-left: 0;
                    width: 100vw;
                    padding: 1.5rem;
                }
                .main-header h1 {
                    font-size: 2.5rem;
                }
                .metric-card h3 {
                    font-size: 2.5rem;
                }
                .chart-container {
                    padding: 1.5rem;
                    margin-bottom: 1.5rem;
                }
            }
            
            /* Feature Grid */
            .feature-grid {
                margin: 2rem 0;
                width: 100%;
            }
            
            .feature-card {
                background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.05) 100%);
                backdrop-filter: blur(25px);
                border: 1px solid rgba(255,255,255,0.2);
                padding: 2.5rem 2rem;
                border-radius: 25px;
                color: white;
                text-align: center;
                box-shadow: 
                    0 15px 50px rgba(0,0,0,0.4),
                    0 0 0 1px rgba(255,255,255,0.1);
                margin: 1rem;
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
                overflow: hidden;
                cursor: pointer;
                height: 100%;
                min-height: 300px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            }
            
            .feature-card:hover {
                transform: translateY(-15px) scale(1.03);
                border-color: rgba(102, 126, 234, 0.6);
                box-shadow: 
                    0 30px 80px rgba(0,0,0,0.5),
                    0 0 0 2px rgba(102, 126, 234, 0.4);
            }
            
            .feature-card::after {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
                opacity: 0;
                transition: opacity 0.4s ease;
            }
            
            .feature-card:hover::after {
                opacity: 1;
            }
            
            .feature-icon {
                font-size: 3rem;
                margin-bottom: 1.5rem;
                display: block;
                background: linear-gradient(45deg, #667eea, #764ba2, #f093fb);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            .feature-title {
                font-size: 1.4rem;
                font-weight: 700;
                margin-bottom: 1rem;
                color: #fff;
            }
            
            .feature-desc {
                color: rgba(255,255,255,0.8);
                line-height: 1.6;
                margin-bottom: 1.5rem;
                font-size: 1rem;
            }
            
            /* Navigation */
            .sidebar {
                background: linear-gradient(180deg, rgba(0,0,0,0.9) 0%, rgba(26,26,46,0.95) 100%);
                backdrop-filter: blur(30px);
                border-right: 1px solid rgba(255,255,255,0.15);
                padding: 2.5rem 1.5rem;
                height: 100vh;
                position: fixed;
                left: 0;
                top: 0;
                width: 300px;
                z-index: 1000;
                box-shadow: 5px 0 30px rgba(0,0,0,0.5);
            }
            
            .nav-link {
                padding: 1.2rem 1.8rem;
                margin: 0.8rem 0;
                border-radius: 18px;
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                cursor: pointer;
                border: 1px solid transparent;
                color: rgba(255,255,255,0.8);
                font-weight: 500;
                position: relative;
                overflow: hidden;
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .nav-link:hover {
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.25) 0%, rgba(118, 75, 162, 0.25) 100%);
                border-color: rgba(102, 126, 234, 0.6);
                transform: translateX(12px);
                color: #fff;
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
            }
            
            .nav-link.active {
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.4) 0%, rgba(118, 75, 162, 0.4) 100%);
                border-color: rgba(102, 126, 234, 0.9);
                box-shadow: 0 8px 30px rgba(102, 126, 234, 0.4);
                color: #fff;
                transform: translateX(8px);
            }
            
            .nav-link::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
                transition: left 0.6s;
            }
            
            .nav-link:hover::before {
                left: 100%;
            }
            
            /* Tables */
            .table {
                background: rgba(255,255,255,0.05);
                backdrop-filter: blur(20px);
                border-radius: 20px;
                overflow: hidden;
                border: 1px solid rgba(255,255,255,0.1);
            }
            
            .table thead th {
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.3) 100%);
                color: #fff;
                font-weight: 600;
                padding: 1.2rem;
                border: none;
                text-transform: uppercase;
                letter-spacing: 1px;
                font-size: 0.9rem;
            }
            
            .table tbody td {
                padding: 1.2rem;
                border: none;
                color: rgba(255,255,255,0.9);
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }
            
            .table tbody tr:hover {
                background: rgba(255,255,255,0.05);
            }
            
            /* Buttons */
            .btn {
                border-radius: 12px;
                font-weight: 600;
                padding: 0.8rem 1.5rem;
                transition: all 0.3s ease;
                border: none;
                position: relative;
                overflow: hidden;
            }
            
            .btn::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
                transition: left 0.5s;
            }
            
            .btn:hover::before {
                left: 100%;
            }
            
            /* Scrollbar */
            ::-webkit-scrollbar {
                width: 8px;
            }
            
            ::-webkit-scrollbar-track {
                background: rgba(255,255,255,0.1);
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb {
                background: linear-gradient(135deg, #667eea, #764ba2);
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: linear-gradient(135deg, #764ba2, #f093fb);
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Initialize Kubernetes client
try:
    config.load_incluster_config()
except:
    try:
        config.load_kube_config()
    except:
        pass

# Global variables
DASHBOARD_URL = os.getenv('DASHBOARD_URL', 'http://localhost:8000')
DASHBOARD_EVENT_API = f"{DASHBOARD_URL}/log_event"

# Utility functions
def get_kubernetes_client():
    """Get Kubernetes client"""
    try:
        return client.CoreV1Api()
    except:
        return None

def get_namespaces():
    """Get list of namespaces"""
    try:
        k8s_client = get_kubernetes_client()
        if k8s_client:
            namespaces = k8s_client.list_namespace()
            return [ns.metadata.name for ns in namespaces.items]
        return ['smartops', 'default', 'kube-system']
    except:
        return ['smartops', 'default', 'kube-system']

def get_pods(namespace='all'):
    """Get pods from Kubernetes"""
    try:
        k8s_client = get_kubernetes_client()
        if not k8s_client:
            return []
        
        if namespace == 'all':
            pods = k8s_client.list_pod_for_all_namespaces()
        else:
            pods = k8s_client.list_namespaced_pod(namespace)
        
        pod_data = []
        for pod in pods.items:
            pod_data.append({
                'name': pod.metadata.name,
                'namespace': pod.metadata.namespace,
                'status': pod.status.phase,
                'node': pod.spec.node_name if pod.spec.node_name else 'N/A',
                'start_time': pod.status.start_time.isoformat() if pod.status.start_time else 'N/A',
                'restarts': sum(container.restart_count for container in pod.status.container_statuses) if pod.status.container_statuses else 0,
                'images': [container.image for container in pod.spec.containers] if pod.spec.containers else []
            })
        return pod_data
    except:
        return []

def get_anomalies():
    """Get anomalies from database"""
    try:
        conn = sqlite3.connect('/app/data/anomalies.db')
        df = pd.read_sql_query("SELECT * FROM anomalies ORDER BY timestamp DESC LIMIT 50", conn)
        conn.close()
        return df
    except:
        return pd.DataFrame()

def get_deployment_events():
    """Get deployment events from database"""
    try:
        conn = sqlite3.connect('/app/data/deployment_events.csv')
        df = pd.read_csv('/app/data/deployment_events.csv')
        return df
    except:
        return pd.DataFrame()

# Layout components
def create_header():
    """Create the main header"""
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1("🚀 SmartOps AI Dashboard", className="text-center mb-3"),
                html.P("AI-Driven DevOps Automation & Monitoring Platform", className="text-center lead")
            ])
        ], className="main-header")
    ], fluid=True)

def create_sidebar():
    """Create the sidebar navigation"""
    return dbc.Nav([
        dbc.NavLink("🏠 Overview", href="/", id="nav-overview", className="nav-link"),
        dbc.NavLink("🏠 Home", href="/home", id="nav-home", className="nav-link"),
        dbc.NavLink("🔥 Anomaly Detection", href="/anomaly-detection", id="nav-anomaly", className="nav-link"),
        dbc.NavLink("🤖 AI Actions", href="/ai-actions", id="nav-ai-actions", className="nav-link"),
        dbc.NavLink("🚀 Deployments", href="/deployments", id="nav-deployments", className="nav-link"),
        dbc.NavLink("🛰️ Pod Explorer", href="/pod-explorer", id="nav-pod-explorer", className="nav-link"),
        dbc.NavLink("🔍 Cluster Explorer", href="/cluster-explorer", id="nav-cluster-explorer", className="nav-link"),
        dbc.NavLink("🖥️ Kubernetes Shell", href="/k8s-shell", id="nav-k8s-shell", className="nav-link"),
        dbc.NavLink("⚖️ Auto-Scaling", href="/auto-scaling", id="nav-auto-scaling", className="nav-link"),
        dbc.NavLink("🕒 Incident Timeline", href="/incident-timeline", id="nav-incident-timeline", className="nav-link"),
        dbc.NavLink("🎯 ArgoCD Management", href="/argocd-management", id="nav-argocd-management", className="nav-link"),
    ], vertical=True, pills=True, className="sidebar")

def create_feature_cards():
    """Create feature cards for the main page"""
    cards = [
        {
            'icon': '🔥',
            'title': 'Anomaly Detection',
            'desc': 'AI-powered anomaly detection with top anomalies by CPU usage and recent anomaly tracking.',
            'href': '/anomaly-detection'
        },
        {
            'icon': '🤖',
            'title': 'AI Actions',
            'desc': 'AI recommendations and action history with model retraining capabilities.',
            'href': '/ai-actions'
        },
        {
            'icon': '🚀',
            'title': 'Deployments',
            'desc': 'Deployment workflow events tracking with success/failure statistics and metrics.',
            'href': '/deployments'
        },
        {
            'icon': '🛰️',
            'title': 'Pod Explorer',
            'desc': 'Pod management with real-time log viewing, filtering, and pod actions (restart, delete, describe).',
            'href': '/pod-explorer'
        },
        {
            'icon': '🔍',
            'title': 'Cluster Explorer',
            'desc': 'Safe kubectl-like queries for exploring cluster resources across namespaces.',
            'href': '/cluster-explorer'
        },
        {
            'icon': '🖥️',
            'title': 'Kubernetes Shell',
            'desc': 'Interactive kubectl command interface with command history and safe execution.',
            'href': '/k8s-shell'
        },
        {
            'icon': '🎯',
            'title': 'ArgoCD Management',
            'desc': 'GitOps deployment management with application monitoring and sync controls.',
            'href': '/argocd-management'
        }
    ]
    
    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div(card['icon'], className="feature-icon text-center"),
                    html.H5(card['title'], className="feature-title"),
                    html.P(card['desc'], className="feature-desc"),
                    dbc.Button("Go to " + card['title'], href=card['href'], color="primary", className="mt-2")
                ])
            ], className="feature-card clickable-card h-100")
        ], width=12, lg=6, xl=4, className="mb-4") for card in cards
    ], className="feature-grid")

# Main layout
app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='session-store'),
    
    # Header
    create_header(),
    
    dbc.Row([
        # Sidebar
        dbc.Col(create_sidebar(), width=3, className="sidebar"),
        
        # Main content
        dbc.Col([
            html.Div(id='page-content', className="content-area")
        ], width=9)
    ])
], fluid=True)

# Callback to update page content
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/' or pathname is None:
        return create_overview_page()
    elif pathname == '/home':
        return create_home_page()
    elif pathname == '/anomaly-detection':
        return create_anomaly_detection_page()
    elif pathname == '/ai-actions':
        return create_ai_actions_page()
    elif pathname == '/deployments':
        return create_deployments_page()
    elif pathname == '/pod-explorer':
        return create_pod_explorer_page()
    elif pathname == '/cluster-explorer':
        return create_cluster_explorer_page()
    elif pathname == '/k8s-shell':
        return create_k8s_shell_page()
    elif pathname == '/auto-scaling':
        return create_auto_scaling_page()
    elif pathname == '/incident-timeline':
        return create_incident_timeline_page()
    elif pathname == '/argocd-management':
        return create_argocd_management_page()
    else:
        return create_404_page()

def create_home_page():
    """Create the home page with feature cards"""
    return html.Div([
        # Header
        html.Div([
            html.H1("🚀 SmartOps AI Dashboard", className="text-center mb-4"),
            html.P("AI-Driven DevOps Automation & Monitoring Platform", 
                   className="text-center text-muted mb-5")
        ], className="main-header fade-in-up"),
        
        # Feature Cards
        html.Div([
            html.H2("🎯 Quick Access", className="text-center mb-5"),
            html.P("Click on any card below to navigate to the corresponding section, or use the sidebar for navigation.", 
                   className="text-center text-muted mb-5"),
            create_feature_cards()
        ], className="fade-in-up")
    ])



# These functions are now imported from the pages modules
# def create_ai_actions_page() and def create_deployments_page() are imported above

def create_pod_explorer_page():
    """Create the pod explorer page"""
    return dbc.Container([
        html.H2("🛰️ Pod Explorer & Logs", className="mb-4"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Pod Management"),
                    dbc.CardBody(id="pods-table")
                ])
            ])
        ])
    ], fluid=True)

def create_cluster_explorer_page():
    """Create the cluster explorer page"""
    return dbc.Container([
        html.H2("🔍 Cluster Explorer", className="mb-4"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Cluster Resources"),
                    dbc.CardBody(id="cluster-resources")
                ])
            ])
        ])
    ], fluid=True)

def create_k8s_shell_page():
    """Create the Kubernetes shell page"""
    return dbc.Container([
        html.H2("🖥️ Kubernetes Shell", className="mb-4"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Interactive kubectl"),
                    dbc.CardBody(id="k8s-shell")
                ])
            ])
        ])
    ], fluid=True)

def create_auto_scaling_page():
    """Create the auto-scaling page"""
    return dbc.Container([
        html.H2("⚖️ Auto-Scaling Recommendations & Control", className="mb-4"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("HPA Recommendations"),
                    dbc.CardBody(id="hpa-recommendations")
                ])
            ])
        ])
    ], fluid=True)

def create_incident_timeline_page():
    """Create the incident timeline page"""
    return dbc.Container([
        html.H2("🕒 Incident Timeline & Postmortem Report Generator", className="mb-4"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Incident Timeline"),
                    dbc.CardBody(id="incident-timeline")
                ])
            ])
        ])
    ], fluid=True)

def create_argocd_management_page():
    """Create the ArgoCD Management page"""
    return dbc.Container([
        html.H2("🎯 ArgoCD Management", className="mb-4"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("ArgoCD Applications"),
                    dbc.CardBody(id="argocd-applications")
                ])
            ])
        ])
    ], fluid=True)

def create_404_page():
    """Create 404 page"""
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1("404 - Page Not Found", className="text-center"),
                html.P("The page you're looking for doesn't exist.", className="text-center"),
                dbc.Button("Go to Home", href="/", color="primary", className="mt-3")
            ], className="text-center")
        ])
    ], fluid=True)

# Callback to update active nav link
@app.callback(
    [Output(f"nav-{page}", "active") for page in ["overview", "home", "anomaly", "ai-actions", "deployments", "pod-explorer", "cluster-explorer", "k8s-shell", "auto-scaling", "incident-timeline", "argocd-management"]],
    Input('url', 'pathname')
)
def update_active_nav(pathname):
    active_states = [False] * 11
    
    if pathname == '/' or pathname is None:
        active_states[0] = True
    elif pathname == '/home':
        active_states[1] = True
    elif pathname == '/anomaly-detection':
        active_states[2] = True
    elif pathname == '/ai-actions':
        active_states[3] = True
    elif pathname == '/deployments':
        active_states[4] = True
    elif pathname == '/pod-explorer':
        active_states[5] = True
    elif pathname == '/cluster-explorer':
        active_states[6] = True
    elif pathname == '/k8s-shell':
        active_states[7] = True
    elif pathname == '/auto-scaling':
        active_states[8] = True
    elif pathname == '/incident-timeline':
        active_states[9] = True
    elif pathname == '/argocd-management':
        active_states[10] = True
    
    return active_states

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8501)
