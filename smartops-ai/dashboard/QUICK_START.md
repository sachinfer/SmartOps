# 🚀 SmartOps Dashboard Quick Start Guide

## ⚡ Get Started in 3 Simple Steps

### 1. 🖥️ Start the Backend API Service
Open a terminal/command prompt and run:

```bash
cd smartops-ai/dashboard
python event_api.py
```

**Expected Output:**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### 2. 🌐 Start the Dashboard
Open another terminal/command prompt and run:

```bash
cd smartops-ai/dashboard
streamlit run streamlit_app.py
```

**Expected Output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.1.100:8501
```

### 3. 🎯 Open Your Browser
Navigate to: `http://localhost:8501`

## 🔧 Troubleshooting

### ❌ "Connection refused" or "Getting Started" messages?
- **Solution**: Make sure the API service is running first (Step 1)
- **Check**: Look for the API service terminal showing "Uvicorn running on http://127.0.0.1:8000"

### ❌ Port already in use?
- **Solution**: Kill existing processes or use different ports
- **API Port**: Change `8000` in `event_api.py` if needed
- **Dashboard Port**: Use `streamlit run streamlit_app.py --server.port 8502`

### ❌ Python not found?
- **Solution**: Install Python 3.8+ and required packages
- **Install**: `pip install -r requirements.txt`

## 📱 What You'll See

✅ **Overview Page**: Cluster status, metrics, and health
✅ **Pod Explorer**: Real-time pod data and logs
✅ **Kubernetes Shell**: Execute kubectl commands
✅ **Anomaly Detection**: AI-powered insights
✅ **AI Actions**: Smart recommendations

## 🎉 Success!
Once both services are running, you'll see:
- Real-time cluster data
- Live pod status
- Interactive shell commands
- Beautiful, modern UI

## 🆘 Need Help?
- Check the terminal outputs for error messages
- Ensure both services are running simultaneously
- Verify ports 8000 (API) and 8501 (Dashboard) are available
