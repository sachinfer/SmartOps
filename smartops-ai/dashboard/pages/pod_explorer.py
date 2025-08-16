import dash
from dash import dcc, html, Input, Output, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_pod_explorer_page():
    """Create the Pod Explorer page with stunning UI and interactive features"""
    
    # Mock pod data
    pods_data = [
        {"name": "smartops-dashboard-689f978896-t9zzt", "status": "Running", "namespace": "smartops", "node": "gke-node-1", "restarts": 0, "age": "2m"},
        {"name": "smartops-app-6f6f5b8898-ndwrc", "status": "Running", "namespace": "smartops", "node": "gke-node-2", "restarts": 0, "age": "5m"},
        {"name": "anomaly-deployment-74966567f4-7jrvb", "status": "Running", "namespace": "smartops", "node": "gke-node-1", "restarts": 0, "age": "8m"},
        {"name": "monitor-67d4674568-w7v76", "status": "Running", "namespace": "smartops", "node": "gke-node-2", "restarts": 0, "age": "2h"},
        {"name": "api-gateway-5f8d9c2b1a", "status": "Failed", "namespace": "smartops", "node": "gke-node-1", "restarts": 3, "age": "15m"}
    ]
    
    # Pod status distribution
    status_counts = pd.Series([pod['status'] for pod in pods_data]).value_counts()
    status_fig = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title="Pod Status Distribution",
        color_discrete_map={
            'Running': '#00b894',
            'Failed': '#ff6b6b',
            'Pending': '#fdcb6e',
            'Terminating': '#e17055'
        }
    )
    status_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    # Pod resource usage chart
    resource_data = pd.DataFrame({
        'pod': [pod['name'] for pod in pods_data],
        'cpu_usage': np.random.uniform(20, 80, len(pods_data)),
        'memory_usage': np.random.uniform(30, 90, len(pods_data))
    })
    
    resource_fig = go.Figure()
    resource_fig.add_trace(go.Bar(
        x=resource_data['pod'],
        y=resource_data['cpu_usage'],
        name='CPU Usage %',
        marker_color='#667eea'
    ))
    resource_fig.add_trace(go.Bar(
        x=resource_data['pod'],
        y=resource_data['memory_usage'],
        name='Memory Usage %',
        marker_color='#00b894'
    ))
    resource_fig.update_layout(
        title="Pod Resource Usage",
        xaxis_title="Pod Name",
        yaxis_title="Usage %",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        barmode='group'
    )
    
    # Pods Table
    pods_table = dbc.Table([
        html.Thead([
            html.Tr([
                html.Th("Pod Name", className="text-white"),
                html.Th("Status", className="text-white"),
                html.Th("Namespace", className="text-white"),
                html.Th("Node", className="text-white"),
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
                            "Terminating": "secondary"
                        }[pod["status"]],
                        className="text-white"
                    )
                ),
                html.Td(pod["namespace"]),
                html.Td(pod["node"]),
                html.Td(pod["restarts"]),
                html.Td(pod["age"]),
                html.Td(
                    dbc.ButtonGroup([
                        dbc.Button("Logs", size="sm", color="info", outline=True),
                        dbc.Button("Restart", size="sm", color="warning", outline=True),
                        dbc.Button("Delete", size="sm", color="danger", outline=True)
                    ])
                )
            ]) for pod in pods_data
        ])
    ], className="text-white", bordered=True, dark=True)
    
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
                        html.H3("5", className="display-4 text-primary"),
                        html.P("Total Pods", className="text-muted")
                    ], className="metric-card text-center")
                ], width=3),
                dbc.Col([
                    html.Div([
                        html.H3("4", className="display-4 text-success"),
                        html.P("Running", className="text-muted")
                    ], className="metric-card text-center")
                ], width=3),
                dbc.Col([
                    html.Div([
                        html.H3("1", className="display-4 text-danger"),
                        html.P("Failed", className="text-muted")
                    ], className="metric-card text-center")
                ], width=3),
                dbc.Col([
                    html.Div([
                        html.H3("2", className="display-4 text-info"),
                        html.P("Nodes", className="text-muted")
                    ], className="metric-card text-center")
                ], width=3)
            ])
        ], className="mb-5 fade-in-up"),
        
        # Charts Row
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("📊 Resource Usage", className="mb-4"),
                    dcc.Graph(figure=resource_fig, config={'displayModeBar': False})
                ], className="chart-container")
            ], width=8),
            dbc.Col([
                html.Div([
                    html.H3("🥧 Status Distribution", className="mb-4"),
                    dcc.Graph(figure=status_fig, config={'displayModeBar': False})
                ], className="chart-container")
            ], width=4)
        ], className="mb-5 fade-in-up"),
        
        # Pods Table
        html.Div([
            html.H3("📋 Pod Details", className="mb-4"),
            pods_table
        ], className="chart-container fade-in-up"),
        
        # Pod Management Controls
        html.Div([
            html.H3("🎮 Pod Management", className="mb-4"),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("🔍 Pod Search", className="card-title"),
                            html.P("Search pods by name, namespace, or status", className="card-text"),
                            dbc.Input(placeholder="Search pods...", type="text", className="mt-3")
                        ])
                    ], className="bg-dark text-white border-info")
                ], width=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("📝 Log Viewer", className="card-title"),
                            html.P("View real-time pod logs", className="card-text"),
                            dbc.Button("Open Logs", color="info", className="mt-3")
                        ])
                    ], className="bg-dark text-white border-success")
                ], width=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("⚡ Quick Actions", className="card-title"),
                            html.P("Restart, scale, or delete pods", className="card-text"),
                            dbc.Button("Manage", color="warning", className="mt-3")
                        ])
                    ], className="bg-dark text-white border-warning")
                ], width=4)
            ])
        ], className="chart-container fade-in-up")
    ])
