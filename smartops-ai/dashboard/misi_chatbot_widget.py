"""
Misi AI Chatbot Widget for SmartOps
Modern floating popup style with interactive chat interface
"""

import streamlit as st
import streamlit.components.v1 as components

def add_misi_to_page(position="bottom-right"):
    """Add Misi chatbot to any page - just call this function"""
    
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
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer !important;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
        transition: all 0.3s ease;
        animation: misi-pulse 2s infinite;
    }
    
    @keyframes misi-pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .misi-icon:hover {
        transform: scale(1.1);
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.6);
    }
    
    .misi-icon-text {
        color: white;
        font-size: 32px;
        font-weight: bold;
    }
    
    .misi-icon-label {
        color: white;
        font-size: 14px;
        font-weight: bold;
        text-align: center;
        margin-top: 8px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    .misi-chat-popup {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 500px;
        height: 600px;
        background: white;
        border-radius: 24px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        z-index: 10000;
        display: none;
        flex-direction: column;
        overflow: hidden;
        animation: misi-slide-in 0.3s ease-out;
        border: 1px solid rgba(0,0,0,0.1);
        max-width: 90vw;
        max-height: 90vh;
        min-width: 400px;
        min-height: 500px;
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }
    
    /* Fallback positioning for edge cases */
    .misi-chat-popup.fallback {
        top: 20px;
        left: 20px;
        right: 20px;
        bottom: 20px;
        transform: none;
        width: auto;
        height: auto;
    }
    
    @keyframes misi-slide-in {
        from {
            opacity: 0;
            transform: translate(-50%, -50%) scale(0.9);
        }
        to {
            opacity: 1;
            transform: translate(-50%, -50%) scale(1);
        }
    }
    
    .misi-chat-header {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 30px 30px 20px 30px;
        text-align: center;
        border-bottom: 1px solid #e2e8f0;
        position: relative;
    }
    
    .misi-header-icon {
        width: 60px;
        height: 60px;
        background: #10b981;
        border-radius: 50%;
        margin: 0 auto 15px auto;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 3px solid #d1fae5;
    }
    
    .misi-header-icon-inner {
        width: 30px;
        height: 30px;
        background: white;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 2px;
    }
    
    .misi-header-icon-lines {
        width: 4px;
        height: 20px;
        background: #10b981;
        border-radius: 2px;
    }
    
    .misi-chat-title {
        font-weight: 600;
        font-size: 18px;
        color: #1e293b;
        margin-bottom: 5px;
    }
    
    .misi-chat-subtitle {
        font-size: 14px;
        color: #64748b;
        font-weight: 400;
    }
    
    .misi-close-btn {
        position: absolute;
        top: 20px;
        right: 20px;
        background: rgba(0,0,0,0.1);
        border: none;
        color: #64748b;
        font-size: 18px;
        cursor: pointer;
        padding: 8px;
        border-radius: 50%;
        transition: all 0.3s ease;
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .misi-close-btn:hover {
        background: rgba(0,0,0,0.2);
        color: #1e293b;
    }
    
    .misi-chat-body {
        flex: 1;
        padding: 20px 30px;
        overflow-y: auto;
        background: #f8fafc;
    }
    
    .misi-message {
        margin-bottom: 20px;
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
        padding: 16px 20px;
        border-radius: 20px;
        font-size: 14px;
        line-height: 1.5;
        word-wrap: break-word;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .misi-message.user .misi-message-bubble {
        background: #10b981;
        color: white;
        border-bottom-right-radius: 6px;
    }
    
    .misi-message.assistant .misi-message-bubble {
        background: white;
        color: #1e293b;
        border: 1px solid #e2e8f0;
        border-bottom-left-radius: 6px;
    }
    
    .misi-suggestions {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin: 20px 30px;
        justify-content: center;
    }
    
    .misi-suggestion-btn {
        background: white;
        border: 1px solid #d1d5db;
        color: #374151;
        padding: 12px 20px;
        border-radius: 20px;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
        white-space: nowrap;
    }
    
    .misi-suggestion-btn:hover {
        background: #f9fafb;
        border-color: #9ca3af;
        transform: translateY(-1px);
    }
    
    .misi-chat-input-container {
        padding: 20px 30px;
        background: white;
        border-top: 1px solid #e2e8f0;
        display: flex;
        gap: 12px;
        align-items: center;
    }
    
    .misi-chat-input {
        flex: 1;
        padding: 16px 20px;
        border: 1px solid #d1d5db;
        border-radius: 25px;
        font-size: 14px;
        outline: none;
        background: #f9fafb;
        color: #1e293b;
        transition: all 0.3s ease;
    }
    
    .misi-chat-input:focus {
        border-color: #10b981;
        background: white;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
    }
    
    .misi-chat-input::placeholder {
        color: #9ca3af;
    }
    
    .misi-send-btn {
        width: 48px;
        height: 48px;
        background: #10b981;
        border: none;
        color: white;
        font-size: 18px;
        cursor: pointer;
        border-radius: 50%;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
    }
    
    .misi-send-btn:hover {
        background: #059669;
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
    }
    </style>
    """
    
    # JavaScript for functionality
    js_code = """
    <script>
    let misiPopupVisible = false;
    let misiMessages = [
        {role: 'assistant', content: 'Hi! I\\'m Misi, your SmartOps AI assistant. How can I help you today?'}
    ];
    
    function toggleMisiPopup() {
        const popup = document.getElementById('misi-chat-popup');
        if (popup) {
            misiPopupVisible = !misiPopupVisible;
            popup.style.display = misiPopupVisible ? 'flex' : 'none';
            
            if (misiPopupVisible) {
                // Ensure popup is properly positioned
                ensurePopupVisibility(popup);
                
                // Focus on input when opening
                setTimeout(() => {
                    const input = document.getElementById('misi-chat-input');
                    if (input) {
                        input.focus();
                    }
                }, 100);
            }
        }
    }
    
    function ensurePopupVisibility(popup) {
        // Reset to default positioning
        popup.classList.remove('fallback');
        popup.style.top = '50%';
        popup.style.left = '50%';
        popup.style.transform = 'translate(-50%, -50%)';
        
        // Check if popup is cut off
        setTimeout(() => {
            const rect = popup.getBoundingClientRect();
            const viewportWidth = window.innerWidth;
            const viewportHeight = window.innerHeight;
            
            // If popup is cut off on left or right, use fallback positioning
            if (rect.left < 0 || rect.right > viewportWidth || rect.top < 0 || rect.bottom > viewportHeight) {
                popup.classList.add('fallback');
                console.log('Using fallback positioning for popup');
            }
        }, 50);
    }
    
    function closeMisiPopup() {
        const popup = document.getElementById('misi-chat-popup');
        if (popup) {
            misiPopupVisible = false;
            popup.style.display = 'none';
        }
    }
    
    function sendMisiMessage(message = null) {
        let messageText;
        
        if (message) {
            messageText = message;
        } else {
            const input = document.getElementById('misi-chat-input');
            if (input && input.value.trim()) {
                messageText = input.value.trim();
                input.value = '';
            } else {
                return;
            }
        }
        
        if (messageText) {
            addMisiMessage('user', messageText);
            
            setTimeout(() => {
                const response = generateMisiResponse(messageText);
                addMisiMessage('assistant', response);
            }, 500);
        }
    }
    
    function addMisiMessage(role, content) {
        const chatBody = document.getElementById('misi-chat-body');
        if (chatBody) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `misi-message ${role}`;
            
            const bubbleDiv = document.createElement('div');
            bubbleDiv.className = 'misi-message-bubble';
            bubbleDiv.textContent = content;
            
            messageDiv.appendChild(bubbleDiv);
            chatBody.appendChild(messageDiv);
            
            chatBody.scrollTop = chatBody.scrollHeight;
            misiMessages.push({role, content});
        }
    }
    
    function generateMisiResponse(query) {
        const responses = {
            'pod': 'To check pods, go to Page 2: Pod Explorer and Logs. You can view real-time pod status, logs, and manage your Kubernetes workloads.',
            'anomaly': 'For anomaly detection, visit Page 4: Anomaly Detection. Our AI models automatically detect unusual patterns in your cluster.',
            'scale': 'Auto-scaling recommendations are available on Page 5: Auto-Scaling Recommendations and Control. Get AI-powered suggestions for optimal HPA settings.',
            'shell': 'Access Kubernetes shell and explore your cluster on Page 3: Kubernetes Shell and Cluster Explorer.',
            'incident': 'Track incidents and generate postmortem reports on Page 6: Incident Timeline and Postmortem Report Generator.',
            'ai': 'Automate operations with AI Actions on Page 8. Let AI handle routine tasks while you focus on strategy.',
            'deploy': 'Monitor deployments and manage rollouts on Page 9: Deployments.',
            'help': 'I can help you with: Pod management, anomaly detection, Kubernetes shell access, auto-scaling, incident management, AI-powered actions, and deployment monitoring. What would you like to know about?',
            'hello': 'Hello! I\\'m Misi, your SmartOps AI assistant. I can help you navigate the dashboard and answer questions about SmartOps features. How can I assist you today?',
            'hi': 'Hi there! I\\'m Misi, your SmartOps AI assistant. I can help you navigate the dashboard and answer questions about SmartOps features. How can I assist you today?',
            'test': 'This is a test message! The chat is working properly. You can now type your own messages and I will respond to them.',
            'pages': 'Here are the available SmartOps dashboard pages: Page 1: Overview, Page 2: Pod Explorer, Page 3: Kubernetes Shell, Page 4: Anomaly Detection, Page 5: Auto-Scaling, Page 6: Incident Timeline, Page 8: AI Actions, Page 9: Deployments. You can navigate to any page using the sidebar!',
            'show pages': 'Here are the available SmartOps dashboard pages: Page 1: Overview, Page 2: Pod Explorer, Page 3: Kubernetes Shell, Page 4: Anomaly Detection, Page 5: Auto-Scaling, Page 6: Incident Timeline, Page 8: AI Actions, Page 9: Deployments. You can navigate to any page using the sidebar!'
        };
        
        query = query.toLowerCase();
        for (const [key, response] of Object.entries(responses)) {
            if (query.includes(key)) {
                return response;
            }
        }
        
        return "I\\'m here to help you with SmartOps! I can assist with pod management, anomaly detection, Kubernetes shell access, auto-scaling, incident management, AI actions, and deployments. What would you like to know about?";
    }
    
    document.addEventListener('DOMContentLoaded', function() {
        const icon = document.getElementById('misi-icon');
        const closeBtn = document.querySelector('.misi-close-btn');
        const input = document.getElementById('misi-chat-input');
        const sendBtn = document.getElementById('misi-send-btn');
        
        if (icon) {
            icon.addEventListener('click', toggleMisiPopup);
        }
        
        if (closeBtn) {
            closeBtn.addEventListener('click', closeMisiPopup);
        }
        
        if (input) {
            input.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMisiMessage();
                }
            });
        }
        
        if (sendBtn) {
            sendBtn.addEventListener('click', function() {
                sendMisiMessage();
            });
        }
        
        // Handle window resize to ensure popup stays visible
        window.addEventListener('resize', function() {
            if (misiPopupVisible) {
                const popup = document.getElementById('misi-chat-popup');
                if (popup) {
                    ensurePopupVisibility(popup);
                }
            }
        });
    });
    
    window.toggleMisiPopup = toggleMisiPopup;
    window.closeMisiPopup = closeMisiPopup;
    window.sendMisiMessage = sendMisiMessage;
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
            <div class="misi-header-icon">
                <div class="misi-header-icon-inner">
                    <div class="misi-header-icon-lines"></div>
                    <div class="misi-header-icon-lines"></div>
                </div>
            </div>
            <div class="misi-chat-title">Ask Misi</div>
            <div class="misi-chat-subtitle">Your SmartOps AI Assistant</div>
            <button class="misi-close-btn" title="Close chat">×</button>
        </div>
        <div class="misi-chat-body" id="misi-chat-body">
            <div class="misi-message assistant">
                <div class="misi-message-bubble">
                    Hi! I'm Misi, your SmartOps AI assistant. How can I help you today?
                </div>
            </div>
        </div>
        <div class="misi-suggestions">
            <button class="misi-suggestion-btn" onclick="sendMisiMessage('pod')">Pods</button>
            <button class="misi-suggestion-btn" onclick="sendMisiMessage('anomaly')">Anomaly</button>
            <button class="misi-suggestion-btn" onclick="sendMisiMessage('scale')">Scale</button>
            <button class="misi-suggestion-btn" onclick="sendMisiMessage('shell')">Shell</button>
            <button class="misi-suggestion-btn" onclick="sendMisiMessage('incident')">Incident</button>
            <button class="misi-suggestion-btn" onclick="sendMisiMessage('ai')">AI Actions</button>
            <button class="misi-suggestion-btn" onclick="sendMisiMessage('deploy')">Deployments</button>
            <button class="misi-suggestion-btn" onclick="sendMisiMessage('help')">Help</button>
        </div>
        <div class="misi-chat-input-container">
            <input type="text" class="misi-chat-input" id="misi-chat-input"
                   placeholder="Ask me anything about SmartOps..." />
            <button class="misi-send-btn" id="misi-send-btn">📤</button>
        </div>
    </div>
    
    {js_code}
    """
    
    # Use Streamlit components for better JavaScript execution
    components.html(html, height=0, scrolling=False)
