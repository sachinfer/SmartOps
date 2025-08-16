import dash
from dash import dcc, html, Input, Output, callback_context, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import kubernetes
from kubernetes import client, config
import os

def create_pod_explorer_page():
    """Create the Pod Explorer page with real Kubernetes data and interactive features"""
    
    # Initialize Kubernetes client
    try:
        config.load_incluster_config()
        k8s_client = client.CoreV1Api()
    except:
        try:
            config.load_kube_config()
            k8s_client = client.CoreV1Api()
        except:
            k8s_client = None
    
    def get_real_pods():
        """Get real pods from Kubernetes cluster"""
        if not k8s_client:
            return []
        
        try:
            pods = k8s_client.list_pod_for_all_namespaces()
            pod_data = []
            
            for pod in pods.items:
                # Get container statuses
                container_statuses = pod.status.container_statuses or []
                total_restarts = sum(container.restart_count for container in container_statuses)
                
                # Calculate age
                if pod.status.start_time:
                    age = datetime.now(pod.status.start_time.tzinfo) - pod.status.start_time
                    if age.days > 0:
                        age_str = f"{age.days}d"
                    elif age.seconds > 3600:
                        age_str = f"{age.seconds // 3600}h"
                    elif age.seconds > 60:
                        age_str = f"{age.seconds // 60}m"
                    else:
                        age_str = f"{age.seconds}s"
                else:
                    age_str = "N/A"
                
                pod_data.append({
                    "name": pod.metadata.name,
                    "status": pod.status.phase,
                    "namespace": pod.metadata.namespace,
                    "node": pod.spec.node_name if pod.spec.node_name else 'N/A',
                    "restarts": total_restarts,
                    "age": age_str,
                    "ready": f"{len([c for c in container_statuses if c.ready])}/{len(container_statuses)}" if container_statuses else "0/0",
                    "ip": pod.status.pod_ip if pod.status.pod_ip else 'N/A',
                    "qos": pod.status.qos_class if pod.status.qos_class else 'N/A'
                })
            
            return pod_data
        except Exception as e:
            print(f"Error getting pods: {e}")
            return []
    
    # Get real pod data
    pods_data = get_real_pods()
    
    # Create status distribution chart
    if pods_data:
        status_counts = pd.Series([pod['status'] for pod in pods_data]).value_counts()
        status_fig = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Pod Status Distribution",
            color_discrete_map={
                'Running': '#00b894',
                'Failed': '#ff6b6b',
                'Pending': '#fdcb6e',
                'Terminating': '#e17055',
                'Succeeded': '#74b9ff',
                'Unknown': '#636e72'
            }
        )
        status_fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=400
        )
        
        # Create namespace distribution chart
        namespace_counts = pd.Series([pod['namespace'] for pod in pods_data]).value_counts()
        namespace_fig = px.bar(
            x=namespace_counts.index,
            y=namespace_counts.values,
            title="Pods by Namespace",
            color_discrete_sequence=['#667eea']
        )
        namespace_fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis_title="Namespace",
            yaxis_title="Number of Pods",
            height=400
        )
    else:
        status_fig = px.pie(values=[1], names=['No Data'], title="No Pods Found")
        status_fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        namespace_fig = px.bar(x=[], y=[], title="No Pods Found")
        namespace_fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    
    # Create interactive pods table
    if pods_data:
        pods_table = dbc.Table([
            html.Thead([
                html.Tr([
                    html.Th("Pod Name", className="text-white"),
                    html.Th("Status", className="text-white"),
                    html.Th("Namespace", className="text-white"),
                    html.Th("Node", className="text-white"),
                    html.Th("Ready", className="text-white"),
                    html.Th("Restarts", className="text-white"),
                    html.Th("Age", className="text-white"),
                    html.Th("Actions", className="text-white")
                ])
            ]),
            html.Tbody([
                html.Tr([
                    html.Td(pod["name"]),
                    html.Td(
                        dbc.Badge(
                            pod["status"],
                            color={
                                "Running": "success",
                                "Failed": "danger",
                                "Pending": "warning",
                                "Terminating": "secondary",
                                "Succeeded": "info",
                                "Unknown": "dark"
                            }.get(pod["status"], "secondary"),
                            className="text-white"
                        )
                    ),
                    html.Td(pod["namespace"]),
                    html.Td(pod["node"]),
                    html.Td(pod["ready"]),
                    html.Td(pod["restarts"]),
                    html.Td(pod["age"]),
                    html.Td(
                        dbc.ButtonGroup([
                            dbc.Button("📋 Describe", size="sm", color="info", outline=True, id=f"describe-{pod['name']}"),
                            dbc.Button("📝 Logs", size="sm", color="success", outline=True, id=f"logs-{pod['name']}"),
                            dbc.Button("🔄 Restart", size="sm", color="warning", outline=True, id=f"restart-{pod['name']}"),
                            dbc.Button("❌ Delete", size="sm", color="danger", outline=True, id=f"delete-{pod['name']}")
                        ])
                    )
                ]) for pod in pods_data
            ])
        ], className="text-white", bordered=True, dark=True, responsive=True)
    else:
        pods_table = html.Div([
            html.H4("No Pods Found", className="text-center text-muted"),
            html.P("Unable to connect to Kubernetes cluster or no pods are running.", className="text-center text-muted")
        ], className="text-center p-5")
    
    return html.Div([
        # Header
        html.Div([
            html.H1("🛰️ Pod Explorer & Management", className="text-center mb-4"),
            html.P("Monitor and manage your Kubernetes pods with real-time insights", 
                   className="text-center text-muted mb-5")
        ], className="main-header fade-in-up"),
        
        # Pod Stats Cards
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H3(str(len(pods_data)), className="display-4 text-primary"),
                        html.P("Total Pods", className="text-muted")
                    ], className="metric-card text-center")
                ], width=3),
                dbc.Col([
                    html.Div([
                        html.H3(str(len([p for p in pods_data if p['status'] == 'Running'])), className="display-4 text-success"),
                        html.P("Running", className="text-muted")
                    ], className="metric-card text-center")
                ], width=3),
                dbc.Col([
                    html.Div([
                        html.H3(str(len([p for p in pods_data if p['status'] in ['Failed', 'Pending']])), className="display-4 text-danger"),
                        html.P("Issues", className="text-muted")
                    ], className="metric-card text-center")
                ], width=3),
                dbc.Col([
                    html.Div([
                        html.H3(str(len(set(p['namespace'] for p in pods_data))), className="display-4 text-info"),
                        html.P("Namespaces", className="text-muted")
                    ], className="metric-card text-center")
                ], width=3)
            ])
        ], className="mb-5 fade-in-up"),
        
        # Charts Row
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("📊 Pod Status Distribution", className="mb-4"),
                    dcc.Graph(figure=status_fig, config={'displayModeBar': False})
                ], className="chart-container")
            ], width=12, className="mb-4")
        ], className="mb-5 fade-in-up"),
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("🏗️ Pods by Namespace", className="mb-4"),
                    dcc.Graph(figure=namespace_fig, config={'displayModeBar': False})
                ], className="chart-container")
            ], width=12, className="mb-4")
        ], className="mb-5 fade-in-up"),
        
        # Pod Management Controls
        html.Div([
            html.H3("🎮 Pod Management", className="mb-4"),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("🔍 Pod Search", className="card-title"),
                            html.P("Search pods by name, namespace, or status", className="card-text"),
                            dbc.Input(
                                id="pod-search-input",
                                placeholder="Search pods...", 
                                type="text", 
                                className="mt-3"
                            )
                        ])
                    ], className="bg-dark text-white border-info")
                ], width=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("📝 Log Viewer", className="card-title"),
                            html.P("View real-time pod logs", className="card-text"),
                            dbc.Button(
                                "Open Logs", 
                                color="info", 
                                className="mt-3",
                                id="open-logs-btn"
                            )
                        ])
                    ], className="bg-dark text-white border-success")
                ], width=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("⚡ Quick Actions", className="card-title"),
                            html.P("Restart, scale, or delete pods", className="card-text"),
                            dbc.Button(
                                "Manage", 
                                color="warning", 
                                className="mt-3",
                                id="manage-pods-btn"
                            )
                        ])
                    ], className="bg-dark text-white border-warning")
                ], width=4)
            ])
        ], className="chart-container fade-in-up mb-5"),
        
        # Pods Table
        html.Div([
            html.H3("📋 Pod Details", className="mb-4"),
            html.Div([
                dbc.Button("🔄 Refresh Pods", color="primary", className="mb-3", id="refresh-pods-btn"),
                html.Span(f"Last updated: {datetime.now().strftime('%H:%M:%S')}", className="text-muted ml-3")
            ]),
            pods_table
        ], className="chart-container fade-in-up"),
        
        # Pod Details Modal
        dbc.Modal([
            dbc.ModalHeader("Pod Details"),
            dbc.ModalBody(id="pod-details-content"),
            dbc.ModalFooter([
                dbc.Button("Close", id="close-pod-modal", className="ms-auto")
            ])
        ], id="pod-details-modal", size="lg"),
        
        # Logs Modal
        dbc.Modal([
            dbc.ModalHeader("Pod Logs"),
            dbc.ModalBody(id="pod-logs-content"),
            dbc.ModalFooter([
                dbc.Button("Close", id="close-logs-modal", className="ms-auto")
            ])
        ], id="pod-logs-modal", size="xl")
    ])
