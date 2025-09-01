# -*- coding: utf-8 -*-
"""
SmartOps Dashboard - Main Application
Multi-page dashboard with full-width layout and dark theme
"""

import streamlit as st
import sys
import os
import importlib.util
from datetime import datetime

# Page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="SmartOps Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ULTRA-AGGRESSIVE full-width CSS and JavaScript
st.markdown("""
<style>
    /* ULTRA-AGGRESSIVE: Override ALL possible width constraints */
    * {
        max-width: none !important;
    }
    
    /* Force the entire app to full width */
    .stApp {
        max-width: 100vw !important;
        width: 100vw !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Override Streamlit's main container */
    .stApp > div {
        max-width: 100vw !important;
        width: 100vw !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Force the main content area */
    .main {
        max-width: 100vw !important;
        width: 100vw !important;
        margin: 0 !important;
        padding: 0 !important;
        flex: 1 !important;
    }
    
    /* Override ALL block containers */
    .block-container,
    .main .block-container,
    [data-testid="stAppViewContainer"],
    .stApp > div[data-testid="stAppViewContainer"] {
        max-width: 100vw !important;
        width: 100vw !important;
        margin: 0 !important;
        padding: 0.5rem !important;
        box-sizing: border-box !important;
    }
    
    /* Force all content elements to full width */
    .stMarkdown,
    .stDataFrame,
    .stMetric,
    .stColumns,
    .stTable,
    .stSelectbox,
    .stButton,
    .stTextInput,
    .stTextArea,
    .stNumberInput,
    .stSlider,
    .stCheckbox,
    .stRadio,
    .stMultiselect,
    .stDateInput,
    .stTimeInput,
    .stFileUploader,
    .stColorPicker,
    .stPlotlyChart,
    .stAltairChart,
    .stVegaLiteChart,
    .stPyplot,
    .stBokehChart,
    .stGraphvizChart,
    .stMap,
    .stImage,
    .stVideo,
    .stAudio,
    .stDownloadButton,
    .stProgress,
    .stSpinner,
    .stBalloons,
    .stSnow,
    .stError,
    .stWarning,
    .stInfo,
    .stSuccess,
    .stException,
    .stHelp,
    .stCode,
    .stJson,
    .stSidebar {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
    
    /* Force columns to use full width */
    .stColumns > div {
        width: 100% !important;
        max-width: 100% !important;
        flex: 1 !important;
    }
    
    /* Override any remaining container constraints */
    .stMarkdown > div,
    .stDataFrame > div,
    .stTable > div {
        width: 100% !important;
        max-width: 100% !important;
    }
    
    /* Force tables to full width */
    .stTable table {
        width: 100% !important;
        max-width: 100% !important;
    }
    
    /* Override Streamlit's internal CSS variables */
    :root {
        --main-width: 100vw !important;
        --max-width: 100vw !important;
        --content-width: 100vw !important;
        --sidebar-width: 20rem !important;
    }
    
    /* Hide any scrollbars that might appear */
    .stApp {
        overflow-x: hidden !important;
    }
    
    /* Ensure no horizontal scrolling */
    body {
        overflow-x: hidden !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Force the viewport to full width */
    html {
        width: 100vw !important;
        max-width: 100vw !important;
        margin: 0 !important;
        padding: 0 !important;
    }
</style>

<script>
    // ULTRA-AGGRESSIVE JavaScript to force full width
    function forceUltraFullWidth() {
        // Override ALL possible containers
        const allContainers = document.querySelectorAll('*');
        allContainers.forEach(element => {
            if (element.style) {
                // Force full width on all elements
                element.style.maxWidth = 'none';
                element.style.width = '100%';
                element.style.boxSizing = 'border-box';
            }
        });
        
        // Specifically target Streamlit containers
        const streamlitContainers = document.querySelectorAll(
            '.stApp, .main, .block-container, [data-testid="stAppViewContainer"], ' +
            '.stMarkdown, .stDataFrame, .stMetric, .stColumns, .stTable, ' +
            '.stSelectbox, .stButton, .stTextInput, .stTextArea, .stNumberInput, ' +
            '.stSlider, .stCheckbox, .stRadio, .stMultiselect, .stDateInput, ' +
            '.stTimeInput, .stFileUploader, .stColorPicker, .stPlotlyChart, ' +
            '.stAltairChart, .stVegaLiteChart, .stPyplot, .stBokehChart, ' +
            '.stGraphvizChart, .stMap, .stImage, .stVideo, .stAudio, ' +
            '.stDownloadButton, .stProgress, .stSpinner, .stBalloons, ' +
            '.stSnow, .stError, .stWarning, .stInfo, .stSuccess, ' +
            '.stException, .stHelp, .stCode, .stJson'
        );
        
        streamlitContainers.forEach(container => {
            container.style.maxWidth = '100vw';
            container.style.width = '100vw';
            container.style.margin = '0';
            container.style.padding = '0.5rem';
            container.style.boxSizing = 'border-box';
        });
        
        // Force the main app container
        const mainApp = document.querySelector('.stApp');
        if (mainApp) {
            mainApp.style.maxWidth = '100vw';
            mainApp.style.width = '100vw';
            mainApp.style.margin = '0';
            mainApp.style.padding = '0';
        }
        
        // Force the main content area
        const mainContent = document.querySelector('.main');
        if (mainContent) {
            mainContent.style.maxWidth = '100vw';
            mainContent.style.width = '100vw';
            mainContent.style.margin = '0';
            mainContent.style.padding = '0';
            mainContent.style.flex = '1';
        }
        
        // Force all block containers
        const blockContainers = document.querySelectorAll('.block-container');
        blockContainers.forEach(container => {
            container.style.maxWidth = '100vw';
            container.style.width = '100vw';
            container.style.margin = '0';
            container.style.padding = '0.5rem';
            container.style.boxSizing = 'border-box';
        });
        
        // Force all content elements
        const contentElements = document.querySelectorAll('.stMarkdown, .stDataFrame, .stMetric, .stColumns, .stTable');
        contentElements.forEach(element => {
            element.style.width = '100%';
            element.style.maxWidth = '100%';
            element.style.boxSizing = 'border-box';
        });
        
        // Force columns to use full width
        const columns = document.querySelectorAll('.stColumns > div');
        columns.forEach(column => {
            column.style.width = '100%';
            column.style.maxWidth = '100%';
            column.style.flex = '1';
        });
        
        // Force tables to full width
        const tables = document.querySelectorAll('.stTable table');
        tables.forEach(table => {
            table.style.width = '100%';
            table.style.maxWidth = '100%';
        });
        
        // Override any CSS variables
        document.documentElement.style.setProperty('--main-width', '100vw');
        document.documentElement.style.setProperty('--max-width', '100vw');
        document.documentElement.style.setProperty('--content-width', '100vw');
        
        // Force body and html to full width
        document.body.style.maxWidth = '100vw';
        document.body.style.width = '100vw';
        document.body.style.margin = '0';
        document.body.style.padding = '0';
        document.body.style.overflowX = 'hidden';
        
        document.documentElement.style.maxWidth = '100vw';
        document.documentElement.style.width = '100vw';
        document.documentElement.style.margin = '0';
        document.documentElement.style.padding = '0';
    }
    
    // Run immediately
    forceUltraFullWidth();
    
    // Run on page load
    document.addEventListener('DOMContentLoaded', forceUltraFullWidth);
    window.addEventListener('load', forceUltraFullWidth);
    
    // Run continuously to catch any dynamic content
    setInterval(forceUltraFullWidth, 100);
    
    // Run on any DOM changes
    const observer = new MutationObserver(forceUltraFullWidth);
    observer.observe(document.body, {
        childList: true,
        subtree: true,
        attributes: true,
        attributeFilter: ['style', 'class']
    });
    
    // Run on window resize
    window.addEventListener('resize', forceUltraFullWidth);
    
    // Run on any scroll events
    window.addEventListener('scroll', forceUltraFullWidth);
</script>
""", unsafe_allow_html=True)

