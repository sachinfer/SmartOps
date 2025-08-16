#!/bin/bash

echo "🚀 Installing ArgoCD in SmartOps cluster..."

# Create ArgoCD namespace
kubectl apply -f argocd-namespace.yaml

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for ArgoCD to be ready
echo "⏳ Waiting for ArgoCD to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/argocd-server -n argocd

# Get ArgoCD admin password
echo "🔐 ArgoCD admin password:"
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
echo ""

# Port forward ArgoCD server
echo "🌐 ArgoCD UI will be available at: http://localhost:8080"
echo "Username: admin"
echo "Password: (see above)"
echo ""
echo "Press Ctrl+C to stop port forwarding"
kubectl port-forward svc/argocd-server -n argocd 8080:443
