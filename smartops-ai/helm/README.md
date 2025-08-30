# SmartOps Helm Chart

This Helm chart deploys the SmartOps AI-powered Kubernetes operations and anomaly detection platform.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+
- kubectl configured to communicate with your cluster

## Installation

### From GitHub Raw URL (Recommended for Open Source)

```bash
# Add the SmartOps repository
helm repo add smartops https://raw.githubusercontent.com/sachinfer/SmartOps/main/smartops-ai/helm

# Install the chart
helm install smartops smartops/smartops --namespace smartops --create-namespace

# Or install with custom values
helm install smartops smartops/smartops --namespace smartops --create-namespace -f values.yaml
```

### From Local Chart

```bash
# Clone the repository
git clone https://github.com/sachinfer/SmartOps.git
cd SmartOps/smartops-ai/helm

# Install the chart
helm install smartops . --namespace smartops --create-namespace
```

### Using kubectl apply (Alternative)

```bash
# Deploy directly using kubectl
kubectl apply -f https://raw.githubusercontent.com/sachinfer/SmartOps/main/smartops-ai/helm/templates/

# Or clone and apply
git clone https://github.com/sachinfer/SmartOps.git
cd SmartOps/smartops-ai/helm
helm template . | kubectl apply -f -
```

## Configuration

The following table lists the configurable parameters of the SmartOps chart and their default values.

| Parameter | Description | Default |
|-----------|-------------|---------|
| `global.namespace` | Kubernetes namespace | `smartops` |
| `dashboard.enabled` | Enable dashboard deployment | `true` |
| `dashboard.replicaCount` | Number of dashboard replicas | `1` |
| `dashboard.image.repository` | Dashboard image repository | `smartops-dashboard` |
| `dashboard.image.tag` | Dashboard image tag | `latest` |
| `dashboard.service.type` | Dashboard service type | `LoadBalancer` |
| `anomaly.enabled` | Enable anomaly detection | `true` |
| `anomaly.image.repository` | Anomaly detection image | `us-docker.pkg.dev/icbt-465109/smartops-repo/smartops-anomaly` |
| `monitor.enabled` | Enable monitoring cronjob | `true` |
| `monitor.cronjob.schedule` | Monitoring schedule | `*/5 * * * *` |

### Custom Values

Create a `custom-values.yaml` file:

```yaml
global:
  namespace: my-smartops

dashboard:
  image:
    repository: my-registry/smartops-dashboard
    tag: v1.0.0
  
  service:
    type: NodePort

anomaly:
  image:
    repository: my-registry/smartops-anomaly
    tag: v1.0.0
```

Install with custom values:

```bash
helm install smartops . --namespace smartops --create-namespace -f custom-values.yaml
```

## Components

### Dashboard
- **Streamlit-based UI** for real-time monitoring
- **LoadBalancer service** for external access
- **Persistent storage** for data retention
- **RBAC** for secure cluster access

### Anomaly Detection
- **FastAPI backend** for ML predictions
- **Sidecar pattern** with anomaly loop
- **Isolation Forest** ML model
- **Real-time monitoring** of cluster resources

### Monitor
- **CronJob-based** metrics collection
- **Configurable schedule** (default: every 5 minutes)
- **Resource monitoring** and logging

## Accessing the Dashboard

### LoadBalancer (Default)
```bash
kubectl get svc -n smartops smartops-dashboard-service
```

### Port Forward
```bash
kubectl port-forward -n smartops svc/smartops-dashboard-service 8501:80
```

Then open http://localhost:8501 in your browser.

## Upgrading

```bash
# Update the repository
helm repo update smartops

# Upgrade the release
helm upgrade smartops smartops/smartops --namespace smartops
```

## Uninstalling

```bash
helm uninstall smartops --namespace smartops
kubectl delete namespace smartops
```

## Troubleshooting

### Check Pod Status
```bash
kubectl get pods -n smartops
kubectl describe pod <pod-name> -n smartops
```

### Check Logs
```bash
kubectl logs -n smartops deployment/smartops-dashboard
kubectl logs -n smartops deployment/smartops-anomaly
```

### Check Services
```bash
kubectl get svc -n smartops
kubectl describe svc <service-name> -n smartops
```

### Check RBAC
```bash
kubectl get serviceaccounts -n smartops
kubectl get roles -n smartops
kubectl get rolebindings -n smartops
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test the chart locally
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- GitHub Issues: [https://github.com/sachinfer/SmartOps/issues](https://github.com/sachinfer/SmartOps/issues)
- Documentation: [https://github.com/sachinfer/SmartOps](https://github.com/sachinfer/SmartOps)
