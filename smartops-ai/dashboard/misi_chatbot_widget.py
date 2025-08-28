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
    /* Modern Clean Interface CSS */
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
        width: 70px;
        height: 70px;
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer !important;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
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
        box-shadow: 0 12px 35px rgba(59, 130, 246, 0.6);
    }
    
    .misi-icon img {
        width: 40px;
        height: 40px;
        object-fit: contain;
        filter: brightness(0) invert(1);
        z-index: 2;
        position: relative;
    }
    
    .misi-icon .misi-icon-fallback {
        font-size: 35px;
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
    
    /* Modern Chat Popup */
    .misi-chat-popup {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(0, 0, 0, 0.5);
        z-index: 10000;
        display: none;
        flex-direction: column;
        overflow: hidden;
        animation: misi-fade-in 0.3s ease-out;
        backdrop-filter: blur(5px);
    }
    
    @keyframes misi-fade-in {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .misi-chat-content {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: white;
        border-radius: 0;
        box-shadow: none;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        animation: misi-popup-enter 0.4s ease-out forwards;
        z-index: 10001;
    }
    
    @keyframes misi-popup-enter {
        0% {
            opacity: 0;
            transform: translateY(-100%);
        }
        100% {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Dark Blue Header */
    .misi-chat-header {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        color: white;
        padding: 25px 30px;
        text-align: left;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        position: relative;
        width: 100%;
        box-sizing: border-box;
        border-radius: 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .misi-header-left {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .misi-header-icon {
        width: 45px;
        height: 45px;
        background: rgba(255,255,255,0.2);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
    }
    
    .misi-robot-avatar {
        width: 35px;
        height: 35px;
        background: white;
        border-radius: 50%;
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .misi-robot-antenna {
        position: absolute;
        top: -8px;
        left: 50%;
        transform: translateX(-50%);
        width: 4px;
        height: 12px;
        background: #1e40af;
        border-radius: 2px;
    }
    
    .misi-robot-eyes {
        display: flex;
        gap: 4px;
        margin-bottom: 2px;
    }
    
    .misi-robot-eye {
        width: 6px;
        height: 6px;
        background: #3b82f6;
        border-radius: 50%;
        animation: robot-blink 3s infinite;
    }
    
    @keyframes robot-blink {
        0%, 90%, 100% { opacity: 1; }
        95% { opacity: 0.3; }
    }
    
    .misi-robot-mouth {
        width: 12px;
        height: 3px;
        background: #1e40af;
        border-radius: 2px;
        margin-top: 2px;
    }
    
    .misi-chat-title {
        font-size: 20px;
        font-weight: 700;
        color: white;
        margin: 0;
    }
    
    .misi-header-right {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .misi-menu-btn {
        background: rgba(255,255,255,0.2);
        color: white;
        border: none;
        font-size: 18px;
        width: 35px;
        height: 35px;
        border-radius: 50%;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .misi-menu-btn:hover {
        background: rgba(255,255,255,0.3);
        transform: scale(1.1);
    }
    
    .misi-close-btn {
        background: rgba(255,255,255,0.2);
        color: white;
        border: none;
        font-size: 20px;
        width: 35px;
        height: 35px;
        border-radius: 50%;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .misi-close-btn:hover {
        background: #ef4444;
        transform: scale(1.1);
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4);
    }
    
    /* Clean White Chat Body */
    .misi-chat-body {
        flex: 1;
        padding: 30px;
        background: white;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 20px;
        position: relative;
        width: 100%;
        box-sizing: border-box;
        min-height: 0;
    }
    
    .misi-message {
        display: flex !important;
        align-items: flex-start;
        gap: 12px;
        max-width: 100%;
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
        flex-direction: row-reverse;
    }
    
    .misi-message.assistant {
        flex-direction: row;
    }
    
    .misi-message-avatar {
        width: 35px;
        height: 35px;
        border-radius: 50%;
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        font-weight: bold;
    }
    
    .misi-message.user .misi-message-avatar {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
    }
    
    .misi-message.assistant .misi-message-avatar {
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
        color: white;
    }
    
    .misi-message-content {
        flex: 1;
        max-width: 80%;
    }
    
    .misi-message-bubble {
        padding: 12px 16px;
        border-radius: 18px;
        line-height: 1.4;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        word-wrap: break-word;
        position: relative;
        z-index: 2;
        transition: all 0.3s ease;
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    
    .misi-message.user .misi-message-bubble {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border-bottom-right-radius: 4px;
        margin-left: auto;
        text-align: right;
    }
    
    .misi-message.assistant .misi-message-bubble {
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
        color: #1e293b;
        border: 1px solid #e2e8f0;
        border-bottom-left-radius: 4px;
        margin-right: auto;
        text-align: left;
    }
    
    .misi-message-bubble:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }
    
    .misi-message-timestamp {
        font-size: 11px;
        color: #64748b;
        margin-top: 4px;
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
        background: #f1f5f9;
        border-radius: 18px;
        margin-bottom: 16px;
        align-self: flex-start;
        max-width: 80%;
        border: 1px solid #e2e8f0;
        border-bottom-left-radius: 4px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
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
    
    /* Light Blue Input Field */
    .misi-chat-input-container {
        padding: 25px 30px;
        background: #f8fafc;
        border-top: 1px solid #e2e8f0;
        display: flex;
        gap: 12px;
        align-items: center;
        border-radius: 0;
    }
    
    .misi-chat-input {
        flex: 1;
        padding: 16px 20px;
        border: 2px solid #e2e8f0;
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
        border-color: #3b82f6;
        background: white;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1), 0 4px 12px rgba(0,0,0,0.1);
        outline: none;
        transform: translateY(-1px);
    }
    
    .misi-chat-input::placeholder {
        color: #9ca3af;
        opacity: 1;
    }
    
    .misi-send-btn {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
        color: white;
        border: none;
        border-radius: 50%;
        font-size: 20px;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
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
        background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
        transform: scale(1.05);
        box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .misi-chat-content {
            width: 100vw;
            height: 100vh;
            max-height: none;
        }
        
        .misi-chat-input-container {
            padding: 20px 25px;
        }
        
        .misi-chat-header {
            padding: 20px 25px;
        }
        
        .misi-chat-body {
            padding: 25px;
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
                <div class="misi-header-left">
                    <div class="misi-header-icon">
                        <div class="misi-robot-avatar">
                            <div class="misi-robot-antenna"></div>
                            <div class="misi-robot-eyes">
                                <div class="misi-robot-eye"></div>
                                <div class="misi-robot-eye"></div>
                            </div>
                            <div class="misi-robot-mouth"></div>
                        </div>
                    </div>
                    <div class="misi-chat-title">AI ChatBot</div>
                </div>
                <div class="misi-header-right">
                    <button class="misi-menu-btn" title="Menu">⋮</button>
                    <button class="misi-close-btn" title="Close chat">×</button>
                </div>
            </div>
            <div class="misi-chat-body" id="misi-chat-body">
                <div class="misi-message assistant">
                    <div class="misi-message-avatar">🤖</div>
                    <div class="misi-message-content">
                        <div class="misi-message-bubble">
                            Hello! How can I help you today?
                        </div>
                        <div class="misi-message-timestamp">12:00</div>
                    </div>
                </div>
                
                <div class="misi-typing-indicator" id="misi-typing-indicator">
                    <div class="misi-typing-dots">
                        <div class="misi-typing-dot"></div>
                        <div class="misi-typing-dot"></div>
                        <div class="misi-typing-dot"></div>
                    </div>
                </div>
            </div>
            <div class="misi-chat-input-container">
                <input type="text" class="misi-chat-input" id="misi-chat-input"
                       placeholder="Enter Message" />
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
                }, 400);
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
            
            const avatarDiv = document.createElement('div');
            avatarDiv.className = 'misi-message-avatar';
            avatarDiv.textContent = isUser ? '👤' : '🤖';
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'misi-message-content';
            
            const bubbleDiv = document.createElement('div');
            bubbleDiv.className = 'misi-message-bubble';
            bubbleDiv.textContent = message;
            
            // Add timestamp
            const timestamp = document.createElement('div');
            timestamp.className = 'misi-message-timestamp';
            const now = new Date();
            timestamp.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            
            contentDiv.appendChild(bubbleDiv);
            contentDiv.appendChild(timestamp);
            
            if (isUser) {
                messageDiv.appendChild(contentDiv);
                messageDiv.appendChild(avatarDiv);
            } else {
                messageDiv.appendChild(avatarDiv);
                messageDiv.appendChild(contentDiv);
            }
            
            chatBody.appendChild(messageDiv);
            
            // Force the message to be visible with multiple fallback methods
            messageDiv.style.setProperty('display', 'flex', 'important');
            messageDiv.style.setProperty('visibility', 'visible', 'important');
            messageDiv.style.setProperty('opacity', '1', 'important');
            messageDiv.style.setProperty('position', 'relative', 'important');
            messageDiv.style.setProperty('z-index', '10', 'important');
            messageDiv.style.setProperty('width', '100%', 'important');
            messageDiv.style.setProperty('min-height', 'auto', 'important');
            
            // Scroll to bottom
            chatBody.scrollTop = chatBody.scrollHeight;
            
            // Force a reflow to ensure the message is visible
            messageDiv.offsetHeight;
            
            // Additional debugging
            console.log('Message added successfully. Total messages:', chatBody.children.length);
            console.log('Message element:', messageDiv);
            console.log('Message display style:', messageDiv.style.display);
            console.log('Message visibility style:', messageDiv.style.visibility);
            
            // Force display refresh
            setTimeout(() => {
                messageDiv.style.display = 'flex';
                messageDiv.style.visibility = 'visible';
                messageDiv.style.opacity = '1';
            }, 100);
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
                e.target.style.borderColor = '#3b82f6';
            });
            
            input.addEventListener('blur', function(e) {
                console.log('Input blurred');
                e.target.style.borderColor = '#e2e8f0';
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
