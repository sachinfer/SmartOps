# 🔧 Troubleshooting Guide - Kubernetes Shell and Cluster Explorer

## 🚨 Common Issues and Solutions

### 1. Page Functions Not Working

**Symptoms:**
- Buttons don't respond
- Commands don't execute
- Error messages about API connections
- Page appears broken or unresponsive

**Root Causes:**
- Backend API service not running
- Kubernetes configuration issues
- Network connectivity problems
- Missing dependencies

### 2. Backend API Service Issues

**Check if API is running:**
```bash
# Check if port 8000 is listening
netstat -an | grep 8000
# or
curl http://localhost:8000/
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "SmartOps API",
  "timestamp": "2024-01-01T00:00:00"
}
```

**If API is not responding:**
1. Start the FastAPI service:
   ```bash
   cd smartops-ai/dashboard
   python -m uvicorn event_api:app --host 0.0.0.0 --port 8000 --reload
   ```

2. Or use the startup script:
   ```bash
   cd smartops-ai/dashboard
   python start_services.py
   ```

### 3. Kubernetes Configuration Issues

**Common Kubernetes Config Problems:**
- No kubeconfig file found
- Invalid cluster credentials
- Cluster not accessible

**Solutions:**
1. **Check kubeconfig:**
   ```bash
   kubectl config view
   kubectl cluster-info
   ```

2. **Set KUBECONFIG environment variable:**
   ```bash
   export KUBECONFIG=~/.kube/config
   ```

3. **Test basic kubectl commands:**
   ```bash
   kubectl get pods
   kubectl get nodes
   ```

### 4. Dependency Issues

**Missing Python packages:**
```bash
cd smartops-ai/dashboard
pip install -r requirements.txt
```

**Key dependencies:**
- `kubernetes` - Kubernetes client library
- `fastapi` - Backend API framework
- `uvicorn` - ASGI server
- `streamlit` - Frontend framework
- `requests` - HTTP client

### 5. Network and Port Issues

**Port conflicts:**
- Port 8000 (API) already in use
- Port 8501 (Streamlit) already in use

**Solutions:**
```bash
# Find processes using ports
lsof -i :8000
lsof -i :8501

# Kill conflicting processes
kill -9 <PID>
```

### 6. Testing API Endpoints

**Use the test script:**
```bash
cd smartops-ai/dashboard
python test_api.py
```

**Manual API testing:**
```bash
# Health check
curl http://localhost:8000/

# Resource types
curl http://localhost:8000/kubectl_resource_types

# Namespaces
curl http://localhost:8000/namespaces

# Test kubectl command
curl -X POST "http://localhost:8000/kubectl_raw?command=get%20pods"
```

### 7. Streamlit Issues

**Page not loading:**
1. Check Streamlit is running:
   ```bash
   streamlit run streamlit_app.py --server.port=8501
   ```

2. Check browser console for JavaScript errors

3. Verify page navigation:
   - Use the sidebar navigation
   - Check URL: `http://localhost:8501/3_Kubernetes_Shell_and_Cluster_Explorer`

### 8. Docker Deployment Issues

**If using Docker:**
```bash
# Build and run
docker build -t smartops-dashboard .
docker run -p 8501:8501 -p 8000:8000 smartops-dashboard

# Check container logs
docker logs <container_id>
```

### 9. Environment Variables

**Required environment variables:**
```bash
# For development
export ENV=dev

# Kubernetes config
export KUBECONFIG=~/.kube/config

# API settings
export API_HOST=0.0.0.0
export API_PORT=8000
```

### 10. Debug Mode

**Enable debug logging:**
```python
# In event_api.py, add:
import logging
logging.basicConfig(level=logging.DEBUG)

# In streamlit_app.py, add:
st.set_page_config(..., initial_sidebar_state="expanded")
```

## 🚀 Quick Start Guide

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start services:**
   ```bash
   python start_services.py
   ```

3. **Access dashboard:**
   - Frontend: http://localhost:8501
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

4. **Test functionality:**
   - Navigate to "Kubernetes Shell and Cluster Explorer"
   - Try basic commands: `kubectl get pods`
   - Use Cluster Explorer to browse resources

## 📋 Troubleshooting Checklist

- [ ] Backend API service running on port 8000
- [ ] Streamlit frontend running on port 8501
- [ ] Kubernetes cluster accessible
- [ ] All dependencies installed
- [ ] No port conflicts
- [ ] Network connectivity working
- [ ] API endpoints responding
- [ ] Page navigation working
- [ ] Command execution functional
- [ ] Error messages clear and helpful

## 🆘 Getting Help

If issues persist:

1. Check the logs for both services
2. Run the test script: `python test_api.py`
3. Verify Kubernetes cluster access
4. Check browser developer console
5. Review this troubleshooting guide
6. Check GitHub issues for similar problems

## 🔍 Debug Commands

**Check service status:**
```bash
# Check running processes
ps aux | grep -E "(uvicorn|streamlit)"

# Check network connections
netstat -tulpn | grep -E "(8000|8501)"

# Check logs
tail -f /var/log/syslog | grep -E "(uvicorn|streamlit)"
```

**Test Kubernetes access:**
```bash
# Test cluster connectivity
kubectl cluster-info

# Test basic operations
kubectl get pods --all-namespaces
kubectl get nodes
kubectl get services --all-namespaces
```
