# 🚀 ArgoCD Integration for SmartOps

## Overview
This directory contains ArgoCD configuration for deploying SmartOps applications using GitOps principles.

## 🏗️ Architecture

```
GitHub Repository → ArgoCD → Kubernetes Cluster
     ↓                ↓           ↓
  Code Changes → Auto-Sync → Auto-Deploy
```

## 📁 Files Structure

```
k8s/
├── argocd-apps/                    # ArgoCD Application Manifests
│   ├── smartops-dashboard-app.yaml # Dashboard Application
│   ├── smartops-monitor-app.yaml   # Monitor Service Application
│   └── smartops-anomaly-app.yaml  # Anomaly Detection Application
├── install-argocd.sh              # ArgoCD Installation Script
├── deploy-argocd-apps.sh          # Deploy Applications Script
└── ARGOCD_README.md               # This File
```

## 🚀 Quick Start

### 1. Install ArgoCD
```bash
# Make script executable
chmod +x install-argocd.sh

# Run installation
./install-argocd.sh
```

### 2. Deploy Applications
```bash
# Make script executable
chmod +x deploy-argocd-apps.sh

# Deploy all applications
./deploy-argocd-apps.sh
```

### 3. Access ArgoCD UI
```bash
# Port forward ArgoCD server
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Open browser: http://localhost:8080
# Username: admin
# Password: (shown during installation)
```

## 🔧 Manual Installation

### Install ArgoCD
```bash
# Create namespace
kubectl create namespace argocd

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for readiness
kubectl wait --for=condition=available --timeout=300s deployment/argocd-server -n argocd
```

### Get Admin Password
```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

## 📊 Application Management

### Check Application Status
```bash
# List all applications
kubectl get applications -n argocd

# Get detailed status
kubectl describe application smartops-dashboard -n argocd
```

### Manual Sync
```bash
# Sync specific application
kubectl exec -n argocd deployment/argocd-server -- argocd app sync smartops-dashboard

# Sync all applications
kubectl exec -n argocd deployment/argocd-server -- argocd app sync --all
```

### Rollback
```bash
# List revisions
kubectl exec -n argocd deployment/argocd-server -- argocd app history smartops-dashboard

# Rollback to specific revision
kubectl exec -n argocd deployment/argocd-server -- argocd app rollback smartops-dashboard <REVISION>
```

## 🌟 Benefits of ArgoCD

### ✅ **Automated Deployments**
- Automatic sync when code changes
- Self-healing capabilities
- Prune deleted resources

### ✅ **GitOps Workflow**
- All changes tracked in Git
- Rollback to any previous state
- Audit trail of deployments

### ✅ **Health Monitoring**
- Real-time application status
- Visual deployment dashboard
- Automatic health checks

### ✅ **Multi-Environment Support**
- Easy to manage dev/staging/prod
- Environment-specific configurations
- Consistent deployment patterns

## 🔍 Troubleshooting

### Check ArgoCD Logs
```bash
# ArgoCD server logs
kubectl logs -n argocd deployment/argocd-server

# Application controller logs
kubectl logs -n argocd deployment/argocd-application-controller

# Repo server logs
kubectl logs -n argocd deployment/argocd-repo-server
```

### Common Issues

#### Application Stuck in Progress
```bash
# Check application events
kubectl describe application smartops-dashboard -n argocd

# Force sync
kubectl exec -n argocd deployment/argocd-server -- argocd app sync smartops-dashboard --force
```

#### Sync Failed
```bash
# Check sync status
kubectl exec -n argocd deployment/argocd-server -- argocd app get smartops-dashboard

# Retry sync
kubectl exec -n argocd deployment/argocd-server -- argocd app sync smartops-dashboard
```

## 🔄 Workflow

### 1. **Code Push**
```bash
git add .
git commit -m "Update SmartOps application"
git push origin Plotly-Dash
```

### 2. **GitHub Actions**
- Builds Docker images
- Pushes to Google Artifact Registry
- Triggers ArgoCD sync

### 3. **ArgoCD Auto-Sync**
- Detects changes in Git
- Automatically deploys to cluster
- Updates application status

### 4. **Health Monitoring**
- ArgoCD monitors deployment health
- Self-heals if issues detected
- Provides visual status dashboard

## 📚 Additional Resources

- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [ArgoCD GitHub](https://github.com/argoproj/argo-cd)
- [GitOps Best Practices](https://www.gitops.tech/)

## 🎯 Next Steps

1. **Install ArgoCD** using the provided script
2. **Deploy applications** via ArgoCD
3. **Monitor deployments** through ArgoCD UI
4. **Customize configurations** as needed
5. **Set up notifications** for deployment events

---

**Happy GitOps-ing! 🚀✨**
