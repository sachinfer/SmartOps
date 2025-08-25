from fastapi import FastAPI, Request, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from datetime import datetime
import os
import pytz
from typing import List, Optional

# Kubernetes client
from kubernetes import client, config

app = FastAPI()

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "SmartOps API", "timestamp": str(datetime.now())}

@app.get("/namespaces")
async def list_namespaces():
    """Get all namespaces"""
    try:
        # Load Kubernetes configuration
        try:
            config.load_incluster_config()
        except Exception:
            try:
                config.load_kube_config()
            except Exception as config_error:
                return JSONResponse(
                    status_code=500,
                    content={"error": f"Failed to load Kubernetes config: {str(config_error)}"}
                )
        
        v1 = client.CoreV1Api()
        ns_list = v1.list_namespace()
        namespaces = [ns.metadata.name for ns in ns_list.items]
        return {"namespaces": namespaces}
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to get namespaces: {str(e)}"}
        )

@app.get("/pods")
async def list_pods(namespace: str = Query("default", description="Namespace to query")):
    """Get pods in a specific namespace"""
    try:
        # Load Kubernetes configuration
        try:
            config.load_incluster_config()
        except Exception:
            try:
                config.load_kube_config()
            except Exception as config_error:
                return JSONResponse(
                    status_code=500,
                    content={"error": f"Failed to load Kubernetes config: {str(config_error)}"}
                )
        
        v1 = client.CoreV1Api()
        
        try:
            pods = v1.list_namespaced_pod(namespace).items
            pod_list = []
            for pod in pods:
                # Calculate age
                age = ""
                if pod.status.start_time:
                    age_delta = datetime.now(pod.status.start_time.tzinfo) - pod.status.start_time
                    if age_delta.days > 0:
                        age = f"{age_delta.days}d"
                    elif age_delta.seconds > 3600:
                        age = f"{age_delta.seconds // 3600}h"
                    else:
                        age = f"{age_delta.seconds // 60}m"
                
                # Get ready status
                ready = "0/0"
                if pod.status.container_statuses:
                    total = len(pod.status.container_statuses)
                    ready_count = sum(1 for cs in pod.status.container_statuses if cs.ready)
                    ready = f"{ready_count}/{total}"
                
                pod_list.append({
                    "name": pod.metadata.name,
                    "namespace": pod.metadata.namespace,
                    "status": pod.status.phase,
                    "age": age,
                    "ready": ready,
                    "node": getattr(pod.spec, 'node_name', ''),
                    "start_time": str(pod.status.start_time) if pod.status.start_time else ''
                })
            
            return {"pods": pod_list}
            
        except Exception as pod_error:
            return JSONResponse(
                status_code=500,
                content={"error": f"Failed to get pods: {str(pod_error)}"}
            )
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to get pods: {str(e)}"}
        )

@app.get("/logs")
async def get_pod_logs(pod: str = Query(..., description="Pod name"), 
                       namespace: str = Query(..., description="Namespace"),
                       container: str = Query(None, description="Container name (optional)"),
                       tail_lines: int = Query(100, description="Number of lines to return")):
    """Get logs for a specific pod"""
    try:
        # Load Kubernetes configuration
        try:
            config.load_incluster_config()
        except Exception:
            try:
                config.load_kube_config()
            except Exception as config_error:
                return JSONResponse(
                    status_code=500,
                    content={"error": f"Failed to load Kubernetes config: {str(config_error)}"}
                )
        
        v1 = client.CoreV1Api()
        
        try:
            # Get pod logs
            if container:
                logs = v1.read_namespaced_pod_log(
                    name=pod,
                    namespace=namespace,
                    container=container,
                    tail_lines=tail_lines
                )
            else:
                logs = v1.read_namespaced_pod_log(
                    name=pod,
                    namespace=namespace,
                    tail_lines=tail_lines
                )
            
            return {"logs": logs}
            
        except Exception as log_error:
            return JSONResponse(
                status_code=500,
                content={"error": f"Failed to get logs: {str(log_error)}"}
            )
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to get logs: {str(e)}"}
        )

