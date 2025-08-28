"""
Misi AI Assistant - Dedicated Page
A reliable, full-page AI chatbot interface for SmartOps
"""

import streamlit as st
import time
from datetime import datetime

def generate_ai_response(user_input):
    """Generate AI response based on user input"""
    input_lower = user_input.lower()
    
    if any(word in input_lower for word in ['pod', 'pods', 'container']):
        return """To check pod status and manage containers:

🔍 **Pod Explorer Page**: Navigate to "Pod Explorer & Logs" to:
• View all pods in your cluster
• Check pod status (Running, Pending, Failed)
• Access real-time logs
• Execute commands in containers
• Monitor resource usage

📊 **Quick Commands**:
• `kubectl get pods` - List all pods
• `kubectl describe pod <pod-name>` - Detailed pod info
• `kubectl logs <pod-name>` - View logs

Need help with a specific pod issue?"""
    
    elif any(word in input_lower for word in ['anomaly', 'anomalies', 'detection']):
        return """🚨 **Anomaly Detection** is available in the sidebar!

**What it monitors**:
• CPU usage spikes
• Memory consumption patterns
• Pod restart frequency
• Network latency issues
• Resource exhaustion

**Features**:
• Real-time monitoring
• Automated alerts
• Historical analysis
• Predictive insights

**Access**: Go to "Anomaly Detection" page in the sidebar to view current anomalies and set up monitoring rules."""
    
    elif any(word in input_lower for word in ['scale', 'scaling', 'auto', 'hpa']):
        return """⚡ **Auto-Scaling & Recommendations**:

**Available on "Auto-Scaling" page**:
• Horizontal Pod Autoscaler (HPA) setup
• Vertical Pod Autoscaler (VPA) configuration
• Resource optimization recommendations
• Scaling policies management
• Performance metrics analysis

**Quick Setup**:
1. Navigate to "Auto-Scaling" page
2. Select your deployment
3. Configure scaling rules
4. Set resource limits
5. Monitor scaling behavior"""
    
    elif any(word in input_lower for word in ['shell', 'kubectl', 'command', 'terminal']):
        return """🖥️ **Kubernetes Shell Access**:

**Available on "Kubernetes Shell" page**:
• Direct kubectl command execution
• Cluster exploration tools
• Resource inspection
• Troubleshooting commands
• YAML editing

**Common Commands**:
• `kubectl get all` - List all resources
• `kubectl exec -it <pod> -- /bin/bash` - Access pod shell
• `kubectl port-forward <pod> 8080:80` - Port forwarding

Go to "Kubernetes Shell & Cluster Explorer" to start using the shell interface!"""
    
    else:
        return f"""I understand you're asking about "{user_input}". 

Here are some ways I can help you in SmartOps:

🔍 **Navigation**: I can guide you to the right pages
📊 **Monitoring**: Help with pod status, metrics, and anomalies  
⚡ **Scaling**: Assist with auto-scaling and resource optimization
🖥️ **Shell**: Guide you through Kubernetes commands

Try asking about:
• "How do I check pod status?"
• "Show me anomaly detection"
• "Help with auto-scaling"

What specific SmartOps feature would you like to learn about?"""

# Page configuration
st.set_page_config(
    page_title="Misi AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state for chat history
if 'misi_chat_history' not in st.session_state:
    st.session_state.misi_chat_history = []

# Header
st.title("🤖 Misi AI Assistant")
st.markdown("Your intelligent SmartOps companion. Ask me anything about your Kubernetes cluster!")

# Sidebar with suggestions
with st.sidebar:
    st.header("💡 Quick Suggestions")
    
    suggestions = [
        "How do I check pod status?",
        "Show me anomaly detection",
        "Help with auto-scaling",
        "Kubernetes shell commands",
        "Deployment troubleshooting"
    ]
    
    for suggestion in suggestions:
        if st.button(suggestion, key=f"sugg_{suggestion}"):
            st.session_state.misi_chat_history.append({
                "role": "user",
                "content": suggestion,
                "timestamp": datetime.now()
            })
            st.rerun()

# Chat messages display
for message in st.session_state.misi_chat_history:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        st.chat_message("assistant").write(message["content"])

# Input section
user_input = st.chat_input("Ask Misi anything about SmartOps...")

if user_input:
    # Add user message
    st.session_state.misi_chat_history.append({
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now()
    })
    
    # Generate AI response
    ai_response = generate_ai_response(user_input)
    
    # Add AI response
    st.session_state.misi_chat_history.append({
        "role": "assistant",
        "content": ai_response,
        "timestamp": datetime.now()
    })
    
    st.rerun()
