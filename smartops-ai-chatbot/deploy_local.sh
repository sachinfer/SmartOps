#!/bin/bash

# Local Deployment Script for Misi AI Chatbot
# This script helps you test Misi locally before pushing to the pipeline

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Local Deployment Script for Misi AI Chatbot${NC}"
echo "=================================================="

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo -e "${RED}❌ Docker is not running. Please start Docker first.${NC}"
    exit 1
fi

# Build the production image locally
echo -e "${YELLOW}🐳 Building Misi AI Chatbot Docker image...${NC}"
docker build -f Dockerfile.production -t misi-ai-chatbot:local .

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Docker image built successfully${NC}"
else
    echo -e "${RED}❌ Failed to build Docker image${NC}"
    exit 1
fi

# Test the image locally
echo -e "${YELLOW}🧪 Testing Misi AI Chatbot locally...${NC}"
echo -e "${BLUE}Starting container on port 8501...${NC}"
echo -e "${BLUE}Access Misi at: http://localhost:8501${NC}"
echo -e "${BLUE}Press Ctrl+C to stop the container${NC}"
echo ""

# Run the container
docker run --rm -p 8501:8501 \
    -e STREAMLIT_SERVER_PORT=8501 \
    -e STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    -e STREAMLIT_SERVER_HEADLESS=true \
    -e STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    misi-ai-chatbot:local

echo ""
echo -e "${GREEN}✅ Local deployment completed!${NC}"
echo ""
echo -e "${BLUE}📋 Next Steps:${NC}"
echo "1. Test Misi chatbot at http://localhost:8501"
echo "2. Verify the floating 🤖 icon appears"
echo "3. Test chat functionality"
echo "4. If everything works, commit and push to trigger the pipeline"
echo ""
echo -e "${BLUE}🔧 Pipeline will automatically:${NC}"
echo "• Build and push Docker image to GCP Artifact Registry"
echo "• Deploy to Kubernetes cluster in 'smartops' namespace"
echo "• Scale with HPA (2-10 replicas)"
echo "• Configure health checks and monitoring"
