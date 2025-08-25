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
        """Initialize the Misi chatbot widget"""
        self.chatbot = SmartOpsAIChatbot()
        
    def render_misi_icon(self, position="bottom-right"):
        """Render the Misi AI icon in the specified corner"""
        
        # CSS for the floating Misi icon
        st.markdown(f"""
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
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
            border: 3px solid white;
        }}
        
        .misi-icon:hover {{
            transform: scale(1.1);
            box-shadow: 0 6px 20px rgba(0,0,0,0.4);
        }}
        
        .misi-icon:active {{
            transform: scale(0.95);
        }}
        
        .misi-icon-text {{
            color: white;
            font-size: 24px;
            font-weight: bold;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }}
        
        .misi-chat-popup {{
            position: fixed;
            {position.split('-')[0]}: 90px;
            {position.split('-')[1]}: 20px;
            width: 400px;
            height: 500px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            z-index: 1001;
            display: none;
            border: 2px solid #667eea;
        }}
        
        .misi-chat-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            border-radius: 13px 13px 0 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .misi-chat-title {{
            font-size: 18px;
            font-weight: bold;
        }}
        
        .misi-close-btn {{
            background: rgba(255,255,255,0.2);
            border: none;
            color: white;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            cursor: pointer;
            font-size: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .misi-close-btn:hover {{
            background: rgba(255,255,255,0.3);
        }}
        
        .misi-chat-body {{
            padding: 15px;
            height: 380px;
            overflow-y: auto;
        }}
        
        .misi-chat-input-container {{
            padding: 15px;
            border-top: 1px solid #eee;
        }}
        
        .misi-chat-input {{
            width: 100%;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 20px;
            font-size: 14px;
            outline: none;
        }}
        
        .misi-chat-input:focus {{
            border-color: #667eea;
        }}
        
        .misi-message {{
            margin-bottom: 15px;
            display: flex;
            align-items: flex-start;
        }}
        
        .misi-message.user {{
            justify-content: flex-end;
        }}
        
        .misi-message.assistant {{
            justify-content: flex-start;
        }}
        
        .misi-message-bubble {{
            max-width: 80%;
            padding: 10px 15px;
            border-radius: 18px;
            font-size: 14px;
            line-height: 1.4;
        }}
        
        .misi-message.user .misi-message-bubble {{
            background: #667eea;
            color: white;
            border-bottom-right-radius: 5px;
        }}
        
        .misi-message.assistant .misi-message-bubble {{
            background: #f1f3f4;
            color: #333;
            border-bottom-left-radius: 5px;
        }}
        
        .misi-navigation-guide {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px;
            border-radius: 10px;
            margin: 10px 0;
            font-size: 13px;
        }}
        
        .misi-suggested-questions {{
            margin-top: 10px;
        }}
        
        .misi-suggested-question {{
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 15px;
            padding: 8px 12px;
            margin: 5px 5px 5px 0;
            display: inline-block;
            cursor: pointer;
            font-size: 12px;
            transition: all 0.2s ease;
        }}
        
        .misi-suggested-question:hover {{
            background: #e9ecef;
            border-color: #667eea;
        }}
        </style>
        """, unsafe_allow_html=True)
        
        # JavaScript for the popup functionality
        js_code = """
        <script>
        let misiPopupVisible = false;
        
        function toggleMisiPopup() {
            const popup = document.getElementById('misi-chat-popup');
            if (misiPopupVisible) {
                popup.style.display = 'none';
                misiPopupVisible = false;
            } else {
                popup.style.display = 'block';
                misiPopupVisible = true;
                // Focus on input when opening
                setTimeout(() => {
                    const input = document.getElementById('misi-chat-input');
                    if (input) input.focus();
                }, 100);
            }
        }
        
        function closeMisiPopup() {
            const popup = document.getElementById('misi-chat-popup');
            popup.style.display = 'none';
            misiPopupVisible = false;
        }
        
        function sendMisiMessage() {
            const input = document.getElementById('misi-chat-input');
            const message = input.value.trim();
            if (message) {
                // This will be handled by Streamlit
                window.parent.postMessage({
                    type: 'misi_message',
                    message: message
                }, '*');
                input.value = '';
            }
        }
        
        // Handle Enter key in input
        document.addEventListener('DOMContentLoaded', function() {
            const input = document.getElementById('misi-chat-input');
            if (input) {
                input.addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        sendMisiMessage();
                    }
                });
            }
        });
        
        // Close popup when clicking outside
        document.addEventListener('click', function(e) {
            const popup = document.getElementById('misi-chat-popup');
            const icon = document.getElementById('misi-icon');
            if (misiPopupVisible && !popup.contains(e.target) && !icon.contains(e.target)) {
                closeMisiPopup();
            }
        });
        </script>
        """
        
        # Render the Misi icon and popup
        st.markdown(f"""
        <div class="misi-icon-container">
            <div class="misi-icon" id="misi-icon" onclick="toggleMisiPopup()">
                <div class="misi-icon-text">🤖</div>
            </div>
        </div>
        
        <div class="misi-chat-popup" id="misi-chat-popup">
            <div class="misi-chat-header">
                <div class="misi-chat-title">🤖 Ask Misi</div>
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
        """, unsafe_allow_html=True)
    
    def render_misi_integration(self, position="bottom-right"):
        """Render the complete Misi integration with icon and popup"""
        
        # Initialize session state for Misi
        if 'misi_messages' not in st.session_state:
            st.session_state.misi_messages = [
                {
                    "role": "assistant",
                    "content": "Hi! I'm Misi, your SmartOps AI assistant. How can I help you today?",
                    "timestamp": datetime.now()
                }
            ]
        
        # Render the Misi icon and popup
        self.render_misi_icon(position)
        
        # Handle chat functionality
        self._handle_misi_chat()
    
    def _handle_misi_chat(self):
        """Handle the Misi chat functionality"""
        
        # Create a hidden chat input for Streamlit
        with st.container():
            st.markdown("<!-- Misi Chat Integration -->", unsafe_allow_html=True)
            
            # Chat input (hidden but functional)
            user_input = st.text_input(
                "Ask Misi (hidden)",
                key="misi_hidden_input",
                label_visibility="collapsed",
                placeholder=""
            )
            
            if user_input:
                # Process the query with Misi
                response = self.chatbot.process_query(user_input)
                
                # Add user message
                st.session_state.misi_messages.append({
                    "role": "user",
                    "content": user_input,
                    "timestamp": datetime.now()
                })
                
                # Add Misi response
                st.session_state.misi_chatbot_response = response
                
                # Clear the input
                st.session_state.misi_hidden_input = ""
                
                # Rerun to update the chat
                st.rerun()
            
            # Display chat messages in the popup via JavaScript
            if 'misi_chatbot_response' in st.session_state:
                response = st.session_state.misi_chatbot_response
                
                # Add Misi's response to messages
                st.session_state.misi_messages.append({
                    "role": "assistant",
                    "content": response["answer"],
                    "timestamp": datetime.now(),
                    "response_data": response
                })
                
                # Clear the response
                del st.session_state.misi_chatbot_response
                
                # Update the chat display
                self._update_chat_display()
    
    def _update_chat_display(self):
        """Update the chat display in the popup"""
        
        # Create JavaScript to update the chat
        chat_html = ""
        for message in st.session_state.misi_messages:
            if message["role"] == "user":
                chat_html += f"""
                <div class="misi-message user">
                    <div class="misi-message-bubble">{message["content"]}</div>
                </div>
                """
            else:
                chat_html += f"""
                <div class="misi-message assistant">
                    <div class="misi-message-bubble">{message["content"]}</div>
                </div>
                """
                
                # Add navigation guide if available
                if "response_data" in message and message["response_data"].get("navigation_guide"):
                    nav = message["response_data"]["navigation_guide"]
                    chat_html += f"""
                    <div class="misi-navigation-guide">
                        🧭 <strong>Navigate to:</strong> Page {nav['page_number']} - {nav['page_name']}
                    </div>
                    """
                
                # Add suggested questions if available
                if "response_data" in message and message["response_data"].get("suggested_questions"):
                    chat_html += '<div class="misi-suggested-questions">'
                    for question in message["response_data"]["suggested_questions"][:3]:
                        chat_html += f'<div class="misi-suggested-question">{question}</div>'
                    chat_html += '</div>'
        
        # Update the chat display
        st.markdown(f"""
        <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const chatBody = document.getElementById('misi-chat-body');
            if (chatBody) {{
                chatBody.innerHTML = `{chat_html}`;
                chatBody.scrollTop = chatBody.scrollHeight;
            }}
        }});
        </script>
        """, unsafe_allow_html=True)

def add_misi_to_page(position="bottom-right"):
    """Add Misi chatbot to any page - just call this function"""
    
    # Initialize Misi widget
    misi = MisiChatbotWidget()
    
    # Render Misi integration
    misi.render_misi_integration(position)
    
    return misi

# Example usage:
# In any page, just add:
# add_misi_to_page()  # Default bottom-right corner
# add_misi_to_page("top-right")  # Top-right corner
# add_misi_to_page("bottom-left")  # Bottom-left corner
