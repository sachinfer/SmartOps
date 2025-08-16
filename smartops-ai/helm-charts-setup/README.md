# 🚀 Helm Charts Repository Setup Guide

## 📁 Required Directory Structure

Your helm-charts repository should have this structure:

```
helm-charts/
└── smartops/
    ├── anomaly/
    │   ├── Chart.yaml
    │   ├── values.yaml
    │   └── templates/
    │       ├── deployment.yaml
    │       ├── service.yaml
    │       └── pvc.yaml
    ├── dashboard/
    │   ├── Chart.yaml
    │   ├── values.yaml
    │   └── templates/
    │       ├── deployment.yaml
    │       ├── service.yaml
    │       └── ingress.yaml
    └── monitor/
        ├── Chart.yaml
        ├── values.yaml
        └── templates/
            ├── deployment.yaml
            └── service.yaml
```

## 🎯 Quick Setup Commands

```bash
# Clone your helm-charts repository
git clone https://github.com/sachinfer/helm-charts.git
cd helm-charts

# Create directory structure
mkdir -p smartops/{anomaly,dashboard,monitor}/{templates,charts}

# Copy the provided files to each directory
# (Files are provided in this setup folder)
```

## 📋 Files to Copy

1. **Copy Chart.yaml files** to each application directory
2. **Copy values.yaml files** to each application directory  
3. **Copy template files** to each templates directory
4. **Commit and push** to trigger ArgoCD sync

## 🔄 After Setup

Once you've set up the helm-charts repository:

1. **ArgoCD will automatically detect** the new structure
2. **Applications will sync** with the new charts
3. **Your automated pipeline** will work perfectly!

## 📊 Verification

```bash
# Check if ArgoCD can access the repository
kubectl get applications -n argocd

# Check application sync status
kubectl get applications smartops-dashboard -n argocd -o yaml
```
