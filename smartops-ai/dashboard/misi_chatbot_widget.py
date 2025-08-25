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
        
        # CSS for styling
        css = f"""
        <style>
        .misi-icon-container {{
            position: fixed;
            {position.split('-')[0]}: 20px;
            {position.split('-')[1]}: 20px;
            z-index: 9999;
        }}
        
        .misi-icon {{
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
            animation: misi-pulse 2s infinite;
            user-select: none;
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
        }}
        
        .misi-icon:hover {{
            transform: scale(1.1);
            box-shadow: 0 6px 20px rgba(0,0,0,0.4);
            background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
        }}
        
        .misi-icon:active {{
            transform: scale(0.95);
        }}
        
        .misi-icon-text {{
            color: white;
            font-size: 24px;
            font-weight: bold;
            pointer-events: none;
        }}
        
        .misi-chat-popup {{
            position: fixed;
            {position.split('-')[0]}: 90px;
            {position.split('-')[1]}: 20px;
            width: 380px;
            height: 500px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
            z-index: 10000;
            display: none;
            flex-direction: column;
            overflow: hidden;
            border: 2px solid #667eea;
        }}
        
        .misi-chat-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-radius: 13px 13px 0 0;
        }}
        
        .misi-chat-title {{
            font-weight: bold;
            font-size: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .misi-close-btn {{
            background: rgba(255,255,255,0.2);
            border: none;
            color: white;
            font-size: 18px;
            cursor: pointer;
            padding: 5px;
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            transition: all 0.3s ease;
            font-weight: bold;
        }}
        
        .misi-close-btn:hover {{
            background: rgba(255,255,255,0.3);
            transform: scale(1.1);
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
            padding: 12px 16px;
            border-radius: 18px;
            word-wrap: break-word;
            line-height: 1.4;
        }}
        
        .misi-message.user .misi-message-bubble {{
            background: #667eea;
            color: white;
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
        }}
        
        .misi-message.assistant .misi-message-bubble {{
            background: white;
            color: #333;
            border: 1px solid #e0e0e0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .misi-chat-input-container {{
            padding: 15px;
            background: white;
            border-top: 1px solid #e0e0e0;
        }}
        
        .misi-chat-input {{
            width: 100%;
            padding: 12px 16px;
            border: 2px solid #ddd;
            border-radius: 25px;
            outline: none;
            font-size: 14px;
            transition: all 0.3s ease;
            box-sizing: border-box;
        }}
        
        .misi-chat-input:focus {{
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
        }}
        
        @keyframes misi-pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
            100% {{ transform: scale(1); }}
        }}
        
        .misi-suggestions {{
            margin-top: 15px;
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}
        
        .misi-suggestion-btn {{
            background: #f0f0f0;
            border: 1px solid #ddd;
            border-radius: 20px;
            padding: 8px 16px;
            font-size: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            color: #333;
            text-decoration: none;
            display: inline-block;
        }}
        
        .misi-suggestion-btn:hover {{
            background: #667eea;
            color: white;
            border-color: #667eea;
            transform: translateY(-2px);
        }}
        
        .misi-welcome-message {{
            background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
            border: 1px solid #2196f3;
            border-radius: 12px;
            padding: 15px;
            margin: 10px 0;
            text-align: center;
        }}
        
        .misi-welcome-message h4 {{
            margin: 0 0 10px 0;
            color: #1976d2;
            font-size: 14px;
        }}
        
        .misi-welcome-message p {{
            margin: 0;
            color: #424242;
            font-size: 12px;
            line-height: 1.4;
        }}
        </style>
        """
        
        # JavaScript for functionality
        js_code = """
        <script>
        let misiPopupVisible = false;
        let misiMessages = [];
        
        // Initialize Misi when page loads
        document.addEventListener('DOMContentLoaded', function() {
            console.log('Misi AI Chatbot initialized');
            initializeMisi();
        });
        
        // Also try to initialize if DOM is already loaded
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initializeMisi);
        } else {
            initializeMisi();
        }
        
        function initializeMisi() {
            console.log('Initializing Misi...');
            
            // Add event listeners
            const icon = document.getElementById('misi-icon');
            const popup = document.getElementById('misi-chat-popup');
            const input = document.getElementById('misi-chat-input');
            const closeBtn = document.querySelector('.misi-close-btn');
            
            if (icon) {
                icon.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    console.log('Misi icon clicked!');
                    toggleMisiPopup();
                });
                console.log('Misi icon event listener added');
            }
            
            if (closeBtn) {
                closeBtn.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    closeMisiPopup();
                });
            }
            
            if (input) {
                input.addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        e.preventDefault();
                        sendMisiMessage();
                    }
                });
            }
            
            // Close popup when clicking outside
            document.addEventListener('click', function(e) {
                if (popup && !popup.contains(e.target) && !icon.contains(e.target)) {
                    closeMisiPopup();
                }
            });
            
            console.log('Misi initialization complete');
        }
        
        function toggleMisiPopup() {
            console.log('Toggle popup called');
            const popup = document.getElementById('misi-chat-popup');
            if (!popup) {
                console.error('Popup not found!');
                return;
            }
            
            if (misiPopupVisible) {
                popup.style.display = 'none';
                misiPopupVisible = false;
                console.log('Popup hidden');
            } else {
                popup.style.display = 'flex';
                misiPopupVisible = true;
                console.log('Popup shown');
                
                // Focus on input
                setTimeout(() => {
                    const input = document.getElementById('misi-chat-input');
                    if (input) {
                        input.focus();
                        console.log('Input focused');
                    }
                }, 100);
            }
        }
        
        function closeMisiPopup() {
            const popup = document.getElementById('misi-chat-popup');
            if (popup) {
                popup.style.display = 'none';
                misiPopupVisible = false;
                console.log('Popup closed');
            }
        }
        
        function sendMisiMessage() {
            const input = document.getElementById('misi-chat-input');
            const message = input.value.trim();
            
            if (message) {
                console.log('Sending message:', message);
                
                // Add user message
                addMisiMessage('user', message);
                input.value = '';
                
                // Simulate AI response
                setTimeout(() => {
                    const response = generateMisiResponse(message);
                    addMisiMessage('assistant', response);
                }, 500);
            }
        }
        
        function addMisiMessage(role, content) {
            const chatBody = document.getElementById('misi-chat-body');
            if (!chatBody) return;
            
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
            console.log('Message added:', role, content);
        }
        
        function generateMisiResponse(query) {
            // Smart response logic based on user query
            const responses = {
                'pod': 'I can help you with pod management! Navigate to Page 2: Pod Explorer and Logs to check pod status, view logs, and monitor pod health.',
                'anomaly': 'SmartOps uses AI-powered anomaly detection to automatically identify issues in your cluster. Go to Page 4: Anomaly Detection to access this feature.',
                'shell': 'Access the Kubernetes shell through Page 3: Kubernetes Shell and Cluster Explorer. Run kubectl commands and explore your cluster directly.',
                'scale': 'Get intelligent scaling recommendations on Page 5: Auto Scaling Recommendations and Control. Optimize your cluster performance automatically.',
                'incident': 'Track incidents and generate postmortem reports on Page 6: Incident Timeline and Postmortem Report Generator.',
                'ai': 'Automate operations with AI Actions on Page 8. Let AI handle routine tasks while you focus on strategy.',
                'deploy': 'Monitor deployments and manage rollouts on Page 9: Deployments.',
                'help': 'I can help you with:\n• Pod management and monitoring\n• Anomaly detection\n• Kubernetes shell access\n• Auto-scaling recommendations\n• Incident management\n• AI-powered actions\n• Deployment monitoring\n\nWhat would you like to know about?',
                'hello': 'Hello! I\'m Misi, your SmartOps AI assistant. I can help you navigate the dashboard and answer questions about SmartOps features. How can I assist you today?',
                'hi': 'Hi there! I\'m Misi, your SmartOps AI assistant. I can help you navigate the dashboard and answer questions about SmartOps features. How can I assist you today?'
            };
            
            query = query.toLowerCase();
            for (const [key, response] of Object.entries(responses)) {
                if (query.includes(key)) {
                    return response;
                }
            }
            
            return "I'm here to help you with SmartOps! I can assist with pod management, anomaly detection, Kubernetes shell access, auto-scaling, incident management, AI actions, and deployments. What would you like to know about?";
        }
        
        // Make functions globally accessible
        window.toggleMisiPopup = toggleMisiPopup;
        window.closeMisiPopup = closeMisiPopup;
        window.sendMisiMessage = sendMisiMessage;
        
        console.log('Misi JavaScript loaded successfully');
        </script>
        """
        
        # HTML structure
        html = f"""
        {css}
        
        <div class="misi-icon-container">
            <div class="misi-icon" id="misi-icon" onclick="toggleMisiPopup()" title="Ask Misi - SmartOps AI Assistant">
                <div class="misi-icon-text">🤖</div>
            </div>
        </div>
        
        <div class="misi-chat-popup" id="misi-chat-popup">
            <div class="misi-chat-header">
                <div class="misi-chat-title">
                    <span>🤖</span>
                    <span>Ask Misi</span>
                </div>
                <button class="misi-close-btn" onclick="closeMisiPopup()" title="Close chat">×</button>
            </div>
            <div class="misi-chat-body" id="misi-chat-body">
                <div class="misi-welcome-message">
                    <h4>Welcome to SmartOps! 🤖</h4>
                    <p>I'm Misi, your AI assistant. Ask me about SmartOps features, navigation, or any Kubernetes questions!</p>
                </div>
                <div class="misi-message assistant">
                    <div class="misi-message-bubble">
                        Hi! I'm Misi, your SmartOps AI assistant. How can I help you today?
                    </div>
                </div>
                <div class="misi-suggestions">
                    <button class="misi-suggestion-btn" onclick="addMisiMessage('user', 'How can I check pods?')">Check Pods</button>
                    <button class="misi-suggestion-btn" onclick="addMisiMessage('user', 'Show me anomaly detection')">Anomaly Detection</button>
                    <button class="misi-suggestion-btn" onclick="addMisiMessage('user', 'Help with scaling')">Auto Scaling</button>
                    <button class="misi-suggestion-btn" onclick="addMisiMessage('user', 'What can you do?')">What can you do?</button>
                </div>
            </div>
            <div class="misi-chat-input-container">
                <input type="text" class="misi-chat-input" id="misi-chat-input"
                       placeholder="Ask me anything about SmartOps..." />
            </div>
        </div>
        
        {js_code}
        """
        
        # Use Streamlit components for better JavaScript execution
        components.html(html, height=0, scrolling=False)
    
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