@app.get("/pod-containers")
async def get_pod_containers(pod_name: str = Query(..., description="Pod name"),
                            namespace: str = Query(..., description="Namespace")):
    """Get container names for a specific pod"""
    try:
        # Load Kubernetes configuration
        try:
            config.load_incluster_config()
        except Exception:
            try:
                config.load_kube_config()
            except Exception as config_error:
                return JSONResponse(
                    status_code=500,
                    content={"error": f"Failed to load Kubernetes config: {str(config_error)}"}
                )
        
        v1 = client.CoreV1Api()
        
        try:
            # Get pod details
            pod = v1.read_namespaced_pod(name=pod_name, namespace=namespace)
            containers = []
            
            # Get init containers
            if pod.spec.init_containers:
                for container in pod.spec.init_containers:
                    containers.append(container.name)
            
            # Get main containers
            if pod.spec.containers:
                for container in pod.spec.containers:
                    containers.append(container.name)
            
            return {"containers": containers}
            
        except Exception as container_error:
            return JSONResponse(
                status_code=500,
                content={"error": f"Failed to get containers: {str(container_error)}"}
            )
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to get containers: {str(e)}"}
        )

@app.get("/kubectl_get")
async def kubectl_get(resource_type: str = Query(..., description="Resource type: pods, services, deployments, nodes"), 
                all_namespaces: bool = Query(False),
                namespace: str = Query("default", description="Namespace to query (ignored if all_namespaces=True)")):
    try:
        # Load Kubernetes configuration
        try:
            config.load_incluster_config()
        except Exception:
            try:
                config.load_kube_config()
            except Exception as config_error:
                return JSONResponse(
                    status_code=500,
                    content={"error": f"Failed to load Kubernetes config: {str(config_error)}"}
                )
        
        v1 = client.CoreV1Api()
        apps_v1 = client.AppsV1Api()
        items = []
        
        try:
            if resource_type == "pods":
                if all_namespaces:
                    pods = v1.list_pod_for_all_namespaces().items
                else:
                    pods = v1.list_namespaced_pod(namespace).items
                for pod in pods:
                    items.append({
                        "name": pod.metadata.name,
                        "namespace": pod.metadata.namespace,
                        "status": pod.status.phase,
                        "node": getattr(pod.spec, 'node_name', ''),
                        "start_time": str(pod.status.start_time) if pod.status.start_time else ''
                    })
            elif resource_type == "services":
                if all_namespaces:
                    svcs = v1.list_service_for_all_namespaces().items
                else:
                    svcs = v1.list_namespaced_service(namespace).items
                for svc in svcs:
                    items.append({
                        "name": svc.metadata.name,
                        "namespace": svc.metadata.namespace,
                        "type": svc.spec.type,
                        "cluster_ip": svc.spec.cluster_ip,
                        "ports": str(svc.spec.ports)
                    })
            elif resource_type == "deployments":
                if all_namespaces:
                    deps = apps_v1.list_deployment_for_all_namespaces().items
                else:
                    deps = apps_v1.list_namespaced_deployment(namespace).items
                for dep in deps:
                    items.append({
                        "name": dep.metadata.name,
                        "namespace": dep.metadata.namespace,
                        "replicas": dep.status.replicas,
                        "available": dep.status.available_replicas,
                        "updated": dep.status.updated_replicas
                    })
            elif resource_type == "nodes":
                nodes = v1.list_node().items
                for node in nodes:
                    try:
                        node_name = getattr(node.metadata, 'name', 'Unknown')
                        status = 'Unknown'
                        if hasattr(node.status, 'conditions') and node.status.conditions:
                            for condition in node.status.conditions:
                                if condition.type == 'Ready':
                                    status = condition.type
                                    break
                        
                        addresses = []
                        if hasattr(node.status, 'addresses') and node.status.addresses:
                            addresses = [a.address for a in node.status.addresses if hasattr(a, 'address')]
                        
                        internal_ip = "Unknown"
                        if addresses:
                            for addr in addresses:
                                if isinstance(addr, str) and addr.replace('.', '').replace('-', '').isdigit():
                                    internal_ip = addr
                                    break
                        
                        items.append({
                            "name": node_name,
                            "status": status,
                            "internal_ip": internal_ip,
                            "addresses": str(addresses) if addresses else 'No addresses'
                        })
                    except Exception as node_error:
                        items.append({
                            "name": "Error processing node",
                            "status": "Error",
                            "addresses": f"Error: {str(node_error)}"
                        })
            else:
                return JSONResponse(status_code=400, content={"error": "Unsupported resource type"})
            
            return {"output": items, "items": items}
            
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"error": f"Internal server error: {str(e)}"}
            )
            
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to load Kubernetes config: {str(e)}"}
        )

@app.post("/kubectl_raw")
async def kubectl_raw(command: str = Query(..., description="kubectl command to execute")):
    """Execute raw kubectl commands"""
    try:
        import subprocess
        import json
        
        # Execute the command
        result = subprocess.run(
            ["kubectl"] + command.split(),
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to execute command: {str(e)}"}
        )

