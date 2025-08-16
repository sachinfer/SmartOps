# 🚀 Complete Setup Guide - Helm Charts + ArgoCD

## 🎯 What We're Doing

1. **Update your existing helm-charts repository** with SmartOps charts
2. **Fix ArgoCD repository URLs** to point to helm-charts instead of SmartOps
3. **Enable automated deployments** through your pipeline

## 📁 Current Status

✅ **Pipeline successful** - Your automation system is ready  
✅ **Helm-charts repository exists** - [https://github.com/sachinfer/helm-charts](https://github.com/sachinfer/helm-charts)  
✅ **ArgoCD applications exist** - But pointing to wrong repository  
🔄 **Next**: Update helm-charts and fix ArgoCD URLs  

## 🚀 Step 1: Update Your Helm Charts Repository

### **Option A: Use the Setup Script (Recommended)**

```powershell
# Run the setup script from your SmartOps directory
.\smartops-ai\scripts\setup-helm-charts.ps1

# The script will copy all necessary files to your helm-charts repository
```

### **Option B: Manual Setup**

```bash
# Navigate to your helm-charts repository
cd C:\Sachin\Git\helm-charts

# Copy the helm chart files from SmartOps setup
cp -r C:\Sachin\Git\SmartOps\smartops-ai\helm-charts-setup\smartops\* smartops\

# Check the structure
ls smartops
```

## 🔧 Step 2: Fix ArgoCD Repository URLs

### **Run the ArgoCD Update Script**

```powershell
# Update ArgoCD to point to helm-charts repository
.\smartops-ai\scripts\update-argocd-repos.ps1
```

### **Manual Update (Alternative)**

```bash
# Update each application to point to helm-charts
kubectl patch application smartops-anomaly -n argocd --type='merge' \
  -p='{"spec":{"source":{"repoURL":"https://github.com/sachinfer/helm-charts.git","path":"smartops/anomaly"}}}'

kubectl patch application smartops-dashboard -n argocd --type='merge' \
  -p='{"spec":{"source":{"repoURL":"https://github.com/sachinfer/helm-charts.git","path":"smartops/dashboard"}}}'

kubectl patch application smartops-monitor -n argocd --type='merge' \
  -p='{"spec":{"source":{"repoURL":"https://github.com/sachinfer/helm-charts.git","path":"smartops/monitor"}}}'
```

## 📋 Step 3: Commit and Push Helm Charts

```bash
# Navigate to helm-charts repository
cd C:\Sachin\Git\helm-charts

# Add all changes
git add .

# Commit the new helm charts
git commit -m "Add SmartOps helm charts for automated deployment"

# Push to trigger ArgoCD sync
git push origin main
```

## 🔍 Step 4: Verify Everything is Working

### **Check ArgoCD Applications**

```bash
# Verify repository URLs are correct
kubectl get applications -n argocd -o yaml | grep -A 5 "repoURL:"

# Check application sync status
kubectl get applications -n argocd
```

### **Check Helm Charts Repository**

```bash
# Verify your helm-charts repository structure
# Should look like:
# smartops/
# ├── anomaly/
# │   ├── Chart.yaml
# │   └── values.yaml
# ├── dashboard/
# │   ├── Chart.yaml
# │   └── values.yaml
# └── monitor/
#     ├── Chart.yaml
#     └── values.yaml
```

## 🎯 Step 5: Test the Complete System

### **Make a Small Change to Trigger Pipeline**

```bash
# Go back to SmartOps repository
cd C:\Sachin\Git\SmartOps

# Make a small change
echo "# Test automated deployment" >> README.md

# Commit and push
git add .
git commit -m "Test automated helm charts update"
git push origin main
```

### **Watch the Magic Happen!**

1. **GitHub Actions runs** → Updates helm-charts repository
2. **ArgoCD detects changes** → Automatically syncs
3. **New pods start** → Your applications deploy automatically!

## 📊 Monitoring Your Deployment

### **GitHub Actions**
- Check Actions tab in SmartOps repository
- Watch the update-helm-charts workflow

### **ArgoCD UI**
```bash
# Port forward to access ArgoCD
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Open: https://localhost:8080
# Username: admin
# Password: (get from kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)
```

### **Kubernetes**
```bash
# Check pod status
kubectl get pods -n smartops -w

# Check deployments
kubectl get deployments -n smartops

# Check services
kubectl get svc -n smartops
```

## 🚨 Troubleshooting

### **If Helm Charts Don't Update**

```bash
# Check if files were copied correctly
ls C:\Sachin\Git\helm-charts\smartops

# Verify git status
cd C:\Sachin\Git\helm-charts
git status
```

### **If ArgoCD Doesn't Sync**

```bash
# Check application configuration
kubectl get application smartops-dashboard -n argocd -o yaml

# Force sync
kubectl patch application smartops-dashboard -n argocd --type='merge' \
  -p='{"spec":{"syncPolicy":{"automated":{"prune":true,"selfHeal":true}}}}'
```

### **If Pipeline Fails**

```bash
# Check GitHub Actions logs
# Verify HELM_CHARTS_TOKEN secret is set
# Ensure token has access to helm-charts repository
```

## 🎉 Success Indicators

✅ **Helm charts repository** contains SmartOps charts  
✅ **ArgoCD applications** point to helm-charts repository  
✅ **GitHub Actions pipeline** runs successfully  
✅ **ArgoCD automatically syncs** when helm-charts update  
✅ **Applications deploy** without manual intervention  

## 🔮 Your Complete Automated Workflow

```
Code Push → GitHub Actions → Update Helm Charts → ArgoCD Auto-Sync → K8s Deployment
```

**Congratulations! 🎉 Your deployment process is now completely automated!**

---

## 📞 Need Help?

1. **Check the troubleshooting section above**
2. **Review GitHub Actions logs** for detailed error messages  
3. **Verify ArgoCD application status** in the UI
4. **Check Kubernetes cluster events** for deployment issues

**You're now running a professional, enterprise-grade CI/CD pipeline! 🚀✨**
