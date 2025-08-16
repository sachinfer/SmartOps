#!/bin/bash

echo "🚀 Deploying SmartOps applications via ArgoCD..."

# Apply ArgoCD applications
kubectl apply -f argocd-apps/smartops-dashboard-app.yaml
kubectl apply -f argocd-apps/smartops-monitor-app.yaml
kubectl apply -f argocd-apps/smartops-anomaly-app.yaml

echo "✅ ArgoCD applications deployed successfully!"
echo ""
echo "📊 Check ArgoCD UI to monitor deployments:"
echo "   kubectl port-forward svc/argocd-server -n argocd 8080:443"
echo ""
echo "🔍 Check application status:"
echo "   kubectl get applications -n argocd"
echo ""
echo "📝 View application logs:"
echo "   kubectl logs -n argocd -l app.kubernetes.io/name=argocd-application-controller"
