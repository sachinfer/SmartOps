# Setup Helm Charts Repository Script
# This script copies the helm chart files to your existing helm-charts repository

param(
    [string]$HelmChartsPath = "C:\Sachin\Git\helm-charts",
    [string]$SourcePath = "C:\Sachin\Git\SmartOps\smartops-ai\helm-charts-setup"
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
Write-Header "Setting up Helm Charts Repository..."

# Check if helm-charts directory exists
if (-not (Test-Path $HelmChartsPath)) {
    Write-Error "Helm charts directory not found: $HelmChartsPath"
    Write-Host "Please update the HelmChartsPath parameter to point to your helm-charts repository"
    exit 1
}

# Check if source directory exists
if (-not (Test-Path $SourcePath)) {
    Write-Error "Source directory not found: $SourcePath"
    exit 1
}

Write-Status "Copying helm chart files to: $HelmChartsPath"

# Create smartops directory structure
$SmartOpsPath = Join-Path $HelmChartsPath "smartops"
if (-not (Test-Path $SmartOpsPath)) {
    New-Item -ItemType Directory -Path $SmartOpsPath -Force
    Write-Success "Created smartops directory"
}

# Copy anomaly files
$AnomalyPath = Join-Path $SmartOpsPath "anomaly"
if (-not (Test-Path $AnomalyPath)) {
    New-Item -ItemType Directory -Path $AnomalyPath -Force
}
Copy-Item -Path "$SourcePath\smartops\anomaly\*" -Destination $AnomalyPath -Recurse -Force
Write-Success "Copied anomaly helm chart files"

# Copy dashboard files
$DashboardPath = Join-Path $SmartOpsPath "dashboard"
if (-not (Test-Path $DashboardPath)) {
    New-Item -ItemType Directory -Path $DashboardPath -Force
}
Copy-Item -Path "$SourcePath\smartops\dashboard\*" -Destination $DashboardPath -Recurse -Force
Write-Success "Copied dashboard helm chart files"

# Copy monitor files
$MonitorPath = Join-Path $SmartOpsPath "monitor"
if (-not (Test-Path $MonitorPath)) {
    New-Item -ItemType Directory -Path $MonitorPath -Force
}
Copy-Item -Path "$SourcePath\smartops\monitor\*" -Destination $MonitorPath -Recurse -Force
Write-Success "Copied monitor helm chart files"

Write-Host ""
Write-Success "Helm charts setup completed!"
Write-Host ""
Write-Host "📋 Next steps:"
Write-Host "1. Navigate to your helm-charts repository:"
Write-Host "   cd $HelmChartsPath"
Write-Host ""
Write-Host "2. Check the files:"
Write-Host "   ls smartops"
Write-Host ""
Write-Host "3. Commit and push changes:"
Write-Host "   git add ."
Write-Host "   git commit -m 'Add SmartOps helm charts'"
Write-Host "   git push origin main"
Write-Host ""
Write-Host "4. ArgoCD will automatically detect and sync the new charts!"
Write-Host ""
Write-Host "🎯 Your helm-charts repository is now ready for automated deployments!"
