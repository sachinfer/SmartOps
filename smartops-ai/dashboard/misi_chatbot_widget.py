"""
Misi AI Chatbot Widget for SmartOps Dashboard
Provides a floating chat interface with AI assistance
"""

import streamlit as st
import streamlit.components.v1 as components

def add_misi_to_page(position="bottom-right"):
    """Add the Misi AI chatbot widget to the current page
    
    Args:
        position (str): Position of the icon (e.g., "bottom-right", "bottom-left", etc.)
                      Currently only "bottom-right" is supported
    """
    
    html = """
    <style>
    /* Enhanced CSS with beautiful animations and popup design */
    * {
        box-sizing: border-box;
    }
    
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
        position: relative;
        overflow: hidden;
    }
    
    .misi-icon::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.3), transparent);
        transform: rotate(45deg);
        animation: misi-shine 3s infinite;
    }
    
    @keyframes misi-shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    @keyframes misi-pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .misi-icon:hover {
        transform: scale(1.1) rotate(5deg);
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.6);
    }
    
    .misi-icon img {
        width: 50px;
        height: 50px;
        object-fit: contain;
        filter: brightness(0) invert(1);
        z-index: 2;
        position: relative;
    }
    
    .misi-icon .misi-icon-fallback {
        font-size: 40px;
        color: white;
        display: none;
        z-index: 2;
        position: relative;
    }
    
    .misi-icon img:not([src]), .misi-icon img[src=""], .misi-icon img[src*="error"] {
        display: none;
    }
    
    .misi-icon img:not([src]) + .misi-icon-fallback,
    .misi-icon img[src=""] + .misi-icon-fallback,
    .misi-icon img[src*="error"] + .misi-icon-fallback {
        display: block;
    }
    
    .misi-icon-label {
        position: absolute;
        bottom: -30px;
        left: 50%;
        transform: translateX(-50%);
        color: white;
        font-size: 12px;
        font-weight: 600;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
        white-space: nowrap;
        opacity: 0;
        transition: opacity 0.3s ease;
        background: rgba(0,0,0,0.7);
        padding: 4px 8px;
        border-radius: 12px;
    }
    
    .misi-icon-container:hover .misi-icon-label {
        opacity: 1;
    }
    
    /* Enhanced Chat Popup with beautiful animations */
    .misi-chat-popup {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(0, 0, 0, 0.8);
        z-index: 10000;
        display: none;
        flex-direction: column;
        overflow: hidden;
        animation: misi-fade-in 0.4s ease-out;
        backdrop-filter: blur(10px);
    }
    
    @keyframes misi-fade-in {
        from { 
            opacity: 0; 
            backdrop-filter: blur(0px);
        }
        to { 
            opacity: 1; 
            backdrop-filter: blur(10px);
        }
    }
    
    .misi-chat-content {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) scale(0.8);
        width: 90vw;
        max-width: 500px;
        height: 80vh;
        max-height: 600px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        display: flex;
        flex-direction: column;
        overflow: hidden;
        animation: misi-popup-enter 0.5s ease-out forwards;
        z-index: 10001;
    }
    
    @keyframes misi-popup-enter {
        0% {
            opacity: 0;
            transform: translate(-50%, -50%) scale(0.8) rotate(-5deg);
        }
        50% {
            transform: translate(-50%, -50%) scale(1.05) rotate(2deg);
        }
        100% {
            opacity: 1;
            transform: translate(-50%, -50%) scale(1) rotate(0deg);
        }
    }
    
    .misi-chat-header {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        padding: 20px 24px;
        text-align: center;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        position: relative;
        width: 100%;
        box-sizing: border-box;
        border-radius: 20px 20px 0 0;
    }
    
    .misi-header-icon {
        width: 60px;
        height: 60px;
        background: rgba(255,255,255,0.2);
        border-radius: 50%;
        margin: 0 auto 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: misi-icon-bounce 2s infinite;
    }
    
    @keyframes misi-icon-bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }
    
    .misi-header-icon-inner {
        width: 40px;
        height: 40px;
        background: white;
        border-radius: 50%;
        position: relative;
        animation: misi-inner-rotate 4s linear infinite;
    }
    
    @keyframes misi-inner-rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .misi-header-icon-lines {
        position: absolute;
        width: 20px;
        height: 3px;
        background: #10b981;
        border-radius: 2px;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }
    
    .misi-header-icon-lines:nth-child(1) { top: 35%; }
    .misi-header-icon-lines:nth-child(2) { top: 65%; }
    
    .misi-chat-title {
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 4px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .misi-chat-subtitle {
        font-size: 14px;
        opacity: 0.9;
        font-weight: 400;
    }
    
    .misi-close-btn {
        position: absolute;
        top: 20px;
        right: 20px;
        background: rgba(255,255,255,0.2);
        color: white;
        border: none;
        font-size: 28px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
        z-index: 10002;
        backdrop-filter: blur(10px);
    }
    
    .misi-close-btn:hover {
        background: #ef4444;
        transform: scale(1.1) rotate(90deg);
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4);
    }
    
    .misi-chat-body {
        flex: 1;
        padding: 24px;
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        min-height: 400px;
        position: relative;
        border: none;
        border-radius: 0;
        margin: 0;
        width: 100%;
        box-sizing: border-box;
    }
    
    .misi-message {
        margin-bottom: 16px;
        display: flex !important;
        flex-direction: column;
        max-width: 85%;
        position: relative;
        z-index: 1;
        opacity: 1 !important;
        visibility: visible !important;
        animation: message-slide-in 0.4s ease-out;
    }
    
    @keyframes message-slide-in {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .misi-message.user {
        align-items: flex-end;
        align-self: flex-end;
        margin-left: auto;
    }
    
    .misi-message.assistant {
        align-items: flex-start;
        align-self: flex-start;
        margin-right: auto;
    }
    
    .misi-message-bubble {
        padding: 12px 16px;
        border-radius: 18px;
        line-height: 1.4;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        word-wrap: break-word;
        max-width: 100%;
        position: relative;
        z-index: 2;
        transition: all 0.3s ease;
    }
    
    .misi-message.user .misi-message-bubble {
        background: linear-gradient(135deg, #dcf8c6 0%, #b8e6a8 100%) !important;
        color: #000 !important;
        border-bottom-right-radius: 4px;
        margin-bottom: 4px;
        border: 1px solid #b8e6a8;
        box-shadow: 0 4px 12px rgba(184, 230, 168, 0.3);
    }
    
    .misi-message.assistant .misi-message-bubble {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
        color: #1e293b !important;
        border: 1px solid #e2e8f0;
        border-bottom-left-radius: 4px;
        margin-bottom: 4px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    .misi-message-bubble:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.15);
    }
    
    .misi-message-timestamp {
        font-size: 11px;
        color: #64748b;
        margin: 0 4px;
        opacity: 0.7;
        font-weight: 500;
    }
    
    .misi-message.user .misi-message-timestamp {
        text-align: right;
    }
    
    .misi-message.assistant .misi-message-timestamp {
        text-align: left;
    }
    
    .misi-typing-indicator {
        display: none;
        padding: 12px 16px;
        background: white;
        border-radius: 18px;
        margin-bottom: 16px;
        align-self: flex-start;
        max-width: 85%;
        border: 1px solid #e2e8f0;
        border-bottom-left-radius: 4px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        animation: typing-pulse 1.5s infinite;
    }
    
    @keyframes typing-pulse {
        0%, 100% { opacity: 0.7; }
        50% { opacity: 1; }
    }
    
    .misi-typing-dots {
        display: flex;
        gap: 4px;
        align-items: center;
    }
    
    .misi-typing-dot {
        width: 8px;
        height: 8px;
        background: #64748b;
        border-radius: 50%;
        animation: misi-typing-bounce 1.4s infinite ease-in-out;
    }
    
    .misi-typing-dot:nth-child(1) { animation-delay: -0.32s; }
    .misi-typing-dot:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes misi-typing-bounce {
        0%, 80%, 100% {
            transform: scale(0.8);
            opacity: 0.5;
        }
        40% {
            transform: scale(1);
            opacity: 1;
        }
    }
    
    @keyframes message-highlight {
        0% {
            transform: scale(0.95);
            opacity: 0.8;
        }
        50% {
            transform: scale(1.02);
            opacity: 1;
        }
        100% {
            transform: scale(1);
            opacity: 1;
        }
    }
    
    .misi-suggestions {
        padding: 20px 24px;
        background: white;
        border-top: 1px solid #e2e8f0;
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        justify-content: center;
        animation: suggestions-slide-up 0.5s ease-out;
    }
    
    @keyframes suggestions-slide-up {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .misi-suggestion-btn {
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
        color: #475569;
        border: 1px solid #e2e8f0;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .misi-suggestion-btn:hover {
        background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%);
        color: #1e293b;
        border-color: #cbd5e1;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .misi-chat-input-container {
        padding: 20px 24px;
        background: white;
        border-top: 1px solid #e2e8f0;
        display: flex;
        gap: 12px;
        align-items: center;
        border-radius: 0 0 20px 20px;
        animation: input-slide-up 0.6s ease-out;
    }
    
    @keyframes input-slide-up {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .misi-chat-input {
        flex: 1;
        padding: 16px 20px;
        border: 2px solid #d1d5db;
        border-radius: 25px;
        font-size: 16px;
        outline: none;
        background: white;
        color: #1e293b;
        transition: all 0.3s ease;
        box-sizing: border-box;
        cursor: text;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        line-height: 1.5;
        resize: none;
        overflow: hidden;
        min-height: 50px;
        max-height: 120px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .misi-chat-input:focus {
        border-color: #10b981;
        background: white;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1), 0 4px 12px rgba(0,0,0,0.1);
        outline: none;
        transform: translateY(-1px);
    }
    
    .misi-chat-input:active {
        border-color: #10b981;
    }
    
    .misi-chat-input::placeholder {
        color: #9ca3af;
        opacity: 1;
    }
    
    .misi-send-btn {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border: none;
        border-radius: 50%;
        font-size: 20px;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .misi-send-btn::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s ease;
    }
    
    .misi-send-btn:hover::before {
        left: 100%;
    }
    
    .misi-send-btn:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        transform: scale(1.05) rotate(5deg);
        box-shadow: 0 6px 16px rgba(16, 185, 129, 0.4);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .misi-chat-content {
            width: 95vw;
            height: 90vh;
            max-height: none;
        }
        
        .misi-suggestions {
            padding: 15px 20px;
        }
        
        .misi-suggestion-btn {
            padding: 6px 12px;
            font-size: 13px;
        }
    }
    
    /* Loading animation for the icon */
    .misi-icon.loading {
        animation: misi-loading 1s infinite;
    }
    
    @keyframes misi-loading {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
    
    <div class="misi-icon-container">
        <div class="misi-icon" id="misi-icon" title="Ask Misi - SmartOps AI Assistant">
            <img src="https://raw.githubusercontent.com/smartops-ai/smartops-ai/main/assets/misi_logo.png" alt="Misi Logo" onerror="this.style.display='none'; this.nextElementSibling.style.display='block';" />
            <span class="misi-icon-fallback">🤖</span>
        </div>
        <div class="misi-icon-label">Ask Misi</div>
    </div>
    
    <div class="misi-chat-popup" id="misi-chat-popup">
        <div class="misi-chat-content">
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
                    <div class="misi-message-timestamp">12:00</div>
                </div>
                
                <div class="misi-typing-indicator" id="misi-typing-indicator">
                    <div class="misi-typing-dots">
                        <div class="misi-typing-dot"></div>
                        <div class="misi-typing-dot"></div>
                        <div class="misi-typing-dot"></div>
                    </div>
                </div>
            </div>
            <div class="misi-suggestions">
                <button class="misi-suggestion-btn" onclick="sendMisiMessage('pod')">🚀 Pods</button>
                <button class="misi-suggestion-btn" onclick="sendMisiMessage('anomaly')">⚠️ Anomaly</button>
                <button class="misi-suggestion-btn" onclick="sendMisiMessage('scale')">📈 Scale</button>
                <button class="misi-suggestion-btn" onclick="sendMisiMessage('shell')">💻 Shell</button>
                <button class="misi-suggestion-btn" onclick="sendMisiMessage('incident')">🚨 Incident</button>
                <button class="misi-suggestion-btn" onclick="sendMisiMessage('ai')">🤖 AI Actions</button>
                <button class="misi-suggestion-btn" onclick="sendMisiMessage('deploy')">🚀 Deployments</button>
                <button class="misi-suggestion-btn" onclick="sendMisiMessage('help')">❓ Help</button>
            </div>
            <div class="misi-chat-input-container">
                <input type="text" class="misi-chat-input" id="misi-chat-input"
                       placeholder="Ask me anything about SmartOps..." />
                <button class="misi-send-btn" id="misi-send-btn">📤</button>
            </div>
        </div>
    </div>
    
    <script>
    let misiPopupVisible = false;
    
    function toggleMisiPopup() {
        const popup = document.getElementById('misi-chat-popup');
        const icon = document.getElementById('misi-icon');
        
        if (popup) {
            misiPopupVisible = !misiPopupVisible;
            
            if (misiPopupVisible) {
                // Add loading animation to icon
                icon.classList.add('loading');
                
                // Show popup with enhanced animation
                popup.style.display = 'flex';
                
                // Remove loading animation after popup is shown
                setTimeout(() => {
                    icon.classList.remove('loading');
                    
                    const input = document.getElementById('misi-chat-input');
                    if (input) {
                        input.value = '';
                        input.focus();
                        console.log('Input focused and ready for input');
                    }
                }, 500);
            } else {
                popup.style.display = 'none';
            }
        }
    }
    
    function closeMisiPopup() {
        const popup = document.getElementById('misi-chat-popup');
        if (popup) {
            misiPopupVisible = false;
            popup.style.display = 'none';
            
            const input = document.getElementById('misi-chat-input');
            if (input) {
                input.value = '';
            }
        }
    }
    
    function addMisiMessage(message, isUser = false) {
        const chatBody = document.getElementById('misi-chat-body');
        if (chatBody) {
            console.log('Adding message:', message, 'isUser:', isUser);
            
            // Remove typing indicator if it exists
            const typingIndicator = document.getElementById('misi-typing-indicator');
            if (typingIndicator) {
                typingIndicator.style.display = 'none';
            }
            
            const messageDiv = document.createElement('div');
            messageDiv.className = `misi-message ${isUser ? 'user' : 'assistant'}`;
            
            const bubbleDiv = document.createElement('div');
            bubbleDiv.className = 'misi-message-bubble';
            bubbleDiv.textContent = message;
            
            // Add timestamp
            const timestamp = document.createElement('div');
            timestamp.className = 'misi-message-timestamp';
            const now = new Date();
            timestamp.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            
            messageDiv.appendChild(bubbleDiv);
            messageDiv.appendChild(timestamp);
            chatBody.appendChild(messageDiv);
            
            // Force the message to be visible with important styles
            messageDiv.style.setProperty('display', 'flex', 'important');
            messageDiv.style.setProperty('visibility', 'visible', 'important');
            messageDiv.style.setProperty('opacity', '1', 'important');
            messageDiv.style.setProperty('position', 'relative', 'important');
            messageDiv.style.setProperty('z-index', '10', 'important');
            
            // Add animation to highlight the new message
            messageDiv.style.animation = 'message-highlight 0.5s ease-out';
            
            // Scroll to bottom
            chatBody.scrollTop = chatBody.scrollHeight;
            
            // Force a reflow to ensure the message is visible
            messageDiv.offsetHeight;
            
            console.log('Message added successfully. Total messages:', chatBody.children.length);
            console.log('Message element:', messageDiv);
            console.log('Message display style:', messageDiv.style.display);
            console.log('Message visibility style:', messageDiv.style.visibility);
        } else {
            console.error('Chat body not found!');
        }
    }
    
    function showTypingIndicator() {
        const indicator = document.getElementById('misi-typing-indicator');
        if (indicator) {
            indicator.style.display = 'block';
            const chatBody = document.getElementById('misi-chat-body');
            if (chatBody) {
                chatBody.scrollTop = chatBody.scrollHeight;
            }
        }
    }
    
    function hideTypingIndicator() {
        const indicator = document.getElementById('misi-typing-indicator');
        if (indicator) {
            indicator.style.display = 'none';
        }
    }
    
    function sendMisiMessage(message = null) {
        let textToSend = message;
        
        if (!textToSend) {
            const input = document.getElementById('misi-chat-input');
            if (input) {
                textToSend = input.value.trim();
                input.value = '';
            }
        }
        
        if (textToSend) {
            console.log('Sending message:', textToSend);
            
            // Add user message immediately
            addMisiMessage(textToSend, true);
            
            // Show typing indicator
            showTypingIndicator();
            
            // Simulate AI response after delay
            setTimeout(() => {
                hideTypingIndicator();
                
                let response = "I understand you're asking about '" + textToSend + "'. ";
                
                if (textToSend.toLowerCase().includes('pod')) {
                    response += "To check pods, go to the Pod Explorer page. You can view logs, check status, and manage pod lifecycle.";
                } else if (textToSend.toLowerCase().includes('anomaly')) {
                    response += "Anomaly detection is available in the sidebar. It monitors CPU and memory usage to identify problematic pods.";
                } else if (textToSend.toLowerCase().includes('scale')) {
                    response += "Auto-scaling recommendations are available on the Auto-Scaling page. You can set up HPA and manage scaling policies.";
                } else if (textToSend.toLowerCase().includes('shell')) {
                    response += "Use the Kubernetes Shell page to run kubectl commands and explore your cluster directly from the dashboard.";
                } else if (textToSend.toLowerCase().includes('incident')) {
                    response += "The Incident Timeline page helps you track and analyze deployment events and generate postmortem reports.";
                } else if (textToSend.toLowerCase().includes('ai')) {
                    response += "AI Actions page provides automated responses to common issues and intelligent recommendations.";
                } else if (textToSend.toLowerCase().includes('deploy')) {
                    response += "Check the Deployments page to monitor deployment status, rollbacks, and deployment events.";
                } else if (textToSend.toLowerCase().includes('help')) {
                    response += "I'm here to help! Ask me about any SmartOps feature, or use the suggestion buttons above for quick access.";
                } else {
                    response += "I can help you navigate SmartOps features. Try asking about pods, anomalies, scaling, shell access, incidents, AI actions, or deployments.";
                }
                
                console.log('Sending AI response:', response);
                addMisiMessage(response, false);
            }, 1500);
        } else {
            console.log('No message to send');
        }
    }
    
    document.addEventListener('DOMContentLoaded', function() {
        const icon = document.getElementById('misi-icon');
        const closeBtn = document.querySelector('.misi-close-btn');
        const input = document.getElementById('misi-chat-input');
        const sendBtn = document.getElementById('misi-send-btn');
        const popup = document.getElementById('misi-chat-popup');
        
        // Add keyboard support
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && misiPopupVisible) {
                closeMisiPopup();
            }
        });
        
        if (icon) {
            icon.addEventListener('click', toggleMisiPopup);
        }
        
        if (closeBtn) {
            closeBtn.addEventListener('click', closeMisiPopup);
        }
        
        if (input) {
            input.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMisiMessage();
                }
            });
            
            input.addEventListener('input', function(e) {
                console.log('Input value:', e.target.value);
            });
            
            input.addEventListener('focus', function(e) {
                console.log('Input focused');
                e.target.style.borderColor = '#10b981';
            });
            
            input.addEventListener('blur', function(e) {
                console.log('Input blurred');
                e.target.style.borderColor = '#d1d5db';
            });
        }
        
        if (sendBtn) {
            sendBtn.addEventListener('click', function() {
                sendMisiMessage();
            });
        }
        
        if (popup) {
            popup.addEventListener('click', function(e) {
                if (e.target === popup) {
                    closeMisiPopup();
                }
            });
        }
        
        // Add some initial animation to the icon
        setTimeout(() => {
            if (icon) {
                icon.style.animation = 'misi-pulse 2s infinite';
            }
        }, 1000);
    });
    </script>
    """
    
    components.html(html, height=0, scrolling=False)
