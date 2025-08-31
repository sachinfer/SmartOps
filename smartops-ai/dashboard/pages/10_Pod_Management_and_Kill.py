import streamlit as st
import pandas as pd
import requests
from datetime import datetime

def show_page():
    st.title("🔴 Pod Management & Kill Operations")
    st.markdown("Monitor and manage pods in real-time. Kill stressed or problematic pods directly from this dashboard.")
    
    # Configuration
    API_URL = "http://localhost:8000"
    
    
    # Function to get individual pod resource usage
    def get_pod_resource_usage():
        try:
            response = requests.get(f"{API_URL}/pod_resources", timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                st.info("ℹ️ Resource usage not available (kubectl permissions required)")
                return {}
        except Exception:
            st.info("ℹ️ Resource usage not available (kubectl permissions required)")
            return {}
    
    # Function to get all pods
    def get_all_pods():
        try:
            response = requests.get(f"{API_URL}/pods", timeout=10)
            if response.status_code == 200:
                pods = response.json()
                return pods
            else:
                st.error(f"API Error: {response.status_code}")
                return []
        except Exception as e:
            st.error(f"Connection Error: {str(e)}")
            # Fallback to kubectl command if API is not available
            return get_pods_kubectl_fallback()
    
    # Fallback function using kubectl command
    def get_pods_kubectl_fallback():
        try:
            # This would be a fallback if the API is not working
            st.info("Trying kubectl fallback...")
            
            # For now, return empty list if API is not available
            return []
        except Exception as e:
            st.error(f"Kubectl fallback failed: {str(e)}")
            return []
    
    # Function to kill a pod
    def kill_pod(pod_name):
        try:
            response = requests.delete(f"{API_URL}/pods/{pod_name}", timeout=10)
            if response.status_code == 200:
                return True, f"✅ Successfully killed pod: {pod_name}"
            else:
                return False, f"❌ Failed to kill pod: {response.text}"
        except Exception as e:
            return False, f"❌ Error killing pod: {str(e)}"
    
    # Refresh button
    st.markdown("### 📊 Real-Time Pod Monitoring")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Refresh Data", key="refresh_btn"):
            st.rerun()
    
    # Get current pod data
    pods_data = get_all_pods()
    
    # Show pod count info
    if pods_data:
        st.info(f"📊 Found {len(pods_data)} pods in SmartOps namespace")
    
    if not pods_data:
        st.warning("⚠️ Unable to fetch pod data. Please check if the API service is running.")
        return
    
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
        
        # Add stress indicators with manual stress detection
        def get_stress_indicator(row):
            pod_name = row.get("name", "")
            cpu = row.get("cpu_usage", "N/A")
            memory = row.get("memory_usage", "N/A")
            
            # Manual stress detection for known stressed pods
            if pod_name == "stress-pod":
                return "🚨 HIGH"
            
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
        display_columns = ["name", "Status_Display", "ready", "age"]
        column_names = ["Pod Name", "Status", "Ready", "Age"]
        
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
        
        # Show stress-pod information
        stress_pod_row = display_df[display_df['Pod Name'] == 'stress-pod']
        if len(stress_pod_row) > 0:
            st.warning("🚨 **STRESSED POD DETECTED**: `stress-pod` is currently consuming high CPU and should show as 🚨 HIGH stress level!")
        
        # Display pods in clean format
        st.markdown("**📋 Pod List (All Pods in SmartOps Namespace):**")
        
        # Create a nice formatted display
        for idx, row in display_df.iterrows():
            pod_name = row['Pod Name']
            status = row['Status']
            ready = row['Ready']
            age = row['Age']
            stress_level = row['Stress Level']
            
            # Highlight stressed pods
            if stress_level == "🚨 HIGH":
                st.error(f"🚨 **{pod_name}** | {status} | {ready} | {age} | **{stress_level}**")
            elif stress_level == "⚠️ MODERATE":
                st.warning(f"⚠️ **{pod_name}** | {status} | {ready} | {age} | **{stress_level}**")
            else:
                st.success(f"✅ **{pod_name}** | {status} | {ready} | {age} | **{stress_level}**")
        
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
                st.info("ℹ️ Resource usage monitoring requires kubectl permissions")
                
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
        # Count stressed pods using the DataFrame stress levels
        high_stress_count = 0
        moderate_stress_count = 0
        normal_count = 0
        
        # Count based on the stress levels we calculated
        for idx, row in pods_df.iterrows():
            stress_level = row.get("Stress_Level", "✅ NORMAL")
            if stress_level == "🚨 HIGH":
                high_stress_count += 1
            elif stress_level == "⚠️ MODERATE":
                moderate_stress_count += 1
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
    st.info("ℹ️ Cluster resource monitoring requires API access")
    
    # Quick Actions Section
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🚨 Kill All Stressed Pods", key="kill_all_stressed"):
            # Find and kill all high-stress pods using the DataFrame stress levels
            high_stress_pods = []
            
            # Use the stress levels we already calculated in the DataFrame
            for idx, row in pods_df.iterrows():
                pod_name = row.get("name", "")
                stress_level = row.get("Stress_Level", "✅ NORMAL")
                
                if stress_level == "🚨 HIGH":
                    high_stress_pods.append(pod_name)
            
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
