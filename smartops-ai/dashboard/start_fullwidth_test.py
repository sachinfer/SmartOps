#!/usr/bin/env python3
"""
Full Width Layout Test Script
This script starts the dashboard with full-width layout fixes applied.
"""

import subprocess
import sys
import os
import time

def main():
    print("🚀 Starting SmartOps Dashboard with Full-Width Layout Fix...")
    print("=" * 60)
    
    # Change to dashboard directory
    dashboard_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(dashboard_dir)
    
    print(f"📁 Working directory: {dashboard_dir}")
    
    # Check if main.py exists
    if not os.path.exists("main.py"):
        print("❌ Error: main.py not found in dashboard directory")
        return 1
    
    print("✅ Found main.py")
    
    # Check if test_fullwidth_fix.py exists
    if not os.path.exists("test_fullwidth_fix.py"):
        print("❌ Error: test_fullwidth_fix.py not found")
        return 1
    
    print("✅ Found test_fullwidth_fix.py")
    
    # Start the dashboard
    print("\n🚀 Starting Streamlit dashboard...")
    print("📊 Dashboard will be available at: http://localhost:8501")
    print("🧪 Test page will be available at: http://localhost:8501/test_fullwidth_fix")
    print("\n💡 To test full-width layout:")
    print("   1. Open the dashboard in your browser")
    print("   2. Navigate to different pages")
    print("   3. Check that all content spans the full width")
    print("   4. Use the test page to verify layout fixes")
    print("\n🔄 Press Ctrl+C to stop the dashboard")
    print("=" * 60)
    
    try:
        # Start the main dashboard
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "main.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n\n🛑 Dashboard stopped by user")
        return 0
    except Exception as e:
        print(f"\n❌ Error starting dashboard: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
