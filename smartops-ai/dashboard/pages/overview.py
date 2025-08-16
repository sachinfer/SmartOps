import dash
from dash import dcc, html, Input, Output, callback_context
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

def create_overview_page():
    """Create the Overview page with cluster health and metrics"""
    
    # Mock data for demonstration (replace with real data)
    cluster_health_score = 85
    total_nodes = 3
    total_pods = 12
    total_services = 8
    total_namespaces = 5
    
    # Pod status summary
    pod_status = {
        'Running': 10,
        'Pending': 1,
        'Failed': 1,
        'Total': 12
    }
    
    # Resource usage
    cpu_usage = 65
    memory_usage = 78
    
    # Node health data
    node_data = [
        {'name': 'gke-cluster-1-default-pool-abc123', 'cpu': 45, 'memory': 60, 'pods': 4, 'status': 'Healthy'},
        {'name': 'gke-cluster-1-default-pool-def456', 'cpu': 75, 'memory': 85, 'pods': 5, 'status': 'Warning'},
        {'name': 'gke-cluster-1-default-pool-ghi789', 'cpu': 35, 'memory': 50, 'pods': 3, 'status': 'Healthy'}
    ]
    
    # Determine health status color
    if cluster_health_score >= 80:
        health_color = "success"
        health_text = "Excellent"
    elif cluster_health_score >= 60:
        health_color = "warning"
        health_text = "Good"
    else:
        health_color = "danger"
        health_text = "Needs Attention"
    
    return dbc.Container([
        # Page Header
        dbc.Row([
            dbc.Col([
                html.H2("🏠 Cluster Overview", className="mb-4"),
                html.P("Real-time cluster health status and resource usage overview", className="text-muted")
            ])
        ]),
        
        # Overall Cluster Health Status
        dbc.Row([
            dbc.Col([
                dbc.Alert([
                    html.H4(f"Cluster Health Score: {cluster_health_score}%", className="alert-heading"),
                    html.P(f"Status: {health_text}", className="mb-0")
                ], color=health_color, className="text-center")
            ])
        ], className="mb-4"),
        
        # Cluster Statistics
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H3(f"{total_nodes}", className="text-center text-primary"),
                        html.P("Nodes", className="text-center text-muted mb-0")
                    ])
                ], className="text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H3(f"{total_pods}", className="text-center text-success"),
                        html.P("Pods", className="text-center text-muted mb-0")
                    ])
                ], className="text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H3(f"{total_services}", className="text-center text-info"),
                        html.P("Services", className="text-center text-muted mb-0")
                    ])
                ], className="text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H3(f"{total_namespaces}", className="text-center text-warning"),
                        html.P("Namespaces", className="text-center text-muted mb-0")
                    ])
                ], className="text-center")
            ], width=3)
        ], className="mb-4"),
        
        # Pod Status Summary
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Pod Status Summary"),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.H4(f"{pod_status['Running']}", className="text-success text-center"),
                                html.P("Running", className="text-center text-muted mb-0")
                            ], width=3),
                            dbc.Col([
                                html.H4(f"{pod_status['Pending']}", className="text-warning text-center"),
                                html.P("Pending", className="text-center text-muted mb-0")
                            ], width=3),
                            dbc.Col([
                                html.H4(f"{pod_status['Failed']}", className="text-danger text-center"),
                                html.P("Failed", className="text-center text-muted mb-0")
                            ], width=3),
                            dbc.Col([
                                html.H4(f"{pod_status['Total']}", className="text-primary text-center"),
                                html.P("Total", className="text-center text-muted mb-0")
                            ], width=3)
                        ])
                    ])
                ])
            ])
        ], className="mb-4"),
        
        # Charts Row
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("📊 Cluster Health Overview", className="mb-4"),
                    dcc.Graph(figure=health_fig, config={'displayModeBar': False})
                ], className="chart-container")
            ], width=12, className="mb-4")
        ], className="mb-5 fade-in-up"),
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("🏗️ Resource Usage Trends", className="mb-4"),
                    dcc.Graph(figure=resource_fig, config={'displayModeBar': False})
                ], className="chart-container")
            ], width=12, className="mb-4")
        ], className="mb-5 fade-in-up"),
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("📈 Node Performance", className="mb-4"),
                    dcc.Graph(figure=node_fig, config={'displayModeBar': False})
                ], className="chart-container")
            ], width=12, className="mb-4")
        ], className="mb-5 fade-in-up"),
        
        # Node Health Status
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Node Health Status"),
                    dbc.CardBody([
                        dbc.Table([
                            html.Thead([
                                html.Tr([
                                    html.Th("Node Name"),
                                    html.Th("CPU (%)"),
                                    html.Th("Memory (%)"),
                                    html.Th("Pods"),
                                    html.Th("Status")
                                ])
                            ]),
                            html.Tbody([
                                html.Tr([
                                    html.Td(node['name']),
                                    html.Td(node['cpu']),
                                    html.Td(node['memory']),
                                    html.Td(node['pods']),
                                    html.Td(
                                        dbc.Badge(
                                            node['status'],
                                            color="success" if node['status'] == 'Healthy' else "warning"
                                        )
                                    )
                                ]) for node in node_data
                            ])
                        ], striped=True, bordered=True, hover=True)
                    ])
                ])
            ])
        ], className="mb-4"),
        
        # Quick Actions
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Quick Actions"),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                dbc.Button("🔄 Refresh Data", color="primary", className="w-100 mb-2")
                            ], width=4),
                            dbc.Col([
                                dbc.Button("🔥 Anomaly Detection", color="warning", className="w-100 mb-2")
                            ], width=4),
                            dbc.Col([
                                dbc.Button("🤖 AI Actions", color="info", className="w-100 mb-2")
                            ], width=4)
                        ])
                    ])
                ])
            ])
        ])
    ], fluid=True)
