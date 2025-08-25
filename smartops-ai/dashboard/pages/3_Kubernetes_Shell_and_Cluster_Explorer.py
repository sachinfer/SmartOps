import streamlit as st
import pandas as pd
import requests
from sidebar_utils import show_sidebar
import sys
import os

# Import Misi from the dashboard directory
try:
    from misi_chatbot_widget import add_misi_to_page
    MISI_AVAILABLE = True
except ImportError:
    MISI_AVAILABLE = False
    st.warning("Misi AI Chatbot not available. Please ensure the chatbot is properly installed.")

# Check if API service is running
def check_api_health():
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        return response.status_code == 200
    except Exception:
        return False

with st.sidebar:
    show_sidebar()

st.title("🖥️ Kubernetes Shell and Cluster Explorer")

# Check if API service is running and show helpful message
if not check_api_health():
    st.warning("⚠️ **Shell Commands**: Kubernetes shell commands require the backend API service to be running.")

tab1, tab2 = st.tabs(["Shell", "Cluster Explorer"])

with tab1:
    st.header("Kubernetes Shell")
    st.info("Only 'kubectl get', 'kubectl describe', and 'kubectl logs' commands are allowed.")
    
    def execute_kubectl_command(shell_cmd):
        allowed = ["kubectl get", "kubectl describe", "kubectl logs"]
        if not any(shell_cmd.strip().startswith(a) for a in allowed):
            st.error("Only 'kubectl get', 'kubectl describe', and 'kubectl logs' commands are allowed.")
            return
        
        # Debug info
        st.info(f"🔍 Executing command: {shell_cmd}")
        
        with st.spinner("Running kubectl..."):
            try:
                # Extract the command part after 'kubectl '
                raw_cmd = shell_cmd.strip()[len("kubectl "):]
                
                # Make API call to the backend - use kubectl_get instead of kubectl_raw
                if shell_cmd.strip().startswith("kubectl get"):
                    # Parse the command to extract resource type and namespace
                    parts = raw_cmd.split()
                    if len(parts) >= 2:
                        resource_type = parts[1]  # e.g., "nodes", "pods", "services"
                        all_namespaces = "-A" in parts or "--all-namespaces" in parts
                        namespace = "default"
                        
                        # Check if namespace is specified
                        for i, part in enumerate(parts):
                            if part == "-n" and i + 1 < len(parts):
                                namespace = parts[i + 1]
                                all_namespaces = False
                                break
                        
                        # Use kubectl_get endpoint
                        if all_namespaces:
                            resp = requests.get(
                                "http://localhost:8000/kubectl_get",
                                params={"resource_type": resource_type, "all_namespaces": True},
                                timeout=30
                            )
                        else:
                            resp = requests.get(
                                "http://localhost:8000/kubectl_get",
                                params={"resource_type": resource_type, "all_namespaces": False, "namespace": namespace},
                                timeout=30
                            )
                    else:
                        st.error("Invalid kubectl get command format")
                        return
                else:
                    # For other commands, try kubectl_raw (but it might not work)
                    resp = requests.post(
                        "http://localhost:8000/kubectl_raw",
                        params={"command": raw_cmd},
                        timeout=30
                    )
                
                if resp.status_code == 200:
                    data = resp.json()
                    
                    if shell_cmd.strip().startswith("kubectl get"):
                        # Handle kubectl_get endpoint response
                        items = data.get("items", [])
                        if items:
                            st.success("✅ Command executed successfully!")
                            
                            # Store the result in session state
                            st.session_state.last_command_output = {
                                "stdout": str(items),  # Convert items to string for display
                                "stderr": "",
                                "returncode": 0,
                                "command": shell_cmd
                            }
                            
                            # Show raw output
                            st.markdown("**Raw Output:**")
                            st.code(str(items), language="json")
                            
                            # Show parsed table
                            st.markdown("**📊 Parsed Table:**")
                            df = pd.DataFrame(items)
                            st.dataframe(df, use_container_width=True)
                        else:
                            st.warning("⚠️ **No results found**")
                            st.info("This could mean:")
                            st.info("1. The resource type doesn't exist")
                            st.info("2. The namespace is empty")
                            st.info("3. There's an issue with the API call")
                    else:
                        # Handle kubectl_raw endpoint response (for non-get commands)
                        stdout = data.get("stdout", "")
                        stderr = data.get("stderr", "")
                        returncode = data.get("returncode", 0)
                        
                        # Store the result in session state
                        st.session_state.last_command_output = {
                            "stdout": stdout,
                            "stderr": stderr,
                            "returncode": returncode,
                            "command": shell_cmd
                        }
                        
                        if stdout:
                            st.success("✅ Command executed successfully!")
                            st.markdown("**Raw Output:**")
                            st.code(stdout, language="shell")
                        else:
                            st.warning("⚠️ **No output received** from the command")
                        
                        if stderr:
                            st.info(f"ℹ️ stderr: {stderr}")
                        
                        if returncode != 0:
                            st.warning(f"⚠️ kubectl exited with code {returncode}")
                        
                else:
                    st.info(f"ℹ️ API Status: {resp.status_code}")
                    
            except requests.exceptions.Timeout:
                st.info("ℹ️ Request timed out. Please try again.")
            except requests.exceptions.ConnectionError:
                st.info("ℹ️ Cannot connect to backend API. Please ensure the API service is running.")
            except Exception:
                st.info("ℹ️ Error running kubectl")

    # Initialize session state variables
    if "kube_shell_history" not in st.session_state:
        st.session_state.kube_shell_history = []
    if "last_command_output" not in st.session_state:
        st.session_state.last_command_output = None
    if "current_command" not in st.session_state:
        st.session_state.current_command = ""
    if "history_index" not in st.session_state:
        st.session_state.history_index = -1

    # Terminal styling
    st.markdown("""
    <style>
    .terminal-container {
        background-color: #1e1e1e;
        border-radius: 8px;
        padding: 20px;
        font-family: 'Courier New', monospace;
        color: #00ff00;
        border: 1px solid #333;
        margin: 10px 0;
    }
    .terminal-prompt {
        color: #00ff00;
        font-weight: bold;
    }
    .terminal-input {
        background: transparent;
        border: none;
        color: #00ff00;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        outline: none;
        width: 100%;
    }
    .terminal-output {
        color: #ffffff;
        white-space: pre-wrap;
        font-family: 'Courier New', monospace;
        font-size: 12px;
        background-color: #2d2d2d;
        padding: 10px;
        border-radius: 4px;
        margin: 10px 0;
        max-height: 400px;
        overflow-y: auto;
    }
    </style>
    """, unsafe_allow_html=True)

    # Command input section
    col1, col2 = st.columns([1, 20])
    with col1:
        st.markdown('<div class="terminal-prompt">$</div>', unsafe_allow_html=True)
    with col2:
        # Command input
        shell_cmd = st.text_input(
            "kubectl >", 
            value=st.session_state.current_command,
            key=f"shell_cmd_{len(st.session_state.kube_shell_history)}",
            placeholder="Type kubectl command here...",
            help="Use ↑↓ arrows to navigate history, Enter to execute"
        )
        
        # Update current command in session state
        if shell_cmd != st.session_state.current_command:
            st.session_state.current_command = shell_cmd
        
        # Execute button
        if st.button("⏎ Execute", key="execute_btn"):
            if st.session_state.current_command.strip():
                # Add to history if not already there
                if st.session_state.current_command not in st.session_state.kube_shell_history:
                    st.session_state.kube_shell_history.append(st.session_state.current_command)
                
                # Execute the command
                execute_kubectl_command(st.session_state.current_command)
                
                # Reset for next command
                st.session_state.current_command = ""
                st.session_state.history_index = -1
                # Don't rerun here - let the output display naturally

    # Command history navigation
    if st.session_state.kube_shell_history:
        st.markdown("**📜 Command History Navigation:**")
        hist_cols = st.columns(5)
        
        with hist_cols[0]:
            if st.button("↑ Previous", key="hist_up"):
                if st.session_state.history_index < len(st.session_state.kube_shell_history) - 1:
                    st.session_state.history_index += 1
                    st.session_state.current_command = st.session_state.kube_shell_history[-(st.session_state.history_index + 1)]
                    st.rerun()
        
        with hist_cols[1]:
            if st.button("↓ Next", key="hist_down"):
                if st.session_state.history_index > 0:
                    st.session_state.history_index -= 1
                    st.session_state.current_command = st.session_state.kube_shell_history[-(st.session_state.history_index + 1)]
                    st.rerun()
                elif st.session_state.history_index == 0:
                    st.session_state.history_index = -1
                    st.session_state.current_command = ""
                    st.rerun()
        
        with hist_cols[2]:
            if st.button("🔄 Clear History", key="clear_hist"):
                st.session_state.kube_shell_history = []
                st.session_state.history_index = -1
                st.session_state.current_command = ""
                st.rerun()
        
        with hist_cols[3]:
            if st.button("📋 Show History", key="show_hist"):
                st.session_state.show_history = not st.session_state.get("show_history", False)
                st.rerun()

    # Display full command history
    if st.session_state.get("show_history", False) and st.session_state.kube_shell_history:
        st.markdown("#### 📜 Full Command History")
        for i, cmd in enumerate(reversed(st.session_state.kube_shell_history)):
            col1, col2, col3 = st.columns([1, 4, 1])
            with col1:
                st.markdown(f"`{len(st.session_state.kube_shell_history) - i}`")
            with col2:
                st.code(cmd, language="shell")
            with col3:
                if st.button(f"▶️", key=f"hist_exec_{i}"):
                    st.session_state.current_command = cmd
                    st.rerun()

    # Display last command output
    if st.session_state.last_command_output:
        st.markdown("#### 📋 Last Command Output")
        output = st.session_state.last_command_output
        st.markdown(f"**Command:** `{output['command']}`")
        
        if output['stdout']:
            st.markdown("**Output:**")
            st.markdown(f'<div class="terminal-output">{output["stdout"]}</div>', unsafe_allow_html=True)
            
            # Also show parsed table if it's a "get" command
            if output['command'].strip().startswith("kubectl get") and output['stdout'].strip():
                lines = output['stdout'].strip().splitlines()
                if len(lines) > 1:
                    try:
                        # Try to parse as table - handle both tab and space separation
                        first_line = lines[0]
                        if '\t' in first_line:
                            # Tab-separated
                            header = first_line.split('\t')
                            separator = '\t'
                        else:
                            # Space-separated (more common)
                            header = first_line.split()
                            separator = ' '
                        
                        rows = []
                        for line in lines[1:]:
                            if line.strip():
                                # Split by the detected separator
                                row_data = line.split(separator)
                                # Pad row if it's shorter than header
                                rows.append(row_data[:len(header)])
                        
                        if rows:
                            st.markdown("**📊 Parsed Table:**")
                            df = pd.DataFrame(rows, columns=header)
                            st.dataframe(df, use_container_width=True)
                    except Exception as e:
                        st.info("Could not parse output as table - showing raw output above")
        
        if output['stderr']:
            st.markdown("**Errors:**")
            st.info(output['stderr'])
        
        if output['returncode'] != 0:
            st.warning(f"⚠️ kubectl exited with code {output['returncode']}")
    
    # Add a clear output button
    if st.session_state.last_command_output:
        if st.button("🗑️ Clear Output", key="clear_output"):
            st.session_state.last_command_output = None
            st.rerun()

