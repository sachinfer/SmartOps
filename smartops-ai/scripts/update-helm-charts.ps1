# Automated Helm Charts Updater for SmartOps (PowerShell Version)
# This script automatically updates image tags in helm-charts repository and pushes changes
# to trigger ArgoCD auto-deploy. Run this after building new Docker images.

param(
    [string]$HelmChartsRepo = "https://github.com/sachinfer/helm-charts.git",
    [string]$HelmChartsPath = "smartops",
    [string]$GitUser = "SmartOps Bot",
    [string]$GitEmail = "bot@smartops.ai"
)

# Error handling
$ErrorActionPreference = "Stop"

# Function to print colored output
function Write-Status {
    param([string]$Message)
    Write-Host "🔧 $Message" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠️ $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

function Write-Header {
    param([string]$Message)
    Write-Host "🚀 $Message" -ForegroundColor Blue
}

# Function to cleanup temporary directory
function Cleanup {
    if ($TempDir -and (Test-Path $TempDir)) {
        Write-Status "Cleaning up temporary directory: $TempDir"
        Remove-Item -Path $TempDir -Recurse -Force -ErrorAction SilentlyContinue
    }
}

# Set trap to cleanup on exit
trap { Cleanup; break }

# Main execution
function Main {
    Write-Header "Starting automated Helm Charts update..."
    Write-Host "📁 Helm Charts Repo: $HelmChartsRepo"
    Write-Host "📂 Helm Charts Path: $HelmChartsPath"
    Write-Host ""

    # Check if git is available
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        Write-Error "Git is not installed. Please install git first."
        exit 1
    }

    # Check if yq is available
    if (-not (Get-Command yq -ErrorAction SilentlyContinue)) {
        Write-Warning "yq is not installed. Please install yq manually:"
        Write-Host "  - Windows: Download from https://github.com/mikefarah/yq/releases"
        Write-Host "  - Or use: winget install mikefarah.yq"
        exit 1
    }

    # Setup git configuration
    Write-Status "Setting up git configuration..."
    git config user.name $GitUser
    git config user.email $GitEmail
    Write-Success "Git configuration set"

    # Create temporary directory
    $script:TempDir = New-TemporaryFile | ForEach-Object { Remove-Item $_; New-Item -ItemType Directory -Path $_ }
    Write-Status "Created temporary directory: $TempDir"

    # Clone helm-charts repository
    Write-Status "Cloning helm-charts repository..."
    git clone --depth 1 $HelmChartsRepo $TempDir
    Write-Success "Repository cloned successfully"

    # Generate new image tags
    $Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $AnomalyTag = "v1.0.$Timestamp"
    $DashboardTag = "v1.0.$Timestamp"
    $MonitorTag = "v1.0.$Timestamp"

    Write-Status "Generated new image tags:"
    Write-Host "  - smartops-anomaly: $AnomalyTag"
    Write-Host "  - smartops-dashboard: $DashboardTag"
    Write-Host "  - smartops-monitor: $MonitorTag"
    Write-Host ""

    # Change to helm-charts directory
    Set-Location $TempDir

    # Update values files
    Write-Status "Updating values.yaml files..."

    # Update anomaly values
    $AnomalyValuesFile = Join-Path $TempDir "smartops\anomaly\values.yaml"
    if (Test-Path $AnomalyValuesFile) {
        yq eval ".image.tag = `"$AnomalyTag`"" -i $AnomalyValuesFile
        Write-Success "Updated smartops-anomaly to tag: $AnomalyTag"
    } else {
        Write-Warning "Values file not found: $AnomalyValuesFile"
    }

    # Update dashboard values
    $DashboardValuesFile = Join-Path $TempDir "smartops\dashboard\values.yaml"
    if (Test-Path $DashboardValuesFile) {
        yq eval ".image.tag = `"$DashboardTag`"" -i $DashboardValuesFile
        Write-Success "Updated smartops-dashboard to tag: $DashboardTag"
    } else {
        Write-Warning "Values file not found: $DashboardValuesFile"
    }

    # Update monitor values
    $MonitorValuesFile = Join-Path $TempDir "smartops\monitor\values.yaml"
    if (Test-Path $MonitorValuesFile) {
        yq eval ".image.tag = `"$MonitorTag`"" -i $MonitorValuesFile
        Write-Success "Updated smartops-monitor to tag: $MonitorTag"
    } else {
        Write-Warning "Values file not found: $MonitorValuesFile"
    }

    # Commit and push changes
    Write-Status "Committing and pushing changes..."
    git add .
    git commit -m "🤖 Auto-update image tags: anomaly=$AnomalyTag, dashboard=$DashboardTag, monitor=$MonitorTag"
    git push origin main
    Write-Success "Changes pushed successfully!"

    # Success message
    Write-Host ""
    Write-Success "Your helm-charts have been updated and pushed!"
    Write-Header "ArgoCD will automatically detect changes and deploy the new versions!"
    Write-Host ""
    Write-Host "📋 Summary of updates:"
    Write-Host "  - smartops-anomaly: $AnomalyTag"
    Write-Host "  - smartops-dashboard: $DashboardTag"
    Write-Host "  - smartops-monitor: $MonitorTag"
    Write-Host ""
    Write-Host "🎯 Next steps:"
    Write-Host "  1. ArgoCD will automatically sync in a few minutes"
    Write-Host "  2. Check ArgoCD UI to monitor deployment progress"
    Write-Host "  3. Verify new versions are running in your cluster"
}

# Run main function
try {
    Main
} catch {
    Write-Error "An error occurred: $($_.Exception.Message)"
    exit 1
} finally {
    Cleanup
}
