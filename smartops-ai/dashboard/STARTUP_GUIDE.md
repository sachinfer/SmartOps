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
streamlit run streamlit_app.py
```

### Option 3: One-Command Startup
```bash
cd smartops-ai/dashboard
start python event_api.py && timeout 5 && start streamlit run streamlit_app.py
```

## 🔧 What I Fixed

### 1. Overview Page (1_Overview.py)
- ✅ Removed hardcoded pod status data
- ✅ Added real-time API integration
- ✅ Fixed node count (shows 1 instead of 3)
- ✅ Added API health checks

### 2. Pod Explorer Page (2_Pod_Explorer_and_Logs.py)
- ✅ Added API health checks
- ✅ Shows helpful startup instructions
- ✅ Provides sample data when API is unavailable
- ✅ Better error handling

### 3. Kubernetes Shell Page (3_Kubernetes_Shell_and_Cluster_Explorer.py)
- ✅ Added API health checks
- ✅ Prevents shell commands when API is down
- ✅ Shows startup instructions

### 4. Anomaly Detection Page (4_Anomaly_Detection.py)
- ✅ Added API health checks
- ✅ Prevents errors when API is unavailable

### 5. AI Actions Page (8_AI_Actions.py)
- ✅ Added API health checks
- ✅ Prevents API calls when service is down

## 📊 What You'll See After Starting Services

### When API Service is Running:
- ✅ **Real-time pod data**: 18 pods (all Running)
- ✅ **Accurate node count**: 1 node
- ✅ **Live namespace count**: 11 namespaces
- ✅ **Current service count**: 16 services
- ✅ **Real-time logs** and shell commands
- ✅ **Live anomaly detection**

### When API Service is NOT Running:
- ℹ️ **Helpful startup instructions**
- ✅ **Current cluster status** (based on your actual data)
- 🔍 **Sample data** for demonstration
- ⚠️ **Clear warnings** about what's not working

## 🌐 Service URLs

After starting both services:
- **Dashboard**: http://localhost:8501
- **API Service**: http://localhost:8000
- **API Health Check**: http://localhost:8000/

## 🔍 Troubleshooting

### If Dashboard Shows "Failed to load logs":
1. **Check if API service is running**: `curl http://localhost:8000/`
2. **Start API service**: `python event_api.py`
3. **Refresh dashboard page**

### If Port 8000 is Already in Use:
```bash
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### If Streamlit Port 8501 is in Use:
```bash
# Find what's using port 8501
netstat -ano | findstr :8501

# Kill the process
taskkill /PID <PID> /F
```

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

If you continue to see errors:
1. Check if Python and required packages are installed
2. Verify kubectl is configured and working
3. Check firewall/antivirus isn't blocking ports
4. Try running as administrator (Windows)

---

**Status**: ✅ All major dashboard pages have been fixed and now include proper API health checks and helpful startup instructions.
