#!/usr/bin/env python3
"""
Start Streamlit with full-width configuration
"""

import subprocess
import sys
import os

def start_streamlit():
    """Start Streamlit with full-width configuration"""
    
    # Set environment variables for full width
    env = os.environ.copy()
    env['STREAMLIT_SERVER_HEADLESS'] = 'true'
    env['STREAMLIT_SERVER_PORT'] = '8501'
    env['STREAMLIT_SERVER_ENABLE_CORS'] = 'false'
    env['STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION'] = 'false'
    env['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    env['STREAMLIT_THEME_PRIMARY_COLOR'] = '#667eea'
    env['STREAMLIT_THEME_BACKGROUND_COLOR'] = '#0e1117'
    env['STREAMLIT_THEME_SECONDARY_BACKGROUND_COLOR'] = '#1e2127'
    env['STREAMLIT_THEME_TEXT_COLOR'] = '#fafafa'
    env['STREAMLIT_THEME_FONT'] = 'sans serif'
    env['STREAMLIT_CLIENT_SHOW_ERROR_DETAILS'] = 'true'
    env['STREAMLIT_LAYOUT_WIDE_MODE'] = 'true'
    env['STREAMLIT_RUNNER_FAST_RERUNS'] = 'true'
    
    # Start Streamlit with custom configuration
    cmd = [
        sys.executable, '-m', 'streamlit', 'run', 'main.py',
        '--server.headless', 'true',
        '--server.port', '8501',
        '--server.enableCORS', 'false',
        '--server.enableXsrfProtection', 'false',
        '--browser.gatherUsageStats', 'false',
        '--theme.primaryColor', '#667eea',
        '--theme.backgroundColor', '#0e1117',
        '--theme.secondaryBackgroundColor', '#1e2127',
        '--theme.textColor', '#fafafa',
        '--theme.font', 'sans serif',
        '--client.showErrorDetails', 'true',
        '--layout.wideMode', 'true',
        '--runner.fastReruns', 'true'
    ]
    
    print("Starting Streamlit with full-width configuration...")
    print("Command:", ' '.join(cmd))
    
    try:
        subprocess.run(cmd, env=env, check=True)
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error starting Streamlit: {e}")

if __name__ == "__main__":
    start_streamlit()
