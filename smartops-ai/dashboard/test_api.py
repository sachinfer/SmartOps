#!/usr/bin/env python3
"""
Test script to verify API endpoints are working correctly
"""

import requests
import json
import time

def test_api_endpoints():
    """Test all the API endpoints used by the Kubernetes Shell and Cluster Explorer"""
    
    base_url = "http://localhost:8000"
    
    print("🧪 Testing API endpoints...")
    print("=" * 50)
    
    # Test 1: Resource types
    print("\n1. Testing /kubectl_resource_types")
    try:
        resp = requests.get(f"{base_url}/kubectl_resource_types", timeout=5)
        print(f"   Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print(f"   Response: {data}")
        else:
            print(f"   Error: {resp.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Namespaces
    print("\n2. Testing /namespaces")
    try:
        resp = requests.get(f"{base_url}/namespaces", timeout=5)
        print(f"   Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print(f"   Response: {data}")
        else:
            print(f"   Error: {resp.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Kubectl get pods
    print("\n3. Testing /kubectl_get (pods)")
    try:
        params = {"resource_type": "pods", "all_namespaces": "false"}
        resp = requests.get(f"{base_url}/kubectl_get", params=params, timeout=10)
        print(f"   Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print(f"   Items found: {len(data.get('items', []))}")
        else:
            print(f"   Error: {resp.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: Kubectl raw command
    print("\n4. Testing /kubectl_raw (get pods)")
    try:
        params = {"command": "get pods"}
        resp = requests.post(f"{base_url}/kubectl_raw", params=params, timeout=10)
        print(f"   Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print(f"   Return code: {data.get('returncode')}")
            print(f"   Stdout length: {len(data.get('stdout', ''))}")
            if data.get('stderr'):
                print(f"   Stderr: {data.get('stderr')}")
        else:
            print(f"   Error: {resp.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 5: Health check (if available)
    print("\n5. Testing basic connectivity")
    try:
        resp = requests.get(f"{base_url}/", timeout=5)
        print(f"   Status: {resp.status_code}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ API testing completed!")

if __name__ == "__main__":
    test_api_endpoints()
