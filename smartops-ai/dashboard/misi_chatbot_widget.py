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
        css = """
        <style>
        .misi-icon-container {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 9999;
        }
        
        .misi-icon {
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
        }
        
        @keyframes misi-pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        .misi-icon:hover {
            transform: scale(1.1);
            box-shadow: 0 6px 20px rgba(0,0,0,0.4);
            background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
        }
        
        .misi-icon:active {
            transform: scale(0.95);
        }
        
        .misi-icon-text {
            color: white;
            font-size: 24px;
            font-weight: bold;
            pointer-events: none;
        }
        
        .misi-chat-popup {
            position: fixed;
            bottom: 90px;
            right: 20px;
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
        }
        
        .misi-chat-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-radius: 13px 13px 0 0;
        }
        
        .misi-chat-title {
            font-weight: bold;
            font-size: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .misi-close-btn {
            background: rgba(255,255,255,0.2);
            border: none;
            color: white;
            font-size: 20px;
            cursor: pointer;
            padding: 5px 10px;
            border-radius: 5px;
            transition: background 0.3s ease;
        }
        
        .misi-close-btn:hover {
            background: rgba(255,255,255,0.3);
        }
        
        .misi-chat-body {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            background: #f8fafc;
        }
        
        .misi-welcome-message {
            background: white;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
        }
        
        .misi-welcome-message h4 {
            margin: 0 0 10px 0;
            color: #667eea;
        }
        
        .misi-welcome-message p {
            margin: 0;
            color: #64748b;
            font-size: 14px;
        }
        
        .misi-message {
            margin-bottom: 15px;
            display: flex;
            flex-direction: column;
        }
        
        .misi-message.user {
            align-items: flex-end;
        }
        
        .misi-message.assistant {
            align-items: flex-start;
        }
        
        .misi-message-bubble {
            max-width: 80%;
            padding: 12px 16px;
            border-radius: 18px;
            font-size: 14px;
            line-height: 1.4;
            word-wrap: break-word;
        }
        
        .misi-message.user .misi-message-bubble {
            background: #667eea;
            color: white;
            border-bottom-right-radius: 6px;
        }
        
        .misi-message.assistant .misi-message-bubble {
            background: white;
            color: #374151;
            border: 1px solid #e5e7eb;
            border-bottom-left-radius: 6px;
        }
        
        .misi-suggestions {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 15px;
        }
        
        .misi-suggestion-btn {
            background: #f1f5f9;
            border: 1px solid #e2e8f0;
            color: #475569;
            padding: 8px 12px;
            border-radius: 20px;
            font-size: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            white-space: nowrap;
        }
        
        .misi-suggestion-btn:hover {
            background: #e2e8f0;
            border-color: #cbd5e1;
            color: #334155;
        }
        
        .misi-chat-input-container {
            padding: 15px;
            background: white;
            border-top: 1px solid #e5e7eb;
        }
        
        .misi-chat-input {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid #e5e7eb;
            border-radius: 25px;
            font-size: 14px;
            outline: none;
            transition: border-color 0.3s ease;
            box-sizing: border-box;
        }
        
        .misi-chat-input:focus {
            border-color: #667eea;
        }
        
        .misi-chat-input::placeholder {
            color: #9ca3af;
        }
        </style>
        """
        
        # JavaScript for functionality
        js_code = """
        <script>
        // Global variables
        let misiPopupVisible = false;
        let misiMessages = [
            {role: 'assistant', content: 'Hi! I\\'m Misi, your SmartOps AI assistant. How can I help you today?'}
        ];
        
        // Function to toggle popup visibility
        function toggleMisiPopup() {
            console.log('toggleMisiPopup called');
            const popup = document.getElementById('misi-chat-popup');
            if (popup) {
                misiPopupVisible = !misiPopupVisible;
                popup.style.display = misiPopupVisible ? 'flex' : 'none';
                console.log('Popup visibility:', misiPopupVisible);
                
                if (misiPopupVisible) {
                    // Focus on input when opening
                    const input = document.getElementById('misi-chat-input');
                    if (input) {
                        setTimeout(() => input.focus(), 100);
                    }
                }
            } else {
                console.error('Popup element not found');
            }
        }
        
        // Function to close popup
        function closeMisiPopup() {
            console.log('closeMisiPopup called');
            const popup = document.getElementById('misi-chat-popup');
            if (popup) {
                misiPopupVisible = false;
                popup.style.display = 'none';
                console.log('Popup closed');
            }
        }
        
        // Function to send message
        function sendMisiMessage() {
            const input = document.getElementById('misi-chat-input');
            if (input && input.value.trim()) {
                const message = input.value.trim();
                addMisiMessage('user', message);
                input.value = '';
                
                // Generate response
                setTimeout(() => {
                    const response = generateMisiResponse(message);
                    addMisiMessage('assistant', response);
                }, 500);
            }
        }
        
        // Function to add message to chat
        function addMisiMessage(role, content) {
            const chatBody = document.getElementById('misi-chat-body');
            if (chatBody) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `misi-message ${role}`;
                
                const bubbleDiv = document.createElement('div');
                bubbleDiv.className = 'misi-message-bubble';
                bubbleDiv.textContent = content;
                
                messageDiv.appendChild(bubbleDiv);
                
                // Insert after welcome message and suggestions
                const welcomeMessage = chatBody.querySelector('.misi-welcome-message');
                const suggestions = chatBody.querySelector('.misi-suggestions');
                
                if (suggestions) {
                    chatBody.insertBefore(messageDiv, suggestions);
                } else {
                    chatBody.appendChild(messageDiv);
                }
                
                // Scroll to bottom
                chatBody.scrollTop = chatBody.scrollHeight;
                
                // Store message
                misiMessages.push({role, content});
            }
        }
        
        // Function to generate response
        function generateMisiResponse(query) {
            const responses = {
                'pod': 'To check pods, go to Page 2: Pod Explorer and Logs. You can view real-time pod status, logs, and manage your Kubernetes workloads.',
                'anomaly': 'For anomaly detection, visit Page 4: Anomaly Detection. Our AI models automatically detect unusual patterns in your cluster.',
                'scale': 'Auto-scaling recommendations are available on Page 5: Auto-Scaling Recommendations and Control. Get AI-powered suggestions for optimal HPA settings.',
                'shell': 'Access Kubernetes shell and explore your cluster on Page 3: Kubernetes Shell and Cluster Explorer.',
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
        
        // Function to handle suggestion clicks
        function handleSuggestionClick(text) {
            addMisiMessage('user', text);
            setTimeout(() => {
                const response = generateMisiResponse(text);
                addMisiMessage('assistant', response);
            }, 500);
        }
        
        // Function to initialize Misi
        function initializeMisi() {
            console.log('Initializing Misi...');
            
            // Add event listeners
            const icon = document.getElementById('misi-icon');
            const closeBtn = document.querySelector('.misi-close-btn');
            const input = document.getElementById('misi-chat-input');
            
            if (icon) {
                icon.addEventListener('click', toggleMisiPopup);
                console.log('Icon click listener added');
            }
            
            if (closeBtn) {
                closeBtn.addEventListener('click', closeMisiPopup);
                console.log('Close button listener added');
            }
            
            if (input) {
                input.addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        sendMisiMessage();
                    }
                });
                console.log('Input keypress listener added');
            }
            
            console.log('Misi initialization complete');
        }
        
        // Initialize when DOM is loaded
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initializeMisi);
        } else {
            initializeMisi();
        }
        
        // Also try to initialize after a short delay to ensure everything is loaded
        setTimeout(initializeMisi, 100);
        
        console.log('Misi JavaScript loaded successfully');
        </script>
        """
        
        # HTML structure
        html = f"""
        {css}
        
        <div class="misi-icon-container">
            <div class="misi-icon" id="misi-icon" title="Ask Misi - SmartOps AI Assistant">
                <div class="misi-icon-text">🤖</div>
            </div>
        </div>
        
        <div class="misi-chat-popup" id="misi-chat-popup">
            <div class="misi-chat-header">
                <div class="misi-chat-title">
                    <span>🤖</span>
                    <span>Ask Misi</span>
                </div>
                <button class="misi-close-btn" title="Close chat">×</button>
            </div>
            <div class="misi-chat-body" id="misi-chat-body">
                <div class="misi-welcome-message">
                    <h4>Welcome to SmartOps! 🤖</h4>
                    <p>I&apos;m Misi, your AI assistant. Ask me about SmartOps features, navigation, or any Kubernetes questions!</p>
                </div>
                <div class="misi-message assistant">
                    <div class="misi-message-bubble">
                        Hi! I&apos;m Misi, your SmartOps AI assistant. How can I help you today?
                    </div>
                </div>
                <div class="misi-suggestions">
                    <button class="misi-suggestion-btn" onclick="handleSuggestionClick('How can I check pods?')">Check Pods</button>
                    <button class="misi-suggestion-btn" onclick="handleSuggestionClick('Show me anomaly detection')">Anomaly Detection</button>
                    <button class="misi-suggestion-btn" onclick="handleSuggestionClick('Help with scaling')">Auto Scaling</button>
                    <button class="misi-suggestion-btn" onclick="handleSuggestionClick('What can you do?')">What can you do?</button>
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
