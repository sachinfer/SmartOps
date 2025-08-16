import dash
from dash import dcc, html, Input, Output, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_deployments_page():
    """Create the Deployments page with stunning UI and interactive features"""
    
    # Mock deployment data
    deployments_data = [
        {"name": "smartops-dashboard", "status": "success", "timestamp": "2 min ago", "version": "v2.1.0", "environment": "production"},
        {"name": "smartops-app", "status": "success", "timestamp": "5 min ago", "version": "v1.8.2", "environment": "staging"},
        {"name": "anomaly-detection", "status": "running", "timestamp": "8 min ago", "version": "v1.5.1", "environment": "production"},
        {"name": "monitor-service", "status": "success", "timestamp": "15 min ago", "version": "v1.2.0", "environment": "production"},
        {"name": "api-gateway", "status": "failed", "timestamp": "25 min ago", "version": "v2.0.1", "environment": "staging"}
    ]
    
    # Deployment timeline data
    timeline_data = pd.DataFrame({
        'time': pd.date_range(start='2024-01-01', periods=48, freq='H'),
        'deployments': np.random.poisson(2, 48),
        'success_rate': np.random.normal(0.92, 0.08, 48)
    })
    
    # Deployment Timeline Chart
    timeline_fig = go.Figure()
    timeline_fig.add_trace(go.Scatter(
        x=timeline_data['time'],
        y=timeline_data['deployments'],
        name='Deployments',
        line=dict(color='#667eea', width=3),
        fill='tonexty',
        fillcolor='rgba(102, 126, 234, 0.2)'
    ))
    timeline_fig.add_trace(go.Scatter(
        x=timeline_data['time'],
        y=timeline_data['success_rate'] * 10,
        name='Success Rate (x10)',
        line=dict(color='#00b894', width=3),
        yaxis='y2'
    ))
    timeline_fig.update_layout(
        title="Deployment Timeline & Success Rate",
        xaxis_title="Time",
        yaxis_title="Number of Deployments",
        yaxis2=dict(title="Success Rate (%)", overlaying="y", side="right"),
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        hovermode='x unified'
    )
    
    # Deployment Status Pie Chart
    status_counts = pd.Series([d['status'] for d in deployments_data]).value_counts()
    pie_fig = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title="Deployment Status Distribution",
        color_discrete_map={
            'success': '#00b894',
            'running': '#667eea',
            'failed': '#ff6b6b',
            'pending': '#fdcb6e'
        }
    )
    pie_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    # Deployments Table
    deployments_table = dbc.Table([
        html.Thead([
            html.Tr([
                html.Th("Service", className="text-white"),
                html.Th("Status", className="text-white"),
                html.Th("Version", className="text-white"),
                html.Th("Environment", className="text-white"),
                html.Th("Timestamp", className="text-white"),
                html.Th("Actions", className="text-white")
            ])
        ]),
        html.Tbody([
            html.Tr([
                html.Td(deployment["name"]),
                html.Td(
                    dbc.Badge(
                        deployment["status"],
                        color={
                            "success": "success",
                            "running": "info",
                            "failed": "danger",
                            "pending": "warning"
                        }[deployment["status"]],
                        className="text-white"
                    )
                ),
                html.Td(deployment["version"]),
                html.Td(
                    dbc.Badge(
                        deployment["environment"],
                        color={
                            "production": "danger",
                            "staging": "warning",
                            "development": "info"
                        }[deployment["environment"]],
                        className="text-white"
                    )
                ),
                html.Td(deployment["timestamp"]),
                html.Td(
                    dbc.ButtonGroup([
                        dbc.Button("Rollback", size="sm", color="warning", outline=True),
                        dbc.Button("Redeploy", size="sm", color="primary", outline=True)
                    ])
                )
            ]) for deployment in deployments_data
        ])
    ], className="text-white", bordered=True, dark=True)
    
    return html.Div([
        # Header
        html.Div([
            html.H1("🚀 Deployments & Releases", className="text-center mb-4"),
            html.P("Monitor and manage your application deployments across environments", 
                   className="text-center text-muted mb-5")
        ], className="main-header fade-in-up"),
        
        # Deployment Stats Cards
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H3("24", className="display-4 text-primary"),
                        html.P("Total Deployments", className="text-muted")
                    ], className="metric-card text-center")
                ], width=3),
                dbc.Col([
                    html.Div([
                        html.H3("92%", className="display-4 text-success"),
                        html.P("Success Rate", className="text-muted")
                    ], className="metric-card text-center")
                ], width=3),
                dbc.Col([
                    html.Div([
                        html.H3("2.1s", className="display-4 text-info"),
                        html.P("Avg Deploy Time", className="text-muted")
                    ], className="metric-card text-center")
                ], width=3),
                dbc.Col([
                    html.Div([
                        html.H3("3", className="display-4 text-warning"),
                        html.P("Active Deployments", className="text-muted")
                    ], className="metric-card text-center")
                ], width=3)
            ])
        ], className="mb-5 fade-in-up"),
        
        # Charts Row
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("📈 Deployment Timeline", className="mb-4"),
                    dcc.Graph(figure=timeline_fig, config={'displayModeBar': False})
                ], className="chart-container")
            ], width=8),
            dbc.Col([
                html.Div([
                    html.H3("🥧 Status Distribution", className="mb-4"),
                    dcc.Graph(figure=pie_fig, config={'displayModeBar': False})
                ], className="chart-container")
            ], width=4)
        ], className="mb-5 fade-in-up"),
        
        # Deployments Table
        html.Div([
            html.H3("📋 Recent Deployments", className="mb-4"),
            deployments_table
        ], className="chart-container fade-in-up"),
        
        # Deployment Controls
        html.Div([
            html.H3("🎮 Deployment Controls", className="mb-4"),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("🚀 New Deployment", className="card-title"),
                            html.P("Deploy a new version", className="card-text"),
                            dbc.Button("Start Deployment", color="primary", className="mt-3")
                        ])
                    ], className="bg-dark text-white border-primary")
                ], width=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("🔄 Rollback", className="card-title"),
                            html.P("Rollback to previous version", className="card-text"),
                            dbc.Button("Rollback", color="warning", className="mt-3")
                        ])
                    ], className="bg-dark text-white border-warning")
                ], width=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("⚙️ Settings", className="card-title"),
                            html.P("Configure deployment settings", className="card-text"),
                            dbc.Button("Configure", color="info", className="mt-3")
                        ])
                    ], className="bg-dark text-white border-info")
                ], width=4)
            ])
        ], className="chart-container fade-in-up")
    ])
