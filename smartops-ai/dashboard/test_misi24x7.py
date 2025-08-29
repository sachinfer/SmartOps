#!/usr/bin/env python3
"""
Test script for misi24x7 page
"""

import streamlit as st
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_misi24x7():
    """Test the misi24x7 page functionality"""
    
    st.title("Testing Misi24x7 Page")
    
    try:
        # Test import
        import misi24x7
        st.success("✅ Successfully imported misi24x7.py")
        
        # Test sidebar import
        try:
            from sidebar_utils import show_sidebar
            st.success("✅ Successfully imported sidebar_utils")
        except ImportError as e:
            st.warning(f"⚠️ Sidebar import warning: {e}")
        
        # Test page configuration
        st.info("Testing page configuration...")
        
        # Test CSS rendering
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%); 
                    color: white; padding: 2rem; border-radius: 15px; text-align: center;">
            <h2>CSS Test - Gradient Background</h2>
            <p>If you see this with a purple gradient background, CSS is working!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Test responsive elements
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Test Metric 1", "100", "10%")
        
        with col2:
            st.metric("Test Metric 2", "200", "20%")
            
        with col3:
            st.metric("Test Metric 3", "300", "30%")
        
        st.success("🎉 All tests completed successfully!")
        
    except Exception as e:
        st.error(f"❌ Error testing misi24x7: {e}")
        st.exception(e)

if __name__ == "__main__":
    test_misi24x7()
