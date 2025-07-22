import streamlit as st
import requests
import pandas as pd

def execute_kubectl_command(shell_cmd):
    """Execute kubectl command and store results"""
    # Only allow safe kubectl commands
    allowed = ["kubectl get", "kubectl describe", "kubectl logs"]
    if not any(shell_cmd.strip().startswith(a) for a in allowed):
        st.error("Only 'kubectl get', 'kubectl describe', and 'kubectl logs' commands are allowed.")
        return
    with st.spinner("Running kubectl..."):
        try:
            # Remove 'kubectl' prefix for backend
            raw_cmd = shell_cmd.strip()[len("kubectl "):]
            resp = requests.post(
                "http://localhost:8000/kubectl_raw",
                params={"command": raw_cmd},
                timeout=30
            )
            if resp.status_code == 200:
                data = resp.json()
                stdout = data.get("stdout", "")
                stderr = data.get("stderr", "")
                returncode = data.get("returncode", 0)
                st.session_state.last_command_output = {
                    "stdout": stdout,
                    "stderr": stderr,
                    "returncode": returncode,
                    "command": shell_cmd
                }
                if stdout:
                    st.success("✅ Command executed successfully!")
                    if shell_cmd.strip().startswith("kubectl get") and stdout.strip():
                        lines = stdout.strip().splitlines()
                        if len(lines) > 1:
                            header = lines[0].split()
                            rows = [l.split() for l in lines[1:] if l.strip()]
                            try:
                                df = pd.DataFrame(rows, columns=header)
                                st.dataframe(df, use_container_width=True)
                            except Exception:
                                st.code(stdout, language="shell")
                        else:
                            st.code(stdout, language="shell")
                    else:
                        st.code(stdout, language="shell")
                if stderr:
                    st.error(f"⚠️ stderr: {stderr}")
                if returncode != 0:
                    st.warning(f"⚠️ kubectl exited with code {returncode}")
            else:
                st.error(f"❌ API Error: {resp.status_code} - {resp.text}")
        except Exception as e:
            st.error(f"❌ Error running kubectl: {e}")

def kubernetes_shell_page():
    st.title("🖥️ Kubernetes Shell")
    st.info("Only 'kubectl get', 'kubectl describe', and 'kubectl logs' commands are allowed.")
    if "kube_shell_history" not in st.session_state:
        st.session_state.kube_shell_history = []
    if "last_command_output" not in st.session_state:
        st.session_state.last_command_output = ""
    if "current_command" not in st.session_state:
        st.session_state.current_command = ""
    if "history_index" not in st.session_state:
        st.session_state.history_index = -1
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
    col1, col2 = st.columns([1, 20])
    with col1:
        st.markdown('<div class="terminal-prompt">$</div>', unsafe_allow_html=True)
    with col2:
        cmd_key = f"shell_cmd_{len(st.session_state.kube_shell_history)}"
        if st.button("⏎ Execute", key="execute_btn"):
            if st.session_state.current_command.strip():
                if st.session_state.current_command not in st.session_state.kube_shell_history:
                    st.session_state.kube_shell_history.append(st.session_state.current_command)
                execute_kubectl_command(st.session_state.current_command)
                st.session_state.current_command = ""
                st.session_state.history_index = -1
                st.rerun()
        shell_cmd = st.text_input(
            "kubectl >", 
            value=st.session_state.current_command,
            key=cmd_key,
            placeholder="Type kubectl command here...",
            help="Use ↑↓ arrows to navigate history, Enter to execute"
        )
        if shell_cmd != st.session_state.current_command:
            st.session_state.current_command = shell_cmd
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
                    st.experimental_rerun()
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
    if st.session_state.last_command_output:
        st.markdown("#### 📋 Last Command Output")
        output = st.session_state.last_command_output
        st.markdown(f"**Command:** `{output['command']}`")
        if output['stdout']:
            st.markdown("**Output:**")
            st.markdown(f'<div class="terminal-output">{output["stdout"]}</div>', unsafe_allow_html=True)
        if output['stderr']:
            st.markdown("**Errors:**")
            st.error(output['stderr'])
        if output['returncode'] != 0:
            st.warning(f"⚠️ kubectl exited with code {output['returncode']}")

if __name__ == "__main__" or True:
    kubernetes_shell_page() 