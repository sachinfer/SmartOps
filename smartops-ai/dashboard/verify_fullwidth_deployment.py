#!/usr/bin/env python3
"""
Full-Width Deployment Verification Script
This script verifies that the full-width layout is working in the deployed environment.
"""

import requests
import time
import sys
import os
from datetime import datetime

def check_dashboard_health(dashboard_url, timeout=30):
    """Check if the dashboard is accessible and responding"""
    try:
        response = requests.get(f"{dashboard_url}/", timeout=timeout)
        if response.status_code == 200:
            print(f"✅ Dashboard is accessible at {dashboard_url}")
            return True
        else:
            print(f"⚠️ Dashboard returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Dashboard is not accessible: {e}")
        return False

def check_fullwidth_test_page(dashboard_url, timeout=30):
    """Check if the full-width test page is accessible"""
    try:
        response = requests.get(f"{dashboard_url}/test_fullwidth_fix", timeout=timeout)
        if response.status_code == 200:
            print(f"✅ Full-width test page is accessible at {dashboard_url}/test_fullwidth_fix")
            return True
        else:
            print(f"⚠️ Full-width test page returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Full-width test page is not accessible: {e}")
        return False

def check_css_inclusion(dashboard_url, timeout=30):
    """Check if the custom CSS is being served"""
    try:
        response = requests.get(f"{dashboard_url}/", timeout=timeout)
        if response.status_code == 200:
            content = response.text
            if "full-width" in content.lower() or "width: 100%" in content:
                print("✅ Full-width CSS appears to be included in the response")
                return True
            else:
                print("⚠️ Full-width CSS may not be properly included")
                return False
        else:
            print(f"⚠️ Could not check CSS inclusion - status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Could not check CSS inclusion: {e}")
        return False

def main():
    print("🔍 Full-Width Deployment Verification")
    print("=" * 50)
    
    # Get dashboard URL from environment or use default
    dashboard_url = os.getenv('DASHBOARD_URL', 'http://localhost:8501')
    
    print(f"📊 Checking dashboard at: {dashboard_url}")
    print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check dashboard health
    print("1. Checking dashboard health...")
    if not check_dashboard_health(dashboard_url):
        print("❌ Dashboard health check failed")
        return 1
    
    print()
    
    # Check full-width test page
    print("2. Checking full-width test page...")
    if not check_fullwidth_test_page(dashboard_url):
        print("❌ Full-width test page check failed")
        return 1
    
    print()
    
    # Check CSS inclusion
    print("3. Checking CSS inclusion...")
    if not check_css_inclusion(dashboard_url):
        print("❌ CSS inclusion check failed")
        return 1
    
    print()
    print("🎉 All checks passed! Full-width layout should be working in the deployed environment.")
    print()
    print("💡 To manually verify:")
    print(f"   1. Open {dashboard_url} in your browser")
    print(f"   2. Navigate to {dashboard_url}/test_fullwidth_fix")
    print("   3. Check that all elements span the full width of the screen")
    print("   4. Verify charts, tables, and forms use the full available space")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
