# 🚀 Automated Helm Charts Update System

This system automatically updates image tags in your helm-charts repository and triggers ArgoCD auto-deploy, making your entire deployment process completely automatic!

## 🎯 What This System Does

1. **Automatically updates image tags** in your helm-charts repository
2. **Pushes changes** to trigger ArgoCD auto-deploy
3. **No manual work needed** after building Docker images
4. **Professional DevOps workflow** with full automation

## 🏗️ Architecture

```
SmartOps Repo → Build Images → Update Helm Charts → ArgoCD Auto-Deploy
     ↓              ↓              ↓              ↓
  Code Push    Docker Build   Tag Update    K8s Deployment
```

## 📁 Files Created

- `scripts/update-helm-charts.py` - Python script for automation
- `scripts/update-helm-charts.sh` - Shell script for local execution
- `.github/workflows/update-helm-charts.yml` - GitHub Actions workflow

## 🚀 Quick Start

### Option 1: GitHub Actions (Recommended)

1. **Set up GitHub Secret:**
   ```bash
   # Go to your SmartOps repository → Settings → Secrets and variables → Actions
   # Add new secret: HELM_CHARTS_TOKEN
   # Value: Your GitHub Personal Access Token with repo access to helm-charts
   ```

2. **Push code to trigger automation:**
   ```bash
   git add .
   git commit -m "Update application code"
   git push origin main
   ```

3. **GitHub Actions will automatically:**
   - Update helm-charts with new image tags
   - Push changes to helm-charts repository
   - Trigger ArgoCD auto-deploy

### Option 2: Local Execution

1. **Make script executable:**
   ```bash
   chmod +x scripts/update-helm-charts.sh
   ```

2. **Run the script:**
   ```bash
   ./scripts/update-helm-charts.sh
   ```

3. **Script will automatically:**
   - Clone helm-charts repository
   - Update image tags
   - Push changes
   - Trigger ArgoCD deployment

## ⚙️ Configuration

### Environment Variables

```bash
# Helm Charts Repository
HELM_CHARTS_REPO="https://github.com/sachinfer/helm-charts.git"
HELM_CHARTS_PATH="smartops"

# Git Configuration
GIT_USER="SmartOps Bot"
GIT_EMAIL="bot@smartops.ai"
```

### Customization

You can customize the script behavior by modifying:

- **Image tag format** in `get_latest_image_tags()` function
- **Repository URLs** in configuration section
- **Git commit messages** and user information
- **File paths** for different chart structures

## 🔄 Workflow

### 1. Code Development
```bash
# Make changes to your SmartOps application
git add .
git commit -m "Add new feature"
git push origin main
```

### 2. Automated Build & Deploy
```bash
# GitHub Actions automatically:
# 1. Builds Docker images
# 2. Updates helm-charts with new tags
# 3. Pushes to helm-charts repository
# 4. ArgoCD detects changes and deploys
```

### 3. Verification
```bash
# Check ArgoCD UI for deployment status
# Verify new versions are running in cluster
kubectl get pods -n smartops
```

## 🛠️ Prerequisites

### For GitHub Actions
- GitHub repository with Actions enabled
- `HELM_CHARTS_TOKEN` secret configured
- Access to helm-charts repository

### For Local Execution
- Git installed
- `yq` command-line tool (script will auto-install)
- Access to helm-charts repository

## 📊 Monitoring

### ArgoCD UI
- Monitor deployment progress
- Check sync status
- View application logs

### Kubernetes
```bash
# Check pod status
kubectl get pods -n smartops

# View logs
kubectl logs -f deployment/smartops-dashboard -n smartops

# Check service endpoints
kubectl get svc -n smartops
```

## 🔧 Troubleshooting

### Common Issues

1. **Permission Denied**
   ```bash
   # Ensure HELM_CHARTS_TOKEN has proper permissions
   # Token needs repo access to helm-charts repository
   ```

2. **yq Not Found**
   ```bash
   # Script will auto-install yq
   # Or install manually: brew install yq (macOS) / apt-get install yq (Ubuntu)
   ```

3. **Git Authentication Failed**
   ```bash
   # Check git credentials
   git config --list | grep user
   # Ensure proper access to helm-charts repository
   ```

### Debug Mode

Run with verbose output:
```bash
bash -x scripts/update-helm-charts.sh
```

## 🎉 Benefits

✅ **Zero Manual Work** - Everything happens automatically
✅ **Consistent Deployments** - Always uses latest image tags
✅ **Professional Workflow** - Industry-standard CI/CD pipeline
✅ **ArgoCD Integration** - Automatic Kubernetes deployments
✅ **Rollback Support** - ArgoCD maintains deployment history

## 🔮 Future Enhancements

- **Multi-environment support** (dev, staging, prod)
- **Image vulnerability scanning** before deployment
- **Automated testing** before helm-charts update
- **Slack/Teams notifications** for deployment status
- **Metrics collection** for deployment analytics

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review GitHub Actions logs for detailed error messages
3. Verify ArgoCD application status
4. Check Kubernetes cluster events

---

**🎯 Your deployment process is now completely automated! Just push code and watch ArgoCD deploy everything automatically! 🚀✨**