# Custom CSS for dark theme and full-width
st.markdown("""
<style>
    /* Dark theme and full-width styling */
    .main {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    
    .header-title {
        color: white;
        font-size: 3rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
        text-shadow: 0 4px 15px rgba(0,0,0,0.4);
    }
    
    .header-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        font-weight: 400;
    }
    
    /* Metric cards */
    .metric-card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    /* Navigation cards */
    .nav-card {
        background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%);
        border: 1px solid rgba(102,126,234,0.3);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .nav-card:hover {
        background: linear-gradient(135deg, rgba(102,126,234,0.2) 0%, rgba(118,75,162,0.2) 100%);
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102,126,234,0.3);
    }
    
    /* Status indicators */
    .status-online {
        background: linear-gradient(135deg, #00d4aa 0%, #0099cc 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 600;
        text-align: center;
        display: inline-block;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Force full width - More aggressive overrides */
    .main .block-container {
        max-width: 100% !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
        width: 100% !important;
    }
    
    /* Override Streamlit's default max-width */
    .block-container {
        max-width: 100% !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        width: 100% !important;
    }
    
    /* Ensure the main content area uses full width */
    .main {
        width: 100% !important;
        max-width: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Override Streamlit's default container */
    .stApp > div:first-child {
        max-width: 100% !important;
        width: 100% !important;
    }
    
    /* Force all containers to full width */
    .stApp > div {
        max-width: 100% !important;
        width: 100% !important;
    }
    
    /* Override any remaining width constraints */
    [data-testid="stAppViewContainer"] {
        max-width: 100% !important;
        width: 100% !important;
    }
    
    /* Additional aggressive overrides */
    .stApp > div[data-testid="stAppViewContainer"] {
        max-width: 100% !important;
        width: 100% !important;
    }
    
    /* Override any CSS variables that might be setting width */
    :root {
        --main-width: 100% !important;
        --max-width: 100% !important;
    }
    
    /* Force all direct children to full width */
    .stApp > * {
        max-width: 100% !important;
        width: 100% !important;
    }
    
    /* Override any remaining container constraints */
    .stApp > div > div {
        max-width: 100% !important;
        width: 100% !important;
    }
    
    /* Ensure sidebar doesn't affect main content width */
    .main .block-container {
        margin-left: 0 !important;
        margin-right: 0 !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }
    
    /* Ensure all content uses full width */
    .stMarkdown, .stDataFrame, .stMetric, .stColumns {
        width: 100% !important;
        max-width: 100% !important;
    }
    
    /* Force columns to use full width */
    .stColumns > div {
        width: 100% !important;
        max-width: 100% !important;
    }
    
    /* Override any remaining width constraints */
    .stMarkdown > div {
        width: 100% !important;
        max-width: 100% !important;
    }
    
    /* Ensure metric cards use full width */
    .metric-card {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
    
    /* Force navigation cards to full width */
    .nav-card {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
    
    /* Better spacing for wide layout */
    .stMarkdown {
        margin-bottom: 1rem;
    }
    
    /* Consistent card styling */
    .stAlert {
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Better table styling */
    .stTable {
        width: 100% !important;
    }
    
    /* Ensure charts use full width */
    .stPlotlyChart, .stAltairChart, .stVegaLiteChart {
        width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

# Create the sidebar with navigation
def create_sidebar():
    """Create a comprehensive sidebar with navigation"""
    
    # Main title with branding
    st.sidebar.title("🚀 SmartOps Dashboard")
    st.sidebar.markdown("**by Misi 24x7**")
    st.sidebar.markdown("---")
    
    # Navigation sections
    st.sidebar.markdown("### 📊 **Core Monitoring**")
    st.sidebar.markdown("• **🟩 Overview** (Current)")
    st.sidebar.markdown("• 🧭 Pod Explorer & Logs")
    st.sidebar.markdown("• 🔍 Kubernetes Shell")
    st.sidebar.markdown("• 🔥 Anomaly Detection")
    
    st.sidebar.markdown("---")
    
    st.sidebar.markdown("### ⚡ **Operations**")
    st.sidebar.markdown("• ⚡ Auto Scaling Control")
    st.sidebar.markdown("• 📝 Incident Timeline")
    st.sidebar.markdown("• 🚀 Deployments")
    
    st.sidebar.markdown("---")
    
    st.sidebar.markdown("### 🤖 **AI & Analytics**")
    st.sidebar.markdown("• 🤖 AI Actions")
    st.sidebar.markdown("• 💬 Misi AI Assistant")
    
    st.sidebar.markdown("---")
    
    # Quick actions
    st.sidebar.markdown("### 🔄 **Quick Actions**")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("🔄 Refresh", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    with col2:
        if st.button("📊 Status", use_container_width=True):
            st.sidebar.success("✅ All systems operational")
    
    # Debug button for troubleshooting
    if st.button("🔍 Debug Pages", use_container_width=True):
        st.sidebar.info("🔍 Debug mode activated")
        st.info("Check the main area for debug information")
        
        # Show debug info
        st.subheader("🔍 Page Debug Information")
        
        # Check all page files
        pages_dir = os.path.join(os.path.dirname(__file__), "pages")
        if os.path.exists(pages_dir):
            st.success(f"✅ Pages directory found: {pages_dir}")
            
            page_files = [f for f in os.listdir(pages_dir) if f.endswith('.py')]
            st.info(f"📁 Found {len(page_files)} page files:")
            
            for page_file in sorted(page_files):
                page_path = os.path.join(pages_dir, page_file)
                try:
                    # Try to import each page
                    spec = importlib.util.spec_from_file_location(page_file[:-3], page_path)
                    page_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(page_module)
                    
                    if hasattr(page_module, 'show_page'):
                        st.success(f"✅ {page_file} - show_page() function found")
                    else:
                        st.warning(f"⚠️ {page_file} - No show_page() function")
                        
                except Exception as e:
                    st.error(f"❌ {page_file} - Import error: {str(e)[:100]}...")
        else:
            st.error(f"❌ Pages directory not found: {pages_dir}")
    
    # System status
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📈 **System Status**")
    st.sidebar.success("🟢 **Online**")
    
    # Environment info
    try:
        env = os.environ.get('KUBERNETES_SERVICE_HOST', 'local')
        if env != 'local':
            st.sidebar.info(f"🌍 **Environment:** {env.upper()}")
        else:
            st.sidebar.info("🌍 **Environment:** Local")
    except:
        st.sidebar.info("🌍 **Environment:** Unknown")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**SmartOps by Misi 24x7**")
    st.sidebar.markdown("*Enterprise Kubernetes Monitoring*")

# Import page functions
def import_page(page_name):
    """Import a specific page using importlib"""
    try:
        page_path = os.path.join(os.path.dirname(__file__), "pages", f"{page_name}.py")
        if os.path.exists(page_path):
            spec = importlib.util.spec_from_file_location(page_name, page_path)
            page_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(page_module)
            
            # Check if the page has a show_page function
            if hasattr(page_module, 'show_page'):
                # Create a wrapper that applies consistent styling and error handling
                def styled_page():
                    try:
                        # Apply ULTRA-AGGRESSIVE page-specific styling
                        st.markdown(f"""
                        <style>
                            /* ULTRA-AGGRESSIVE Page-specific full-width styling */
                            .stPage {{
                                background-color: #0e1117 !important;
                                color: #fafafa !important;
                                max-width: 100vw !important;
                                width: 100vw !important;
                            }}
                            
                            /* Force full width for this page - ULTRA-AGGRESSIVE */
                            .main .block-container {{
                                max-width: 100vw !important;
                                padding-left: 0.5rem !important;
                                padding-right: 0.5rem !important;
                                width: 100vw !important;
                                margin: 0 !important;
                                box-sizing: border-box !important;
                            }}
                            
                            /* Override ALL container constraints */
                            .block-container {{
                                max-width: 100vw !important;
                                width: 100vw !important;
                                padding: 0.5rem !important;
                                margin: 0 !important;
                                box-sizing: border-box !important;
                            }}
                            
                            /* Force ALL elements to full width */
                            .stMarkdown, .stDataFrame, .stMetric, .stColumns, .stTable,
                            .stSelectbox, .stButton, .stTextInput, .stTextArea, .stNumberInput,
                            .stSlider, .stCheckbox, .stRadio, .stMultiselect, .stDateInput,
                            .stTimeInput, .stFileUploader, .stColorPicker, .stPlotlyChart,
                            .stAltairChart, .stVegaLiteChart, .stPyplot, .stBokehChart,
                            .stGraphvizChart, .stMap, .stImage, .stVideo, .stAudio,
                            .stDownloadButton, .stProgress, .stSpinner, .stBalloons,
                            .stSnow, .stError, .stWarning, .stInfo, .stSuccess,
                            .stException, .stHelp, .stCode, .stJson {{
                                width: 100% !important;
                                max-width: 100% !important;
                                box-sizing: border-box !important;
                            }}
                            
                            /* Override Streamlit's default layout - ULTRA-AGGRESSIVE */
                            [data-testid="stAppViewContainer"] {{
                                max-width: 100vw !important;
                                width: 100vw !important;
                                margin: 0 !important;
                                padding: 0 !important;
                            }}
                            
                            /* Force the main app container */
                            .stApp {{
                                max-width: 100vw !important;
                                width: 100vw !important;
                                margin: 0 !important;
                                padding: 0 !important;
                            }}
                            
                            /* Force the main content area */
                            .main {{
                                max-width: 100vw !important;
                                width: 100vw !important;
                                margin: 0 !important;
                                padding: 0 !important;
                                flex: 1 !important;
                            }}
                            
                            /* Force columns to use full width */
                            .stColumns > div {{
                                width: 100% !important;
                                max-width: 100% !important;
                                flex: 1 !important;
                                box-sizing: border-box !important;
                            }}
                            
                            /* Force tables to full width */
                            .stTable table {{
                                width: 100% !important;
                                max-width: 100% !important;
                            }}
                            
                            /* Override CSS variables */
                            :root {{
                                --main-width: 100vw !important;
                                --max-width: 100vw !important;
                                --content-width: 100vw !important;
                            }}
                            
                            /* Better spacing */
                            .stMarkdown {{
                                margin-bottom: 1rem;
                            }}
                            
                            /* Ensure no horizontal scrolling */
                            body {{
                                overflow-x: hidden !important;
                                margin: 0 !important;
                                padding: 0 !important;
                            }}
                            
                            html {{
                                width: 100vw !important;
                                max-width: 100vw !important;
                                margin: 0 !important;
                                padding: 0 !important;
                            }}
                        </style>
                        
                        <script>
                            // ULTRA-AGGRESSIVE JavaScript for this specific page
                            function forcePageFullWidth() {{
                                // Override ALL possible containers on this page
                                const allElements = document.querySelectorAll('*');
                                allElements.forEach(element => {{
                                    if (element.style) {{
                                        element.style.maxWidth = 'none';
                                        element.style.width = '100%';
                                        element.style.boxSizing = 'border-box';
                                    }}
                                }});
                                
                                // Force Streamlit containers
                                const streamlitElements = document.querySelectorAll(
                                    '.stApp, .main, .block-container, [data-testid="stAppViewContainer"], ' +
                                    '.stMarkdown, .stDataFrame, .stMetric, .stColumns, .stTable, ' +
                                    '.stSelectbox, .stButton, .stTextInput, .stTextArea, .stNumberInput, ' +
                                    '.stSlider, .stCheckbox, .stRadio, .stMultiselect, .stDateInput, ' +
                                    '.stTimeInput, .stFileUploader, .stColorPicker, .stPlotlyChart, ' +
                                    '.stAltairChart, .stVegaLiteChart, .stPyplot, .stBokehChart, ' +
                                    '.stGraphvizChart, .stMap, .stImage, .stVideo, .stAudio, ' +
                                    '.stDownloadButton, .stProgress, .stSpinner, .stBalloons, ' +
                                    '.stSnow, .stError, .stWarning, .stInfo, .stSuccess, ' +
                                    '.stException, .stHelp, .stCode, .stJson'
                                );
                                
                                streamlitElements.forEach(element => {{
                                    element.style.maxWidth = '100vw';
                                    element.style.width = '100vw';
                                    element.style.margin = '0';
                                    element.style.padding = '0.5rem';
                                    element.style.boxSizing = 'border-box';
                                }});
                                
                                // Force CSS variables
                                document.documentElement.style.setProperty('--main-width', '100vw');
                                document.documentElement.style.setProperty('--max-width', '100vw');
                                document.documentElement.style.setProperty('--content-width', '100vw');
                            }}
                            
                            // Run immediately and continuously
                            forcePageFullWidth();
                            setInterval(forcePageFullWidth, 50);
                        </script>
                        """, unsafe_allow_html=True)
                        
                        # Call the original page function with error handling
                        page_module.show_page()
                        
                    except Exception as page_error:
                        st.error(f"Error displaying page {page_name}: {page_error}")
                        st.info("Showing fallback content...")
                        
                        # Show fallback content
                        st.title(f"📄 {page_name.replace('_', ' ').title()}")
                        st.markdown("---")
                        st.warning("⚠️ There was an error loading this page. Please check the console for details.")
                        
                        # Try to show basic page info
                        try:
                            if hasattr(page_module, '__doc__') and page_module.__doc__:
                                st.markdown(f"**Description:** {page_module.__doc__}")
                        except:
                            pass
                        
                        st.info("🔧 **Troubleshooting:** Check if all required dependencies are installed and the page file is accessible.")
                
                return styled_page
            else:
                # If no show_page function, create a simple one with styling
                def simple_page():
                    st.markdown(f"""
                    <style>
                        .stPage {{
                            background-color: #0e1117 !important;
                            color: #fafafa !important;
                        }}
                        .main .block-container {{
                            max-width: 100% !important;
                        }}
                    </style>
                    """, unsafe_allow_html=True)
                    st.title(f"{page_name.replace('_', ' ').title()}")
                    st.write(f"Content for {page_name}")
                    st.warning("⚠️ This page doesn't have a show_page() function defined.")
                return simple_page
        else:
            return None
    except Exception as e:
        st.error(f"Error importing {page_name}: {e}")
        st.info("This usually means there's a syntax error or missing dependency in the page file.")
        return None

# Main dashboard content
def show_main_dashboard():
    """Show the main dashboard overview"""
    
    # Header
    st.markdown("""
    <div class="header-container">
        <div class="header-title">🚀 SmartOps Dashboard</div>
        <div class="header-subtitle">Enterprise Kubernetes Monitoring by Misi 24x7</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Active Pods</h3>
            <h2 style="color: #00d4aa; font-size: 2.5rem;">24</h2>
            <p style="color: #00d4aa;">+2 from yesterday</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>⚡ CPU Usage</h3>
            <h2 style="color: #ff6b6b; font-size: 2.5rem;">68%</h2>
            <p style="color: #ff6b6b;">-5% from yesterday</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>💾 Memory Usage</h3>
            <h2 style="color: #4ecdc4; font-size: 2.5rem;">72%</h2>
            <p style="color: #4ecdc4;">+3% from yesterday</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>🔗 Services</h3>
            <h2 style="color: #45b7d1; font-size: 2.5rem;">12</h2>
            <p style="color: #45b7d1;">All healthy</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Access Section
    st.subheader("🚀 Quick Access to Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="nav-card">
            <h3>📊 Monitoring & Analytics</h3>
            <p>• <strong>Pod Explorer & Logs</strong> - Explore pods and view logs</p>
            <p>• <strong>Kubernetes Shell</strong> - Interactive cluster exploration</p>
            <p>• <strong>Anomaly Detection</strong> - AI-powered anomaly detection</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="nav-card">
            <h3>⚡ Operations & Control</h3>
            <p>• <strong>Auto Scaling Control</strong> - Manage HPA and scaling</p>
            <p>• <strong>Incident Timeline</strong> - Track incidents and generate reports</p>
            <p>• <strong>Deployments</strong> - Monitor deployment status</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # System Status
    st.subheader("🔍 System Status")
    
    status_col1, status_col2 = st.columns(2)
    
    with status_col1:
        st.markdown("""
        <div class="metric-card">
            <h3>System Health</h3>
            <div class="status-online">🟢 OPERATIONAL</div>
            <p>All systems are running normally</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("🌍 **Environment:** Local Development")
        st.warning("⚠️ **Alerts:** 2 active (low priority)")
    
    with status_col2:
        st.markdown("""
        <div class="metric-card">
            <h3>Cluster Status</h3>
            <p><strong>Pods Running:</strong> 24/25</p>
            <p><strong>Services:</strong> 12/12</p>
            <p><strong>Deployments:</strong> 8/8</p>
            <p><strong>Nodes:</strong> 3/3</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("*SmartOps Dashboard - Powered by Misi 24x7*")

# Page routing
def main():
    """Main application with page routing"""
    
    # Create sidebar
    create_sidebar()
    
    # Page selection
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🧭 **Page Navigation**")
    
    # Get current page from query params or default to main
    try:
        query_params = st.experimental_get_query_params()
        current_page = query_params.get("page", ["main"])[0]
    except:
        current_page = "main"
    
    # Page selection buttons
    if st.sidebar.button("🏠 Main Dashboard", use_container_width=True):
        current_page = "main"
        st.experimental_set_query_params(page="main")
    
    if st.sidebar.button("📊 Overview", use_container_width=True):
        current_page = "1_Overview"
        try:
            st.experimental_set_query_params(page="1_Overview")
        except:
            pass
    
    if st.sidebar.button("🧭 Pod Explorer", use_container_width=True):
        current_page = "2_Pod_Explorer_and_Logs"
        try:
            st.experimental_set_query_params(page="2_Pod_Explorer_and_Logs")
        except:
            pass
    
    if st.sidebar.button("🔍 K8s Shell", use_container_width=True):
        current_page = "3_Kubernetes_Shell_and_Cluster_Explorer"
        try:
            st.experimental_set_query_params(page="3_Kubernetes_Shell_and_Cluster_Explorer")
        except:
            pass
    
    if st.sidebar.button("🔥 Anomaly Detection", use_container_width=True):
        current_page = "4_Anomaly_Detection"
        try:
            st.experimental_set_query_params(page="4_Anomaly_Detection")
        except:
            pass
    
    if st.sidebar.button("⚡ Auto Scaling", use_container_width=True):
        current_page = "5_Auto_Scaling_Recommendations_and_Control"
        try:
            st.experimental_set_query_params(page="5_Auto_Scaling_Recommendations_and_Control")
        except:
            pass
    
    if st.sidebar.button("📝 Incident Timeline", use_container_width=True):
        current_page = "6_Incident_Timeline_and_Postmortem_Report_Generator"
        try:
            st.experimental_set_query_params(page="6_Incident_Timeline_and_Postmortem_Report_Generator")
        except:
            pass
    
    if st.sidebar.button("💬 AI Assistant", use_container_width=True):
        current_page = "7_Misi_AI_Assistant"
        try:
            st.experimental_set_query_params(page="7_Misi_AI_Assistant")
        except:
            pass
    
    if st.sidebar.button("🤖 AI Actions", use_container_width=True):
        current_page = "8_AI_Actions"
        try:
            st.experimental_set_query_params(page="8_AI_Actions")
        except:
            pass
    
    if st.sidebar.button("🚀 Deployments", use_container_width=True):
        current_page = "9_Deployments"
        try:
            st.experimental_set_query_params(page="9_Deployments")
        except:
            pass
    
    # Display current page
    if current_page == "main":
        show_main_dashboard()
    else:
        # Try to import and show the selected page
        st.sidebar.info(f"🔄 Loading page: {current_page}")
        
        try:
            page_function = import_page(current_page)
            if page_function:
                st.sidebar.success(f"✅ Page loaded: {current_page}")
                page_function()
            else:
                st.error(f"❌ Page {current_page} not found or has errors")
                st.info("Falling back to main dashboard")
                show_main_dashboard()
        except Exception as e:
            st.error(f"❌ Error loading page {current_page}: {e}")
            st.info("Falling back to main dashboard")
            show_main_dashboard()

# Run the main application
if __name__ == "__main__":
    main()
