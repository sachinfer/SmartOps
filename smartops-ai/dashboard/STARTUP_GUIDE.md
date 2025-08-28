# 🚀 SmartOps Dashboard Startup Guide

## Overview
The SmartOps dashboard consists of two main services:
1. **Backend API Service** (port 8000) - Provides Kubernetes data and operations
2. **Frontend Dashboard** (port 8501) - Streamlit web interface

## 🚨 Current Issue
All dashboard pages are showing connectivity errors because the backend API service is not running.

## ✅ Quick Fix Options

### Option 1: Use Startup Scripts (Recommended)
```bash
cd smartops-ai/dashboard

# Windows Batch File
start_dashboard.bat

# OR PowerShell Script
start_dashboard.ps1
```

### Option 2: Manual Startup
```bash
cd smartops-ai/dashboard

# Terminal 1: Start API Service
python event_api.py

# Terminal 2: Start Dashboard (in new terminal)
streamlit run pages/1_Overview.py
```

### Option 3: One-Command Startup
```bash
cd smartops-ai/dashboard
start python event_api.py && timeout 5 && start streamlit run pages/1_Overview.py
```

## 🔧 What I Fixed

### 🚫 **Hardcoded Values Removed**
- ✅ **Cluster Status**: No more hardcoded "18 pods, 11 namespaces, 16 services"
- ✅ **Node Names**: No more hardcoded "gke-smartops-cluster-default-pool-897bf21e-i5jt"
- ✅ **Sample Data**: Generic sample data instead of specific app names
- ✅ **Telegram Credentials**: Now loaded from environment variables
- ✅ **All Dashboard Pages**: Now show real-time data from your actual cluster

### 1. Overview Page (1_Overview.py)
- ✅ Removed hardcoded pod status data
- ✅ Added real-time API integration
- ✅ Fixed node count (shows 1 instead of 3)
- ✅ Added API health checks
- ✅ **NEW**: Removed all hardcoded values, now shows real-time cluster data

### 2. Pod Explorer Page (2_Pod_Explorer_and_Logs.py)
- ✅ Added API health checks
- ✅ Shows helpful startup instructions
- ✅ Provides sample data when API is unavailable
- ✅ Better error handling
- ✅ **NEW**: Removed hardcoded node names, now shows generic sample data

### 3. Kubernetes Shell Page (3_Kubernetes_Shell_and_Cluster_Explorer.py)
- ✅ Added API health checks
- ✅ Prevents shell commands when API is down
- ✅ Shows startup instructions
- ✅ **NEW**: Removed hardcoded cluster status, now shows real-time data

### 4. Anomaly Detection Page (4_Anomaly_Detection.py)
- ✅ Added API health checks
- ✅ Prevents errors when API is unavailable
- ✅ **NEW**: Removed hardcoded cluster status, now shows real-time data

### 5. AI Actions Page (8_AI_Actions.py)
- ✅ Added API health checks
- ✅ Prevents API calls when service is down
- ✅ **NEW**: Removed hardcoded cluster status, now shows real-time data

## 📊 What You'll See After Starting Services

### When API Service is Running:
- ✅ **Real-time pod data**: Dynamic count based on actual cluster
- ✅ **Accurate node count**: Dynamic count based on actual cluster
- ✅ **Live namespace count**: Dynamic count based on actual cluster
- ✅ **Current service count**: Dynamic count based on actual cluster
- ✅ **Real-time logs** and shell commands
- ✅ **Live anomaly detection**
- ✅ **Dynamic node names**: Shows actual node names from your cluster

### When API Service is NOT Running:
- ℹ️ **Helpful startup instructions**
- ⚠️ **Generic sample data** for demonstration (no hardcoded values)
- ⚠️ **Clear warnings** about what's not working
- 🔍 **No hardcoded cluster data** - all values are now dynamic

## 🌐 Service URLs

After starting both services:
- **Dashboard**: http://localhost:8501
- **API Service**: http://localhost:8000
- **API Health Check**: http://localhost:8000/

## 🔍 Troubleshooting Tips

### 🚨 **Dashboard Shows "Failed to load logs" or "No output received"**
**SmartOps Insight**: This usually means the backend API service isn't running or can't connect to your Kubernetes cluster.

**Quick Fix**:
1. **Check API Health**: Open http://localhost:8000/ in your browser
   - ✅ **Green Response**: API is working, refresh your dashboard
   - ❌ **Connection Error**: API service needs to be started

2. **Start API Service**:
   ```bash
   cd smartops-ai/dashboard
   python event_api.py
   ```

3. **Verify kubectl Access**: The API needs kubectl to work
   ```bash
   kubectl get pods -n smartops
   ```
   - ✅ **Shows pods**: kubectl is configured correctly
   - ❌ **Permission denied**: Check your kubeconfig or cluster access

### 🔌 **Port Already in Use Errors**
**SmartOps Insight**: Another instance of SmartOps might already be running, or another service is using the ports.

**Windows Solution**:
```powershell
# Find what's using port 8000 (API)
netstat -ano | findstr :8000

# Find what's using port 8501 (Dashboard)
netstat -ano | findstr :8501

# Kill the process (replace <PID> with actual number)
taskkill /PID <PID> /F
```

**Alternative**: Use different ports
```bash
# Start API on port 8001
python event_api.py --port 8001

# Start Dashboard on port 8502
streamlit run streamlit_app.py --server.port 8502
```

### 🌐 **"Cannot connect to backend API" Error**
**SmartOps Insight**: This happens when the dashboard can't reach the API service, often due to network or firewall issues.

