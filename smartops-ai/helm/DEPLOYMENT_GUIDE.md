# 🚀 SmartOps Helm Chart - Quick Deployment Guide

## 🎯 What You'll Get

Your SmartOps application will be deployed with:
- **Dashboard**: Streamlit-based monitoring UI (LoadBalancer service)
- **Anomaly Detection**: AI-powered ML monitoring with FastAPI backend
- **Monitor**: Automated metrics collection via CronJob
- **RBAC**: Secure access to cluster resources
- **Persistent Storage**: Data retention for analytics

## 🚀 Quick Start (3 Ways to Deploy)

### 1. 🎯 GitHub Raw URL (Recommended for Open Source)

```bash
# Deploy directly from GitHub
kubectl apply -f https://raw.githubusercontent.com/sachinfer/SmartOps/main/smartops-ai/helm/templates/

# Or use Helm with the raw URL
helm install smartops https://raw.githubusercontent.com/sachinfer/SmartOps/main/smartops-ai/helm --namespace smartops --create-namespace
```

### 2. 🔧 Helm Chart Installation

```bash
# Clone and deploy
git clone https://github.com/sachinfer/SmartOps.git
cd SmartOps/smartops-ai/helm

# Deploy with default values
helm install smartops . --namespace smartops --create-namespace

# Deploy with custom values
helm install smartops . --namespace smartops --create-namespace -f custom-values.yaml
```

### 3. 🐚 Script Deployment

```bash
# Linux/Mac
chmod +x deploy.sh
./deploy.sh

# Windows PowerShell
.\deploy.ps1

# With custom options
.\deploy.ps1 -ReleaseName my-smartops -Namespace my-namespace
```

## ⚙️ Configuration

### Basic Customization

Create `custom-values.yaml`:

```yaml
global:
  namespace: my-smartops

dashboard:
  image:
    repository: my-registry/smartops-dashboard
    tag: v1.0.0
  
  service:
    type: NodePort  # or ClusterIP, LoadBalancer

anomaly:
  image:
    repository: my-registry/smartops-anomaly
    tag: v1.0.0
```

### Advanced Configuration

```yaml
# Enable ingress
ingress:
  enabled: true
  hosts:
    - host: smartops.mycompany.com
      paths:
        - path: /
          pathType: Prefix

# Enable auto-scaling
hpa:
  enabled: true
  minReplicas: 2
  maxReplicas: 10

# Custom resources
dashboard:
  resources:
    limits:
      cpu: 2000m
      memory: 4Gi
    requests:
      cpu: 1000m
      memory: 2Gi
```

## 🌐 Access Your Dashboard

### LoadBalancer (Default)
```bash
kubectl get svc -n smartops smartops-dashboard-service
# Use the EXTERNAL-IP to access dashboard
```

### Port Forward
```bash
kubectl port-forward -n smartops svc/smartops-dashboard-service 8501:80
# Open http://localhost:8501 in browser
```

### Ingress (if enabled)
```bash
# Access via your configured hostname
# e.g., http://smartops.mycompany.com
```

## 📊 Monitor Your Deployment

### Check Status
```bash
# Overall status
helm status smartops -n smartops

# Pod status
kubectl get pods -n smartops

# Service status
kubectl get svc -n smartops
```

### View Logs
```bash
# Dashboard logs
kubectl logs -n smartops deployment/smartops-dashboard

# Anomaly detection logs
kubectl logs -n smartops deployment/smartops-anomaly

# Monitor cronjob logs
kubectl logs -n smartops job/smartops-monitor-<timestamp>
```

### Check RBAC
```bash
# Service accounts
kubectl get serviceaccounts -n smartops

# Roles and bindings
kubectl get roles,rolebindings -n smartops
```

## 🔄 Upgrading

```bash
# Update from GitHub
helm upgrade smartops https://raw.githubusercontent.com/sachinfer/SmartOps/main/smartops-ai/helm --namespace smartops

# Update local chart
helm upgrade smartops . --namespace smartops

# Using script
.\deploy.ps1 -Upgrade
```

## 🗑️ Uninstalling

```bash
# Remove Helm release
helm uninstall smartops -n smartops

# Remove namespace (optional)
kubectl delete namespace smartops

# Using script
.\deploy.ps1 -ReleaseName smartops -Namespace smartops
```

## 🐛 Troubleshooting

### Common Issues

1. **Pods not starting**
   ```bash
   kubectl describe pod <pod-name> -n smartops
   kubectl get events -n smartops --sort-by='.lastTimestamp'
   ```

2. **Service not accessible**
   ```bash
   kubectl describe svc <service-name> -n smartops
   kubectl get endpoints -n smartops
   ```

3. **RBAC issues**
   ```bash
   kubectl auth can-i get pods -n smartops
   kubectl auth can-i list services -n smartops
   ```

### Debug Commands

```bash
# Test connectivity
kubectl run test-pod --image=busybox --rm -it --restart=Never -- nslookup smartops-dashboard-service.smartops.svc.cluster.local

# Check configmaps
kubectl get configmaps -n smartops
kubectl describe configmap smartops-config -n smartops

# Verify persistent volumes
kubectl get pvc -n smartops
kubectl describe pvc smartops-dashboard-pvc -n smartops
```

## 📚 Next Steps

1. **Customize Images**: Update image repositories in `values.yaml`
2. **Configure Storage**: Set storage class for persistent volumes
3. **Enable Ingress**: Configure ingress controller and hostnames
4. **Set Up Monitoring**: Integrate with Prometheus/Grafana
5. **Configure Alerts**: Set up alerting for anomalies

## 🆘 Need Help?

- **GitHub Issues**: [https://github.com/sachinfer/SmartOps/issues](https://github.com/sachinfer/SmartOps/issues)
- **Documentation**: [https://github.com/sachinfer/SmartOps](https://github.com/sachinfer/SmartOps)
- **Helm Docs**: [https://helm.sh/docs/](https://helm.sh/docs/)

---

**Happy Deploying! 🚀**
