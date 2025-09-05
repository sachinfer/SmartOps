# Full-Width Layout Deployment Guide for GCP

## Overview
This guide explains how to deploy the SmartOps dashboard with full-width layout fixes to Google Cloud Platform (GCP) using Docker and Kubernetes.

## Prerequisites
- GCP project with GKE cluster
- Docker registry access
- kubectl configured
- GitHub Actions secrets configured

## Files Modified for Full-Width Deployment

### 1. Docker Configuration
- **`Dockerfile`**: Updated to include full-width files verification
- **`supervisord.conf`**: Enhanced with full-width Streamlit parameters

### 2. Kubernetes Configuration
- **`smartops-dashboard-deployment.yaml`**: Added full-width environment variables
- **Environment variables added**:
  - `STREAMLIT_LAYOUT_WIDE_MODE=true`
  - `STREAMLIT_THEME_WIDE_MODE=true`
  - `STREAMLIT_UI_GLOBAL_CUSTOM_CODE=true`

### 3. GitHub Actions
- **`.github/workflows/deploy.yml`**: Added fullwidth branch trigger and verification step

## Deployment Process

### 1. Automatic Deployment (Recommended)
The deployment will trigger automatically when you push to the following branches:
- `main`
- `gcp`
- `gcp2`
- `dash`
- `misi`
- `kill`
- `update`
- `anomaly`
- `time`
- `fullwidth` (new)

### 2. Manual Deployment
If you need to deploy manually:

```bash
# 1. Build and push Docker images
docker build -t us-docker.pkg.dev/PROJECT_ID/smartops-repo/smartops-dashboard:latest -f smartops-ai/dashboard/Dockerfile ./smartops-ai/dashboard

# 2. Push to registry
docker push us-docker.pkg.dev/PROJECT_ID/smartops-repo/smartops-dashboard:latest

# 3. Deploy to Kubernetes
kubectl apply -f smartops-ai/k8s/smartops-dashboard-deployment.yaml -n smartops

# 4. Update deployment with new image
kubectl set image deployment/smartops-dashboard dashboard=us-docker.pkg.dev/PROJECT_ID/smartops-repo/smartops-dashboard:latest -n smartops
```

## Verification Steps

### 1. Check Deployment Status
```bash
# Check if pods are running
kubectl get pods -n smartops

# Check deployment status
kubectl get deployment smartops-dashboard -n smartops

# Check service
kubectl get service smartops-dashboard-service -n smartops
```

### 2. Get Dashboard URL
```bash
# Get external IP
kubectl get service smartops-dashboard-service -n smartops -o jsonpath='{.status.loadBalancer.ingress[0].ip}'

# Or use port-forward for testing
kubectl port-forward service/smartops-dashboard-service 8501:8501 -n smartops
```

### 3. Verify Full-Width Layout
1. Open the dashboard in your browser
2. Navigate to different pages
3. Check that all content spans the full width
4. Visit `/test_fullwidth_fix` for comprehensive testing

### 4. Run Verification Script
```bash
# Run the verification script
python smartops-ai/dashboard/verify_fullwidth_deployment.py

# Or with custom URL
DASHBOARD_URL=http://YOUR_DASHBOARD_IP python smartops-ai/dashboard/verify_fullwidth_deployment.py
```

## Troubleshooting

### Common Issues

#### 1. Dashboard Not Accessible
```bash
# Check pod logs
kubectl logs deployment/smartops-dashboard -n smartops

# Check service
kubectl describe service smartops-dashboard-service -n smartops
```

#### 2. Full-Width Layout Not Working
- Verify the custom CSS is being loaded
- Check browser developer tools for CSS conflicts
- Ensure all environment variables are set correctly

#### 3. Images Not Updating
```bash
# Force image pull
kubectl rollout restart deployment/smartops-dashboard -n smartops

# Check image being used
kubectl describe deployment smartops-dashboard -n smartops
```

### Debug Commands

```bash
# Check all resources
kubectl get all -n smartops

# Check events
kubectl get events -n smartops --sort-by='.lastTimestamp'

# Check pod details
kubectl describe pod -l app=smartops-dashboard -n smartops

# Check service details
kubectl describe service smartops-dashboard-service -n smartops
```

## Environment Variables

The following environment variables are set in the deployment for full-width functionality:

```yaml
env:
- name: STREAMLIT_LAYOUT_WIDE_MODE
  value: "true"
- name: STREAMLIT_THEME_WIDE_MODE
  value: "true"
- name: STREAMLIT_UI_GLOBAL_CUSTOM_CODE
  value: "true"
- name: STREAMLIT_SERVER_HEADLESS
  value: "true"
- name: STREAMLIT_SERVER_ENABLE_CORS
  value: "false"
- name: STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION
  value: "false"
```

## Monitoring

### Health Checks
The deployment includes:
- **Readiness Probe**: HTTP GET on port 8501
- **Liveness Probe**: HTTP GET on port 8501
- **Resource Limits**: 256Mi memory, 100m CPU

### Logs
```bash
# View logs
kubectl logs -f deployment/smartops-dashboard -n smartops

# View logs with timestamps
kubectl logs -f deployment/smartops-dashboard -n smartops --timestamps=true
```

## Rollback

If you need to rollback to a previous version:

```bash
# Check rollout history
kubectl rollout history deployment/smartops-dashboard -n smartops

# Rollback to previous version
kubectl rollout undo deployment/smartops-dashboard -n smartops

# Rollback to specific revision
kubectl rollout undo deployment/smartops-dashboard --to-revision=2 -n smartops
```

## Support

If you encounter issues:
1. Check the logs using the commands above
2. Verify all files are present in the Docker image
3. Test the full-width layout locally first
4. Check the GitHub Actions logs for build issues

## Notes

- The full-width layout is applied via CSS and JavaScript
- All changes are included in the Docker image
- The deployment uses a persistent volume for data storage
- The dashboard runs on port 8501, API on port 8000
