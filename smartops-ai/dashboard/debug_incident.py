#!/usr/bin/env python3
"""
Debug Incident Timeline Page Loading
This script helps identify why the Incident Timeline page shows a black screen
"""

import streamlit as st
import sys
import os
import importlib.util

def debug_incident_page():
    """Debug the Incident Timeline page loading"""
    
    st.title("🔍 Debug: Incident Timeline Page")
    st.markdown("---")
    
    # Test 1: Check if the page file exists
    page_path = os.path.join(os.path.dirname(__file__), "pages", "6_Incident_Timeline_and_Postmortem_Report_Generator.py")
    st.subheader("📁 File Check")
    
    if os.path.exists(page_path):
        st.success(f"✅ Page file exists: {page_path}")
        st.info(f"File size: {os.path.getsize(page_path)} bytes")
    else:
        st.error(f"❌ Page file not found: {page_path}")
        return
    
    # Test 2: Try to import the page
    st.subheader("📦 Import Test")
    try:
        spec = importlib.util.spec_from_file_location("incident_page", page_path)
        st.success("✅ Module spec created")
        
        page_module = importlib.util.module_from_spec(spec)
        st.success("✅ Module object created")
        
        # Execute the module
        spec.loader.exec_module(page_module)
        st.success("✅ Module executed successfully")
        
        # Check if show_page function exists
        if hasattr(page_module, 'show_page'):
            st.success("✅ show_page function found")
            
            # Test 3: Try to call show_page
            st.subheader("🚀 Function Execution Test")
            try:
                st.info("🔄 Attempting to call show_page()...")
                page_module.show_page()
                st.success("✅ show_page() executed successfully!")
                
            except Exception as func_error:
                st.error(f"❌ Error calling show_page(): {func_error}")
                st.code(str(func_error), language="python")
                
                # Show the full traceback
                import traceback
                st.subheader("📋 Full Error Traceback")
                st.code(traceback.format_exc(), language="python")
                
        else:
            st.error("❌ show_page function not found")
            st.info("Available functions:")
            for attr in dir(page_module):
                if not attr.startswith('_'):
                    st.write(f"• {attr}")
                    
    except Exception as import_error:
        st.error(f"❌ Error importing page: {import_error}")
        st.code(str(import_error), language="python")
        
        # Show the full traceback
        import traceback
        st.subheader("📋 Full Import Error Traceback")
        st.code(traceback.format_exc(), language="python")
    
    # Test 4: Check dependencies
    st.subheader("🔧 Dependency Check")
    try:
        import pandas as pd
        st.success("✅ pandas imported successfully")
    except ImportError as e:
        st.error(f"❌ pandas import failed: {e}")
    
    try:
        import requests
        st.success("✅ requests imported successfully")
    except ImportError as e:
        st.error(f"❌ requests import failed: {e}")
    
    try:
        from datetime import datetime
        st.success("✅ datetime imported successfully")
    except ImportError as e:
        st.error(f"❌ datetime import failed: {e}")
    
    # Test 5: Check Streamlit context
    st.subheader("🌐 Streamlit Context")
    st.info(f"Streamlit version: {st.__version__}")
    st.info(f"Current working directory: {os.getcwd()}")
    st.info(f"Python version: {sys.version}")
    
    # Test 6: Try to create a simple page function
    st.subheader("🧪 Simple Page Test")
    try:
        def simple_test_page():
            st.title("🧪 Test Page")
            st.write("This is a simple test page")
            st.success("✅ Test page working!")
        
        simple_test_page()
        st.success("✅ Simple page function works!")
        
    except Exception as e:
        st.error(f"❌ Simple page failed: {e}")

if __name__ == "__main__":
    debug_incident_page()
