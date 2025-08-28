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
        background: rgba(0, 0, 0, 0.1);
        z-index: 10000;
        display: none;
        flex-direction: column;
        overflow: hidden;
        animation: misi-fade-in 0.3s ease-out;
        backdrop-filter: blur(1px);
        pointer-events: none;
    }
    
    .misi-chat-popup.active {
        pointer-events: auto;
    }
    
    @keyframes misi-fade-in {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .misi-chat-content {
        position: fixed;
        bottom: 80px;
        right: 25px;
        width: 320px;
        height: 450px;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.15);
        display: flex;
        flex-direction: column;
        overflow: hidden;
        animation: misi-popup-enter 0.4s ease-out forwards;
        z-index: 10001;
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        cursor: move;
        user-select: none;
        resize: both;
        min-width: 280px;
        min-height: 400px;
        max-width: 600px;
        max-height: 800px;
    }
    
    @keyframes misi-popup-enter {
        0% {
            opacity: 0;
            transform: translateY(100px) scale(0.8);
        }
        100% {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    /* Dark Blue Header */
    .misi-chat-header {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        color: white;
        padding: 12px 16px;
        text-align: left;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        position: relative;
        width: 100%;
        box-sizing: border-box;
        border-radius: 16px 16px 0 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        cursor: move;
        user-select: none;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
    }
    
    .misi-header-left {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .misi-header-icon {
        width: 40px;
        height: 40px;
        background: rgba(255,255,255,0.2);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
    }
    
    .misi-robot-avatar {
        width: 30px;
        height: 30px;
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
        font-size: 18px;
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
        font-size: 16px;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .misi-menu-btn:hover, .misi-zoom-btn:hover {
        background: rgba(255,255,255,0.3);
        transform: scale(1.1);
    }
    
    .misi-close-btn {
        background: rgba(255,255,255,0.2);
        color: white;
        border: none;
        font-size: 18px;
        width: 30px;
        height: 30px;
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
        padding: 16px;
        background: rgba(255, 255, 255, 0.9);
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 10px;
        position: relative;
        width: 100%;
        box-sizing: border-box;
        min-height: 0;
        visibility: visible !important;
        opacity: 1 !important;
    }
    
    .misi-chat-body * {
        visibility: visible !important;
        opacity: 1 !important;
    }
    
    .misi-message {
        display: flex !important;
        align-items: flex-start;
        gap: 10px;
        max-width: 100%;
        position: relative;
        z-index: 1;
        opacity: 1 !important;
        visibility: visible !important;
        animation: message-slide-in 0.4s ease-out;
        margin-bottom: 12px;
        width: 100%;
        box-sizing: border-box;
        min-height: 50px;
        background: transparent;
    }
    
    .misi-message::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(255, 0, 0, 0.1);
        z-index: -1;
        pointer-events: none;
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
        width: 30px;
        height: 30px;
        border-radius: 50%;
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
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
        max-width: 85%;
        min-width: 0;
    }
    
    .misi-message-bubble {
        padding: 10px 14px;
        border-radius: 14px;
        line-height: 1.3;
        font-size: 13px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        word-wrap: break-word;
        word-break: break-word;
        overflow-wrap: break-word;
        position: relative;
        z-index: 2;
        transition: all 0.3s ease;
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        min-height: 18px;
        white-space: pre-wrap;
        max-width: 100%;
        box-sizing: border-box;
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
        padding: 12px 16px;
        background: rgba(248, 250, 252, 0.9);
        border-top: 1px solid rgba(226, 232, 240, 0.5);
        display: flex;
        gap: 10px;
        align-items: center;
        border-radius: 0 0 16px 16px;
    }
    
    .misi-chat-input {
        flex: 1;
        padding: 10px 14px;
        border: 2px solid rgba(226, 232, 240, 0.6);
        border-radius: 16px;
        font-size: 14px;
        outline: none;
        background: rgba(255, 255, 255, 0.9);
        color: #1e293b;
        transition: all 0.3s ease;
        box-sizing: border-box;
        cursor: text;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        line-height: 1.4;
        resize: none;
        overflow: hidden;
        min-height: 40px;
        max-height: 100px;
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
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
        color: white;
        border: none;
        border-radius: 50%;
        font-size: 16px;
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
            width: 85vw;
            height: 55vh;
            max-width: 350px;
            bottom: 70px;
            right: 15px;
        }
        
        .misi-chat-input-container {
            padding: 10px 14px;
        }
        
        .misi-chat-header {
            padding: 10px 14px;
        }
        
        .misi-chat-body {
            padding: 14px;
        }
    }
    
         /* Resize handle */
     .misi-resize-handle {
         position: absolute;
         bottom: 0;
         right: 0;
         width: 20px;
         height: 20px;
         background: linear-gradient(-45deg, transparent 30%, #3b82f6 30%, #3b82f6 40%, transparent 40%);
         cursor: nw-resize;
         border-radius: 0 0 16px 0;
         opacity: 0.6;
         transition: opacity 0.3s ease;
     }
     
     .misi-resize-handle:hover {
         opacity: 1;
         background: linear-gradient(-45deg, transparent 30%, #1e40af 30%, #1e40af 40%, transparent 40%);
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
                     <button class="misi-zoom-btn" onclick="toggleZoom()" title="Toggle Zoom">🔍</button>
                     <button class="misi-menu-btn" title="Menu">⋮</button>
                     <button class="misi-close-btn" title="Close chat">×</button>
                 </div>
            </div>
            <div class="misi-chat-body" id="misi-chat-body">
                                <!-- Debug message to ensure visibility -->
                <div style="background: #ff0000; color: white; padding: 15px; margin: 15px; border-radius: 8px; font-weight: bold; text-align: center; border: 3px solid #000; display: block !important; visibility: visible !important; opacity: 1 !important;">
                    🔍 DEBUG: This message should be visible! If you see this, the chat body is working.
                </div>
                
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
                 <button class="misi-test-btn" onclick="testMessageDisplay()" style="background: #ef4444; color: white; border: none; padding: 8px 12px; border-radius: 8px; cursor: pointer; margin-left: 10px;">🧪 Test</button>
             </div>
             
             <!-- Resize handle -->
             <div class="misi-resize-handle" id="misi-resize-handle"></div>
        </div>
    </div>
    
    <script>
         let misiPopupVisible = false;
     let isZoomed = false;
     let currentScale = 1;
    
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
                popup.classList.add('active');
                
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
                popup.classList.remove('active');
            }
        }
    }
    
         function closeMisiPopup() {
         const popup = document.getElementById('misi-chat-popup');
         if (popup) {
             misiPopupVisible = false;
             popup.style.display = 'none';
             popup.classList.remove('active');
             
             const input = document.getElementById('misi-chat-input');
             if (input) {
                 input.value = '';
             }
         }
     }
     
     function toggleZoom() {
         const chatContent = document.querySelector('.misi-chat-content');
         if (chatContent) {
             if (isZoomed) {
                 // Zoom out
                 currentScale = 1;
                 chatContent.style.transform = `translate(${xOffset}px, ${yOffset}px) scale(1)`;
                 isZoomed = false;
             } else {
                 // Zoom in
                 currentScale = 1.5;
                 chatContent.style.transform = `translate(${xOffset}px, ${yOffset}px) scale(1.5)`;
                 isZoomed = true;
             }
         }
     }
     
     function zoomIn() {
         const chatContent = document.querySelector('.misi-chat-content');
         if (chatContent && currentScale < 3) {
             currentScale = Math.min(currentScale + 0.25, 3);
             chatContent.style.transform = `translate(${xOffset}px, ${yOffset}px) scale(${currentScale})`;
             isZoomed = currentScale > 1;
         }
     }
     
     function zoomOut() {
         const chatContent = document.querySelector('.misi-chat-content');
         if (chatContent && currentScale > 0.5) {
             currentScale = Math.max(currentScale - 0.25, 0.5);
             chatContent.style.transform = `translate(${xOffset}px, ${yOffset}px) scale(${currentScale})`;
             isZoomed = currentScale > 1;
         }
     }
     
     function resetZoom() {
         const chatContent = document.querySelector('.misi-chat-content');
         if (chatContent) {
             currentScale = 1;
             chatContent.style.transform = `translate(${xOffset}px, ${yOffset}px) scale(1)`;
             isZoomed = false;
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
            
            // Force the bubble to be visible
            bubbleDiv.style.setProperty('display', 'block', 'important');
            bubbleDiv.style.setProperty('visibility', 'visible', 'important');
            bubbleDiv.style.setProperty('opacity', '1', 'important');
            
            // Scroll to bottom
            chatBody.scrollTop = chatBody.scrollHeight;
            
            // Force a reflow to ensure the message is visible
            messageDiv.offsetHeight;
            bubbleDiv.offsetHeight;
            
            // Additional debugging
            console.log('Message added successfully. Total messages:', chatBody.children.length);
            console.log('Message element:', messageDiv);
            console.log('Message display style:', messageDiv.style.display);
            console.log('Message visibility style:', messageDiv.style.visibility);
            console.log('Bubble element:', bubbleDiv);
            console.log('Bubble display style:', bubbleDiv.style.display);
            
            // Force display refresh with multiple attempts
            setTimeout(() => {
                messageDiv.style.display = 'flex';
                messageDiv.style.visibility = 'visible';
                messageDiv.style.opacity = '1';
                bubbleDiv.style.display = 'block';
                bubbleDiv.style.visibility = 'visible';
                bubbleDiv.style.opacity = '1';
            }, 100);
            
            setTimeout(() => {
                messageDiv.style.display = 'flex';
                messageDiv.style.visibility = 'visible';
                messageDiv.style.opacity = '1';
                bubbleDiv.style.display = 'block';
                bubbleDiv.style.visibility = 'visible';
                bubbleDiv.style.opacity = '1';
            }, 500);
            
            // Final force refresh
            setTimeout(() => {
                messageDiv.style.cssText = 'display: flex !important; visibility: visible !important; opacity: 1 !important; position: relative !important; z-index: 10 !important; width: 100% !important; min-height: auto !important;';
                bubbleDiv.style.cssText = 'display: block !important; visibility: visible !important; opacity: 1 !important;';
            }, 1000);
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
        console.log('🧪 Testing message display...');
        
        // Test if chat body exists
        const chatBody = document.getElementById('misi-chat-body');
        if (chatBody) {
            console.log('✅ Chat body found:', chatBody);
            console.log('📊 Chat body children:', chatBody.children.length);
            console.log('🎨 Chat body styles:', chatBody.style.cssText);
            
            // Add a simple test message with forced styles
            const testDiv = document.createElement('div');
            testDiv.textContent = '🧪 TEST MESSAGE - This should be visible!';
            testDiv.style.cssText = 'background: #ef4444; color: white; padding: 15px; margin: 15px; border-radius: 8px; font-weight: bold; text-align: center; border: 3px solid #000; display: block !important; visibility: visible !important; opacity: 1 !important; font-size: 18px; z-index: 9999; position: relative;';
            chatBody.appendChild(testDiv);
            
            console.log('✅ Test message added. Total children:', chatBody.children.length);
            
            // Also test the normal message function
            setTimeout(() => {
                addMisiMessage('This is a test message from user', true);
            }, 500);
            
            setTimeout(() => {
                addMisiMessage('This is a test response from AI', false);
            }, 1000);
            
            // Force scroll to show the test message
            setTimeout(() => {
                chatBody.scrollTop = 0;
                console.log('📜 Scrolled to top to show test message');
            }, 100);
        } else {
            console.error('❌ Chat body not found in test function!');
        }
    }
    
    document.addEventListener('DOMContentLoaded', function() {
        const icon = document.getElementById('misi-icon');
        const closeBtn = document.querySelector('.misi-close-btn');
        const input = document.getElementById('misi-chat-input');
        const sendBtn = document.getElementById('misi-send-btn');
        const popup = document.getElementById('misi-chat-popup');
        const chatContent = document.querySelector('.misi-chat-content');
        
                 // Enhanced Draggable functionality with zoom support
         let isDragging = false;
         let currentX;
         let currentY;
         let initialX;
         let initialY;
         let xOffset = 0;
         let yOffset = 0;
         
         function dragStart(e) {
             // Don't start dragging if clicking on buttons
             if (e.target.closest('.misi-close-btn') || 
                 e.target.closest('.misi-menu-btn') || 
                 e.target.closest('.misi-zoom-btn')) {
                 return;
             }
             
             // Allow dragging from anywhere on the header
             if (e.target.closest('.misi-chat-header')) {
                 isDragging = true;
                 e.preventDefault();
                 
                 initialX = e.clientX - xOffset;
                 initialY = e.clientY - yOffset;
                 
                 // Add dragging visual feedback
                 chatContent.style.cursor = 'grabbing';
                 chatContent.style.boxShadow = '0 15px 50px rgba(0,0,0,0.3)';
             }
         }
         
         function drag(e) {
             if (isDragging) {
                 e.preventDefault();
                 
                 currentX = e.clientX - initialX;
                 currentY = e.clientY - initialY;
                 
                 xOffset = currentX;
                 yOffset = currentY;
                 
                 setTranslate(currentX, currentY, chatContent);
             }
         }
         
         function setTranslate(xPos, yPos, el) {
             // Apply both translation and current zoom scale
             el.style.transform = `translate(${xPos}px, ${yPos}px) scale(${currentScale})`;
         }
         
         function dragEnd() {
             if (isDragging) {
                 initialX = currentX;
                 initialY = currentY;
                 isDragging = false;
                 
                 // Reset cursor and shadow
                 chatContent.style.cursor = 'move';
                 chatContent.style.boxShadow = '0 8px 32px rgba(0,0,0,0.15)';
             }
         }
        
                 // Add keyboard support
         document.addEventListener('keydown', function(e) {
             if (e.key === 'Escape' && misiPopupVisible) {
                 closeMisiPopup();
             }
             
             // Zoom controls with keyboard
             if (e.ctrlKey || e.metaKey) {
                 if (e.key === '+' || e.key === '=') {
                     e.preventDefault();
                     zoomIn();
                 } else if (e.key === '-') {
                     e.preventDefault();
                     zoomOut();
                 } else if (e.key === '0') {
                     e.preventDefault();
                     resetZoom();
                 }
             }
             
             // Arrow key movement (when popup is visible)
             if (misiPopupVisible && !isDragging) {
                 const moveAmount = e.shiftKey ? 50 : 20; // Shift = bigger movement
                 
                 if (e.key === 'ArrowUp') {
                     e.preventDefault();
                     yOffset -= moveAmount;
                     setTranslate(xOffset, yOffset, chatContent);
                 } else if (e.key === 'ArrowDown') {
                     e.preventDefault();
                     yOffset += moveAmount;
                     setTranslate(xOffset, yOffset, chatContent);
                 } else if (e.key === 'ArrowLeft') {
                     e.preventDefault();
                     xOffset -= moveAmount;
                     setTranslate(xOffset, yOffset, chatContent);
                 } else if (e.key === 'ArrowRight') {
                     e.preventDefault();
                     xOffset += moveAmount;
                     setTranslate(xOffset, yOffset, chatContent);
                 }
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
        
                 // Add drag event listeners
         if (chatContent) {
             chatContent.addEventListener('mousedown', dragStart);
             document.addEventListener('mousemove', drag);
             document.addEventListener('mouseup', dragEnd);
         }
         
         // Add resize functionality
         const resizeHandle = document.getElementById('misi-resize-handle');
         if (resizeHandle) {
             let isResizing = false;
             let startWidth, startHeight, startX, startY;
             
             resizeHandle.addEventListener('mousedown', function(e) {
                 isResizing = true;
                 startX = e.clientX;
                 startY = e.clientY;
                 startWidth = chatContent.offsetWidth;
                 startHeight = chatContent.offsetHeight;
                 
                 e.preventDefault();
                 e.stopPropagation();
             });
             
             document.addEventListener('mousemove', function(e) {
                 if (isResizing) {
                     const newWidth = startWidth + (e.clientX - startX);
                     const newHeight = startHeight + (e.clientY - startY);
                     
                     // Apply size constraints
                     const constrainedWidth = Math.max(280, Math.min(600, newWidth));
                     const constrainedHeight = Math.max(400, Math.min(800, newHeight));
                     
                     chatContent.style.width = constrainedWidth + 'px';
                     chatContent.style.height = constrainedHeight + 'px';
                 }
             });
             
             document.addEventListener('mouseup', function() {
                 isResizing = false;
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