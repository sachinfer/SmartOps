#!/bin/bash

# SmartOps Helm Chart Deployment Script
# This script deploys the SmartOps application using Helm

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
RELEASE_NAME="smartops"
NAMESPACE="smartops"
CHART_PATH="."
VALUES_FILE=""
DRY_RUN=false
UPGRADE=false

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -r, --release-name NAME    Release name (default: smartops)"
    echo "  -n, --namespace NAME       Kubernetes namespace (default: smartops)"
    echo "  -f, --values FILE          Values file to use"
    echo "  -d, --dry-run              Dry run mode"
    echo "  -u, --upgrade              Upgrade existing release"
    echo "  -h, --help                 Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                                    # Deploy with default values"
    echo "  $0 -f custom-values.yaml             # Deploy with custom values"
    echo "  $0 -r my-smartops -n my-namespace    # Deploy with custom release name and namespace"
    echo "  $0 -u                                # Upgrade existing release"
    echo "  $0 -d                                # Dry run mode"
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check if kubectl is installed
    if ! command -v kubectl &> /dev/null; then
        print_error "kubectl is not installed. Please install kubectl first."
        exit 1
    fi
    
    # Check if helm is installed
    if ! command -v helm &> /dev/null; then
        print_error "Helm is not installed. Please install Helm first."
        exit 1
    fi
    
    # Check if kubectl can connect to cluster
    if ! kubectl cluster-info &> /dev/null; then
        print_error "Cannot connect to Kubernetes cluster. Please check your kubectl configuration."
        exit 1
    fi
    
    print_success "Prerequisites check passed"
}

# Function to create namespace
create_namespace() {
    if ! kubectl get namespace $NAMESPACE &> /dev/null; then
        print_status "Creating namespace: $NAMESPACE"
        kubectl create namespace $NAMESPACE
        print_success "Namespace created: $NAMESPACE"
    else
        print_status "Namespace already exists: $NAMESPACE"
    fi
}

# Function to deploy the chart
deploy_chart() {
    local helm_cmd="helm"
    local args=()
    
    if [ "$UPGRADE" = true ]; then
        helm_cmd="helm upgrade"
        args+=("$RELEASE_NAME" "$CHART_PATH")
    else
        helm_cmd="helm install"
        args+=("$RELEASE_NAME" "$CHART_PATH")
    fi
    
    args+=("--namespace" "$NAMESPACE")
    
    if [ -n "$VALUES_FILE" ]; then
        args+=("-f" "$VALUES_FILE")
    fi
    
    if [ "$DRY_RUN" = true ]; then
        args+=("--dry-run")
    fi
    
    print_status "Deploying SmartOps chart..."
    print_status "Command: $helm_cmd ${args[*]}"
    
    if $helm_cmd "${args[@]}"; then
        if [ "$DRY_RUN" = true ]; then
            print_success "Dry run completed successfully"
        else
            print_success "SmartOps deployed successfully!"
            print_status "Release name: $RELEASE_NAME"
            print_status "Namespace: $NAMESPACE"
            
            if [ "$UPGRADE" = false ]; then
                echo ""
                print_status "To check the status:"
                echo "  helm status $RELEASE_NAME -n $NAMESPACE"
                echo ""
                print_status "To access the dashboard:"
                echo "  kubectl get svc -n $NAMESPACE"
                echo "  kubectl port-forward -n $NAMESPACE svc/${RELEASE_NAME}-dashboard-service 8501:80"
                echo ""
                print_status "To view logs:"
                echo "  kubectl logs -n $NAMESPACE deployment/${RELEASE_NAME}-dashboard"
                echo "  kubectl logs -n $NAMESPACE deployment/${RELEASE_NAME}-anomaly"
            fi
        fi
    else
        print_error "Deployment failed!"
        exit 1
    fi
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -r|--release-name)
            RELEASE_NAME="$2"
            shift 2
            ;;
        -n|--namespace)
            NAMESPACE="$2"
            shift 2
            ;;
        -f|--values)
            VALUES_FILE="$2"
            shift 2
            ;;
        -d|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -u|--upgrade)
            UPGRADE=true
            shift
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Main execution
main() {
    print_status "Starting SmartOps deployment..."
    print_status "Release name: $RELEASE_NAME"
    print_status "Namespace: $NAMESPACE"
    if [ -n "$VALUES_FILE" ]; then
        print_status "Values file: $VALUES_FILE"
    fi
    if [ "$DRY_RUN" = true ]; then
        print_status "Dry run mode enabled"
    fi
    if [ "$UPGRADE" = true ]; then
        print_status "Upgrade mode enabled"
    fi
    echo ""
    
    check_prerequisites
    create_namespace
    deploy_chart
    
    print_success "Deployment script completed!"
}

# Run main function
main
