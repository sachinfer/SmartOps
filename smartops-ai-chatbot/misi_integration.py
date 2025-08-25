"""
Misi AI Chatbot Integration for SmartOps
Simple one-line integration to add Misi to any page
"""

import streamlit as st
from misi_chatbot_widget import MisiChatbotWidget

def add_misi_to_page(position="bottom-right"):
    """
    Add Misi AI chatbot to any page with one line of code
    
    Args:
        position (str): Position of the Misi icon
            - "bottom-right" (default)
            - "top-right"
            - "bottom-left"
            - "top-left"
    
    Usage:
        # In any page, just add this line:
        add_misi_to_page()
        
        # Or specify position:
        add_misi_to_page("top-right")
    """
    
    # Initialize Misi widget
    misi = MisiChatbotWidget()
    
    # Render Misi integration
    misi.render_misi_integration(position)
    
    return misi

def add_misi_to_sidebar():
    """
    Add Misi AI chatbot to the sidebar
    
    Usage:
        # In sidebar:
        with st.sidebar:
            add_misi_to_sidebar()
    """
    
    st.markdown("## 🤖 Ask Misi")
    
    # Initialize Misi widget
    misi = MisiChatbotWidget()
    
    # Simple chat interface for sidebar
    user_input = st.text_input("Ask Misi anything about SmartOps...", key="misi_sidebar_input")
    
    if user_input:
        response = misi.chatbot.process_query(user_input)
        
        # Display response
        st.info(response["answer"])
        
        # Show navigation guide if available
        if response.get("navigation_guide"):
            nav = response["navigation_guide"]
            st.success(f"🧭 Navigate to: Page {nav['page_number']} - {nav['page_name']}")
            
            # Navigation button
            if st.button(f"Go to {nav['page_name']}"):
                st.session_state.current_page = nav['page_number']
                st.rerun()
        
        # Show suggested questions
        if response.get("suggested_questions"):
            st.markdown("**💡 Suggested Questions:**")
            for question in response["suggested_questions"][:2]:
                if st.button(question, key=f"misi_suggest_{hash(question)}"):
                    # Process suggested question
                    suggested_response = misi.chatbot.process_query(question)
                    st.info(suggested_response["answer"])
                    st.rerun()

def add_misi_quick_help():
    """
    Add a quick help section with Misi suggestions
    
    Usage:
        # Add quick help section:
        add_misi_quick_help()
    """
    
    st.markdown("### 🤖 Quick Help with Misi")
    
    # Common questions
    common_questions = [
        "How can I check pod status?",
        "What is anomaly detection?",
        "How do I access the Kubernetes shell?",
        "Tell me about auto-scaling"
    ]
    
    for question in common_questions:
        if st.button(question, key=f"misi_quick_{hash(question)}"):
            # Initialize Misi and get response
            misi = MisiChatbotWidget()
            response = misi.chatbot.process_query(question)
            
            # Display response
            st.info(response["answer"])
            
            # Show navigation if available
            if response.get("navigation_guide"):
                nav = response["navigation_guide"]
                st.success(f"🧭 Navigate to: Page {nav['page_number']} - {nav['page_name']}")
            
            st.rerun()

# Convenience functions for different positions
def add_misi_top_right():
    """Add Misi to top-right corner"""
    return add_misi_to_page("top-right")

def add_misi_bottom_left():
    """Add Misi to bottom-left corner"""
    return add_misi_to_page("bottom-left")

def add_misi_top_left():
    """Add Misi to top-left corner"""
    return add_misi_to_page("top-left")

def add_misi_bottom_right():
    """Add Misi to bottom-right corner (default)"""
    return add_misi_to_page("bottom-right")

# Example usage in comments:
"""
# ===========================================
# HOW TO USE MISI IN YOUR SMARTops PAGES
# ===========================================

# 1. Import Misi in your page:
from smartops_ai_chatbot.misi_integration import add_misi_to_page

# 2. Add Misi to your page (anywhere in your code):
add_misi_to_page()  # Default: bottom-right corner

# 3. Or specify position:
add_misi_to_page("top-right")
add_misi_to_page("bottom-left")
add_misi_to_page("top-left")

# 4. For sidebar integration:
from smartops_ai_chatbot.misi_integration import add_misi_to_sidebar

with st.sidebar:
    add_misi_to_sidebar()

# 5. For quick help section:
from smartops_ai_chatbot.misi_integration import add_misi_quick_help

add_misi_quick_help()

# ===========================================
# COMPLETE EXAMPLE PAGE
# ===========================================

import streamlit as st
from smartops_ai_chatbot.misi_integration import add_misi_to_page

st.title("My SmartOps Page")

# Your page content here
st.write("This is my page content...")

# Add Misi to the page (this will show the floating icon)
add_misi_to_page()

# ===========================================
"""
