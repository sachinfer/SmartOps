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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