@app.get("/incidents")
async def get_incidents():
    """Get incident data for timeline and postmortem reports"""
    try:
        # For now, return sample incident data
        # In a real implementation, this would fetch from a database
        sample_incidents = [
            {
                "id": 1,
                "timestamp": "2025-08-25 05:30:00",
                "type": "Pod Crash",
                "app": "smartops-app",
                "namespace": "smartops",
                "details": "Pod smartops-app-8c6cd4cbb-7226b crashed due to memory limit exceeded",
                "root_cause": "Memory leak in application code causing OOM",
                "impact": "Service unavailable for 2 minutes, affecting 15 users",
                "remediation": "Increased memory limits and fixed memory leak in code",
                "status": "Resolved"
            },
            {
                "id": 2,
                "timestamp": "2025-08-25 04:15:00",
                "type": "High CPU Usage",
                "app": "smartops-monitor",
                "namespace": "smartops",
                "details": "CPU usage spiked to 95% for 10 minutes",
                "root_cause": "Inefficient database queries during peak load",
                "impact": "Increased response times, monitoring alerts delayed",
                "remediation": "Optimized database queries and added caching",
                "status": "Resolved"
            },
            {
                "id": 3,
                "timestamp": "2025-08-25 03:45:00",
                "type": "Network Latency",
                "app": "smartops-dashboard",
                "namespace": "smartops",
                "details": "API response times increased from 200ms to 2s",
                "root_cause": "Database connection pool exhaustion",
                "impact": "Dashboard loading slowly, user experience degraded",
                "remediation": "Increased connection pool size and added connection monitoring",
                "status": "Resolved"
            }
        ]
        
        return {"incidents": sample_incidents}
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to fetch incidents: {str(e)}"}
        )

@app.post("/postmortem")
async def save_postmortem(postmortem_data: dict):
    """Save postmortem report to audit trail"""
    try:
        # In a real implementation, this would save to a database
        # For now, just return success
        return {"message": "Postmortem report saved successfully", "id": postmortem_data.get("id", "new")}
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to save postmortem: {str(e)}"}
        )

@app.get("/hpa_status")
async def get_hpa_status():
    """Get HPA status and usage data for auto-scaling recommendations"""
    try:
        # Load Kubernetes configuration
        try:
            config.load_incluster_config()
        except Exception:
            try:
                config.load_kube_config()
            except Exception as config_error:
                return JSONResponse(
                    status_code=500,
                    content={"error": f"Failed to load Kubernetes config: {str(config_error)}"}
                )
        
        # For now, return sample HPA data
        # In a real implementation, this would fetch actual HPA and metrics
        sample_hpa_data = [
            {
                "pod": "smartops-app",
                "namespace": "smartops",
                "current_replicas": 1,
                "min_replicas": 1,
                "max_replicas": 5,
                "cpu_avg": 0.65,
                "mem_avg": 0.72,
                "cpu_target": 0.7,
                "mem_target": 0.8,
                "last_scale_time": "2025-08-25 05:30:00",
                "status": "Active"
            },
            {
                "pod": "smartops-monitor",
                "namespace": "smartops",
                "current_replicas": 1,
                "min_replicas": 1,
                "max_replicas": 3,
                "cpu_avg": 0.45,
                "mem_avg": 0.38,
                "cpu_target": 0.7,
                "mem_target": 0.8,
                "last_scale_time": "2025-08-25 04:15:00",
                "status": "Active"
            },
            {
                "pod": "smartops-dashboard",
                "namespace": "smartops",
                "current_replicas": 1,
                "min_replicas": 1,
                "max_replicas": 3,
                "cpu_avg": 0.28,
                "mem_avg": 0.35,
                "cpu_target": 0.7,
                "mem_target": 0.8,
                "last_scale_time": "2025-08-25 03:45:00",
                "status": "Active"
            }
        ]
        
        return {"hpa": sample_hpa_data}
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to fetch HPA data: {str(e)}"}
        )

@app.post("/update_hpa")
async def update_hpa(hpa_data: dict):
    """Update HPA settings for a pod"""
    try:
        # In a real implementation, this would update the actual HPA
        # For now, just return success
        pod = hpa_data.get("pod", "unknown")
        min_replicas = hpa_data.get("min_replicas", 1)
        max_replicas = hpa_data.get("max_replicas", 5)
        
        return {
            "message": f"HPA updated successfully for {pod}",
            "pod": pod,
            "min_replicas": min_replicas,
            "max_replicas": max_replicas,
            "status": "Applied"
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to update HPA: {str(e)}"}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
