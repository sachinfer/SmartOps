# 🚀 Kubernetes Deployment Guide for Misi AI Chatbot

## 🎯 Overview

This guide explains how to deploy **Misi AI Chatbot** to your Kubernetes cluster using the existing GitHub Actions pipeline. The pipeline automatically builds, tests, and deploys Misi to your GKE cluster.

## ✨ What Gets Deployed

- **Misi AI Chatbot**: Floating 🤖 icon with popup chat interface
- **Auto-scaling**: 2-10 replicas based on CPU/Memory usage
- **Health checks**: Liveness and readiness probes
- **Monitoring**: Resource metrics and health status
- **Load balancing**: ClusterIP service with ingress support

## 🔧 Pipeline Integration

### Updated Pipeline Features

The existing pipeline now includes:

1. **Parallel Build**: Misi chatbot builds alongside other services
2. **Docker Caching**: Optimized layer caching for faster builds
3. **Auto-deployment**: Automatic deployment to `smartops` namespace
4. **Health Monitoring**: Waits for Misi to be ready before completing
5. **Telegram Notifications**: Deployment status updates

### Pipeline Steps

```yaml
# 1. Build Misi Docker Image
docker buildx build \
  --platform linux/amd64 \
  --tag $REGISTRY/misi-ai-chatbot:latest \
  --file smartops-ai-chatbot/Dockerfile.production \
  ./smartops-ai-chatbot

# 2. Deploy to Kubernetes
kubectl apply -f smartops-ai-chatbot/k8s/misi-chatbot-deployment.yaml

# 3. Update Image
kubectl set image deployment/misi-ai-chatbot misi-chatbot=$MISI_TAG

# 4. Wait for Ready
kubectl wait --for=condition=available deployment/misi-ai-chatbot
```

## 🚀 Deployment Process

### Step 1: Local Testing (Optional)

Before pushing to the pipeline, test locally:

```bash
# Make script executable
chmod +x deploy_local.sh

# Run local deployment
./deploy_local.sh
```

This will:
- Build the Docker image locally
- Start Misi on http://localhost:8501
- Test the floating 🤖 icon and chat functionality

### Step 2: Commit and Push

```bash
# Add all changes
git add .

# Commit with descriptive message
git commit -m "feat: Add Misi AI Chatbot deployment to pipeline

- Add Misi chatbot build and deployment steps
- Integrate with existing SmartOps pipeline
- Include health checks and auto-scaling
- Update Telegram notifications"

# Push to trigger pipeline
git push origin main
```

### Step 3: Pipeline Execution

The pipeline automatically:

1. **Builds** Misi Docker image with production optimizations
2. **Pushes** to GCP Artifact Registry
3. **Deploys** to Kubernetes cluster in `smartops` namespace
4. **Scales** with HPA (2-10 replicas)
5. **Monitors** health and readiness
6. **Notifies** via Telegram on success/failure

## 📊 Kubernetes Resources

### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: misi-ai-chatbot
spec:
  replicas: 2
  selector:
    matchLabels:
      app: misi-ai-chatbot
```

**Features:**
- **2 replicas** by default
- **Resource limits**: 512Mi RAM, 500m CPU
- **Health checks**: Liveness and readiness probes
- **Auto-restart**: Always restart policy

### Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: misi-ai-chatbot-service
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 8501
```

**Features:**
- **ClusterIP** service type
- **Port 80** external, **8501** internal
- **Load balancing** across all replicas

### Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

**Features:**
- **CPU-based scaling**: Scales when CPU > 70%
- **Memory-based scaling**: Scales when memory > 80%
- **Range**: 2-10 replicas based on demand

### Ingress (Optional)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
spec:
  rules:
  - host: misi.yourdomain.com
    http:
      paths:
      - path: /
        backend:
          service:
            name: misi-ai-chatbot-service
```

**Features:**
- **Custom domain** support
- **SSL termination** ready
- **Path-based routing**

## 🔍 Monitoring and Debugging

### Check Deployment Status

```bash
# View pods
kubectl get pods -n smartops -l app=misi-ai-chatbot

# View deployment
kubectl get deployment misi-ai-chatbot -n smartops

# View service
kubectl get svc misi-ai-chatbot-service -n smartops

