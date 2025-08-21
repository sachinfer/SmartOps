#!/usr/bin/env python3
"""
Test script to debug the kubectl API endpoint
Run this to test if the API is working correctly
"""

import requests
import json

def test_kubectl_api():
    """Test the kubectl_raw endpoint"""
    
    # Test the API health first
    try:
        health_response = requests.get("http://localhost:8000/", timeout=5)
        print(f"✅ API Health Check: {health_response.status_code}")
        if health_response.status_code == 200:
            print(f"   Response: {health_response.json()}")
    except Exception as e:
        print(f"❌ API Health Check Failed: {e}")
        return
    
    # Test kubectl get pods -n smartops
    print("\n🔍 Testing: kubectl get pods -n smartops")
    try:
        response = requests.post(
            "http://localhost:8000/kubectl_raw",
            params={"command": "get pods -n smartops"},
            timeout=30
        )
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Response Keys: {list(data.keys())}")
            print(f"   stdout length: {len(data.get('stdout', ''))}")
            print(f"   stderr length: {len(data.get('stderr', ''))}")
            print(f"   returncode: {data.get('returncode')}")
            
            if data.get('stdout'):
                print(f"   stdout content:\n{data['stdout']}")
            if data.get('stderr'):
                print(f"   stderr content:\n{data['stderr']}")
        else:
            print(f"   Error Response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Request Failed: {e}")
    
    # Test kubectl get pods -A
    print("\n🔍 Testing: kubectl get pods -A")
    try:
        response = requests.post(
            "http://localhost:8000/kubectl_raw",
            params={"command": "get pods -A"},
            timeout=30
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   stdout length: {len(data.get('stdout', ''))}")
            print(f"   stderr length: {len(data.get('stderr', ''))}")
            print(f"   returncode: {data.get('returncode')}")
            
            if data.get('stdout'):
                print(f"   stdout content:\n{data['stdout']}")
            if data.get('stderr'):
                print(f"   stderr content:\n{data['stderr']}")
        else:
            print(f"   Error Response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Request Failed: {e}")

if __name__ == "__main__":
    print("🚀 Testing SmartOps kubectl API...")
    test_kubectl_api()
    print("\n✨ Test completed!")
