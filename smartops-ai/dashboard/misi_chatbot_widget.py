"""
Misi AI Chatbot Widget for SmartOps
A reusable widget that can be embedded in any page with a corner icon and popup chat interface
"""

import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

class MisiChatbotWidget:
    def __init__(self):
        pass
    
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
            width: 80px;
            height: 80px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer !important;
            box-shadow: 0 6px 20px rgba(0,0,0,0.4);
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
            box-shadow: 0 8px 25px rgba(0,0,0,0.5);
            background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
        }
        
        .misi-icon:active {
            transform: scale(0.95);
        }
        
        .misi-icon-text {
            color: white;
            font-size: 32px;
            font-weight: bold;
            pointer-events: none;
        }
        
        .misi-icon-label {
            color: white;
            font-size: 14px;
            font-weight: bold;
            text-align: center;
            margin-top: 8px;
            pointer-events: none;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }
        
        .misi-chat-popup {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            z-index: 10000;
            display: none;
            flex-direction: column;
            overflow: hidden;
            animation: misi-slide-in 0.3s ease-out;
        }
        
        @keyframes misi-slide-in {
            from {
                opacity: 0;
                transform: scale(0.9);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }
        
        .misi-chat-header {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            color: white;
            padding: 25px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
            position: relative;
        }
        
        .misi-chat-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
            pointer-events: none;
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
            padding: 30px;
            overflow-y: auto;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            position: relative;
        }
        
        .misi-chat-body::-webkit-scrollbar {
            width: 8px;
        }
        
        .misi-chat-body::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        }
        
        .misi-chat-body::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.3);
            border-radius: 10px;
        }
        
        .misi-chat-body::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.5);
        }
        
        .misi-welcome-message {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(20px);
            padding: 25px;
            border-radius: 20px;
            margin-bottom: 25px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            text-align: center;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
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
            width: 100%;
            position: relative;
        }
        
        .misi-message.user {
            align-items: flex-end;
        }
        
        .misi-message.assistant {
            align-items: flex-start;
        }
        
        .misi-message-bubble {
            max-width: 70%;
            padding: 18px 24px;
            border-radius: 25px;
            font-size: 15px;
            line-height: 1.5;
            word-wrap: break-word;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        
        .misi-message.user .misi-message-bubble {
            background: rgba(255, 255, 255, 0.9);
            color: #1a202c;
            border-bottom-right-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
        
        .misi-message.assistant .misi-message-bubble {
            background: rgba(255, 255, 255, 0.15);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-bottom-left-radius: 8px;
        }
        
        .misi-message-bubble:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
        }
        
        .misi-suggestions {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 25px;
            justify-content: center;
        }
        
        .misi-suggestion-btn {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: white;
            padding: 12px 20px;
            border-radius: 25px;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.3s ease;
            white-space: nowrap;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
        
        .misi-suggestion-btn:hover {
            background: rgba(255, 255, 255, 0.25);
            border-color: rgba(255, 255, 255, 0.4);
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        }
        
        .misi-chat-input-container {
            padding: 25px 30px;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            border-top: 1px solid rgba(255, 255, 255, 0.2);
            position: relative;
        }
        
        .misi-chat-input {
            width: calc(100% - 70px);
            padding: 18px 24px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 30px 0 0 30px;
            font-size: 15px;
            outline: none;
            transition: all 0.3s ease;
            box-sizing: border-box;
            float: left;
            background: rgba(255, 255, 255, 0.1);
            color: white;
            backdrop-filter: blur(10px);
        }
        
        .misi-send-btn {
            width: 70px;
            height: 60px;
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(20px);
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 0 30px 30px 0;
            color: white;
            font-size: 18px;
            cursor: pointer;
            transition: all 0.3s ease;
            float: right;
        }
        
        .misi-send-btn:hover {
            background: rgba(255, 255, 255, 0.3);
            border-color: rgba(255, 255, 255, 0.5);
            transform: scale(1.05);
        }
        
        .misi-send-btn:active {
            transform: scale(0.95);
        }
        
        .misi-chat-input:focus {
            border-color: rgba(255, 255, 255, 0.6);
            background: rgba(255, 255, 255, 0.15);
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
        }
        
        .misi-chat-input::placeholder {
            color: rgba(255, 255, 255, 0.7);
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
            console.log('=== sendMisiMessage function called ===');
            console.log('Function context:', this);
            console.log('Window object:', window);
            
            const input = document.getElementById('misi-chat-input');
            console.log('Input element found:', input);
            console.log('Input value:', input ? input.value : 'Input not found');
            
            if (input && input.value.trim()) {
                const message = input.value.trim();
                console.log('Sending message:', message);
                
                try {
                    // Add user message
                    console.log('Calling addMisiMessage for user...');
                    addMisiMessage('user', message);
                    input.value = '';
                    
                    // Generate response
                    console.log('Generating response...');
                    setTimeout(() => {
                        try {
                            const response = generateMisiResponse(message);
                            console.log('Generated response:', response);
                            addMisiMessage('assistant', response);
                        } catch (error) {
                            console.error('Error generating response:', error);
                        }
                    }, 500);
                } catch (error) {
                    console.error('Error in sendMisiMessage:', error);
                }
            } else {
                console.log('No message to send or input not found');
                if (input) {
                    console.log('Input value:', input.value);
                }
            }
        }
        
        // Function to add message to chat
        function addMisiMessage(role, content) {
            const chatBody = document.getElementById('misi-chat-body');
            if (chatBody) {
                console.log('Adding message:', role, content);
                
                const messageDiv = document.createElement('div');
                messageDiv.className = `misi-message ${role}`;
                
                const bubbleDiv = document.createElement('div');
                bubbleDiv.className = 'misi-message-bubble';
                bubbleDiv.innerHTML = content;
                
                // Remove debug border and use CSS classes instead of inline styles
                messageDiv.style.border = 'none';
                messageDiv.style.minHeight = 'auto';
                
                messageDiv.appendChild(bubbleDiv);
                
                console.log('Message div created:', messageDiv);
                console.log('Message div HTML:', messageDiv.outerHTML);
                
                // Find the suggestions section to insert messages before it
                const suggestions = chatBody.querySelector('.misi-suggestions');
                
                if (suggestions) {
                    // Insert the new message before the suggestions
                    chatBody.insertBefore(messageDiv, suggestions);
                    console.log('Message inserted before suggestions');
                    console.log('Chat body children after insert:', chatBody.children.length);
                } else {
                    // If no suggestions found, append to the end
                    chatBody.appendChild(messageDiv);
                    console.log('Message appended to end');
                    console.log('Chat body children after append:', chatBody.children.length);
                }
                
                // Ensure the message is visible
                messageDiv.style.display = 'flex';
                messageDiv.style.visibility = 'visible';
                messageDiv.style.opacity = '1';
                
                // Scroll to bottom
                chatBody.scrollTop = chatBody.scrollHeight;
                
                // Store message
                misiMessages.push({role, content});
                console.log('Message added successfully. Total messages:', misiMessages.length);
                
                // Force a reflow to ensure the message is visible
                messageDiv.offsetHeight;
                
                // Additional debugging
                console.log('Message div computed styles:', window.getComputedStyle(messageDiv));
                console.log('Message div is visible:', messageDiv.offsetWidth > 0 && messageDiv.offsetHeight > 0);
            } else {
                console.error('Chat body not found!');
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
                'help': 'I can help you with:<br>• Pod management and monitoring<br>• Anomaly detection<br>• Kubernetes shell access<br>• Auto-scaling recommendations<br>• Incident management<br>• AI-powered actions<br>• Deployment monitoring<br><br>What would you like to know about?',
                'hello': 'Hello! I\\'m Misi, your SmartOps AI assistant. I can help you navigate the dashboard and answer questions about SmartOps features. How can I assist you today?',
                'hi': 'Hi there! I\\'m Misi, your SmartOps AI assistant. I can help you navigate the dashboard and answer questions about SmartOps features. How can I assist you today?',
                'test': 'This is a test message! The chat is working properly. You can now type your own messages and I will respond to them.',
                'pages': 'Here are the available SmartOps dashboard pages:<br><br>📊 <strong>Page 1: Overview</strong> - Cluster overview and metrics<br>🛰️ <strong>Page 2: Pod Explorer</strong> - Pod management and logs<br>💻 <strong>Page 3: Kubernetes Shell</strong> - Cluster exploration<br>🔍 <strong>Page 4: Anomaly Detection</strong> - AI-powered monitoring<br>⚖️ <strong>Page 5: Auto-Scaling</strong> - HPA recommendations<br>📋 <strong>Page 6: Incident Timeline</strong> - Incident management<br>🤖 <strong>Page 8: AI Actions</strong> - Automated operations<br>🚀 <strong>Page 9: Deployments</strong> - Deployment monitoring<br><br>You can navigate to any page using the sidebar!',
                'show pages': 'Here are the available SmartOps dashboard pages:<br><br>📊 <strong>Page 1: Overview</strong> - Cluster overview and metrics<br>🛰️ <strong>Page 2: Pod Explorer</strong> - Pod management and logs<br>💻 <strong>Page 3: Kubernetes Shell</strong> - Cluster exploration<br>🔍 <strong>Page 4: Anomaly Detection</strong> - AI-powered monitoring<br>⚖️ <strong>Page 5: Auto-Scaling</strong> - HPA recommendations<br>📋 <strong>Page 6: Incident Timeline</strong> - Incident management<br>🤖 <strong>Page 8: AI Actions</strong> - Automated operations<br>🚀 <strong>Page 9: Deployments</strong> - Deployment monitoring<br><br>You can navigate to any page using the sidebar!'
            };
            
            query = query.toLowerCase();
            for (const [key, response] of Object.entries(responses)) {
                if (query.includes(key)) {
                    return response;
                }
            }
            
            return "I\\'m here to help you with SmartOps! I can assist with pod management, anomaly detection, Kubernetes shell access, auto-scaling, incident management, AI actions, and deployments. What would you like to know about?";
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
            const sendBtn = document.getElementById('misi-send-btn');
            
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
                        console.log('Enter key pressed, calling sendMisiMessage');
                        sendMisiMessage();
                    }
                });
                console.log('Input keypress listener added');
            }
            
            if (sendBtn) {
                sendBtn.addEventListener('click', function() {
                    console.log('Send button clicked, calling sendMisiMessage');
                    sendMisiMessage();
                });
                console.log('Send button listener added');
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
        
        // Expose functions globally for debugging
        window.toggleMisiPopup = toggleMisiPopup;
        window.closeMisiPopup = closeMisiPopup;
        window.sendMisiMessage = sendMisiMessage;
        window.addMisiMessage = addMisiMessage;
        window.generateMisiResponse = generateMisiResponse;
        window.handleSuggestionClick = handleSuggestionClick;
        window.initializeMisi = initializeMisi;
        
        console.log('Misi JavaScript loaded successfully');
        console.log('Global functions exposed:', {
            toggleMisiPopup: typeof toggleMisiPopup,
            sendMisiMessage: typeof sendMisiMessage,
            addMisiMessage: typeof addMisiMessage
        });
        </script>
        """
        
        # HTML structure
        html = f"""
        {css}
        
        <div class="misi-icon-container">
            <div class="misi-icon" id="misi-icon" title="Ask Misi - SmartOps AI Assistant">
                <div class="misi-icon-text">🤖</div>
            </div>
            <div class="misi-icon-label">Ask Misi</div>
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
                    <button class="misi-suggestion-btn" onclick="handleSuggestionClick('show pages')">Show Pages</button>
                    <button class="misi-suggestion-btn" onclick="handleSuggestionClick('test')">Test Chat</button>
                </div>
            </div>
            <div class="misi-chat-input-container">
                <input type="text" class="misi-chat-input" id="misi-chat-input"
                       placeholder="Ask me anything about SmartOps..." />
                <button class="misi-send-btn" id="misi-send-btn" title="Send message">↵</button>
            </div>
        </div>
        
        {js_code}
        """
        
        # Use Streamlit components for better JavaScript execution
        components.html(html, height=0, scrolling=False)
    
    def render_misi_integration(self, position="bottom-right"):
        """Render the complete Misi integration with icon and popup"""
        self.render_misi_icon(position)

def add_misi_to_page(position="bottom-right"):
    """Add Misi chatbot to any page - just call this function"""
    misi = MisiChatbotWidget()
    misi.render_misi_integration(position)
    return misi
