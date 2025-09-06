"""
Misi AI Chatbot Widget for SmartOps
A reusable widget that can be embedded in any page with a corner icon and popup chat interface
"""

import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from ai_chatbot_engine import SmartOpsAIChatbot
from smartops_knowledge_base import get_knowledge_base

class MisiChatbotWidget:
    def __init__(self):
        self.chatbot = SmartOpsAIChatbot()
    
    def render_misi_icon(self, position="bottom-right"):
        """Render the floating Misi icon with popup chat interface"""
        
        # Convert logo to base64
        import base64
        try:
            with open("misi_24x7_logo.png", "rb") as img_file:
                logo_base64 = base64.b64encode(img_file.read()).decode()
        except FileNotFoundError:
            # Fallback to emoji if logo not found
            logo_base64 = ""
        
        # CSS for styling
        css = f"""
        <style>
        .misi-icon-container {{
            position: fixed;
            {position.split('-')[0]}: 20px;
            {position.split('-')[1]}: 20px;
            z-index: 1000;
        }}
        
        .misi-icon {{
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
            animation: pulse 2s infinite;
        }}
        
        .misi-icon:hover {{
            transform: scale(1.1);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }}
        
        .misi-icon-text {{
            color: white;
            font-size: 24px;
            font-weight: bold;
        }}
        
        .misi-logo {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
        }}
        
        .misi-chat-popup {{
            position: fixed;
            {position.split('-')[0]}: 90px;
            {position.split('-')[1]}: 20px;
            width: 350px;
            height: 500px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            z-index: 1001;
            display: none;
            flex-direction: column;
            overflow: hidden;
        }}
        
        .misi-chat-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-radius: 15px 15px 0 0;
        }}
        
        .misi-chat-title {{
            font-weight: bold;
            font-size: 16px;
        }}
        
        .misi-close-btn {{
            background: none;
            border: none;
            color: white;
            font-size: 20px;
            cursor: pointer;
            padding: 0;
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            transition: background 0.3s ease;
        }}
        
        .misi-close-btn:hover {{
            background: rgba(255,255,255,0.2);
        }}
        
        .misi-chat-body {{
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            background: #f8f9fa;
        }}
        
        .misi-message {{
            margin-bottom: 15px;
            display: flex;
            flex-direction: column;
        }}
        
        .misi-message.user {{
            align-items: flex-end;
        }}
        
        .misi-message.assistant {{
            align-items: flex-start;
        }}
        
        .misi-message-bubble {{
            max-width: 80%;
            padding: 10px 15px;
            border-radius: 18px;
            word-wrap: break-word;
        }}
        
        .misi-message.user .misi-message-bubble {{
            background: #667eea;
            color: white;
        }}
        
        .misi-message.assistant .misi-message-bubble {{
            background: white;
            color: #333;
            border: 1px solid #e0e0e0;
        }}
        
        .misi-chat-input-container {{
            padding: 15px;
            background: white;
            border-top: 1px solid #e0e0e0;
        }}
        
        .misi-chat-input {{
            width: 100%;
            padding: 10px 15px;
            border: 1px solid #ddd;
            border-radius: 20px;
            outline: none;
            font-size: 14px;
        }}
        
        .misi-chat-input:focus {{
            border-color: #667eea;
            box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
        }}
        
        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
            100% {{ transform: scale(1); }}
        }}
        
        .misi-navigation-card {{
            background: #e3f2fd;
            border: 1px solid #2196f3;
            border-radius: 8px;
            padding: 12px;
            margin: 10px 0;
        }}
        
        .misi-suggestions {{
            margin-top: 10px;
        }}
        
        .misi-suggestion-btn {{
            background: #f0f0f0;
            border: 1px solid #ddd;
            border-radius: 15px;
            padding: 5px 12px;
            margin: 2px;
            font-size: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .misi-suggestion-btn:hover {{
            background: #e0e0e0;
            border-color: #bbb;
        }}
        </style>
        """
        
        # JavaScript for functionality
        js_code = """
        <script>
        let misiPopupVisible = false;
        let misiMessages = [];
        
        function toggleMisiPopup() {
            const popup = document.getElementById('misi-chat-popup');
            if (misiPopupVisible) {
                popup.style.display = 'none';
                misiPopupVisible = false;
            } else {
                popup.style.display = 'flex';
                misiPopupVisible = true;
                // Focus on input
                setTimeout(() => {
                    document.getElementById('misi-chat-input').focus();
                }, 100);
            }
        }
        
        function closeMisiPopup() {
            document.getElementById('misi-chat-popup').style.display = 'none';
            misiPopupVisible = false;
        }
        
        function sendMisiMessage() {
            const input = document.getElementById('misi-chat-input');
            const message = input.value.trim();
            
            if (message) {
                // Add user message
                addMisiMessage('user', message);
                input.value = '';
                
                // Simulate AI response (in real implementation, this would call your backend)
                setTimeout(() => {
                    const response = generateMisiResponse(message);
                    addMisiMessage('assistant', response);
                }, 500);
            }
        }
        
        function addMisiMessage(role, content) {
            const chatBody = document.getElementById('misi-chat-body');
            const messageDiv = document.createElement('div');
            messageDiv.className = `misi-message ${role}`;
            
            const bubble = document.createElement('div');
            bubble.className = 'misi-message-bubble';
            bubble.textContent = content;
            
            messageDiv.appendChild(bubble);
            chatBody.appendChild(messageDiv);
            
            // Scroll to bottom
            chatBody.scrollTop = chatBody.scrollHeight;
            
            // Store message
            misiMessages.push({role, content, timestamp: new Date()});
        }
        
        function generateMisiResponse(query) {
            // Simple response logic - in real implementation, this would call your AI engine
            const responses = {
                'pod': 'I can help you with pod management! Navigate to Page 2: Pod Explorer and Logs to check pod status, view logs, and monitor pod health.',
                'anomaly': 'SmartOps uses AI-powered anomaly detection to automatically identify issues in your cluster. Go to Page 4: Anomaly Detection to access this feature.',
                'shell': 'Access the Kubernetes shell through Page 3: Kubernetes Shell and Cluster Explorer. Run kubectl commands and explore your cluster directly.',
                'scale': 'Get intelligent scaling recommendations on Page 5: Auto Scaling Recommendations and Control. Optimize your cluster performance automatically.',
                'incident': 'Track incidents and generate postmortem reports on Page 6: Incident Timeline and Postmortem Report Generator.',
                'ai': 'Automate operations with AI Actions on Page 8. Let AI handle routine tasks while you focus on strategy.',
                'deploy': 'Monitor deployments and manage rollouts on Page 9: Deployments.'
            };
            
            query = query.toLowerCase();
            for (const [key, response] of Object.entries(responses)) {
                if (query.includes(key)) {
                    return response;
                }
            }
            
            return "I'm here to help you with SmartOps! I can assist with pod management, anomaly detection, Kubernetes shell access, auto-scaling, incident management, AI actions, and deployments. What would you like to know about?";
        }
        
        // Event listeners
        document.addEventListener('DOMContentLoaded', function() {
            // Enter key to send message
            document.getElementById('misi-chat-input').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMisiMessage();
                }
            });
            
            // Close popup when clicking outside
            document.addEventListener('click', function(e) {
                const popup = document.getElementById('misi-chat-popup');
                const icon = document.getElementById('misi-icon');
                if (!popup.contains(e.target) && !icon.contains(e.target)) {
                    closeMisiPopup();
                }
            });
        });
        </script>
        """
        
        # HTML structure
        html = f"""
        {css}
        
        <div class="misi-icon-container">
            <div class="misi-icon" id="misi-icon" onclick="toggleMisiPopup()">
                {"<img src='data:image/png;base64," + logo_base64 + "' class='misi-logo' alt='Misi 24x7'>" if logo_base64 else "<div class='misi-icon-text'>🤖</div>"}
            </div>
        </div>
        
        <div class="misi-chat-popup" id="misi-chat-popup">
            <div class="misi-chat-header">
                <div class="misi-chat-title">
                    {"<img src='data:image/png;base64," + logo_base64 + "' style='width: 24px; height: 24px; margin-right: 8px; vertical-align: middle;' alt='Misi 24x7'>" if logo_base64 else "🤖"} Ask Misi
                </div>
                <button class="misi-close-btn" onclick="closeMisiPopup()">×</button>
            </div>
            <div class="misi-chat-body" id="misi-chat-body">
                <div class="misi-message assistant">
                    <div class="misi-message-bubble">
                        Hi! I'm Misi, your SmartOps AI assistant. How can I help you today?
                    </div>
                </div>
            </div>
            <div class="misi-chat-input-container">
                <input type="text" class="misi-chat-input" id="misi-chat-input"
                       placeholder="Ask me anything about SmartOps..." />
            </div>
        </div>
        
        {js_code}
        """
        
        st.markdown(html, unsafe_allow_html=True)
    
    def render_misi_integration(self, position="bottom-right"):
        """Render the complete Misi integration with icon and popup"""
        if 'misi_messages' not in st.session_state:
            st.session_state.misi_messages = [
                {"role": "assistant", "content": "Hi! I'm Misi, your SmartOps AI assistant. How can I help you today?", "timestamp": datetime.now()}
            ]
        
        self.render_misi_icon(position)
        self._handle_misi_chat()
    
    def _handle_misi_chat(self):
        """Handle chat functionality"""
        # This would integrate with Streamlit's chat interface
        # For now, we'll use the JavaScript-based popup
        pass
    
    def _update_chat_display(self):
        """Update the chat display with new messages"""
        pass

def add_misi_to_page(position="bottom-right"):
    """Add Misi chatbot to any page - just call this function"""
    misi = MisiChatbotWidget()
    misi.render_misi_integration(position)
    return misi
