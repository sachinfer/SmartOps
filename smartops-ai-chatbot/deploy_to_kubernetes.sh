#!/bin/bash

# Misi AI Chatbot Kubernetes Deployment Script
# This script deploys Misi AI chatbot to your Kubernetes cluster

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="misi-ai-chatbot"
IMAGE_TAG="latest"
REGISTRY="your-registry.com"  # Replace with your registry
NAMESPACE="smartops"
DEPLOYMENT_FILE="k8s/misi-chatbot-deployment.yaml"

echo -e "${BLUE}🚀 Deploying Misi AI Chatbot to Kubernetes${NC}"
echo "=================================================="

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}❌ kubectl is not installed. Please install kubectl first.${NC}"
    exit 1
fi

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Check if we're connected to a cluster
echo -e "${YELLOW}🔍 Checking Kubernetes cluster connection...${NC}"
if ! kubectl cluster-info &> /dev/null; then
    echo -e "${RED}❌ Not connected to Kubernetes cluster. Please connect first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Connected to Kubernetes cluster${NC}"
echo -e "Cluster: $(kubectl config current-context)"

# Create namespace if it doesn't exist
echo -e "${YELLOW}📁 Creating namespace if it doesn't exist...${NC}"
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Build Docker image
echo -e "${YELLOW}🐳 Building Docker image...${NC}"
docker build -f Dockerfile.production -t $IMAGE_NAME:$IMAGE_TAG .

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Docker image built successfully${NC}"
else
    echo -e "${RED}❌ Failed to build Docker image${NC}"
    exit 1
fi

# Tag image for registry (if using external registry)
if [ "$REGISTRY" != "your-registry.com" ]; then
    echo -e "${YELLOW}🏷️  Tagging image for registry...${NC}"
    docker tag $IMAGE_NAME:$IMAGE_TAG $REGISTRY/$IMAGE_NAME:$IMAGE_TAG
    
    # Push to registry
    echo -e "${YELLOW}📤 Pushing image to registry...${NC}"
    docker push $REGISTRY/$IMAGE_NAME:$IMAGE_TAG
    
    # Update deployment file with registry image
    sed -i "s|image: $IMAGE_NAME:$IMAGE_TAG|image: $REGISTRY/$IMAGE_NAME:$IMAGE_TAG|g" $DEPLOYMENT_FILE
fi

# Apply Kubernetes manifests
echo -e "${YELLOW}📋 Applying Kubernetes manifests...${NC}"
kubectl apply -f $DEPLOYMENT_FILE -n $NAMESPACE

# Wait for deployment to be ready
echo -e "${YELLOW}⏳ Waiting for deployment to be ready...${NC}"
kubectl wait --for=condition=available --timeout=300s deployment/misi-ai-chatbot -n $NAMESPACE

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Deployment is ready${NC}"
else
    echo -e "${RED}❌ Deployment failed to become ready${NC}"
    echo -e "${YELLOW}🔍 Checking deployment status...${NC}"
    kubectl describe deployment misi-ai-chatbot -n $NAMESPACE
    kubectl get pods -n $NAMESPACE -l app=misi-ai-chatbot
    exit 1
fi

# Show deployment status
echo -e "${GREEN}📊 Deployment Status:${NC}"
kubectl get pods -n $NAMESPACE -l app=misi-ai-chatbot

echo -e "${GREEN}🌐 Service Status:${NC}"
kubectl get svc -n $NAMESPACE -l app=misi-ai-chatbot

echo -e "${GREEN}📈 HPA Status:${NC}"
kubectl get hpa -n $NAMESPACE -l app=misi-ai-chatbot

# Get service URL
echo -e "${GREEN}🔗 Access Information:${NC}"
echo "Service: misi-ai-chatbot-service"
echo "Port: 80"
echo "Target Port: 8501"

# If using LoadBalancer or NodePort, show external IP
SERVICE_TYPE=$(kubectl get svc misi-ai-chatbot-service -n $NAMESPACE -o jsonpath='{.spec.type}')
if [ "$SERVICE_TYPE" = "LoadBalancer" ]; then
    echo -e "${YELLOW}⏳ Waiting for LoadBalancer external IP...${NC}"
    kubectl wait --for=condition=Ready --timeout=300s service/misi-ai-chatbot-service -n $NAMESPACE
    EXTERNAL_IP=$(kubectl get svc misi-ai-chatbot-service -n $NAMESPACE -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
    if [ ! -z "$EXTERNAL_IP" ]; then
        echo -e "${GREEN}🌍 External IP: $EXTERNAL_IP${NC}"
        echo -e "${GREEN}🔗 Access URL: http://$EXTERNAL_IP${NC}"
    fi
fi

echo ""
echo -e "${GREEN}🎉 Misi AI Chatbot deployed successfully to Kubernetes!${NC}"
echo ""
echo -e "${BLUE}📋 Next Steps:${NC}"
echo "1. Configure your ingress controller if using Ingress"
echo "2. Set up DNS pointing to your cluster"
echo "3. Test the chatbot by accessing the service"
echo "4. Monitor logs: kubectl logs -f deployment/misi-ai-chatbot -n $NAMESPACE"
echo ""
echo -e "${BLUE}🔧 Useful Commands:${NC}"
echo "View pods: kubectl get pods -n $NAMESPACE -l app=misi-ai-chatbot"
echo "View logs: kubectl logs -f deployment/misi-ai-chatbot -n $NAMESPACE"
echo "Scale up: kubectl scale deployment misi-ai-chatbot --replicas=5 -n $NAMESPACE"
echo "Delete deployment: kubectl delete -f $DEPLOYMENT_FILE -n $NAMESPACE"
