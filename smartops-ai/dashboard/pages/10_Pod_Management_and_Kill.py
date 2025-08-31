import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime

def show_page():
    """Pod Management and Kill Page - Accessible from SmartOps Navigation Bar"""
    
    st.title("🔴 Pod Management & Kill Operations")
    st.markdown("**Monitor and manage pods in real-time. Kill stressed or problematic pods directly from this dashboard.**")
    
    # Current testing status
    st.info("🧪 **Testing Mode**: A `stress-test-pod` is currently running for testing anomaly detection and pod killing functionality.")
    
    # API URL
    API_URL = "http://localhost:8000"
    
    # Function to get pod metrics
    def get_pod_metrics():
        try:
            response = requests.get(f"{API_URL}/cluster_metrics", timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception:
            return None
    
    # Function to get all pods
    def get_all_pods():
        try:
            response = requests.get(f"{API_URL}/pods", params={"namespace": "smartops"}, timeout=10)
            if response.status_code == 200:
                return response.json().get("pods", [])
            else:
                st.warning(f"⚠️ API returned status {response.status_code}")
                return []
        except Exception as e:
            st.warning(f"⚠️ API connection failed: {str(e)}")
            # Fallback: Try to get pods using kubectl
            try:
                import subprocess
                result = subprocess.run(
                    ["kubectl", "get", "pods", "-n", "smartops", "-o", "json"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    import json
                    pods_json = json.loads(result.stdout)
                    pods = []
                    for pod in pods_json.get("items", []):
                        pod_data = {
                            "name": pod["metadata"]["name"],
                            "ready": f"{pod['status']['readyReplicas']}/{pod['spec']['replicas']}" if 'readyReplicas' in pod['status'] else "1/1",
                            "status": pod["status"]["phase"],
                            "age": "unknown",  # Would need to calculate from creationTimestamp
                            "namespace": pod["metadata"]["namespace"]
                        }
                        pods.append(pod_data)
                    return pods
                else:
                    st.error(f"⚠️ kubectl fallback failed: {result.stderr}")
                    return []
            except Exception as kubectl_error:
                st.error(f"⚠️ kubectl fallback error: {str(kubectl_error)}")
                return []
    
    # Function to kill a pod
    def kill_pod(pod_name, namespace="smartops"):
        try:
            # Use kubectl delete command
            import subprocess
            result = subprocess.run(
                ["kubectl", "delete", "pod", pod_name, "-n", namespace],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return True, f"Pod {pod_name} killed successfully"
            else:
                return False, f"Failed to kill pod: {result.stderr}"
        except Exception as e:
            # Fallback: Try to use the API if kubectl is not available
            try:
                st.info(f"🔄 kubectl not available, trying API fallback...")
                # This would be implemented in the API
                return False, f"kubectl not available in container. Use: kubectl delete pod {pod_name} -n {namespace}"
            except Exception as api_error:
                return False, f"Error killing pod: {str(e)}. Manual command: kubectl delete pod {pod_name} -n {namespace}"
    
    # Real-time monitoring section
    st.markdown("### 📊 Real-Time Pod Monitoring")
    
    # Auto-refresh every 10 seconds
    if st.button("🔄 Refresh Data", key="refresh_btn"):
        st.rerun()
    
    # Get current pod data
    pods_data = get_all_pods()
    
    # Debug: Show what data structure we're getting
    if pods_data:
        st.info(f"📊 API returned {len(pods_data)} pods")
        if len(pods_data) > 0:
            st.json(pods_data[0])  # Show first pod structure for debugging
    
    if not pods_data:
        st.warning("⚠️ Unable to fetch pod data. Please check if the API service is running.")
        # Show sample data for demonstration
        st.info("Showing sample data for demonstration:")
        sample_pods = [
            {
                "name": "stress-test-pod",
                "ready": "1/1",
                "status": "Running",
                "age": "2m",
                "namespace": "smartops"
            },
            {
                "name": "smartops-app-7456b5c68-rw4j8",
                "ready": "1/1",
                "status": "Running",
                "age": "10h",
                "namespace": "smartops"
            }
        ]
        pods_data = sample_pods
    
    # Display pods in a table
    if pods_data:
        st.markdown("#### 🚀 Current Pods in SmartOps Namespace")
        
        # Convert to DataFrame for better display
        pods_df = pd.DataFrame(pods_data)
        
        # Add status indicators
        def get_status_color(status):
            if status == "Running":
                return "🟢"
            elif status == "Pending":
                return "🟡"
            elif status == "Failed":
                return "🔴"
            elif status == "CrashLoopBackOff":
                return "🟠"
            else:
                return "⚪"
        
        pods_df["Status_Icon"] = pods_df["status"].apply(get_status_color)
        pods_df["Status_Display"] = pods_df["Status_Icon"] + " " + pods_df["status"]
        
        # Handle missing columns gracefully
        available_columns = pods_df.columns.tolist()
        
        # Define required columns with fallbacks
        display_columns = []
        column_names = []
        
        if "name" in available_columns:
            display_columns.append("name")
            column_names.append("Pod Name")
        
        if "Status_Display" in available_columns:
            display_columns.append("Status_Display")
            column_names.append("Status")
        
        if "ready" in available_columns:
            display_columns.append("ready")
            column_names.append("Ready")
        
        if "age" in available_columns:
            display_columns.append("age")
            column_names.append("Age")
        
        # Only add containers if it exists
        if "containers" in available_columns:
            display_columns.append("containers")
            column_names.append("Containers")
        
        # Create display DataFrame with available columns
        display_df = pods_df[display_columns].copy()
        display_df.columns = column_names
        
        st.dataframe(display_df, use_container_width=True)
        
        # Pod actions section
        st.markdown("### ⚡ Pod Actions")
        
        # Select pod to manage
        pod_names = [pod["name"] for pod in pods_data]
        selected_pod = st.selectbox("Select Pod to Manage", pod_names, key="pod_selector")
        
        if selected_pod:
            # Get selected pod details
            selected_pod_data = next((pod for pod in pods_data if pod["name"] == selected_pod), None)
            
            if selected_pod_data:
                st.markdown(f"#### 📋 Pod Details: **{selected_pod}**")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Status", selected_pod_data["status"])
                
                with col2:
                    st.metric("Ready", selected_pod_data["ready"])
                
                with col3:
                    st.metric("Age", selected_pod_data["age"])
                
                # Container information
                containers = selected_pod_data.get("containers", [])
                if containers:
                    st.markdown("**Containers:**")
                    for container in containers:
                        st.code(container, language="bash")
                else:
                    st.info("ℹ️ Container information not available")
                
                # Action buttons
                st.markdown("#### 🎯 Available Actions")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button("🔴 Kill Pod", key=f"kill_{selected_pod}", type="primary"):
                        with st.spinner(f"Killing pod {selected_pod}..."):
                            success, message = kill_pod(selected_pod)
                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)
                
                with col2:
                    if st.button("📋 View Logs", key=f"logs_{selected_pod}"):
                        st.info(f"Logs for {selected_pod} would be displayed here")
                
                with col3:
                    if st.button("🔍 Describe Pod", key=f"describe_{selected_pod}"):
                        st.info(f"Pod description for {selected_pod} would be displayed here")
                
                with col4:
                    if st.button("📊 Resource Usage", key=f"resources_{selected_pod}"):
                        st.info(f"Resource usage for {selected_pod} would be displayed here")
    
    # High Resource Usage Alert Section
    st.markdown("### 🚨 High Resource Usage Alerts")
    
    # Get cluster metrics
    cluster_metrics = get_pod_metrics()
    
    if cluster_metrics:
        col1, col2 = st.columns(2)
        
        with col1:
            cpu_usage = cluster_metrics.get("cpu_usage", 0)
            cpu_capacity = cluster_metrics.get("cpu_capacity", 1)
            cpu_percent = (cpu_usage / cpu_capacity * 100) if cpu_capacity > 0 else 0
            
            st.metric(
                "CPU Usage",
                f"{cpu_percent:.1f}%",
                delta=f"{cpu_usage:.2f} cores"
            )
            
            if cpu_percent > 80:
                st.error("🚨 High CPU usage detected!")
            elif cpu_percent > 60:
                st.warning("⚠️ Moderate CPU usage")
            else:
                st.success("✅ CPU usage normal")
        
        with col2:
            memory_usage = cluster_metrics.get("memory_usage", 0)
            memory_capacity = cluster_metrics.get("memory_capacity", 1)
            memory_percent = (memory_usage / memory_capacity * 100) if memory_capacity > 0 else 0
            
            st.metric(
                "Memory Usage",
                f"{memory_percent:.1f}%",
                delta=f"{memory_usage / (1024**3):.2f} GB"
            )
            
            if memory_percent > 80:
                st.error("🚨 High memory usage detected!")
            elif memory_percent > 60:
                st.warning("⚠️ Moderate memory usage")
            else:
                st.success("✅ Memory usage normal")
    
    # Quick Actions Section
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚨 Kill All Stressed Pods", key="kill_all_stressed"):
            st.info("This would kill all pods with high resource usage")
    
    with col2:
        if st.button("🔄 Restart All Pods", key="restart_all"):
            st.info("This would restart all pods in the namespace")
    
    with col3:
        if st.button("📊 Generate Report", key="generate_report"):
            st.info("This would generate a pod health report")
    
    # Footer
    st.markdown("---")
    st.markdown("*Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "*")
    st.markdown("**⚠️ Warning: Pod killing operations are irreversible. Use with caution!**")

if __name__ == "__main__":
    show_page()
