# SmartOps Helm Chart Deployment Script for PowerShell
# This script deploys the SmartOps application using Helm

param(
    [string]$ReleaseName = "smartops",
    [string]$Namespace = "smartops",
    [string]$ChartPath = ".",
    [string]$ValuesFile = "",
    [switch]$DryRun,
    [switch]$Upgrade,
    [switch]$Help
)

# Function to print colored output
function Write-Status {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Function to show usage
function Show-Usage {
    Write-Host "Usage: .\deploy.ps1 [OPTIONS]" -ForegroundColor White
    Write-Host ""
    Write-Host "Options:" -ForegroundColor White
    Write-Host "  -ReleaseName NAME     Release name (default: smartops)" -ForegroundColor White
    Write-Host "  -Namespace NAME       Kubernetes namespace (default: smartops)" -ForegroundColor White
    Write-Host "  -ChartPath PATH       Chart path (default: .)" -ForegroundColor White
    Write-Host "  -ValuesFile FILE      Values file to use" -ForegroundColor White
    Write-Host "  -DryRun               Dry run mode" -ForegroundColor White
    Write-Host "  -Upgrade              Upgrade existing release" -ForegroundColor White
    Write-Host "  -Help                 Show this help message" -ForegroundColor White
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor White
    Write-Host "  .\deploy.ps1                                    # Deploy with default values" -ForegroundColor White
    Write-Host "  .\deploy.ps1 -ValuesFile custom-values.yaml     # Deploy with custom values" -ForegroundColor White
    Write-Host "  .\deploy.ps1 -ReleaseName my-smartops -Namespace my-namespace" -ForegroundColor White
    Write-Host "  .\deploy.ps1 -Upgrade                           # Upgrade existing release" -ForegroundColor White
    Write-Host "  .\deploy.ps1 -DryRun                            # Dry run mode" -ForegroundColor White
}

# Function to check prerequisites
function Test-Prerequisites {
    Write-Status "Checking prerequisites..."
    
    # Check if kubectl is installed
    try {
        $null = Get-Command kubectl -ErrorAction Stop
        Write-Success "kubectl found"
    }
    catch {
        Write-Error "kubectl is not installed. Please install kubectl first."
        exit 1
    }
    
    # Check if helm is installed
    try {
        $null = Get-Command helm -ErrorAction Stop
        Write-Success "Helm found"
    }
    catch {
        Write-Error "Helm is not installed. Please install Helm first."
        exit 1
    }
    
    # Check if kubectl can connect to cluster
    try {
        $null = kubectl cluster-info 2>$null
        Write-Success "Connected to Kubernetes cluster"
    }
    catch {
        Write-Error "Cannot connect to Kubernetes cluster. Please check your kubectl configuration."
        exit 1
    }
    
    Write-Success "Prerequisites check passed"
}

# Function to create namespace
function New-NamespaceIfNotExists {
    $namespaceExists = kubectl get namespace $Namespace 2>$null
    if (-not $namespaceExists) {
        Write-Status "Creating namespace: $Namespace"
        kubectl create namespace $Namespace
        Write-Success "Namespace created: $Namespace"
    }
    else {
        Write-Status "Namespace already exists: $Namespace"
    }
}

# Function to deploy the chart
function Deploy-Chart {
    $helmArgs = @()
    
    if ($Upgrade) {
        $helmCmd = "helm upgrade"
        $helmArgs += @($ReleaseName, $ChartPath)
    }
    else {
        $helmCmd = "helm install"
        $helmArgs += @($ReleaseName, $ChartPath)
    }
    
    $helmArgs += @("--namespace", $Namespace)
    
    if ($ValuesFile -and (Test-Path $ValuesFile)) {
        $helmArgs += @("-f", $ValuesFile)
    }
    
    if ($DryRun) {
        $helmArgs += "--dry-run"
    }
    
    Write-Status "Deploying SmartOps chart..."
    Write-Status "Command: $helmCmd $($helmArgs -join ' ')"
    
    try {
        & $helmCmd @helmArgs
        if ($LASTEXITCODE -eq 0) {
            if ($DryRun) {
                Write-Success "Dry run completed successfully"
            }
            else {
                Write-Success "SmartOps deployed successfully!"
                Write-Status "Release name: $ReleaseName"
                Write-Status "Namespace: $Namespace"
                
                if (-not $Upgrade) {
                    Write-Host ""
                    Write-Status "To check the status:"
                    Write-Host "  helm status $ReleaseName -n $Namespace" -ForegroundColor White
                    Write-Host ""
                    Write-Status "To access the dashboard:"
                    Write-Host "  kubectl get svc -n $Namespace" -ForegroundColor White
                    Write-Host "  kubectl port-forward -n $Namespace svc/${ReleaseName}-dashboard-service 8501:80" -ForegroundColor White
                    Write-Host ""
                    Write-Status "To view logs:"
                    Write-Host "  kubectl logs -n $Namespace deployment/${ReleaseName}-dashboard" -ForegroundColor White
                    Write-Host "  kubectl logs -n $Namespace deployment/${ReleaseName}-anomaly" -ForegroundColor White
                }
            }
        }
        else {
            Write-Error "Deployment failed with exit code: $LASTEXITCODE"
            exit 1
        }
    }
    catch {
        Write-Error "Deployment failed: $($_.Exception.Message)"
        exit 1
    }
}

# Main execution
function Main {
    if ($Help) {
        Show-Usage
        return
    }
    
    Write-Status "Starting SmartOps deployment..."
    Write-Status "Release name: $ReleaseName"
    Write-Status "Namespace: $Namespace"
    Write-Status "Chart path: $ChartPath"
    if ($ValuesFile) {
        Write-Status "Values file: $ValuesFile"
    }
    if ($DryRun) {
        Write-Status "Dry run mode enabled"
    }
    if ($Upgrade) {
        Write-Status "Upgrade mode enabled"
    }
    Write-Host ""
    
    Test-Prerequisites
    New-NamespaceIfNotExists
    Deploy-Chart
    
    Write-Success "Deployment script completed!"
}

# Run main function
Main
