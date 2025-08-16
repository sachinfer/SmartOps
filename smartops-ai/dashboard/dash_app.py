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
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
                color: #ffffff;
                min-height: 100vh;
                overflow-x: hidden;
            }
            
            /* Stunning Header */
            .main-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
                padding: 3rem 2rem;
                border-radius: 20px;
                margin: 2rem;
                text-align: center;
                color: white;
                box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
                position: relative;
                overflow: hidden;
            }
            
            .main-header::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
                opacity: 0.3;
            }
            
            .main-header h1 {
                font-size: 3rem;
                font-weight: 700;
                margin-bottom: 1rem;
                text-shadow: 0 4px 20px rgba(0,0,0,0.3);
                position: relative;
                z-index: 1;
            }
            
            .main-header p {
                font-size: 1.2rem;
                opacity: 0.9;
                position: relative;
                z-index: 1;
            }
            
            /* Modern Cards */
            .metric-card {
                background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255,255,255,0.2);
                padding: 2rem;
                border-radius: 20px;
                color: white;
                text-align: center;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
                margin: 1rem;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
                overflow: hidden;
            }
            
            .metric-card:hover {
                transform: translateY(-8px) scale(1.02);
                box-shadow: 0 20px 60px rgba(0,0,0,0.4);
                border-color: rgba(102, 126, 234, 0.5);
            }
            
            .metric-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
                transition: left 0.5s;
            }
            
            .metric-card:hover::before {
                left: 100%;
            }
            
            /* Alert Banners */
            .alert-banner {
                background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
                padding: 2rem;
                border-radius: 20px;
                color: white;
                margin: 1.5rem;
                box-shadow: 0 8px 32px rgba(255,107,107,0.4);
                border: 1px solid rgba(255,255,255,0.2);
            }
            
            .success-banner {
                background: linear-gradient(135deg, #00b894 0%, #00a085 100%);
                padding: 2rem;
                border-radius: 20px;
                color: white;
                margin: 1.5rem;
                box-shadow: 0 8px 32px rgba(0,184,148,0.4);
                border: 1px solid rgba(255,255,255,0.2);
            }
            
            /* Chart Containers */
            .chart-container {
                background: rgba(255,255,255,0.05);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255,255,255,0.1);
                padding: 2rem;
                border-radius: 20px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
                margin: 1.5rem;
                transition: all 0.3s ease;
            }
            
            .chart-container:hover {
                border-color: rgba(102, 126, 234, 0.3);
                box-shadow: 0 12px 40px rgba(0,0,0,0.4);
            }
            
            /* Feature Grid */
            .feature-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                gap: 2rem;
                margin: 2rem;
                padding: 0 1rem;
            }
            
            .feature-card {
                background: rgba(255,255,255,0.05);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255,255,255,0.1);
                padding: 2rem;
                border-radius: 20px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                cursor: pointer;
                position: relative;
                overflow: hidden;
            }
            
            .feature-card:hover {
                transform: translateY(-8px) scale(1.02);
                border-color: rgba(102, 126, 234, 0.5);
                box-shadow: 0 20px 60px rgba(0,0,0,0.4);
            }
            
            .feature-card::after {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
                opacity: 0;
                transition: opacity 0.3s ease;
            }
            
            .feature-card:hover::after {
                opacity: 1;
            }
            
            /* Navigation */
            .sidebar {
                background: rgba(0,0,0,0.8);
                backdrop-filter: blur(20px);
                border-right: 1px solid rgba(255,255,255,0.1);
                padding: 2rem 1rem;
                height: 100vh;
                position: fixed;
                left: 0;
                top: 0;
                width: 280px;
                z-index: 1000;
            }
            
            .nav-item {
                padding: 1rem 1.5rem;
                margin: 0.5rem 0;
                border-radius: 15px;
                transition: all 0.3s ease;
                cursor: pointer;
                border: 1px solid transparent;
            }
            
            .nav-item:hover {
                background: rgba(102, 126, 234, 0.2);
                border-color: rgba(102, 126, 234, 0.5);
                transform: translateX(8px);
            }
            
            .nav-item.active {
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.3) 100%);
                border-color: rgba(102, 126, 234, 0.8);
                box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
            }
            
            /* Content Area */
            .content-area {
                margin-left: 280px;
                padding: 2rem;
                min-height: 100vh;
            }
            
            /* Animations */
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
            
            .fade-in-up {
                animation: fadeInUp 0.6s ease-out;
            }
            
            /* Responsive */
            @media (max-width: 768px) {
                .sidebar {
                    width: 100%;
                    height: auto;
                    position: relative;
                }
                .content-area {
                    margin-left: 0;
                }
                .main-header h1 {
                    font-size: 2rem;
                }
            }
        </style>
            .feature-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);
                border-color: #667eea;
            }
            .feature-card:active {
                transform: translateY(-2px);
            }
            .feature-icon {
                font-size: 2rem;
                margin-bottom: 1rem;
            }
            .feature-title {
                font-size: 1.2rem;
                font-weight: bold;
                margin-bottom: 0.5rem;
                color: #2c3e50;
            }
            .feature-desc {
                color: #666;
                line-height: 1.5;
            }
            .clickable-card {
                cursor: pointer;
                user-select: none;
            }
            .sidebar {
                background: #f8f9fa;
                padding: 1rem;
                border-right: 1px solid #dee2e6;
            }
            .content-area {
                padding: 2rem;
            }
            .nav-link {
                color: #495057;
                padding: 0.75rem 1rem;
                border-radius: 0.375rem;
                margin-bottom: 0.25rem;
                transition: all 0.2s ease;
            }
            .nav-link:hover {
                background-color: #e9ecef;
                color: #212529;
            }
            .nav-link.active {
                background-color: #667eea;
                color: white;
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
        ], width=6, lg=4) for card in cards
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
    else:
        return create_404_page()

def create_home_page():
    """Create the home page with feature cards"""
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H2("🎯 Quick Access", className="mb-4"),
                html.P("Click on any card below to navigate to the corresponding section, or use the sidebar for navigation.", className="mb-4")
            ])
        ]),
        create_feature_cards()
    ], fluid=True)



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
    [Output(f"nav-{page}", "active") for page in ["overview", "home", "anomaly", "ai-actions", "deployments", "pod-explorer", "cluster-explorer", "k8s-shell", "auto-scaling", "incident-timeline"]],
    Input('url', 'pathname')
)
def update_active_nav(pathname):
    active_states = [False] * 10
    
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
    
    return active_states

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8501)
