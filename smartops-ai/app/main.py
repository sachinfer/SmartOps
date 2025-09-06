from fastapi import FastAPI, Request
from pydantic import BaseModel
import numpy as np
import joblib
import subprocess
import json
import re

app = FastAPI()
model = joblib.load("/app/app/model/isolation_forest.pkl")

class InputData(BaseModel):
    cpu: float
    memory: float

@app.post("/predict")
def predict_anomaly(data: InputData):
    features = np.array([[data.cpu, data.memory]])
    prediction = model.predict(features)
    is_anomaly = bool(prediction[0] == -1)
    return {
        "anomaly": is_anomaly,
        "message": "Anomaly detected" if is_anomaly else "Normal"
    }

def get_kubectl_output(command):
    """Execute kubectl command and return output"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        return result.stdout.strip()
    except Exception as e:
        print(f"Error executing kubectl command: {e}")
        return ""

@app.get("/cluster_metrics")
def get_cluster_metrics():
    """Get cluster-wide CPU and memory metrics"""
    try:
        # Get node metrics using kubectl
        nodes_output = get_kubectl_output("kubectl top nodes --no-headers")
        
        total_cpu_usage = 0
        total_cpu_capacity = 0
        total_memory_usage = 0
        total_memory_capacity = 0
        
        if nodes_output:
            for line in nodes_output.strip().split('\n'):
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 5:
                        # Parse CPU usage (cores)
                        cpu_usage_str = parts[2]
                        cpu_usage = float(cpu_usage_str.replace('m', '')) / 1000 if 'm' in cpu_usage_str else float(cpu_usage_str)
                        
                        # Parse CPU capacity (cores)
                        cpu_capacity_str = parts[3]
                        cpu_capacity = float(cpu_capacity_str.replace('m', '')) / 1000 if 'm' in cpu_capacity_str else float(cpu_capacity_str)
                        
                        # Parse memory usage (bytes)
                        memory_usage_str = parts[4]
                        memory_usage = parse_memory(memory_usage_str)
                        
                        # Parse memory capacity (bytes)
                        memory_capacity_str = parts[5]
                        memory_capacity = parse_memory(memory_capacity_str)
                        
                        total_cpu_usage += cpu_usage
                        total_cpu_capacity += cpu_capacity
                        total_memory_usage += memory_usage
                        total_memory_capacity += memory_capacity
        
        return {
            "cpu_usage": total_cpu_usage,
            "cpu_capacity": total_cpu_capacity,
            "memory_usage": total_memory_usage,
            "memory_capacity": total_memory_capacity
        }
    except Exception as e:
        print(f"Error getting cluster metrics: {e}")
        return {
            "cpu_usage": 0,
            "cpu_capacity": 1,
            "memory_usage": 0,
            "memory_capacity": 1
        }

@app.get("/node_metrics")
def get_node_metrics():
    """Get node-level CPU and memory metrics"""
    try:
        nodes_output = get_kubectl_output("kubectl top nodes --no-headers")
        nodes = []
        
        if nodes_output:
            for line in nodes_output.strip().split('\n'):
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 6:
                        node_name = parts[0]
                        
                        # Parse CPU usage (cores)
                        cpu_usage_str = parts[2]
                        cpu_usage = float(cpu_usage_str.replace('m', '')) / 1000 if 'm' in cpu_usage_str else float(cpu_usage_str)
                        
                        # Parse CPU capacity (cores)
                        cpu_capacity_str = parts[3]
                        cpu_capacity = float(cpu_capacity_str.replace('m', '')) / 1000 if 'm' in cpu_capacity_str else float(cpu_capacity_str)
                        
                        # Parse memory usage (bytes)
                        memory_usage_str = parts[4]
                        memory_usage = parse_memory(memory_usage_str)
                        
                        # Parse memory capacity (bytes)
                        memory_capacity_str = parts[5]
                        memory_capacity = parse_memory(memory_capacity_str)
                        
                        # Get node status
                        status_output = get_kubectl_output(f"kubectl get node {node_name} -o jsonpath='{{.status.conditions[?(@.type==\"Ready\")].status}}'")
                        status = "Ready" if status_output == "True" else "NotReady"
                        
                        nodes.append({
                            "name": node_name,
                            "cpu_usage": cpu_usage,
                            "cpu_capacity": cpu_capacity,
                            "memory_usage": memory_usage,
                            "memory_capacity": memory_capacity,
                            "status": status
                        })
        
        return {"nodes": nodes}
    except Exception as e:
        print(f"Error getting node metrics: {e}")
        return {"nodes": []}

def parse_memory(memory_str):
    """Parse memory string to bytes"""
    try:
        if 'Ki' in memory_str:
            return int(memory_str.replace('Ki', '')) * 1024
        elif 'Mi' in memory_str:
            return int(memory_str.replace('Mi', '')) * 1024 * 1024
        elif 'Gi' in memory_str:
            return int(memory_str.replace('Gi', '')) * 1024 * 1024 * 1024
        elif 'Ti' in memory_str:
            return int(memory_str.replace('Ti', '')) * 1024 * 1024 * 1024 * 1024
        else:
            return int(memory_str)
    except:
        return 0

@app.get("/namespaces")
def get_namespaces():
    """Get all namespaces"""
    try:
        output = get_kubectl_output("kubectl get namespaces --no-headers -o custom-columns=NAME:.metadata.name")
        namespaces = [ns.strip() for ns in output.split('\n') if ns.strip()]
        return {"namespaces": namespaces}
    except Exception as e:
        print(f"Error getting namespaces: {e}")
        return {"namespaces": []}

@app.get("/namespace_stats")
def get_namespace_stats(namespace: str = "all"):
    """Get namespace statistics"""
    try:
        if namespace == "all":
            # Get stats for all namespaces
            output = get_kubectl_output("kubectl get pods --all-namespaces --no-headers | wc -l")
            pod_count = int(output.strip()) if output.strip().isdigit() else 0
            
            services_output = get_kubectl_output("kubectl get services --all-namespaces --no-headers | wc -l")
            service_count = int(services_output.strip()) if services_output.strip().isdigit() else 0
        else:
            # Get stats for specific namespace
            output = get_kubectl_output(f"kubectl get pods -n {namespace} --no-headers | wc -l")
            pod_count = int(output.strip()) if output.strip().isdigit() else 0
            
            services_output = get_kubectl_output(f"kubectl get services -n {namespace} --no-headers | wc -l")
            service_count = int(services_output.strip()) if services_output.strip().isdigit() else 0
        
        return {
            "pod_count": pod_count,
            "service_count": service_count
        }
    except Exception as e:
        print(f"Error getting namespace stats: {e}")
        return {"pod_count": 0, "service_count": 0}

@app.get("/pods")
def get_pods(namespace: str = "default"):
    """Get pods for a specific namespace"""
    try:
        output = get_kubectl_output(f"kubectl get pods -n {namespace} --no-headers")
        pods = []
        
        if output:
            for line in output.strip().split('\n'):
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 4:
                        pod_name = parts[0]
                        ready = parts[1]
                        status = parts[2]
                        age = parts[3]
                        
                        # Get pod details
                        pod_details = get_kubectl_output(f"kubectl get pod {pod_name} -n {namespace} -o json")
                        if pod_details:
                            try:
                                pod_json = json.loads(pod_details)
                                containers = pod_json.get('spec', {}).get('containers', [])
                                container_names = [c.get('name', '') for c in containers]
                            except:
                                container_names = []
                        else:
                            container_names = []
                        
                        pods.append({
                            "name": pod_name,
                            "ready": ready,
                            "status": status,
                            "age": age,
                            "namespace": namespace,
                            "containers": container_names
                        })
        
        return {"pods": pods}
    except Exception as e:
        print(f"Error getting pods: {e}")
        return {"pods": []}

@app.get("/logs")
def get_logs(namespace: str, pod: str, container: str = None):
    """Get logs for a specific pod"""
    try:
        cmd = f"kubectl logs {pod} -n {namespace}"
        if container:
            cmd += f" -c {container}"
        cmd += " --tail=100"
        
        output = get_kubectl_output(cmd)
        return {"logs": output}
    except Exception as e:
        print(f"Error getting logs: {e}")
        return {"logs": ""}

@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "SmartOps by Misi 24x7 API is running"}

# Unit test for FastAPI endpoint
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
