# 🔧 Google Cloud Deployment Troubleshooting Guide

## 🚨 **Current Issue: ERR_CONNECTION_REFUSED**

Your dashboard is running but can't connect to the backend API service. Here's how to fix it:

## 📋 **Quick Diagnosis Steps:**

### 1. **Check if API Service is Running:**
```bash
# Check pods
kubectl get pods -n <your-namespace>

# Check services
kubectl get services -n <your-namespace>

# Check endpoints
kubectl get endpoints -n <your-namespace>
```

### 2. **Verify Service Names:**
Make sure your backend service is named one of these:
- `smartops-api-service`
- `smartops-api`
- `smartops-backend`
- `api-service`

### 3. **Check Service Ports:**
```bash
# Check service details
kubectl describe service smartops-api-service -n <your-namespace>

# Should show port 8000
```

## 🔍 **Common Google Cloud Issues:**

### **Issue 1: Service Not Deployed**
```bash
# Check if the service exists
kubectl get services -n <your-namespace> | grep api

# If not found, deploy it:
kubectl apply -f k8s/smartops-api-service.yaml
```

### **Issue 2: Wrong Namespace**
```bash
# Check current namespace
kubectl config view --minify --output 'jsonpath={..namespace}'

# Switch to correct namespace
kubectl config set-context --current --namespace=<your-namespace>
```

### **Issue 3: Network Policies Blocking**
```bash
# Check network policies
kubectl get networkpolicies -n <your-namespace>

# If blocking, either remove or update them
kubectl delete networkpolicy <policy-name> -n <your-namespace>
```

### **Issue 4: Service Port Mismatch**
```bash
# Check service port configuration
kubectl get service smartops-api-service -n <your-namespace> -o yaml

# Should show:
# ports:
# - port: 8000
#   targetPort: 8000
```

## 🚀 **Fix Commands:**

### **Option 1: Redeploy API Service**
```bash
# Delete existing service
kubectl delete service smartops-api-service -n <your-namespace>

# Redeploy
kubectl apply -f k8s/smartops-api-service.yaml
```

### **Option 2: Update Service Configuration**
```yaml
# k8s/smartops-api-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: smartops-api-service
  namespace: <your-namespace>
spec:
  selector:
    app: smartops-api
  ports:
  - port: 8000
    targetPort: 8000
  type: ClusterIP
```

### **Option 3: Check Pod Labels**
```bash
# Make sure pod labels match service selector
kubectl get pods -n <your-namespace> --show-labels

# Pod should have label: app=smartops-api
```

## 📊 **Dashboard Configuration:**

The dashboard now automatically:
- ✅ Detects Google Cloud environment
- ✅ Tests multiple API endpoints
- ✅ Shows connectivity test results
- ✅ Provides troubleshooting steps

## 🔧 **Manual Testing:**

```bash
# Test from within the cluster
kubectl exec -it <dashboard-pod> -n <your-namespace> -- curl http://smartops-api-service:8000/

# Test from your local machine (if port-forwarded)
kubectl port-forward service/smartops-api-service 8000:8000 -n <your-namespace>
curl http://localhost:8000/
```

## 📞 **Still Having Issues?**

1. **Check logs:**
   ```bash
   kubectl logs -f deployment/smartops-api-service -n <your-namespace>
   ```

2. **Check events:**
   ```bash
   kubectl get events -n <your-namespace> --sort-by='.lastTimestamp'
   ```

3. **Verify RBAC:**
   ```bash
   kubectl get serviceaccount -n <your-namespace>
   kubectl get rolebinding -n <your-namespace>
   ```

## 🎯 **Expected Result:**

After fixing, you should see:
- ✅ Environment: GOOGLE_CLOUD
- ✅ API Status: Available
- ✅ Cluster: Connected
- 📊 Dashboard showing real-time cluster data
