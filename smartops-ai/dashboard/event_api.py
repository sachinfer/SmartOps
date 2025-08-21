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

@app.get("/debug/nodes")
async def debug_nodes():
    """Debug endpoint to test node data fetching"""
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
    
    try:
        v1 = client.CoreV1Api()
        nodes = v1.list_node()
        
        debug_info = {
            "total_nodes": len(nodes.items),
            "node_details": []
        }
        
        for i, node in enumerate(nodes.items):
            try:
                node_info = {
                    "index": i,
                    "name": getattr(node.metadata, 'name', 'Unknown'),
                    "has_status": hasattr(node, 'status'),
                    "has_conditions": hasattr(node.status, 'conditions') if hasattr(node, 'status') else False,
                    "conditions_count": len(node.status.conditions) if hasattr(node, 'status') and hasattr(node.status, 'conditions') else 0,
                    "has_addresses": hasattr(node.status, 'addresses') if hasattr(node, 'status') else False,
                    "addresses_count": len(node.status.addresses) if hasattr(node, 'status') and hasattr(node.status, 'addresses') else 0,
                    "has_node_info": hasattr(node.status, 'node_info') if hasattr(node, 'status') else False
                }
                debug_info["node_details"].append(node_info)
            except Exception as node_error:
                debug_info["node_details"].append({
                    "index": i,
                    "error": str(node_error)
                })
        
        return debug_info
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Debug endpoint error: {str(e)}"}
        )

@app.get("/debug/logs")
async def debug_logs():
    """Debug endpoint to test logs functionality"""
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
    
    try:
        v1 = client.CoreV1Api()
        
        # Get some basic cluster info
        debug_info = {
            "kubernetes_config": "Loaded successfully",
            "api_available": True,
            "sample_pods": []
        }
        
        # Try to get a few pods to test access
        try:
            pods = v1.list_pod_for_all_namespaces(limit=3)
            for pod in pods.items:
                pod_info = {
                    "name": pod.metadata.name,
                    "namespace": pod.metadata.namespace,
                    "status": pod.status.phase,
                    "containers": [c.name for c in pod.spec.containers] if pod.spec.containers else []
                }
                debug_info["sample_pods"].append(pod_info)
        except Exception as pod_error:
            debug_info["sample_pods"] = [{"error": str(pod_error)}]
        
        return debug_info
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Debug logs endpoint error: {str(e)}"}
        )

# Simulated HPA data (replace with real DB/API integration)
hpa_data = [
    {"pod": "sample-pod-1", "cpu_avg": 0.45, "mem_avg": 0.60, "min_replicas": 1, "max_replicas": 5},
    {"pod": "sample-pod-2", "cpu_avg": 0.80, "mem_avg": 0.70, "min_replicas": 2, "max_replicas": 10},
    {"pod": "sample-pod-3", "cpu_avg": 0.30, "mem_avg": 0.25, "min_replicas": 1, "max_replicas": 3},
]

class HPAUpdateRequest(BaseModel):
    pod: str
    min_replicas: int
    max_replicas: int

@app.get("/hpa_status")
async def get_hpa_status():
    # In real use, fetch from K8s API or DB
    return {"hpa": hpa_data}

@app.post("/update_hpa")
async def update_hpa(req: HPAUpdateRequest):
    # In real use, update K8s HPA via API
    for hpa in hpa_data:
        if hpa["pod"] == req.pod:
            hpa["min_replicas"] = req.min_replicas
            hpa["max_replicas"] = req.max_replicas
            return {"status": "success", "msg": f"HPA updated for {req.pod}"}
    return JSONResponse(status_code=404, content={"status": "error", "msg": "Pod not found"})

DB_PATH = "data/deployment_events.db"

class Event(BaseModel):
    status: str
    message: str
    namespace: str = "smartops"
    timestamp: str = None

