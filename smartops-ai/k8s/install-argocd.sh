#!/bin/bash

echo "🚀 Installing ArgoCD in SmartOps cluster..."

# Create ArgoCD namespace
kubectl apply -f argocd-namespace.yaml

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for ArgoCD to be ready
echo "⏳ Waiting for ArgoCD to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/argocd-server -n argocd

# Apply LoadBalancer service
echo "🌐 Setting up LoadBalancer for ArgoCD UI..."
kubectl apply -f argocd-loadbalancer.yaml

# Wait for LoadBalancer to get external IP
echo "⏳ Waiting for LoadBalancer to get external IP..."
kubectl wait --for=condition=available --timeout=300s service/argocd-server-loadbalancer -n argocd

# Get the external IP
echo "🔍 Getting LoadBalancer external IP..."
EXTERNAL_IP=""
while [ -z "$EXTERNAL_IP" ]; do
    EXTERNAL_IP=$(kubectl get service argocd-server-loadbalancer -n argocd -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null)
    if [ -z "$EXTERNAL_IP" ]; then
        echo "Waiting for external IP to be assigned..."
        sleep 10
    fi
done

# Get ArgoCD admin password
echo "🔐 ArgoCD admin password:"
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
echo ""

echo "🎉 ArgoCD installation completed!"
echo ""
echo "🌐 ArgoCD UI is available at:"
echo "   HTTP:  http://$EXTERNAL_IP"
echo "   HTTPS: https://$EXTERNAL_IP"
echo ""
echo "👤 Login credentials:"
echo "   Username: admin"
echo "   Password: (see above)"
echo ""
echo "📊 To check LoadBalancer status:"
echo "   kubectl get service argocd-server-loadbalancer -n argocd"
echo ""
echo "🔍 To view ArgoCD logs:"
echo "   kubectl logs -n argocd deployment/argocd-server"