with tab2:
    st.header("Cluster Explorer")
    
    @st.cache_data(ttl=30)
    def fetch_resource_types():
        try:
            resp = requests.get("http://localhost:8000/kubectl_resource_types", timeout=5)
            if resp.status_code == 200:
                return resp.json().get("resource_types", [])
            else:
                return ["pods", "services", "deployments", "nodes", "events"]
        except Exception:
            return ["pods", "services", "deployments", "nodes", "events"]
    
    @st.cache_data(ttl=30)
    def fetch_namespaces():
        try:
            url = "http://localhost:8000/namespaces"
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                return resp.json().get('namespaces', [])
            else:
                return []
        except Exception:
            return []

    # Fetch available resources and namespaces
    resource_types = fetch_resource_types()
    namespaces = fetch_namespaces()
    
    # Resource selection
    resource = st.selectbox("Resource Type", resource_types, index=0, key="explorer_resource")
    ns = st.selectbox("Namespace", ["All"] + namespaces, index=0, key="explorer_ns")
    all_ns = ns == "All"
    
    # Fetch button
    if st.button("Fetch", key="explorer_fetch"):
        with st.spinner("Fetching data..."):
            try:
                if all_ns:
                    params = {"resource_type": resource, "all_namespaces": "true"}
                else:
                    params = {"resource_type": resource, "all_namespaces": "false", "namespace": ns}
                
                resp = requests.get("http://localhost:8000/kubectl_get", params=params, timeout=15)
                
                if resp.status_code == 200:
                    data = resp.json()
                    items = data.get("items", [])
                    
                    if not items:
                        st.info("No results found.")
                        st.info("This could mean:")
                        st.info("1. The namespace doesn't exist")
                        st.info("2. The namespace is empty")
                        st.info("3. There's an issue with the API call")
                    else:
                        df = pd.DataFrame(items)
                        st.dataframe(df, use_container_width=True)
                else:
                    st.info(f"ℹ️ API Status: {resp.status_code}")
                    
            except requests.exceptions.Timeout:
                st.info("ℹ️ Request timed out. Please try again.")
            except requests.exceptions.ConnectionError:
                st.info("ℹ️ Cannot connect to backend API. Please ensure the API service is running.")
            except Exception:
                st.info("ℹ️ Error fetching data")
    
    # Quick access buttons for common resources
    st.markdown("#### 🚀 Quick Access")
    quick_cols = st.columns(4)
    
    with quick_cols[0]:
        if st.button("📊 All Pods", key="quick_pods"):
            st.session_state.quick_resource = "pods"
            st.session_state.quick_namespace = "All"
            st.rerun()
    
    with quick_cols[1]:
        if st.button("🔗 All Services", key="quick_services"):
            st.session_state.quick_resource = "services"
            st.session_state.quick_namespace = "All"
            st.rerun()
    
    with quick_cols[2]:
        if st.button("🚀 All Deployments", key="quick_deployments"):
            st.session_state.quick_resource = "deployments"
            st.session_state.quick_namespace = "All"
            st.rerun()
    
    with quick_cols[3]:
        if st.button("🖥️ All Nodes", key="quick_nodes"):
            st.session_state.quick_resource = "nodes"
            st.session_state.quick_namespace = "All"
            st.rerun()
    
    # Handle quick access
    if hasattr(st.session_state, 'quick_resource'):
        resource = st.session_state.quick_resource
        all_ns = True
        del st.session_state.quick_resource
        del st.session_state.quick_namespace
        
        with st.spinner(f"Fetching {resource}..."):
            try:
                params = {"resource_type": resource, "all_namespaces": "true"}
                
                resp = requests.get("http://localhost:8000/kubectl_get", params=params, timeout=15)
                
                if resp.status_code == 200:
                    data = resp.json()
                    items = data.get("items", [])
                    
                    if not items:
                        st.info(f"No {resource} found in any namespace.")
                    else:
                        df = pd.DataFrame(items)
                        st.dataframe(df, use_container_width=True)
                else:
                    st.info(f"ℹ️ API Status: {resp.status_code}")
                    
            except Exception:
                st.info(f"ℹ️ Error fetching {resource}")

# Add Misi AI Chatbot Widget
if MISI_AVAILABLE:
    add_misi_to_page("bottom-right")
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white;">
        <h3>🤖 Misi AI Assistant Available</h3>
        <p>Click the floating 🤖 icon in the bottom-right corner to chat with Misi about SmartOps features!</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("🤖 Misi AI Chatbot integration is being set up. You'll see the floating 🤖 icon soon!") 