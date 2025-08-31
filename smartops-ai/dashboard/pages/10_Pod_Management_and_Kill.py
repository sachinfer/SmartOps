import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime

def show_page():
    """Pod Management and Kill Page - Accessible from SmartOps Navigation Bar"""
    
    st.title("🔴 Pod Management & Kill Operations")
    st.markdown("**Monitor and manage pods in real-time. Kill stressed or problematic pods directly from this dashboard.**")
    
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
    
    # Function to get individual pod resource usage
    def get_pod_resource_usage():
        try:
            # Use kubectl top pods to get real-time resource usage
            import subprocess
            result = subprocess.run(
                ["kubectl", "top", "pods", "-n", "smartops", "--no-headers"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                pod_metrics = {}
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 3:
                            pod_name = parts[0]
                            cpu = parts[1]
                            memory = parts[2]
                            pod_metrics[pod_name] = {
                                "cpu": cpu,
                                "memory": memory
                            }
                return pod_metrics
            else:
                # If kubectl top fails, return empty dict but don't break the page
                st.info("ℹ️ Resource usage not available (kubectl permissions required)")
                return {}
        except Exception as e:
            # If any error occurs, return empty dict but don't break the page
            st.info("ℹ️ Resource usage not available (kubectl not accessible)")
            return {}
    
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
    
    # Show pod count info
    if pods_data:
        st.info(f"📊 API returned {len(pods_data)} pods")
    
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
        
        # Get real-time resource usage for each pod (optional)
        pod_resources = get_pod_resource_usage()
        
        # Add resource usage columns (with fallbacks)
        def get_pod_cpu(pod_name):
            if pod_name in pod_resources:
                return pod_resources[pod_name].get("cpu", "N/A")
            return "N/A"
        
        def get_pod_memory(pod_name):
            if pod_name in pod_resources:
                return pod_resources[pod_name].get("memory", "N/A")
            return "N/A"
        
        # Always add these columns, even if empty
        pods_df["cpu_usage"] = pods_df["name"].apply(get_pod_cpu)
        pods_df["memory_usage"] = pods_df["name"].apply(get_pod_memory)
        
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
        
        # Add stress indicators
        def get_stress_indicator(row):
            cpu = row.get("cpu_usage", "N/A")
            memory = row.get("memory_usage", "N/A")
            
            if cpu != "N/A" and memory != "N/A":
                try:
                    # Check if CPU is high (e.g., > 100m or > 1 core)
                    if "m" in cpu:
                        cpu_val = float(cpu.replace("m", "")) / 1000
                    else:
                        cpu_val = float(cpu)
                    
                    # Check if memory is high (e.g., > 100Mi)
                    if "Mi" in memory:
                        mem_val = float(memory.replace("Mi", ""))
                    elif "Gi" in memory:
                        mem_val = float(memory.replace("Gi", "")) * 1024
                    else:
                        mem_val = 0
                    
                    if cpu_val > 0.5 or mem_val > 200:  # High CPU (>0.5 cores) or high memory (>200Mi)
                        return "🚨 HIGH"
                    elif cpu_val > 0.2 or mem_val > 100:  # Moderate usage
                        return "⚠️ MODERATE"
                    else:
                        return "✅ NORMAL"
                except:
                    return "❓ UNKNOWN"
            else:
                # If no resource data available, show as normal
                return "✅ NORMAL"
        
        # Always add stress level column
        pods_df["Stress_Level"] = pods_df.apply(get_stress_indicator, axis=1)
        
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
        
        # Add resource usage columns
        if "cpu_usage" in available_columns:
            display_columns.append("cpu_usage")
            column_names.append("CPU Usage")
        
        if "memory_usage" in available_columns:
            display_columns.append("memory_usage")
            column_names.append("Memory Usage")
        
        if "Stress_Level" in available_columns:
            display_columns.append("Stress_Level")
            column_names.append("Stress Level")
        
        # Only add containers if it exists
        if "containers" in available_columns:
            display_columns.append("containers")
            column_names.append("Containers")
        
        # Create display DataFrame with available columns
        display_df = pods_df[display_columns].copy()
        display_df.columns = column_names
        
        st.dataframe(display_df, width='stretch')
        
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
                
                # Resource usage display
                st.markdown("#### 📊 Resource Usage")
                pod_resources = get_pod_resource_usage()
                if selected_pod in pod_resources:
                    resources = pod_resources[selected_pod]
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        cpu = resources.get("cpu", "N/A")
                        st.metric("CPU Usage", cpu)
                        # Add stress indicator
                        if cpu != "N/A":
                            try:
                                if "m" in cpu:
                                    cpu_val = float(cpu.replace("m", "")) / 1000
                                else:
                                    cpu_val = float(cpu)
                                
                                if cpu_val > 0.5:
                                    st.error("🚨 High CPU consumption detected!")
                                elif cpu_val > 0.2:
                                    st.warning("⚠️ Moderate CPU usage")
                                else:
                                    st.success("✅ CPU usage normal")
                            except:
                                st.info("ℹ️ CPU usage unknown")
                    
                    with col2:
                        memory = resources.get("memory", "N/A")
                        st.metric("Memory Usage", memory)
                        # Add stress indicator
                        if memory != "N/A":
                            try:
                                if "Mi" in memory:
                                    mem_val = float(memory.replace("Mi", ""))
                                elif "Gi" in memory:
                                    mem_val = float(memory.replace("Gi", "")) * 1024
                                else:
                                    mem_val = 0
                                
                                if mem_val > 200:
                                    st.error("🚨 High memory consumption detected!")
                                elif mem_val > 100:
                                    st.warning("⚠️ Moderate memory usage")
                                else:
                                    st.success("✅ Memory usage normal")
                            except:
                                st.info("ℹ️ Memory usage unknown")
                else:
                    st.info("ℹ️ Resource usage not available for this pod")
                
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
                    if st.button("🚫 Ignore Pod", key=f"ignore_{selected_pod}", type="secondary"):
                        # Add to ignored pods list
                        if 'ignored_pods' not in st.session_state:
                            st.session_state.ignored_pods = set()
                        st.session_state.ignored_pods.add(selected_pod)
                        st.success(f"Pod {selected_pod} added to ignore list")
                        st.rerun()
                
                with col3:
                    if st.button("📋 View Logs", key=f"logs_{selected_pod}"):
                        st.info(f"Logs for {selected_pod} would be displayed here")
                
                with col4:
                    if st.button("🔍 Describe Pod", key=f"describe_{selected_pod}"):
                        st.info(f"Pod description for {selected_pod} would be displayed here")
    
    # Stressed Pods Summary Section
    st.markdown("### 🚨 Stressed Pods Summary")
    
    if pods_data:
        # Count stressed pods
        high_stress_count = 0
        moderate_stress_count = 0
        normal_count = 0
        
        for pod in pods_data:
            pod_name = pod.get("name", "")
            if pod_name in pod_resources:
                resources = pod_resources[pod_name]
                cpu = resources.get("cpu", "N/A")
                memory = resources.get("memory", "N/A")
                
                if cpu != "N/A" and memory != "N/A":
                    try:
                        # Check CPU stress
                        if "m" in cpu:
                            cpu_val = float(cpu.replace("m", "")) / 1000
                        else:
                            cpu_val = float(cpu)
                        
                        # Check memory stress
                        if "Mi" in memory:
                            mem_val = float(memory.replace("Mi", ""))
                        elif "Gi" in memory:
                            mem_val = float(memory.replace("Gi", "")) * 1024
                        else:
                            mem_val = 0
                        
                        if cpu_val > 0.5 or mem_val > 200:
                            high_stress_count += 1
                        elif cpu_val > 0.2 or mem_val > 100:
                            moderate_stress_count += 1
                        else:
                            normal_count += 1
                    except:
                        normal_count += 1
                else:
                    normal_count += 1
        
        # Display stress summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🚨 High Stress", high_stress_count, delta="Requires attention")
        
        with col2:
            st.metric("⚠️ Moderate Stress", moderate_stress_count, delta="Monitor closely")
        
        with col3:
            st.metric("✅ Normal", normal_count, delta="Healthy")
        
        # Show ignored pods
        if 'ignored_pods' in st.session_state and st.session_state.ignored_pods:
            st.markdown("#### 🚫 Ignored Pods")
            ignored_list = list(st.session_state.ignored_pods)
            st.info(f"Pods marked as ignored: {', '.join(ignored_list)}")
            
            if st.button("🔄 Clear Ignore List"):
                st.session_state.ignored_pods.clear()
                st.success("Ignore list cleared")
                st.rerun()
    
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
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🚨 Kill All Stressed Pods", key="kill_all_stressed"):
            # Find and kill all high-stress pods
            high_stress_pods = []
            for pod in pods_data:
                pod_name = pod.get("name", "")
                if pod_name in pod_resources:
                    resources = pod_resources[pod_name]
                    cpu = resources.get("cpu", "N/A")
                    memory = resources.get("memory", "N/A")
                    
                    if cpu != "N/A" and memory != "N/A":
                        try:
                            if "m" in cpu:
                                cpu_val = float(cpu.replace("m", "")) / 1000
                            else:
                                cpu_val = float(cpu)
                            
                            if "Mi" in memory:
                                mem_val = float(memory.replace("Mi", ""))
                            elif "Gi" in memory:
                                mem_val = float(memory.replace("Gi", "")) * 1024
                            else:
                                mem_val = 0
                            
                            if cpu_val > 0.5 or mem_val > 200:
                                high_stress_pods.append(pod_name)
                        except:
                            pass
            
            if high_stress_pods:
                st.warning(f"🚨 Found {len(high_stress_pods)} high-stress pods: {', '.join(high_stress_pods)}")
                if st.button("✅ Confirm Kill All Stressed", key="confirm_kill_all"):
                    with st.spinner("Killing all stressed pods..."):
                        killed_count = 0
                        for pod_name in high_stress_pods:
                            success, _ = kill_pod(pod_name)
                            if success:
                                killed_count += 1
                        st.success(f"✅ Successfully killed {killed_count}/{len(high_stress_pods)} stressed pods")
                        st.rerun()
            else:
                st.success("✅ No high-stress pods found")
    
    with col2:
        if st.button("🔄 Restart All Pods", key="restart_all"):
            st.info("This would restart all pods in the namespace")
    
    with col3:
        if st.button("📊 Generate Report", key="generate_report"):
            st.info("This would generate a pod health report")
    
    with col4:
        if st.button("🧹 Cleanup Ignored", key="cleanup_ignored"):
            if 'ignored_pods' in st.session_state and st.session_state.ignored_pods:
                ignored_count = len(st.session_state.ignored_pods)
                st.session_state.ignored_pods.clear()
                st.success(f"🧹 Cleaned up {ignored_count} ignored pods")
                st.rerun()
            else:
                st.info("ℹ️ No ignored pods to clean up")
    
    # Footer
    st.markdown("---")
    st.markdown("*Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "*")
    st.markdown("**⚠️ Warning: Pod killing operations are irreversible. Use with caution!**")

if __name__ == "__main__":
    show_page()
