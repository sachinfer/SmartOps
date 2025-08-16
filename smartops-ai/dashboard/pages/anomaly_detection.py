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

def create_anomaly_detection_page():
    """Create the Anomaly Detection page"""
    
    # Mock data for demonstration
    anomalies_data = [
        {
            'timestamp': '2024-01-15 14:30:00',
            'pod_name': 'smartops-app-abc123',
            'cpu_usage': 95.2,
            'memory_usage': 87.5,
            'anomaly_score': 0.92,
            'status': 'High CPU Usage'
        },
        {
            'timestamp': '2024-01-15 14:25:00',
            'pod_name': 'smartops-anomaly-def456',
            'cpu_usage': 78.3,
            'memory_usage': 92.1,
            'anomaly_score': 0.85,
            'status': 'High Memory Usage'
        },
        {
            'timestamp': '2024-01-15 14:20:00',
            'pod_name': 'smartops-dashboard-ghi789',
            'cpu_usage': 45.7,
            'memory_usage': 65.2,
            'anomaly_score': 0.72,
            'status': 'Moderate Anomaly'
        }
    ]
    
    # Create a timeline figure
    timeline_fig = go.Figure([
        go.Scatter(
            x=[anomaly['timestamp'] for anomaly in anomalies_data],
            y=[anomaly['anomaly_score'] for anomaly in anomalies_data],
            mode='lines+markers',
            name='Anomaly Score',
            line=dict(color='red', width=2),
            marker=dict(size=8)
        )
    ]).update_layout(
        xaxis_title="Time",
        yaxis_title="Anomaly Score",
        height=400
    )

    # Create a table for recent anomalies
    anomalies_table = dbc.Table([
        html.Thead([
            html.Tr([
                html.Th("Timestamp"),
                html.Th("Pod Name"),
                html.Th("CPU (%)"),
                html.Th("Memory (%)"),
                html.Th("Anomaly Score"),
                html.Th("Status")
            ])
        ]),
        html.Tbody([
            html.Tr([
                html.Td(anomaly['timestamp']),
                html.Td(anomaly['pod_name']),
                html.Td(f"{anomaly['cpu_usage']:.1f}"),
                html.Td(f"{anomaly['memory_usage']:.1f}"),
                html.Td(f"{anomaly['anomaly_score']:.2f}"),
                html.Td(
                    dbc.Badge(
                        anomaly['status'],
                        color="danger" if anomaly['anomaly_score'] > 0.8 else "warning"
                    )
                )
            ]) for anomaly in anomalies_data
        ])
    ], striped=True, bordered=True, hover=True)

    return dbc.Container([
        # Page Header
        dbc.Row([
            dbc.Col([
                html.H2("🔥 Anomaly Detection", className="mb-4"),
                html.P("AI-powered anomaly detection and analysis", className="text-muted")
            ])
        ]),
        
        # Anomaly Statistics
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H3(f"{len(anomalies_data)}", className="text-danger text-center"),
                        html.P("Active Anomalies", className="text-center text-muted mb-0")
                    ])
                ], className="text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H3("0.89", className="text-warning text-center"),
                        html.P("Avg Anomaly Score", className="text-center text-muted mb-0")
                    ])
                ], className="text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H3("3", className="text-info text-center"),
                        html.P("Pods Monitored", className="text-center text-muted mb-0")
                    ])
                ], className="text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H3("24h", className="text-success text-center"),
                        html.P("Monitoring Period", className="text-center text-muted mb-0")
                    ])
                ], className="text-center")
            ], width=3)
        ], className="mb-4"),
        
        # Charts Row
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("📊 Anomaly Score Timeline", className="mb-4"),
                    dcc.Graph(figure=timeline_fig, config={'displayModeBar': False})
                ], className="chart-container")
            ], width=12, className="mb-4")
        ], className="mb-5 fade-in-up"),
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("🔍 Recent Anomalies", className="mb-4"),
                    anomalies_table
                ], className="chart-container")
            ], width=12, className="mb-4")
        ], className="mb-5 fade-in-up"),
        
        # Actions
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
                                dbc.Button("📊 View Details", color="info", className="w-100 mb-2")
                            ], width=4),
                            dbc.Col([
                                dbc.Button("⚙️ Configure Alerts", color="warning", className="w-100 mb-2")
                            ], width=4)
                        ])
                    ])
                ])
            ])
        ])
    ], fluid=True)