# View HPA
kubectl get hpa misi-ai-chatbot-hpa -n smartops
```

### View Logs

```bash
# View logs for all Misi pods
kubectl logs -f deployment/misi-ai-chatbot -n smartops

# View logs for specific pod
kubectl logs -f <pod-name> -n smartops
```

### Check Health

```bash
# Check pod health
kubectl describe pod <pod-name> -n smartops

# Check service endpoints
kubectl get endpoints misi-ai-chatbot-service -n smartops

# Test health endpoint
kubectl port-forward svc/misi-ai-chatbot-service 8080:80 -n smartops
curl http://localhost:8080/_stcore/health
```

## 🚨 Troubleshooting

### Common Issues

#### 1. **Pod Not Starting**

```bash
# Check pod events
kubectl describe pod <pod-name> -n smartops

# Check pod logs
kubectl logs <pod-name> -n smartops

# Check resource limits
kubectl top pods -n smartops
```

#### 2. **Service Not Accessible**

```bash
# Check service endpoints
kubectl get endpoints misi-ai-chatbot-service -n smartops

# Check service configuration
kubectl describe svc misi-ai-chatbot-service -n smartops

# Test internal connectivity
kubectl run test-pod --image=busybox --rm -it --restart=Never -- nslookup misi-ai-chatbot-service
```

#### 3. **HPA Not Working**

```bash
# Check HPA status
kubectl describe hpa misi-ai-chatbot-hpa -n smartops

# Check metrics server
kubectl get apiservice v1beta1.metrics.k8s.io

# Check resource usage
kubectl top pods -n smartops
```

### Debug Commands

```bash
# Get all resources for Misi
kubectl get all -l app=misi-ai-chatbot -n smartops

# Check events in namespace
kubectl get events -n smartops --sort-by='.lastTimestamp'

# Port forward to test locally
kubectl port-forward svc/misi-ai-chatbot-service 8501:80 -n smartops
```

## 📈 Scaling and Performance

### Manual Scaling

```bash
# Scale to specific number of replicas
kubectl scale deployment misi-ai-chatbot --replicas=5 -n smartops

# Scale based on CPU usage
kubectl autoscale deployment misi-ai-chatbot --cpu-percent=50 --min=2 --max=10 -n smartops
```

### Performance Monitoring

```bash
# Monitor resource usage
kubectl top pods -n smartops -l app=misi-ai-chatbot

# Monitor HPA
kubectl get hpa misi-ai-chatbot-hpa -n smartops -w

# Check pod metrics
kubectl describe hpa misi-ai-chatbot-hpa -n smartops
```

## 🔄 Updates and Rollbacks

### Update Deployment

```bash
# Update to new image
kubectl set image deployment/misi-ai-chatbot misi-chatbot=new-image:tag -n smartops

# Check rollout status
kubectl rollout status deployment/misi-ai-chatbot -n smartops
```

### Rollback

```bash
# Rollback to previous version
kubectl rollout undo deployment/misi-ai-chatbot -n smartops

# Rollback to specific revision
kubectl rollout undo deployment/misi-ai-chatbot --to-revision=2 -n smartops
```

## 🎉 Success Indicators

### ✅ Deployment Successful

- **Pods**: All replicas running and ready
- **Service**: Endpoints populated
- **HPA**: Metrics server working
- **Health**: `/health` endpoint responding
- **Pipeline**: All steps completed successfully
- **Telegram**: Success notification received

### 📊 Access Information

- **Service**: `misi-ai-chatbot-service.smartops.svc.cluster.local:80`
- **Port**: 80 (external), 8501 (internal)
- **Health**: `/_stcore/health`
- **Namespace**: `smartops`

## 🚀 Next Steps

1. **Test locally** using `./deploy_local.sh`
2. **Commit and push** to trigger pipeline
3. **Monitor deployment** via pipeline logs
4. **Verify functionality** in Kubernetes cluster
5. **Configure ingress** for external access
6. **Set up monitoring** and alerting

## 💡 Pro Tips

- **Always test locally** before pushing to pipeline
- **Monitor resource usage** to optimize HPA settings
- **Use health checks** to ensure service reliability
- **Set up logging** for debugging and monitoring
- **Configure alerts** for deployment failures

**Misi AI Chatbot is now fully integrated into your SmartOps pipeline and will automatically deploy to Kubernetes on every push!** 🎯