@app.post("/log_event")
def log_event(event: Event):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS deployment_events (
            timestamp TEXT,
            status TEXT,
            message TEXT,
            namespace TEXT
        )
    """)
    if event.timestamp:
        ts = event.timestamp
    else:
        ist = pytz.timezone('Asia/Kolkata')
        ts = datetime.now(ist).isoformat()
    conn.execute(
        "INSERT INTO deployment_events (timestamp, status, message, namespace) VALUES (?, ?, ?, ?)",
        (ts, event.status, event.message, event.namespace)
    )
    conn.commit()
    conn.close()
    return {"result": "success", "timestamp": ts}

@app.get("/pods")
def list_pods(namespace: Optional[str] = Query(None, description="Namespace to filter by")):
    try:
        config.load_incluster_config()
    except Exception:
        config.load_kube_config()
    v1 = client.CoreV1Api()
    if namespace and namespace != 'all':
        pods = v1.list_namespaced_pod(namespace=namespace)
    else:
        pods = v1.list_pod_for_all_namespaces()
    pod_list = []
    for pod in pods.items:
        restarts = sum([c.restart_count for c in pod.status.container_statuses or []])
        images = ', '.join([c.image for c in pod.spec.containers])
        containers = [c.name for c in pod.spec.containers]
        pod_list.append({
            "name": pod.metadata.name,
            "namespace": pod.metadata.namespace,
            "status": pod.status.phase,
            "node": getattr(pod.spec, 'node_name', ''),
            "start_time": str(pod.status.start_time) if pod.status.start_time else '',
            "restarts": restarts,
            "images": images,
            "containers": containers
        })
    return {"pods": pod_list}

@app.get("/namespaces")
def list_namespaces():
    try:
        config.load_incluster_config()
    except Exception:
        config.load_kube_config()
    v1 = client.CoreV1Api()
    ns_list = v1.list_namespace()
    namespaces = [ns.metadata.name for ns in ns_list.items]
    return {"namespaces": namespaces}

@app.get("/logs")
def get_pod_logs(namespace: str = Query(..., description="Namespace of the pod"), pod: str = Query(..., description="Pod name"), container: Optional[str] = Query(None, description="Container name (optional)")):
    """
    Fetch logs for a given pod in a given namespace. Optionally specify container.
    """
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
                    content={"error": f"Failed to load Kubernetes config: {str(config_error)}", "logs": ""}
                )
        
        v1 = client.CoreV1Api()
        
        # First check if the pod exists
        try:
            pod_obj = v1.read_namespaced_pod(name=pod, namespace=namespace)
        except Exception as pod_error:
            return JSONResponse(
                status_code=404,
                content={"error": f"Pod not found: {str(pod_error)}", "logs": ""}
            )
        
        # Check if pod is running
        if pod_obj.status.phase != 'Running':
            return JSONResponse(
                status_code=400,
                content={"error": f"Pod is not running (status: {pod_obj.status.phase})", "logs": ""}
            )
        
        # Get logs
        try:
            logs = v1.read_namespaced_pod_log(name=pod, namespace=namespace, container=container)
            if not logs:
                logs = "No logs available for this pod/container"
            return {"logs": logs}
        except Exception as log_error:
            return JSONResponse(
                status_code=500,
                content={"error": f"Failed to fetch logs: {str(log_error)}", "logs": ""}
            )
            
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Unexpected error: {str(e)}", "logs": ""}
        )

@app.get("/pod-containers")
def get_pod_containers(pod_name: str = Query(..., description="Pod name"), namespace: str = Query(..., description="Namespace of the pod")):
    """
    Get container names for a specific pod
    """
    try:
        config.load_incluster_config()
    except Exception:
        config.load_kube_config()
    v1 = client.CoreV1Api()
    try:
        pod_obj = v1.read_namespaced_pod(name=pod_name, namespace=namespace)
        containers = [container.name for container in pod_obj.spec.containers]
        return {"containers": containers}
    except Exception as e:
        return {"error": str(e), "containers": []}

@app.post("/restart_pod")
def restart_pod(namespace: str = Query(...), pod: str = Query(...)):
    try:
        config.load_incluster_config()
    except Exception:
        config.load_kube_config()
    v1 = client.CoreV1Api()
    try:
        v1.delete_namespaced_pod(name=pod, namespace=namespace)
        return {"result": "restarted"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/delete_pod")
def delete_pod(namespace: str = Query(...), pod: str = Query(...)):
    try:
        config.load_incluster_config()
    except Exception:
        config.load_kube_config()
    v1 = client.CoreV1Api()
    try:
        v1.delete_namespaced_pod(name=pod, namespace=namespace)
        return {"result": "deleted"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/describe_pod")
def describe_pod(namespace: str = Query(...), pod: str = Query(...)):
    try:
        config.load_incluster_config()
    except Exception:
        config.load_kube_config()
    v1 = client.CoreV1Api()
    try:
        pod_obj = v1.read_namespaced_pod(name=pod, namespace=namespace)
        return pod_obj.to_dict()
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/namespace_stats")
def namespace_stats(namespace: str = Query(...)):
    try:
        config.load_incluster_config()
    except Exception:
        config.load_kube_config()
    v1 = client.CoreV1Api()
    # Count pods
    if namespace == 'all':
        pod_count = len(v1.list_pod_for_all_namespaces().items)
        svc_count = len(v1.list_service_for_all_namespaces().items)
    else:
        pod_count = len(v1.list_namespaced_pod(namespace=namespace).items)
        svc_count = len(v1.list_namespaced_service(namespace=namespace).items)
    return {"pod_count": pod_count, "service_count": svc_count}

@app.get("/ai_actions")
def list_ai_actions(all: bool = Query(False, description="Return all actions if true, only pending if false")):
    db_path = "/app/dashboard/data/ai_actions.db"
    import sqlite3
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute('''CREATE TABLE IF NOT EXISTS ai_actions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        pod_name TEXT,
        namespace TEXT,
        reason TEXT,
        status TEXT
    )''')
    if all:
        actions = conn.execute("SELECT * FROM ai_actions ORDER BY timestamp DESC").fetchall()
    else:
        actions = conn.execute("SELECT * FROM ai_actions WHERE status='pending' ORDER BY timestamp DESC").fetchall()
    conn.close()
    return {"actions": [dict(a) for a in actions]}

@app.post("/confirm_ai_action")
def confirm_ai_action(action_id: int = Query(...)):
    db_path = "/app/dashboard/data/ai_actions.db"
    import sqlite3
    conn = sqlite3.connect(db_path)
    action = conn.execute("SELECT * FROM ai_actions WHERE id=?", (action_id,)).fetchone()
    if not action:
        conn.close()
        return JSONResponse(status_code=404, content={"error": "Action not found"})
    pod_name = action[2]
    namespace = action[3]
    # Delete the pod
    try:
        config.load_incluster_config()
    except Exception:
        config.load_kube_config()
    v1 = client.CoreV1Api()
    try:
        v1.delete_namespaced_pod(name=pod_name, namespace=namespace)
        # Mark action as completed
        conn.execute("UPDATE ai_actions SET status='completed' WHERE id=?", (action_id,))
        conn.commit()
        conn.close()
        return {"result": "pod deleted", "pod": pod_name, "namespace": namespace}
    except Exception as e:
        # If pod not found, mark as not_found and return friendly message
        if 'NotFound' in str(e) or 'not found' in str(e):
            conn.execute("UPDATE ai_actions SET status='not_found' WHERE id=?", (action_id,))
            conn.commit()
            conn.close()
            return JSONResponse(status_code=404, content={"error": f"Pod {pod_name} not found. It may have already been deleted or replaced.", "status": "not_found"})
        conn.close()
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/retrain_model")
def retrain_model():
    import subprocess
    try:
        result = subprocess.run([
            "python", "/app/train_model_from_real_data.py"
        ], capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            return {"result": "Model retrained successfully", "output": result.stdout}
        else:
            return JSONResponse(status_code=500, content={"error": result.stderr})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/ignore_ai_action")
def ignore_ai_action(action_id: int = Query(...)):
    db_path = "/app/dashboard/data/ai_actions.db"
    import sqlite3
    conn = sqlite3.connect(db_path)
    action = conn.execute("SELECT * FROM ai_actions WHERE id=?", (action_id,)).fetchone()
    if not action:
        conn.close()
        return JSONResponse(status_code=404, content={"error": "Action not found"})
    conn.execute("UPDATE ai_actions SET status='ignored' WHERE id=?", (action_id,))
    conn.commit()
    conn.close()
    return {"result": "action ignored", "action_id": action_id}

@app.get("/kubectl_get")
def kubectl_get(resource_type: str = Query(..., description="Resource type: pods, services, deployments, nodes"), 
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
                # Safe access to node status with proper error handling
                node_name = getattr(node.metadata, 'name', 'Unknown')
                
                # Safe access to conditions
                status = 'Unknown'
                if hasattr(node.status, 'conditions') and node.status.conditions:
                    try:
                        # Look for Ready condition first
                        ready_condition = None
                        for condition in node.status.conditions:
                            if condition.type == 'Ready':
                                ready_condition = condition
                                break
                        
                        if ready_condition:
                            status = ready_condition.type
                        else:
                            # Fallback to last condition
                            status = node.status.conditions[-1].type
                    except (IndexError, AttributeError):
                        status = 'Unknown'
                
                # Safe access to addresses
                addresses = []
                if hasattr(node.status, 'addresses') and node.status.addresses:
                    try:
                        addresses = [a.address for a in node.status.addresses if hasattr(a, 'address')]
                    except (AttributeError, TypeError):
                        addresses = []
                
                # Extract internal IP from addresses
                internal_ip = "Unknown"
                if addresses:
                    for addr in addresses:
                        if isinstance(addr, str) and addr.replace('.', '').replace('-', '').isdigit():
                            internal_ip = addr
                            break
                
                # Get version information if available
                version = "Unknown"
                if hasattr(node.status, 'node_info') and node.status.node_info:
                    try:
                        version = getattr(node.status.node_info, 'kubelet_version', 'Unknown')
                    except (AttributeError, TypeError):
                        version = "Unknown"
                
                items.append({
                    "name": node_name,
                    "status": status,
                    "roles": "<none>",  # Default value for roles
                    "age": "",  # Default value for age
                    "version": version,
                    "internal_ip": internal_ip,
                    "addresses": str(addresses) if addresses else 'No addresses'
                })
            except Exception as node_error:
                # If there's an error processing a specific node, log it and continue
                items.append({
                    "name": "Error processing node",
                    "status": "Error",
                    "addresses": f"Error: {str(node_error)}"
                })
    else:
        return JSONResponse(status_code=400, content={"error": "Unsupported resource type"})
    
    return {"output": items, "items": items}  # Support both formats for backward compatibility
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {str(e)}"}
        )

@app.post("/kubectl_raw")
def kubectl_raw(command: str = Query(..., description="kubectl command after 'kubectl' (e.g., 'get pods -A')")):
    # WARNING: This is only for dev environments! Do NOT use in production!
    if os.environ.get("ENV", "dev") != "dev":
        return JSONResponse(status_code=403, content={"error": "Raw kubectl commands are only allowed in dev environments."})
    
    try:
        # Parse the command
        parts = command.strip().split()
        if not parts:
            return JSONResponse(status_code=400, content={"error": "Empty command"})
        
        # Load Kubernetes config
        try:
            config.load_incluster_config()
        except Exception as e:
            try:
                config.load_kube_config()
            except Exception as config_error:
                return JSONResponse(
                    status_code=500, 
                    content={
                        "error": f"Failed to load Kubernetes config: {str(config_error)}",
                        "stdout": "",
                        "stderr": f"Kubernetes config error: {str(config_error)}",
                        "returncode": 1
                    }
                )
        
        # Handle different kubectl commands
        if parts[0] == "get":
            return handle_kubectl_get(parts[1:])
        elif parts[0] == "describe":
            return handle_kubectl_describe(parts[1:])
        elif parts[0] == "logs":
            return handle_kubectl_logs(parts[1:])
        else:
            return JSONResponse(
                status_code=400, 
                content={
                    "error": f"Unsupported command: {parts[0]}",
                    "stdout": "",
                    "stderr": f"Unsupported command: {parts[0]}",
                    "returncode": 1
                }
            )
            
    except Exception as e:
        return JSONResponse(
            status_code=500, 
            content={
                "error": str(e),
                "stdout": "",
                "stderr": str(e),
                "returncode": 1
            }
        )

def handle_kubectl_get(args):
    """Handle kubectl get commands using Python client"""
    try:
        v1 = client.CoreV1Api()
        apps_v1 = client.AppsV1Api()
        
        if not args:
            return {"stdout": "", "stderr": "No resource type specified", "returncode": 1}
        
        resource_type = args[0]
        all_namespaces = "-A" in args or "--all-namespaces" in args
        
        # Parse namespace from args (e.g., -n smartops)
        target_namespace = "default"
        for i, arg in enumerate(args):
            if arg == "-n" and i + 1 < len(args):
                target_namespace = args[i + 1]
                break
            elif arg.startswith("--namespace="):
                target_namespace = arg.split("=", 1)[1]
                break
        
        # Debug logging
        print(f"DEBUG: resource_type={resource_type}, all_namespaces={all_namespaces}, target_namespace={target_namespace}, args={args}")
        
        if resource_type == "pods":
            if all_namespaces:
                items = v1.list_pod_for_all_namespaces().items
            else:
                items = v1.list_namespaced_pod(target_namespace).items
            
            output_lines = ["NAME\tNAMESPACE\tSTATUS\tNODE\tSTART_TIME"]
            for pod in items:
                start_time = str(pod.status.start_time) if pod.status.start_time else ""
                node = getattr(pod.spec, 'node_name', '')
                output_lines.append(f"{pod.metadata.name}\t{pod.metadata.namespace}\t{pod.status.phase}\t{node}\t{start_time}")
            
            output = "\n".join(output_lines)
            print(f"DEBUG: pods output length={len(output)}, lines={len(output_lines)}")
            return {"stdout": output, "stderr": "", "returncode": 0}
            
        elif resource_type == "services":
            if all_namespaces:
                items = v1.list_service_for_all_namespaces().items
            else:
                items = v1.list_namespaced_service(target_namespace).items
            
            output_lines = ["NAME\tNAMESPACE\tTYPE\tCLUSTER-IP\tPORTS"]
            for svc in items:
                ports = str(svc.spec.ports) if svc.spec.ports else ""
                output_lines.append(f"{svc.metadata.name}\t{svc.metadata.namespace}\t{svc.spec.type}\t{svc.spec.cluster_ip}\t{ports}")
            
            return {"stdout": "\n".join(output_lines), "stderr": "", "returncode": 0}
            
        elif resource_type == "deployments":
            if all_namespaces:
                items = apps_v1.list_deployment_for_all_namespaces().items
            else:
                items = apps_v1.list_deployment_for_all_namespaces().items
            
            output_lines = ["NAME\tNAMESPACE\tREPLICAS\tAVAILABLE\tUPDATED"]
            for dep in items:
                output_lines.append(f"{dep.metadata.name}\t{dep.metadata.namespace}\t{dep.status.replicas}\t{dep.status.available_replicas}\t{dep.status.updated_replicas}")
            
            return {"stdout": "\n".join(output_lines), "stderr": "", "returncode": 0}
            
        elif resource_type == "nodes":
            items = v1.list_node().items
            output_lines = ["NAME\tSTATUS\tADDRESSES"]
            for node in items:
                status = node.status.conditions[-1].type if node.status.conditions else ""
                addresses = ", ".join([a.address for a in node.status.addresses])
                output_lines.append(f"{node.metadata.name}\t{status}\t{addresses}")
            
            return {"stdout": "\n".join(output_lines), "stderr": "", "returncode": 0}
            
        else:
            return {"stdout": "", "stderr": f"Unsupported resource type: {resource_type}. Supported: pods, services, deployments, nodes", "returncode": 1}
            
    except Exception as e:
        return {"stdout": "", "stderr": str(e), "returncode": 1}

def handle_kubectl_describe(args):
    """Handle kubectl describe commands using Python client"""
    try:
        v1 = client.CoreV1Api()
        apps_v1 = client.AppsV1Api()
        
        if not args:
            return {"stdout": "", "stderr": "No resource specified", "returncode": 1}
        
        resource_type = args[0]
        resource_name = args[1] if len(args) > 1 else None
        namespace = args[2] if len(args) > 2 else "default"
        
        if resource_type == "pod":
            if not resource_name:
                return {"stdout": "", "stderr": "Pod name required", "returncode": 1}
            pod = v1.read_namespaced_pod(name=resource_name, namespace=namespace)
            # Convert to YAML-like format
            output = f"Name:         {pod.metadata.name}\n"
            output += f"Namespace:    {pod.metadata.namespace}\n"
            output += f"Status:       {pod.status.phase}\n"
            output += f"Node:         {getattr(pod.spec, 'node_name', '')}\n"
            output += f"Start Time:   {pod.status.start_time}\n"
            return {"stdout": output, "stderr": "", "returncode": 0}
            
        else:
            return {"stdout": "", "stderr": f"Unsupported resource type for describe: {resource_type}", "returncode": 1}
            
    except Exception as e:
        return {"stdout": "", "stderr": str(e), "returncode": 1}

def handle_kubectl_logs(args):
    """Handle kubectl logs commands using Python client"""
    try:
        v1 = client.CoreV1Api()
        
        if not args:
            return {"stdout": "", "stderr": "Pod name required", "returncode": 1}
        
        pod_name = args[0]
        namespace = "default"
        container = None
        
        # Parse additional arguments
        for i, arg in enumerate(args[1:], 1):
            if arg == "-n" and i + 1 < len(args):
                namespace = args[i + 1]
            elif arg == "-c" and i + 1 < len(args):
                container = args[i + 1]
        
        logs = v1.read_namespaced_pod_log(name=pod_name, namespace=namespace, container=container)
        return {"stdout": logs, "stderr": "", "returncode": 0}
        
    except Exception as e:
        return {"stdout": "", "stderr": str(e), "returncode": 1}

@app.get("/kubectl_namespaces")
def kubectl_namespaces():
    try:
        config.load_incluster_config()
    except Exception:
        config.load_kube_config()
    v1 = client.CoreV1Api()
    ns_list = v1.list_namespace()
    namespaces = [ns.metadata.name for ns in ns_list.items]
    return {"namespaces": namespaces}

@app.get("/kubectl_resource_types")
def kubectl_resource_types():
    # Only allow safe resource types
    return {"resource_types": ["pods", "services", "deployments", "nodes", "events"]} 

# Simulated incident data (replace with real DB/API integration)
incident_data = [
    {"timestamp": "2024-05-01 10:00:00", "namespace": "default", "app": "sample-app-1", "type": "CPU Spike", "details": "CPU > 90% for 5m", "root_cause": "Traffic surge", "impact": "Slow response", "remediation": "Scaled up replicas"},
    {"timestamp": "2024-05-01 11:30:00", "namespace": "default", "app": "sample-app-2", "type": "Pod Crash", "details": "OOMKilled", "root_cause": "Memory leak", "impact": "Pod restart", "remediation": "Fixed memory leak"},
    {"timestamp": "2024-05-02 09:15:00", "namespace": "smartops", "app": "sample-app-3", "type": "Alert Sent", "details": "Telegram alert", "root_cause": "Manual scale down", "impact": "Reduced capacity", "remediation": "Restored replicas"},
]

class PostmortemReport(BaseModel):
    timestamp: str
    namespace: str
    app: str
    type: str
    details: str
    root_cause: str
    impact: str
    remediation: str
    report: str

@app.get("/incidents")
async def get_incidents():
    return {"incidents": incident_data}

@app.post("/postmortem")
async def save_postmortem(report: PostmortemReport):
    # In real use, save to DB
    incident_data.append(report.dict())
    return {"status": "success", "msg": "Postmortem report saved."} 

@app.get("/service_dependencies")
async def get_service_dependencies():
    # Simulated data; replace with real service mesh/network flow data
    return {
        "edges": [
            ["frontend", "backend"],
            ["backend", "database"],
            ["frontend", "auth"],
            ["auth", "database"],
            ["worker", "database"],
            ["worker", "cache"],
            ["frontend", "worker"],
        ]
    } 