import dash
from dash import dcc, html, Input, Output, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_ai_actions_page():
    """Create the AI Actions page with stunning UI and interactive features"""
    
    # Mock data for AI actions
    ai_actions_data = [
        {"action": "Auto-scaling triggered", "status": "success", "timestamp": "2 min ago", "confidence": 0.95, "impact": "high"},
        {"action": "Load balancer optimized", "status": "success", "timestamp": "5 min ago", "confidence": 0.88, "impact": "medium"},
        {"action": "Security threat detected", "status": "warning", "timestamp": "8 min ago", "confidence": 0.92, "impact": "critical"},
        {"action": "Performance optimization", "status": "info", "timestamp": "12 min ago", "confidence": 0.78, "impact": "medium"},
        {"action": "Resource allocation", "status": "success", "timestamp": "15 min ago", "confidence": 0.85, "impact": "low"}
    ]
    
    # Create AI performance chart
    performance_data = pd.DataFrame({
        'time': pd.date_range(start='2024-01-01', periods=24, freq='H'),
        'accuracy': np.random.normal(0.92, 0.05, 24),
        'response_time': np.random.normal(150, 20, 24),
        'efficiency': np.random.normal(0.88, 0.08, 24)
    })
    
    # AI Performance Chart
    performance_fig = go.Figure()
    performance_fig.add_trace(go.Scatter(
        x=performance_data['time'],
        y=performance_data['accuracy'],
        name='Accuracy',
        line=dict(color='#00b894', width=3),
        fill='tonexty'
    ))
    performance_fig.add_trace(go.Scatter(
        x=performance_data['time'],
        y=performance_data['efficiency'],
        name='Efficiency',
        line=dict(color='#667eea', width=3),
        fill='tonexty'
    ))
    performance_fig.update_layout(
        title="AI Performance Metrics",
        xaxis_title="Time",
        yaxis_title="Score",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        hovermode='x unified'
    )
    
    # AI Actions Table
    actions_table = dbc.Table([
        html.Thead([
            html.Tr([
                html.Th("Action", className="text-white"),
                html.Th("Status", className="text-white"),
                html.Th("Timestamp", className="text-white"),
                html.Th("Confidence", className="text-white"),
                html.Th("Impact", className="text-white")
            ])
        ]),
        html.Tbody([
            html.Tr([
                html.Td(action["action"]),
                html.Td(
                    dbc.Badge(
                        action["status"],
                        color={
                            "success": "success",
                            "warning": "warning",
                            "info": "info",
                            "critical": "danger"
                        }[action["status"]],
                        className="text-white"
                    )
                ),
                html.Td(action["timestamp"]),
                html.Td(f"{action['confidence']*100:.0f}%"),
                html.Td(
                    dbc.Badge(
                        action["impact"],
                        color={
                            "high": "danger",
                            "medium": "warning",
                            "low": "success"
                        }[action["impact"]],
                        className="text-white"
                    )
                )
            ]) for action in ai_actions_data
        ])
    ], className="text-white", bordered=True, dark=True)
    
    return html.Div([
        # Header
        html.Div([
            html.H1("🤖 AI Actions & Automation", className="text-center mb-4"),
            html.P("Intelligent automation and AI-driven decision making for your infrastructure", 
                   className="text-center text-muted mb-5")
        ], className="main-header fade-in-up"),
        
        # AI Stats Cards
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H3("95%", className="display-4 text-success"),
                        html.P("Success Rate", className="text-muted")
                    ], className="metric-card text-center")
                ], width=3),
                dbc.Col([
                    html.Div([
                        html.H3("2.3s", className="display-4 text-info"),
                        html.P("Avg Response Time", className="text-muted")
                    ], className="metric-card text-center")
                ], width=3),
                dbc.Col([
                    html.Div([
                        html.H3("24/7", className="display-4 text-warning"),
                        html.P("Monitoring", className="text-muted")
                    ], className="metric-card text-center")
                ], width=3),
                dbc.Col([
                    html.Div([
                        html.H3("89%", className="display-4 text-primary"),
                        html.P("Efficiency Score", className="text-muted")
                    ], className="metric-card text-center")
                ], width=3)
            ])
        ], className="mb-5 fade-in-up"),
        
        # Charts Row
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("📊 AI Performance Metrics", className="mb-4"),
                    dcc.Graph(figure=performance_fig, config={'displayModeBar': False})
                ], className="chart-container")
            ], width=12, className="mb-4")
        ], className="mb-5 fade-in-up"),
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("🤖 AI Actions Table", className="mb-4"),
                    actions_table
                ], className="chart-container")
            ], width=12, className="mb-4")
        ], className="mb-5 fade-in-up"),
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("🎮 AI Control Panel", className="mb-4"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H5("Auto-scaling", className="card-title"),
                                    html.P("Enable intelligent resource scaling", className="card-text"),
                                    dbc.Switch(id="auto-scaling-switch", label="Enabled", value=True, className="mt-3")
                                ])
                            ], className="bg-dark text-white border-primary")
                        ], width=4),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H5("Security AI", className="card-title"),
                                    html.P("AI-powered threat detection", className="card-text"),
                                    dbc.Switch(id="security-ai-switch", label="Enabled", value=True, className="mt-3")
                                ])
                            ], className="bg-dark text-white border-success")
                        ], width=4),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H5("Performance AI", className="card-title"),
                                    html.P("Automatic optimization", className="card-text"),
                                    dbc.Switch(id="performance-ai-switch", label="Enabled", value=False, className="mt-3")
                                ])
                            ], className="bg-dark text-white border-warning")
                        ], width=4)
                    ])
                ], className="chart-container")
            ], width=12, className="mb-4")
        ], className="mb-5 fade-in-up")
    ])
