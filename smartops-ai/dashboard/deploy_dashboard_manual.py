#!/usr/bin/env python3
"""
Manual Dashboard Deployment Script for Free Tier GCP
This script can be run when resources are available
"""

import subprocess
import time
import sys

def run_command(cmd):
    """Run a command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_cluster_resources():
    """Check if cluster has enough resources"""
    print("🔍 Checking cluster resources...")
    
    # Get node resources
    success, stdout, stderr = run_command("kubectl describe nodes | grep -A 10 'Allocatable:'")
    if success:
        print("✅ Cluster resources:")
        print(stdout)
        return True
    else:
        print(f"❌ Error checking resources: {stderr}")
        return False

def delete_old_pods():
    """Delete old dashboard pods to free up resources"""
    print("🗑️ Deleting old dashboard pods...")
    
    # Get all dashboard pods
    success, stdout, stderr = run_command("kubectl get pods -n smartops -l app=smartops-dashboard -o name")
    if success and stdout.strip():
        pod_names = stdout.strip().split('\n')
        for pod_name in pod_names:
            print(f"Deleting {pod_name}...")
            run_command(f"kubectl delete {pod_name} -n smartops")
        print("✅ Old pods deleted")
    else:
        print("ℹ️ No old dashboard pods found")

def deploy_dashboard():
    """Deploy the dashboard with minimal resources"""
    print("🚀 Deploying dashboard...")
    
    # Apply the deployment
    success, stdout, stderr = run_command("kubectl apply -f k8s/smartops-dashboard-deployment.yaml")
    if success:
        print("✅ Deployment applied")
        return True
    else:
        print(f"❌ Error applying deployment: {stderr}")
        return False

def wait_for_pod_ready():
    """Wait for the pod to be ready"""
    print("⏳ Waiting for pod to be ready...")
    
    max_attempts = 30
    for attempt in range(max_attempts):
        success, stdout, stderr = run_command("kubectl get pods -n smartops -l app=smartops-dashboard --field-selector=status.phase=Running")
        if success and stdout.strip():
            print("✅ Dashboard pod is running!")
            return True
        
        print(f"Attempt {attempt + 1}/{max_attempts} - Pod not ready yet...")
        time.sleep(10)
    
    print("❌ Pod failed to become ready")
    return False

def main():
    """Main deployment function"""
    print("🚀 SmartOps Dashboard Manual Deployment")
    print("=" * 50)
    
    # Check resources
    if not check_cluster_resources():
        print("❌ Cannot check cluster resources")
        return False
    
    # Delete old pods
    delete_old_pods()
    
    # Wait a bit for cleanup
    print("⏳ Waiting for cleanup...")
    time.sleep(5)
    
    # Deploy dashboard
    if not deploy_dashboard():
        return False
    
    # Wait for pod to be ready
    if not wait_for_pod_ready():
        return False
    
    print("🎉 Dashboard deployed successfully!")
    print("🌐 Access your dashboard at the LoadBalancer IP")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
