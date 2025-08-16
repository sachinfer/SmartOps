#!/bin/bash

# Automated Helm Charts Updater for SmartOps
# This script automatically updates image tags in helm-charts repository and pushes changes
# to trigger ArgoCD auto-deploy. Run this after building new Docker images.

set -e

# Configuration
HELM_CHARTS_REPO="https://github.com/sachinfer/helm-charts.git"
HELM_CHARTS_PATH="smartops"
GIT_USER="SmartOps Bot"
GIT_EMAIL="bot@smartops.ai"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}🔧${NC} $1"
}

print_success() {
    echo -e "${GREEN}✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

print_header() {
    echo -e "${BLUE}🚀${NC} $1"
}

# Function to cleanup temporary directory
cleanup() {
    if [ -n "$TEMP_DIR" ] && [ -d "$TEMP_DIR" ]; then
        print_status "Cleaning up temporary directory: $TEMP_DIR"
        rm -rf "$TEMP_DIR"
    fi
}

# Set trap to cleanup on exit
trap cleanup EXIT

# Main execution
main() {
    print_header "Starting automated Helm Charts update..."
    echo "📁 Helm Charts Repo: $HELM_CHARTS_REPO"
    echo "📂 Helm Charts Path: $HELM_CHARTS_PATH"
    echo ""

    # Check if git is available
    if ! command -v git &> /dev/null; then
        print_error "Git is not installed. Please install git first."
        exit 1
    fi

    # Check if yq is available
    if ! command -v yq &> /dev/null; then
        print_warning "yq is not installed. Installing yq..."
        if command -v brew &> /dev/null; then
            brew install yq
        elif command -v apt-get &> /dev/null; then
            sudo apt-get update && sudo apt-get install -y yq
        else
            print_error "Cannot install yq automatically. Please install yq manually."
            exit 1
        fi
    fi

    # Setup git configuration
    print_status "Setting up git configuration..."
    git config user.name "$GIT_USER"
    git config user.email "$GIT_EMAIL"
    print_success "Git configuration set"

    # Create temporary directory
    TEMP_DIR=$(mktemp -d)
    print_status "Created temporary directory: $TEMP_DIR"

    # Clone helm-charts repository
    print_status "Cloning helm-charts repository..."
    git clone --depth 1 "$HELM_CHARTS_REPO" "$TEMP_DIR"
    print_success "Repository cloned successfully"

    # Generate new image tags
    TIMESTAMP=$(date +%Y%m%d-%H%M%S)
    ANOMALY_TAG="v1.0.$TIMESTAMP"
    DASHBOARD_TAG="v1.0.$TIMESTAMP"
    MONITOR_TAG="v1.0.$TIMESTAMP"

    print_status "Generated new image tags:"
    echo "  - smartops-anomaly: $ANOMALY_TAG"
    echo "  - smartops-dashboard: $DASHBOARD_TAG"
    echo "  - smartops-monitor: $MONITOR_TAG"
    echo ""

    # Change to helm-charts directory
    cd "$TEMP_DIR"

    # Update values files
    print_status "Updating values.yaml files..."

    # Update anomaly values
    if [ -f "smartops/anomaly/values.yaml" ]; then
        yq eval ".image.tag = \"$ANOMALY_TAG\"" -i smartops/anomaly/values.yaml
        print_success "Updated smartops-anomaly to tag: $ANOMALY_TAG"
    else
        print_warning "Values file not found: smartops/anomaly/values.yaml"
    fi

    # Update dashboard values
    if [ -f "smartops/dashboard/values.yaml" ]; then
        yq eval ".image.tag = \"$DASHBOARD_TAG\"" -i smartops/dashboard/values.yaml
        print_success "Updated smartops-dashboard to tag: $DASHBOARD_TAG"
    else
        print_warning "Values file not found: smartops/dashboard/values.yaml"
    fi

    # Update monitor values
    if [ -f "smartops/monitor/values.yaml" ]; then
        yq eval ".image.tag = \"$MONITOR_TAG\"" -i smartops/monitor/values.yaml
        print_success "Updated smartops-monitor to tag: $MONITOR_TAG"
    else
        print_warning "Values file not found: smartops/monitor/values.yaml"
    fi

    # Commit and push changes
    print_status "Committing and pushing changes..."
    git add .
    git commit -m "🤖 Auto-update image tags: anomaly=$ANOMALY_TAG, dashboard=$DASHBOARD_TAG, monitor=$MONITOR_TAG"
    git push origin main
    print_success "Changes pushed successfully!"

    # Success message
    echo ""
    print_success "Your helm-charts have been updated and pushed!"
    print_header "ArgoCD will automatically detect changes and deploy the new versions!"
    echo ""
    echo "📋 Summary of updates:"
    echo "  - smartops-anomaly: $ANOMALY_TAG"
    echo "  - smartops-dashboard: $DASHBOARD_TAG"
    echo "  - smartops-monitor: $MONITOR_TAG"
    echo ""
    echo "🎯 Next steps:"
    echo "  1. ArgoCD will automatically sync in a few minutes"
    echo "  2. Check ArgoCD UI to monitor deployment progress"
    echo "  3. Verify new versions are running in your cluster"
}

# Run main function
main "$@"
