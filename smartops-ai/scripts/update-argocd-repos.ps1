# Update ArgoCD Repository URLs Script
# This script updates your ArgoCD applications to point to the correct helm-charts repository

param(
    [string]$KubeConfig = "",
    [string]$ArgoCDNamespace = "argocd"
)

# Colors for output
$Red = 'Red'
$Green = 'Green'
$Yellow = 'Yellow'
$Blue = 'Blue'

function Write-Status {
    param([string]$Message)
    Write-Host "🔧 $Message" -ForegroundColor $Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor $Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠️ $Message" -ForegroundColor $Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor $Red
}

function Write-Header {
    param([string]$Message)
    Write-Host "🚀 $Message" -ForegroundColor $Blue
}

# Main execution
Write-Header "Updating ArgoCD Repository URLs..."

# Check if kubectl is available
if (-not (Get-Command kubectl -ErrorAction SilentlyContinue)) {
    Write-Error "kubectl is not installed. Please install kubectl first."
    exit 1
}

# Check if ArgoCD namespace exists
Write-Status "Checking ArgoCD namespace..."
try {
    $namespace = kubectl get namespace $ArgoCDNamespace --ignore-not-found
    if (-not $namespace) {
        Write-Error "ArgoCD namespace '$ArgoCDNamespace' not found."
        Write-Host "Please ensure ArgoCD is installed and running."
        exit 1
    }
    Write-Success "ArgoCD namespace found: $ArgoCDNamespace"
} catch {
    Write-Error "Failed to check ArgoCD namespace: $_"
    exit 1
}

# Check current ArgoCD applications
Write-Status "Checking current ArgoCD applications..."
try {
    $applications = kubectl get applications -n $ArgoCDNamespace -o name
    if (-not $applications) {
        Write-Warning "No ArgoCD applications found in namespace: $ArgoCDNamespace"
        Write-Host "You may need to create the applications first."
        exit 1
    }
    Write-Success "Found ArgoCD applications:"
    $applications | ForEach-Object { Write-Host "  - $_" }
} catch {
    Write-Error "Failed to get ArgoCD applications: $_"
    exit 1
}

# Update repository URLs for each application
$applicationsToUpdate = @(
    "smartops-anomaly",
    "smartops-dashboard", 
    "smartops-monitor"
)

Write-Status "Updating repository URLs to point to helm-charts repository..."

foreach ($app in $applicationsToUpdate) {
    Write-Status "Updating $app..."
    
    try {
        # Get current application configuration
        $currentApp = kubectl get application $app -n $ArgoCDNamespace -o yaml
        
        # Check if repoURL needs updating
        if ($currentApp -match "repoURL: https://github.com/sachinfer/SmartOps.git") {
            Write-Warning "Updating $app repository URL from SmartOps to helm-charts..."
            
            # Update the repository URL
            kubectl patch application $app -n $ArgoCDNamespace --type='merge' -p="{\"spec\":{\"source\":{\"repoURL\":\"https://github.com/sachinfer/helm-charts.git\"}}}"
            
            Write-Success "Updated $app repository URL to helm-charts"
        } else {
            Write-Success "$app already points to correct repository"
        }
        
        # Update the path to point to smartops subdirectory
        Write-Status "Updating $app chart path..."
        kubectl patch application $app -n $ArgoCDNamespace --type='merge' -p="{\"spec\":{\"source\":{\"path\":\"smartops/$($app.Split('-')[1])\"}}}"
        
        Write-Success "Updated $app chart path"
        
    } catch {
        Write-Error "Failed to update $app : $_"
    }
}

Write-Host ""
Write-Success "ArgoCD repository URLs updated successfully!"
Write-Host ""
Write-Host "📋 Verification steps:"
Write-Host "1. Check ArgoCD applications:"
Write-Host "   kubectl get applications -n $ArgoCDNamespace"
Write-Host ""
Write-Host "2. Check application details:"
Write-Host "   kubectl get application smartops-dashboard -n $ArgoCDNamespace -o yaml"
Write-Host ""
Write-Host "3. Force sync applications:"
Write-Host "   kubectl patch application smartops-dashboard -n $ArgoCDNamespace --type='merge' -p='{\"spec\":{\"syncPolicy\":{\"automated\":{\"prune\":true,\"selfHeal\":true}}}}'"
Write-Host ""
Write-Host "🎯 Your ArgoCD applications now point to the correct helm-charts repository!"
Write-Host "🔄 They will automatically sync with your helm charts when you push changes!"
