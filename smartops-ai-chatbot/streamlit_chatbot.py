"""
SmartOps by Misi 24x7 AI Chatbot - Main Application
Complete chatbot interface with Misi integration
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from ai_chatbot_engine import SmartOpsAIChatbot
from smartops_knowledge_base import get_knowledge_base
from misi_chatbot_widget import add_misi_to_page

# Page configuration
st.set_page_config(
    page_title="SmartOps by Misi 24x7 AI Chatbot",
    page_icon="misi_24x7_logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .chat-container {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .user-message {
        background: #667eea;
        color: white;
        padding: 1rem;
        border-radius: 18px;
        margin: 0.5rem 0;
        text-align: right;
        max-width: 80%;
        margin-left: auto;
    }
    
    .assistant-message {
        background: white;
        color: #333;
        padding: 1rem;
        border-radius: 18px;
        margin: 0.5rem 0;
        border: 1px solid #e0e0e0;
        max-width: 80%;
    }
    
    .navigation-card {
        background: #e3f2fd;
        border: 1px solid #2196f3;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .suggestions-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin: 1rem 0;
    }
    
    .suggestion-btn {
        background: #f0f0f0;
        border: 1px solid #ddd;
        border-radius: 15px;
        padding: 0.5rem 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .suggestion-btn:hover {
        background: #e0e0e0;
        border-color: #bbb;
    }
    
    .confidence-badge {
        background: #4caf50;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 12px;
        font-size: 0.8rem;
        margin-left: 1rem;
    }
    
    .features-list {
        background: #f5f5f5;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize session state
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = SmartOpsAIChatbot()
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Header
    # Logo and header section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.image("misi_24x7_logo.png", width=100)
    with col2:
        st.markdown("""
        <div class="main-header">
            <h1>🤖 SmartOps by Misi 24x7 AI Chatbot</h1>
            <p>Your intelligent Kubernetes operations assistant</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.write("")  # Empty column for spacing
    
    # Sidebar
    with st.sidebar:
        st.header("🚀 Quick Actions")
        
        # Quick navigation
        st.subheader("📱 SmartOps Pages")
        pages = get_knowledge_base()
        for category, info in pages.items():
            if st.button(f"Page {info['page_number']}: {info['page']}", key=f"nav_{category}"):
                st.info(f"Navigate to {info['page']} to access {', '.join(info['features'][:2])}.")
        
        # Chat history
        st.subheader("💬 Chat History")
        if st.button("Clear History"):
            st.session_state.messages = []
            st.session_state.chatbot.clear_conversation_history()
            st.rerun()
        
        # Available features
        st.subheader("✨ Available Features")
        features = st.session_state.chatbot.get_available_features()
        for feature in features[:10]:  # Show first 10 features
            st.write(f"• {feature}")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Chat with Misi")
        
        # Chat input
        user_input = st.chat_input("Ask me anything about SmartOps...")
        
        if user_input:
            # Process query
            response = st.session_state.chatbot.process_query(user_input)
            
            # Add messages to session state
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.messages.append({"role": "assistant", "content": response["answer"]})
            
            # Rerun to display new messages
            st.rerun()
        
        # Display chat messages
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="assistant-message">{message["content"]}</div>', unsafe_allow_html=True)
        
        # Display last response details if available
        if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
            last_response = st.session_state.chatbot.process_query(st.session_state.messages[-2]["content"]) if len(st.session_state.messages) >= 2 else None
            
            if last_response:
                # Navigation guide
                if last_response.get("navigation_guide"):
                    nav_guide = last_response["navigation_guide"]
                    st.markdown(f"""
                    <div class="navigation-card">
                        <h4>🧭 Navigation Guide</h4>
                        <p><strong>Page {nav_guide['page_number']}:</strong> {nav_guide['page_name']}</p>
                        <p>{nav_guide['instruction']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Suggested questions
                if last_response.get("suggested_questions"):
                    st.subheader("💡 Suggested Questions")
                    suggestions = last_response["suggested_questions"]
                    
                    cols = st.columns(len(suggestions))
                    for i, suggestion in enumerate(suggestions):
                        with cols[i]:
                            if st.button(suggestion, key=f"suggest_{i}"):
                                # Process suggested question
                                suggested_response = st.session_state.chatbot.process_query(suggestion)
                                st.session_state.messages.append({"role": "user", "content": suggestion})
                                st.session_state.messages.append({"role": "assistant", "content": suggested_response["answer"]})
                                st.rerun()
                
                # Features
                if last_response.get("features"):
                    st.markdown("""
                    <div class="features-list">
                        <h4>🔧 Key Features</h4>
                    """, unsafe_allow_html=True)
                    for feature in last_response["features"]:
                        st.write(f"• {feature}")
                    st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.header("📊 SmartOps Overview")
        
        # Quick stats
        st.metric("Total Pages", "9")
        st.metric("AI Features", "8")
        st.metric("Chat Sessions", len(st.session_state.messages) // 2)
        
        # Quick help
        st.subheader("🚀 Quick Help")
        quick_questions = [
            "How can AI check pods?",
            "What is anomaly detection?",
            "How do I access the Kubernetes shell?",
            "Tell me about auto-scaling"
        ]
        
        for question in quick_questions:
            if st.button(question, key=f"quick_{hash(question)}"):
                response = st.session_state.chatbot.process_query(question)
                st.session_state.messages.append({"role": "user", "content": question})
                st.session_state.messages.append({"role": "assistant", "content": response["answer"]})
                st.rerun()
    
    # Add Misi floating widget
    add_misi_to_page("bottom-right")

if __name__ == "__main__":
    main()
