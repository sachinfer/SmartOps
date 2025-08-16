# 🚀 Quick Setup Guide - Automated Helm Charts Update

## ⚡ Get Running in 5 Minutes!

### 1. Set Up GitHub Secret (Required for GitHub Actions)

```bash
# Go to: https://github.com/sachinfer/SmartOps/settings/secrets/actions
# Click "New repository secret"
# Name: HELM_CHARTS_TOKEN
# Value: Your GitHub Personal Access Token with repo access to helm-charts
```

**How to get the token:**
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token
3. Select scopes: `repo` (full control of private repositories)
4. Copy the token and paste it as the secret value

### 2. Test the System (Optional)

```bash
# Test locally (Windows PowerShell)
.\smartops-ai\scripts\update-helm-charts.ps1

# Test locally (Linux/Mac)
chmod +x smartops-ai/scripts/update-helm-charts.sh
./smartops-ai/scripts/update-helm-charts.sh
```

### 3. Push Code to Trigger Automation

```bash
git add .
git commit -m "Add automated helm charts updater"
git push origin main
```

**That's it! 🎉**

## 🔍 What Happens Next

1. **GitHub Actions automatically runs** the update-helm-charts workflow
2. **Image tags are updated** in your helm-charts repository
3. **Changes are pushed** to helm-charts repo
4. **ArgoCD detects changes** and automatically deploys
5. **New versions are running** in your Kubernetes cluster

## 📊 Monitor Progress

- **GitHub Actions**: Check the Actions tab in your SmartOps repo
- **ArgoCD UI**: Monitor deployment progress in ArgoCD
- **Kubernetes**: `kubectl get pods -n smartops`

## 🚨 Troubleshooting

### If GitHub Actions fails:
- Check that `HELM_CHARTS_TOKEN` secret is set correctly
- Verify the token has access to helm-charts repository
- Check Actions logs for detailed error messages

### If ArgoCD doesn't sync:
- Verify helm-charts repository URL in ArgoCD apps
- Check ArgoCD application status
- Ensure automated sync is enabled

## 🎯 Your Workflow is Now:

```
Code Push → GitHub Actions → Update Helm Charts → ArgoCD Auto-Deploy
```

**No more manual work! Everything happens automatically! 🚀✨**
