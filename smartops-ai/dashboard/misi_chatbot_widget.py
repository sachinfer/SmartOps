"""
Misi AI Chatbot Widget for SmartOps
A reusable widget that can be embedded in any page with a corner icon and popup chat interface
"""

import streamlit as st
from datetime import datetime

class MisiChatbotWidget:
    def __init__(self):
        # Initialize session state for Misi
        if 'misi_messages' not in st.session_state:
            st.session_state.misi_messages = [
                {'role': 'assistant', 'content': "Hi! I'm Misi, your SmartOps AI assistant. How can I help you today?"}
            ]
        if 'misi_popup_open' not in st.session_state:
            st.session_state.misi_popup_open = False
    
    def render_misi_icon(self, position="bottom-right"):
        """Render the floating Misi icon using Streamlit components"""
        
        # Create columns to position the icon
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col3:
            # Create a button that looks like an icon
            if st.button("🤖", key="misi_icon_button", help="Ask Misi - SmartOps AI Assistant"):
                st.session_state.misi_popup_open = True
                st.rerun()
        
        # Add label below the icon
        with col3:
            st.markdown("<div style='text-align: center; color: white; font-size: 12px; margin-top: -10px;'>Ask Misi</div>", unsafe_allow_html=True)
    
    def render_misi_popup(self):
        """Render the Misi chat popup using Streamlit components"""
        
        if st.session_state.misi_popup_open:
            # Create a container for the popup
            with st.container():
                # Header
                st.markdown("""
                <div style="
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 20px;
                    border-radius: 10px;
                    margin-bottom: 20px;
                    color: white;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                ">
                    <h3 style="margin: 0; display: flex; align-items: center; gap: 10px;">
                        🤖 Ask Misi
                    </h3>
                    <button onclick="window.parent.postMessage({type: 'close_misi'}, '*')" style="
                        background: rgba(255,255,255,0.2);
                        border: none;
                        color: white;
                        font-size: 20px;
                        cursor: pointer;
                        padding: 5px 10px;
                        border-radius: 5px;
                    ">×</button>
                </div>
                """, unsafe_allow_html=True)
                
                # Chat messages
                for message in st.session_state.misi_messages:
                    if message['role'] == 'user':
                        st.markdown(f"""
                        <div style="
                            background: rgba(255,255,255,0.9);
                            padding: 15px;
                            border-radius: 20px;
                            margin: 10px 0;
                            text-align: right;
                            color: #333;
                        ">
                            {message['content']}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="
                            background: rgba(255,255,255,0.15);
                            padding: 15px;
                            border-radius: 20px;
                            margin: 10px 0;
                            color: white;
                        ">
                            {message['content']}
                        </div>
                        """, unsafe_allow_html=True)
                
                # Suggested questions
                st.markdown("**Quick Questions:**")
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("Check Pods", key="suggest_pods"):
                        self.add_user_message("How can I check pods?")
                        self.generate_response("How can I check pods?")
                        st.rerun()
                    
                    if st.button("Anomaly Detection", key="suggest_anomaly"):
                        self.add_user_message("Show me anomaly detection")
                        self.generate_response("Show me anomaly detection")
                        st.rerun()
                
                with col2:
                    if st.button("Auto Scaling", key="suggest_scaling"):
                        self.add_user_message("Help with scaling")
                        self.generate_response("Help with scaling")
                        st.rerun()
                    
                    if st.button("What can you do?", key="suggest_help"):
                        self.add_user_message("What can you do?")
                        self.generate_response("What can you do?")
                        st.rerun()
                
                # Chat input
                st.markdown("---")
                user_input = st.text_input("Ask me anything about SmartOps...", key="misi_input", placeholder="Type your question here...")
                
                col1, col2 = st.columns([4, 1])
                with col1:
                    if st.button("Send", key="misi_send", use_container_width=True):
                        if user_input.strip():
                            self.add_user_message(user_input.strip())
                            self.generate_response(user_input.strip())
                            st.rerun()
                
                with col2:
                    if st.button("Close", key="misi_close"):
                        st.session_state.misi_popup_open = False
                        st.rerun()
    
    def add_user_message(self, message):
        """Add a user message to the chat"""
        st.session_state.misi_messages.append({'role': 'user', 'content': message})
    
    def generate_response(self, query):
        """Generate a response based on the user query"""
        responses = {
            'pod': 'To check pods, go to Page 2: Pod Explorer and Logs. You can view real-time pod status, logs, and manage your Kubernetes workloads.',
            'anomaly': 'For anomaly detection, visit Page 4: Anomaly Detection. Our AI models automatically detect unusual patterns in your cluster.',
            'scale': 'Auto-scaling recommendations are available on Page 5: Auto-Scaling Recommendations and Control. Get AI-powered suggestions for optimal HPA settings.',
            'shell': 'Access Kubernetes shell and explore your cluster on Page 3: Kubernetes Shell and Cluster Explorer.',
            'incident': 'Track incidents and generate postmortem reports on Page 6: Incident Timeline and Postmortem Report Generator.',
            'ai': 'Automate operations with AI Actions on Page 8. Let AI handle routine tasks while you focus on strategy.',
            'deploy': 'Monitor deployments and manage rollouts on Page 9: Deployments.',
            'help': 'I can help you with:\n• Pod management and monitoring\n• Anomaly detection\n• Kubernetes shell access\n• Auto-scaling recommendations\n• Incident management\n• AI-powered actions\n• Deployment monitoring\n\nWhat would you like to know about?',
            'hello': "Hello! I'm Misi, your SmartOps AI assistant. I can help you navigate the dashboard and answer questions about SmartOps features. How can I assist you today?",
            'hi': "Hi there! I'm Misi, your SmartOps AI assistant. I can help you navigate the dashboard and answer questions about SmartOps features. How can I assist you today?",
            'test': 'This is a test message! The chat is working properly. You can now type your own messages and I will respond to them.',
            'pages': 'Here are the available SmartOps dashboard pages:\n\n📊 Page 1: Overview - Cluster overview and metrics\n🛰️ Page 2: Pod Explorer - Pod management and logs\n💻 Page 3: Kubernetes Shell - Cluster exploration\n🔍 Page 4: Anomaly Detection - AI-powered monitoring\n⚖️ Page 5: Auto-Scaling - HPA recommendations\n📋 Page 6: Incident Timeline - Incident management\n🤖 Page 8: AI Actions - Automated operations\n🚀 Page 9: Deployments - Deployment monitoring\n\nYou can navigate to any page using the sidebar!',
            'show pages': 'Here are the available SmartOps dashboard pages:\n\n📊 Page 1: Overview - Cluster overview and metrics\n🛰️ Page 2: Pod Explorer - Pod management and logs\n💻 Page 3: Kubernetes Shell - Cluster exploration\n🔍 Page 4: Anomaly Detection - AI-powered monitoring\n⚖️ Page 5: Auto-Scaling - HPA recommendations\n📋 Page 6: Incident Timeline - Incident management\n🤖 Page 8: AI Actions - Automated operations\n🚀 Page 9: Deployments - Deployment monitoring\n\nYou can navigate to any page using the sidebar!'
        }
        
        query_lower = query.lower()
        for key, response in responses.items():
            if key in query_lower:
                st.session_state.misi_messages.append({'role': 'assistant', 'content': response})
                return
        
        # Default response
        default_response = "I'm here to help you with SmartOps! I can assist with pod management, anomaly detection, Kubernetes shell access, auto-scaling, incident management, AI actions, and deployments. What would you like to know about?"
        st.session_state.misi_messages.append({'role': 'assistant', 'content': default_response})
    
    def render_misi_integration(self, position="bottom-right"):
        """Render the complete Misi integration with icon and popup"""
        # Render the popup first (so it appears above the icon)
        self.render_misi_popup()
        
        # Render the icon
        self.render_misi_icon(position)

def add_misi_to_page(position="bottom-right"):
    """Add Misi chatbot to any page - just call this function"""
    misi = MisiChatbotWidget()
    misi.render_misi_integration(position)
    return misi
