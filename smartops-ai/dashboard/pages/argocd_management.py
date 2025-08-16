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

def create_argocd_management_page():
    """Create the ArgoCD Management page with embedded UI and custom controls"""
    
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
    
    def get_argocd_applications():
        """Get ArgoCD applications status"""
        if not k8s_client:
            return []
        
        try:
            # Get ArgoCD applications
            applications = k8s_client.list_namespaced_custom_object(
                group="argoproj.io",
                version="v1alpha1",
                namespace="argocd",
                plural="applications"
            )
            
            app_data = []
            for app in applications['items']:
                # Get sync status
                sync_status = app.get('status', {}).get('sync', {})
                health_status = app.get('status', {}).get('health', {})
                
                app_data.append({
                    'name': app['metadata']['name'],
                    'namespace': app['metadata']['namespace'],
                    'project': app['spec']['project'],
                    'repo_url': app['spec']['source']['repoURL'],
                    'target_revision': app['spec']['source']['targetRevision'],
                    'path': app['spec']['source']['path'],
                    'sync_status': sync_status.get('status', 'Unknown'),
                    'health_status': health_status.get('status', 'Unknown'),
                    'last_sync': sync_status.get('finishedAt', 'Never'),
                    'created': app['metadata']['creationTimestamp']
                })
            
            return app_data
        except Exception as e:
            print(f"Error getting ArgoCD applications: {e}")
            return []
    
    # Get ArgoCD applications data
    apps_data = get_argocd_applications()
    
    # Create status distribution charts
    if apps_data:
        sync_counts = pd.Series([app['sync_status'] for app in apps_data]).value_counts()
        health_counts = pd.Series([app['health_status'] for app in apps_data]).value_counts()
        
        sync_fig = px.pie(
            values=sync_counts.values,
            names=sync_counts.index,
            title="Sync Status Distribution",
            color_discrete_map={
                'Synced': '#00b894',
                'OutOfSync': '#ff6b6b',
                'Unknown': '#636e72'
            }
        )
        sync_fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=400
        )
        
        health_fig = px.pie(
            values=health_counts.values,
            names=health_counts.index,
            title="Health Status Distribution",
            color_discrete_map={
                'Healthy': '#00b894',
                'Degraded': '#fdcb6e',
                'Progressing': '#74b9ff',
                'Unknown': '#636e72'
            }
        )
        health_fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=400
        )
    else:
        sync_fig = px.pie(values=[1], names=['No Data'], title="No Applications Found")
        sync_fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        health_fig = px.pie(values=[1], names=['No Data'], title="No Applications Found")
        health_fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    
    # Create applications table
    if apps_data:
        apps_table = dbc.Table([
            html.Thead([
                html.Tr([
                    html.Th("Application", className="text-white"),
                    html.Th("Project", className="text-white"),
                    html.Th("Sync Status", className="text-white"),
                    html.Th("Health Status", className="text-white"),
                    html.Th("Repository", className="text-white"),
                    html.Th("Path", className="text-white"),
                    html.Th("Actions", className="text-white")
                ])
            ]),
            html.Tbody([
                html.Tr([
                    html.Td(app["name"]),
                    html.Td(app["project"]),
                    html.Td(
                        dbc.Badge(
                            app["sync_status"],
                            color={
                                "Synced": "success",
                                "OutOfSync": "danger",
                                "Unknown": "secondary"
                            }.get(app["sync_status"], "secondary"),
                            className="text-white"
                        )
                    ),
                    html.Td(
                        dbc.Badge(
                            app["health_status"],
                            color={
                                "Healthy": "success",
                                "Degraded": "warning",
                                "Progressing": "info",
                                "Unknown": "secondary"
                            }.get(app["health_status"], "secondary"),
                            className="text-white"
                        )
                    ),
                    html.Td(
                        html.A(
                            app["repo_url"].split("/")[-1],
                            href=app["repo_url"],
                            target="_blank",
                            className="text-info"
                        )
                    ),
                    html.Td(app["path"]),
                    html.Td(
                        dbc.ButtonGroup([
                            dbc.Button("🔄 Sync", size="sm", color="primary", outline=True, id=f"sync-{app['name']}"),
                            dbc.Button("📊 Details", size="sm", color="info", outline=True, id=f"details-{app['name']}"),
                            dbc.Button("📝 Logs", size="sm", color="success", outline=True, id=f"logs-{app['name']}")
                        ])
                    )
                ]) for app in apps_data
            ])
        ], className="text-white", bordered=True, dark=True, responsive=True)
    else:
        apps_table = html.Div([
            html.H4("No ArgoCD Applications Found", className="text-center text-muted"),
            html.P("Unable to connect to ArgoCD or no applications are configured.", className="text-center text-muted")
        ], className="text-center p-5")
    
    return html.Div([
        # Header
        html.Div([
            html.H1("🎯 ArgoCD Management", className="text-center mb-4"),
            html.P("GitOps Deployment Management & Application Monitoring", 
                   className="text-center text-muted mb-5")
        ], className="main-header fade-in-up"),
        
        # ArgoCD Stats Cards
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H3(str(len(apps_data)), className="display-4 text-primary"),
                        html.P("Total Applications", className="text-muted")
                    ], className="metric-card text-center")
                ], width=3),
                dbc.Col([
                    html.Div([
                        html.H3(str(len([a for a in apps_data if a['sync_status'] == 'Synced'])), className="display-4 text-success"),
                        html.P("Synced", className="text-muted")
                    ], className="metric-card text-center")
                ], width=3),
                dbc.Col([
                    html.Div([
                        html.H3(str(len([a for a in apps_data if a['health_status'] == 'Healthy'])), className="display-4 text-success"),
                        html.P("Healthy", className="text-muted")
                    ], className="metric-card text-center")
                ], width=3),
                dbc.Col([
                    html.Div([
                        html.H3(str(len([a for a in apps_data if a['sync_status'] == 'OutOfSync'])), className="display-4 text-danger"),
                        html.P("Out of Sync", className="text-muted")
                    ], className="metric-card text-center")
                ], width=3)
            ])
        ], className="mb-5 fade-in-up"),
        
        # Charts Row
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("📊 Sync Status Distribution", className="mb-4"),
                    dcc.Graph(figure=sync_fig, config={'displayModeBar': False})
                ], className="chart-container")
            ], width=6, className="mb-4")
        ], className="mb-5 fade-in-up"),
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("🏥 Health Status Distribution", className="mb-4"),
                    dcc.Graph(figure=health_fig, config={'displayModeBar': False})
                ], className="chart-container")
            ], width=6, className="mb-4")
        ], className="mb-5 fade-in-up"),
        
        # ArgoCD Management Controls
        html.Div([
            html.H3("🎮 ArgoCD Controls", className="mb-4"),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("🔄 Sync All Apps", className="card-title"),
                            html.P("Synchronize all applications", className="card-text"),
                            dbc.Button(
                                "Sync All", 
                                color="primary", 
                                className="mt-3",
                                id="sync-all-apps-btn"
                            )
                        ])
                    ], className="bg-dark text-white border-primary")
                ], width=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("📊 ArgoCD UI", className="card-title"),
                            html.P("Access full ArgoCD interface", className="card-text"),
                            dbc.Button(
                                "Open ArgoCD UI", 
                                color="info", 
                                className="mt-3",
                                id="open-argocd-ui-btn"
                            )
                        ])
                    ], className="bg-dark text-white border-info")
                ], width=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("📝 Application Logs", className="card-title"),
                            html.P("View deployment logs", className="card-text"),
                            dbc.Button(
                                "View Logs", 
                                color="success", 
                                className="mt-3",
                                id="view-logs-btn"
                            )
                        ])
                    ], className="bg-dark text-white border-success")
                ], width=4)
            ])
        ], className="chart-container fade-in-up mb-5"),
        
        # Applications Table
        html.Div([
            html.H3("📋 ArgoCD Applications", className="mb-4"),
            html.Div([
                dbc.Button("🔄 Refresh", color="primary", className="mb-3", id="refresh-apps-btn"),
                html.Span(f"Last updated: {datetime.now().strftime('%H:%M:%S')}", className="text-muted ml-3")
            ]),
            apps_table
        ], className="chart-container fade-in-up"),
        
        # ArgoCD UI Embed Modal
        dbc.Modal([
            dbc.ModalHeader("ArgoCD UI"),
            dbc.ModalBody([
                html.Iframe(
                    src="http://localhost:8080",  # This will be updated with actual ArgoCD URL
                    style={"width": "100%", "height": "600px", "border": "none"}
                )
            ]),
            dbc.ModalFooter([
                dbc.Button("Close", id="close-argocd-modal", className="ms-auto")
            ])
        ], id="argocd-ui-modal", size="xl")
    ])
