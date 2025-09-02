#!/usr/bin/env python3
"""
Startup script for SmartOps Dashboard
This script helps start both the FastAPI backend and Streamlit frontend
"""

import subprocess
import time
import requests
import sys
import os
from pathlib import Path

def check_port_available(port):
    """Check if a port is available"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) != 0

def wait_for_service(url, timeout=30):
    """Wait for a service to become available"""
    print(f"Waiting for {url} to become available...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                print(f"✅ {url} is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
    return False

def start_fastapi():
    """Start the FastAPI backend service"""
    print("🚀 Starting FastAPI backend service...")
    
    if not check_port_available(8000):
        print("❌ Port 8000 is already in use. Please stop the existing service first.")
        return False
    
    try:
        # Start FastAPI in background
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "event_api:app", 
            "--host", "0.0.0.0", "--port", "8000", "--reload"
        ], cwd=Path(__file__).parent)
        
        print(f"FastAPI process started with PID: {process.pid}")
        
        # Wait for service to be ready
        if wait_for_service("http://localhost:8000/"):
            return process
        else:
            print("❌ FastAPI service failed to start within timeout")
            process.terminate()
            return False
            
    except Exception as e:
        print(f"❌ Failed to start FastAPI: {e}")
        return False

def start_streamlit():
    """Start the Streamlit frontend service"""
    print("🎨 Starting Streamlit frontend service...")
    
    if not check_port_available(8501):
        print("❌ Port 8501 is already in use. Please stop the existing service first.")
        return False
    
    try:
        # Start Streamlit in background
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501", "--server.address", "0.0.0.0"
        ], cwd=Path(__file__).parent)
        
        print(f"Streamlit process started with PID: {process.pid}")
        
        # Wait for service to be ready
        if wait_for_service("http://localhost:8501/"):
            return process
        else:
            print("❌ Streamlit service failed to start within timeout")
            process.terminate()
            return False
            
    except Exception as e:
        print(f"❌ Failed to start Streamlit: {e}")
        return False

def main():
    """Main startup function"""
    print("🚀 SmartOps Dashboard Startup Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("event_api.py").exists() or not Path("streamlit_app.py").exists():
        print("❌ Please run this script from the dashboard directory")
        print("   Expected files: event_api.py, streamlit_app.py")
        sys.exit(1)
    
    # Check dependencies
    try:
        import fastapi
        import streamlit
        import kubernetes
        print("✅ All required dependencies are available")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("   Please run: pip install -r requirements.txt")
        sys.exit(1)
    
    # Start services
    fastapi_process = start_fastapi()
    if not fastapi_process:
        print("❌ Failed to start FastAPI backend")
        sys.exit(1)
    
    time.sleep(2)  # Give FastAPI a moment to fully initialize
    
    streamlit_process = start_streamlit()
    if not streamlit_process:
        print("❌ Failed to start Streamlit frontend")
        fastapi_process.terminate()
        sys.exit(1)
    
    print("\n🎉 All services started successfully!")
    print("=" * 50)
    print("📊 Dashboard: http://localhost:8501")
    print("🔌 API: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("\n💡 Press Ctrl+C to stop all services")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
            # Check if processes are still running
            if fastapi_process.poll() is not None:
                print("❌ FastAPI process stopped unexpectedly")
                break
            if streamlit_process.poll() is not None:
                print("❌ Streamlit process stopped unexpectedly")
                break
    except KeyboardInterrupt:
        print("\n🛑 Shutting down services...")
        fastapi_process.terminate()
        streamlit_process.terminate()
        print("✅ All services stopped")

if __name__ == "__main__":
    main()
