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
    
    .misi-icon img {
        width: 50px;
        height: 50px;
        object-fit: contain;
        filter: brightness(0) invert(1);
    }
    
    .misi-icon .misi-icon-fallback {
        font-size: 40px;
        color: white;
        display: none;
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
    }
    
    .misi-icon-container:hover .misi-icon-label {
        opacity: 1;
    }
    
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
        animation: misi-fade-in 0.3s ease-out;
        backdrop-filter: blur(10px);
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
        animation: misi-slide-in-top 0.3s ease-out;
        z-index: 10001;
    }
    
    @keyframes misi-slide-in-top {
        from {
            opacity: 0;
            transform: translateY(-100%);
        }
        to {
            opacity: 1;
            transform: translateY(0);
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
    }
    
    .misi-header-icon-inner {
        width: 40px;
        height: 40px;
        background: white;
        border-radius: 50%;
        position: relative;
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
    }
    
    .misi-close-btn:hover {
        background: rgba(255,255,255,0.3);
        transform: scale(1.1);
        background: #ef4444;
    }
    
    .misi-chat-body {
        flex: 1;
        padding: 24px;
        background: #f0f2f5;
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
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        word-wrap: break-word;
        max-width: 100%;
        position: relative;
        z-index: 2;
    }
    
    .misi-message.user .misi-message-bubble {
        background: #dcf8c6 !important;
        color: #000 !important;
        border-bottom-right-radius: 4px;
        margin-bottom: 4px;
        border: 1px solid #b8e6a8;
    }
    
    .misi-message.assistant .misi-message-bubble {
        background: white !important;
        color: #1e293b !important;
        border: 1px solid #e2e8f0;
        border-bottom-left-radius: 4px;
        margin-bottom: 4px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .misi-message-timestamp {
        font-size: 11px;
        color: #64748b;
        margin: 0 4px;
        opacity: 0.7;
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
    }
    
    .misi-suggestion-btn {
        background: #f1f5f9;
        color: #475569;
        border: 1px solid #e2e8f0;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .misi-suggestion-btn:hover {
        background: #e2e8f0;
        color: #1e293b;
        border-color: #cbd5e1;
    }
    
    .misi-chat-input-container {
        padding: 20px 24px;
        background: white;
        border-top: 1px solid #e2e8f0;
        display: flex;
        gap: 12px;
        align-items: center;
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
    }
    
    .misi-chat-input:focus {
        border-color: #10b981;
        background: white;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
        outline: none;
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
        background: #10b981;
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
    }
    
    .misi-send-btn:hover {
        background: #059669;
        transform: scale(1.05);
        box-shadow: 0 6px 16px rgba(16, 185, 129, 0.4);
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
                
                <!-- Debug message to ensure visibility -->
                <div style="background: #ff0000; color: white; padding: 15px; margin: 15px; border-radius: 8px; font-weight: bold; text-align: center; border: 3px solid #000;">
                    🔍 DEBUG: This message should be visible! If you see this, the chat body is working.
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
                <button class="misi-suggestion-btn" onclick="sendMisiMessage('pod')">Pods</button>
                <button class="misi-suggestion-btn" onclick="sendMisiMessage('anomaly')">Anomaly</button>
                <button class="misi-suggestion-btn" onclick="sendMisiMessage('scale')">Scale</button>
                <button class="misi-suggestion-btn" onclick="sendMisiMessage('shell')">Shell</button>
                <button class="misi-suggestion-btn" onclick="sendMisiMessage('incident')">Incident</button>
                <button class="misi-suggestion-btn" onclick="sendMisiMessage('ai')">AI Actions</button>
                <button class="misi-suggestion-btn" onclick="sendMisiMessage('deploy')">Deployments</button>
                <button class="misi-suggestion-btn" onclick="sendMisiMessage('help')">Help</button>
                <button class="misi-suggestion-btn" onclick="testMessageDisplay()" style="background: #ef4444; color: white;">Test Message</button>
                <button class="misi-suggestion-btn" onclick="forceRefreshDisplay()" style="background: #3b82f6; color: white;">Refresh Display</button>
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
        if (popup) {
            misiPopupVisible = !misiPopupVisible;
            popup.style.display = misiPopupVisible ? 'flex' : 'none';
            
            if (misiPopupVisible) {
                setTimeout(() => {
                    const input = document.getElementById('misi-chat-input');
                    if (input) {
                        input.value = '';
                        input.focus();
                        console.log('Input focused and ready for input');
                    }
                }, 300);
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
    
    function testMessageDisplay() {
        console.log('Testing message display...');
        
        // Test if chat body exists
        const chatBody = document.getElementById('misi-chat-body');
        if (chatBody) {
            console.log('Chat body found:', chatBody);
            console.log('Chat body children:', chatBody.children.length);
            console.log('Chat body styles:', chatBody.style.cssText);
            
            // Add a simple test message
            const testDiv = document.createElement('div');
            testDiv.textContent = 'TEST MESSAGE - This should be visible!';
            testDiv.style.cssText = 'background: red; color: white; padding: 10px; margin: 10px; border-radius: 5px; font-weight: bold;';
            chatBody.appendChild(testDiv);
            
            console.log('Test message added. Total children:', chatBody.children.length);
        } else {
            console.error('Chat body not found in test function!');
        }
        
        // Also test the normal message function
        addMisiMessage('This is a test message from user', true);
        setTimeout(() => {
            addMisiMessage('This is a test response from AI', false);
        }, 1000);
    }

    function forceRefreshDisplay() {
        console.log('Forcing display refresh...');
        const chatBody = document.getElementById('misi-chat-body');
        if (chatBody) {
            // Force a reflow to ensure all styles are applied
            chatBody.offsetHeight;
            console.log('Display refreshed. Total children:', chatBody.children.length);
        } else {
            console.error('Chat body not found for display refresh!');
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
    });
    </script>
    """
    
    components.html(html, height=0, scrolling=False)
