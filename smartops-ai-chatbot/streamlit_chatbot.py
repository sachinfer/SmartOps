"""
SmartOps AI Chatbot Streamlit Interface
Provides a modern chat interface for users to interact with the AI assistant
"""

import streamlit as st
import json
from datetime import datetime
from ai_chatbot_engine import SmartOpsAIChatbot
from smartops_knowledge_base import get_knowledge_base

# Page configuration
st.set_page_config(
    page_title="SmartOps AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
    }
    .chat-message.user {
        background-color: #2b313e;
        border-left: 4px solid #00ff88;
    }
    .chat-message.assistant {
        background-color: #1e1e1e;
        border-left: 4px solid #ff6b6b;
    }
    .chat-message .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin-right: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        font-weight: bold;
    }
    .chat-message .message {
        flex: 1;
    }
    .navigation-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        color: white;
        margin: 1rem 0;
    }
    .suggested-questions {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 1rem;
    }
    .suggested-question {
        background: #4a5568;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .suggested-question:hover {
        background: #2d3748;
        transform: translateY(-2px);
    }
    .confidence-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-top: 0.5rem;
    }
    .confidence-bar {
        flex: 1;
        height: 8px;
        background: #2d3748;
        border-radius: 4px;
        overflow: hidden;
    }
    .confidence-fill {
        height: 100%;
        background: linear-gradient(90deg, #ff6b6b, #00ff88);
        transition: width 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = SmartOpsAIChatbot()
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 1

def display_header():
    """Display the main header"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h1 style="color: #00ff88; font-size: 3rem; margin-bottom: 0.5rem;">🤖</h1>
            <h1 style="color: white; margin-bottom: 0.5rem;">SmartOps AI Assistant</h1>
            <p style="color: #a0aec0; font-size: 1.1rem;">Your intelligent Kubernetes operations companion</p>
        </div>
        """, unsafe_allow_html=True)

def display_sidebar():
    """Display the sidebar with information and controls"""
    with st.sidebar:
        st.markdown("## 🎯 Quick Actions")
        
        # Quick navigation buttons
        st.markdown("### 📱 Navigate to Pages")
        pages = {
            1: "Overview",
            2: "Pod Explorer & Logs",
            3: "Kubernetes Shell",
            4: "Anomaly Detection",
            5: "Auto Scaling",
            6: "Incident Management",
            8: "AI Actions",
            9: "Deployments"
        }
        
        for page_num, page_name in pages.items():
            if st.button(f"📄 {page_name}", key=f"nav_{page_num}"):
                st.session_state.current_page = page_num
                st.rerun()
        
        st.markdown("---")
        
        # Knowledge base info
        st.markdown("### 📚 Knowledge Base")
        knowledge_base = get_knowledge_base()
        st.write(f"**Categories:** {len(knowledge_base)}")
        st.write(f"**Total Features:** {sum(len(info['features']) for info in knowledge_base.values())}")
        
        # Conversation controls
        st.markdown("### 💬 Conversation")
        if st.button("🗑️ Clear Chat"):
            st.session_state.chatbot.clear_conversation()
            st.session_state.messages = []
            st.rerun()
        
        if st.button("📋 Show Context"):
            context = st.session_state.chatbot.get_context_summary()
            st.text_area("Conversation Context", context, height=200)
        
        st.markdown("---")
        
        # Current page indicator
        st.markdown("### 🧭 Current Location")
        current_page_name = pages.get(st.session_state.current_page, "Unknown")
        st.info(f"**Page {st.session_state.current_page}:** {current_page_name}")

def display_chat_interface():
    """Display the main chat interface"""
    st.markdown("## 💬 Chat with AI Assistant")
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Display existing messages
        for message in st.session_state.messages:
            display_message(message)
        
        # Chat input
        user_input = st.chat_input("Ask me anything about SmartOps...")
        
        if user_input:
            # Add user message
            user_message = {
                "role": "user",
                "content": user_input,
                "timestamp": datetime.now()
            }
            st.session_state.messages.append(user_message)
            
            # Get AI response
            with st.spinner("🤖 AI is thinking..."):
                response = st.session_state.chatbot.process_query(user_input)
            
            # Add AI response
            ai_message = {
                "role": "assistant",
                "content": response["answer"],
                "response_data": response,
                "timestamp": datetime.now()
            }
            st.session_state.messages.append(ai_message)
            
            # Rerun to display new messages
            st.rerun()

def display_message(message):
    """Display a single chat message"""
    if message["role"] == "user":
        st.markdown(f"""
        <div class="chat-message user">
            <div class="avatar" style="background-color: #00ff88; color: #1a202c;">👤</div>
            <div class="message">
                <strong>You:</strong><br>
                {message["content"]}
                <br><small style="color: #a0aec0;">{message["timestamp"].strftime('%H:%M')}</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # AI message
        response_data = message.get("response_data", {})
        
        st.markdown(f"""
        <div class="chat-message assistant">
            <div class="avatar" style="background-color: #ff6b6b; color: white;">🤖</div>
            <div class="message">
                <strong>AI Assistant:</strong><br>
                {message["content"]}
                <br><small style="color: #a0aec0;">{message["timestamp"].strftime('%H:%M')}</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display navigation guide if available
        if response_data.get("navigation_guide"):
            nav_guide = response_data["navigation_guide"]
            st.markdown(f"""
            <div class="navigation-card">
                <h4>🧭 Navigation Guide</h4>
                <p><strong>Page {nav_guide['page_number']}:</strong> {nav_guide['page_name']}</p>
                <p>{nav_guide['instruction']}</p>
                <button onclick="window.parent.postMessage({{type: 'navigate', page: {nav_guide['page_number']}}}, '*')" 
                        style="background: white; color: #667eea; border: none; padding: 0.5rem 1rem; border-radius: 0.25rem; cursor: pointer;">
                    Go to Page {nav_guide['page_number']}
                </button>
            </div>
            """, unsafe_allow_html=True)
        
        # Display suggested questions
        if response_data.get("suggested_questions"):
            st.markdown("### 💡 Suggested Questions")
            st.markdown('<div class="suggested-questions">', unsafe_allow_html=True)
            
            for question in response_data["suggested_questions"]:
                if st.button(question, key=f"suggest_{hash(question)}"):
                    # Add suggested question as user input
                    user_message = {
                        "role": "user",
                        "content": question,
                        "timestamp": datetime.now()
                    }
                    st.session_state.messages.append(user_message)
                    
                    # Get AI response
                    with st.spinner("🤖 AI is thinking..."):
                        response = st.session_state.chatbot.process_query(question)
                    
                    # Add AI response
                    ai_message = {
                        "role": "assistant",
                        "content": response["answer"],
                        "response_data": response,
                        "timestamp": datetime.now()
                    }
                    st.session_state.messages.append(ai_message)
                    
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Display confidence indicator
        if response_data.get("confidence"):
            confidence = response_data["confidence"]
            confidence_color = "#00ff88" if confidence > 0.7 else "#ffaa00" if confidence > 0.4 else "#ff6b6b"
            
            st.markdown(f"""
            <div class="confidence-indicator">
                <span style="color: {confidence_color}; font-weight: bold;">Confidence:</span>
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: {confidence * 100}%; background: {confidence_color};"></div>
                </div>
                <span style="color: {confidence_color}; font-weight: bold;">{confidence:.1%}</span>
            </div>
            """, unsafe_allow_html=True)

def display_features_overview():
    """Display an overview of SmartOps features"""
    st.markdown("## 🚀 SmartOps Features Overview")
    
    knowledge_base = get_knowledge_base()
    
    # Create feature cards
    cols = st.columns(3)
    
    for i, (category, info) in enumerate(knowledge_base.items()):
        col = cols[i % 3]
        
        with col:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%); 
                        padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;">
                <h4 style="color: #00ff88; margin-bottom: 0.5rem;">{info['page']}</h4>
                <p style="color: #e2e8f0; font-size: 0.9rem;">{info['answer'][:100]}...</p>
                <p style="color: #a0aec0; font-size: 0.8rem;">Page {info['page_number']}</p>
            </div>
            """, unsafe_allow_html=True)

def main():
    """Main function"""
    initialize_session_state()
    
    # Display header
    display_header()
    
    # Create columns for layout
    col1, col2 = st.columns([1, 3])
    
    with col1:
        display_sidebar()
    
    with col2:
        # Main content area
        tab1, tab2 = st.tabs(["💬 AI Chat", "📚 Features"])
        
        with tab1:
            display_chat_interface()
        
        with tab2:
            display_features_overview()

if __name__ == "__main__":
    main()