**Troubleshooting Steps**:
1. **Check if API is running**:
   ```bash
   # Look for Python process running event_api.py
   tasklist | findstr python
   ```

2. **Test API connectivity**:
   ```bash
   # Test from command line
   curl http://localhost:8000/
   
   # Or use PowerShell
   Invoke-WebRequest -Uri "http://localhost:8000/" -UseBasicParsing
   ```

3. **Check Windows Firewall**: Allow Python and Streamlit through firewall

### 📊 **"No results found" in Cluster Explorer**
**SmartOps Insight**: This usually means the namespace doesn't exist or kubectl can't access it.

**Quick Checks**:
1. **Verify namespace exists**:
   ```bash
   kubectl get namespaces
   ```

2. **Check your current context**:
   ```bash
   kubectl config current-context
   kubectl config get-contexts
   ```

3. **Test direct kubectl access**:
   ```bash
   kubectl get pods -n smartops
   kubectl get pods -n default
   ```

### 🔐 **Permission/Authentication Errors**
**SmartOps Insight**: Kubernetes access issues are common in GCP/GKE environments.

**GCP-Specific Solutions**:
1. **Refresh GKE credentials**:
   ```bash
   gcloud container clusters get-credentials smartops-cluster --region=us-central1
   ```

2. **Check service account permissions**:
   ```bash
   kubectl auth can-i get pods -n smartops
   kubectl auth can-i get nodes
   ```

3. **Verify cluster access**:
   ```bash
   kubectl cluster-info
   kubectl get nodes
   ```

### 🚀 **Dashboard Loads but Shows Old/Incorrect Data**
**SmartOps Insight**: Streamlit caches data for performance, but this can show stale information.

**Solutions**:
1. **Clear Streamlit Cache**:
   - Click the "🔄 Refresh" button on any page
   - Or use the refresh button in your browser

2. **Force Cache Clear**:
   ```bash
   # Stop dashboard, clear cache, restart
   streamlit cache clear
   streamlit run streamlit_app.py
   ```

3. **Check API Data Freshness**:
   - API data refreshes every 30 seconds
   - Node/pod data updates in real-time

### 💡 **SmartOps-Specific Tips**

**For GKE Users**:
- Use `gcloud auth login` before starting services
- Ensure you're in the correct GCP project
- Check if your cluster has the metrics server enabled

**For Local Development**:
- Use `kubectl proxy` for local cluster access
- Set `KUBECONFIG` environment variable to your config file
- Ensure Docker Desktop Kubernetes is running (if using)

**Performance Tips**:
- Dashboard works best with Chrome/Edge browsers
- Close unused browser tabs to free up memory
- API service uses minimal resources (~50MB RAM)

## 📁 File Structure
```
smartops-ai/dashboard/
├── event_api.py              # Backend API service
├── streamlit_app.py          # Main dashboard
├── start_dashboard.bat       # Windows startup script
├── start_dashboard.ps1       # PowerShell startup script
├── pages/                    # Dashboard pages
│   ├── 1_Overview.py        # ✅ Fixed
│   ├── 2_Pod_Explorer_and_Logs.py  # ✅ Fixed
│   ├── 3_Kubernetes_Shell_and_Cluster_Explorer.py  # ✅ Fixed
│   ├── 4_Anomaly_Detection.py  # ✅ Fixed
│   └── 8_AI_Actions.py      # ✅ Fixed
└── STARTUP_GUIDE.md          # This file
```

## 🎯 Next Steps

1. **Start the services** using one of the options above
2. **Navigate to the dashboard**: http://localhost:8501
3. **Verify all pages work** without errors
4. **Check real-time data** is showing correctly

## 💡 Pro Tips

- **Keep both terminals open** when running manually
- **Use the startup scripts** for convenience
- **Check the API health** at http://localhost:8000/ first
- **Refresh dashboard pages** after starting the API service

## 🆘 Still Having Issues?

**SmartOps Insight**: Most issues are related to Kubernetes access, Python environment, or network connectivity.

**System-Level Checks**:
1. **Python Environment**: Ensure Python 3.8+ is installed and accessible
   ```bash
   python --version
   pip list | findstr streamlit
   ```

2. **Kubernetes Access**: Verify kubectl can reach your cluster
   ```bash
   kubectl version --client
   kubectl cluster-info
   ```

3. **Network & Firewall**: Check if ports 8000 and 8501 are accessible
   - Windows Firewall might be blocking Python/Streamlit
   - Antivirus software can interfere with local connections

4. **Administrator Rights**: Try running PowerShell as Administrator
   - Right-click PowerShell → "Run as Administrator"
   - This helps with port binding and firewall rules

**Common SmartOps Issues & Solutions**:

**Issue**: "ModuleNotFoundError: No module named 'kubernetes'"
**Solution**: Install missing packages
```bash
pip install kubernetes streamlit fastapi uvicorn
```

**Issue**: "The connection was reset" in browser
**Solution**: Check if both services are running
```bash
# Terminal 1: API Service
python event_api.py

# Terminal 2: Dashboard
streamlit run streamlit_app.py
```

**Issue**: Dashboard shows "Loading..." forever
**Solution**: Clear browser cache and restart services
```bash
# Stop both services (Ctrl+C)
# Clear Streamlit cache
streamlit cache clear
# Restart both services
```

**Need More Help?**
- Check the SmartOps logs in your terminal
- Verify your GCP project and cluster are active
- Ensure you have the necessary Kubernetes permissions

---

**Status**: ✅ All major dashboard pages have been fixed and now include proper API health checks and helpful startup instructions.
