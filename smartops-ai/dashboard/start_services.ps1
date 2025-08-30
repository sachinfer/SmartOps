# �� SmartOps Dashboard Services Startup Script for PowerShell
# ===========================================================

Write-Host "🚀 SmartOps Dashboard Services Startup Script" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from https://python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if we're in the right directory
Write-Host "Checking required files..." -ForegroundColor Yellow

if (-not (Test-Path "event_api.py")) {
    Write-Host "❌ ERROR: event_api.py not found!" -ForegroundColor Red
    Write-Host "Expected files: event_api.py, main.py" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

if (-not (Test-Path "main.py")) {
    Write-Host "❌ ERROR: main.py not found!" -ForegroundColor Red
    Write-Host "Expected files: event_api.py, main.py" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ All required files found!" -ForegroundColor Green
Write-Host ""

# Check dependencies
Write-Host "Checking dependencies..." -ForegroundColor Yellow
try {
    python -c "import fastapi, streamlit, kubernetes" 2>$null
    Write-Host "✅ All required dependencies are available" -ForegroundColor Green
} catch {
    Write-Host "❌ Missing dependencies. Installing..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "✅ Dependencies installed" -ForegroundColor Green
}

# Check if ports are available
Write-Host "Checking port availability..." -ForegroundColor Yellow
$port8000 = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
$port8501 = Get-NetTCPConnection -LocalPort 8501 -ErrorAction SilentlyContinue

if ($port8000) {
    Write-Host "❌ Port 8000 is already in use" -ForegroundColor Red
    Write-Host "Please stop the existing service first" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

if ($port8501) {
    Write-Host "❌ Port 8501 is already in use" -ForegroundColor Red
    Write-Host "Please stop the existing service first" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ Ports 8000 and 8501 are available" -ForegroundColor Green

# Start FastAPI backend
Write-Host "🚀 Starting FastAPI backend service..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; python -m uvicorn event_api:app --host 0.0.0.0 --port 8000 --reload" -WindowStyle Normal

# Wait a moment for FastAPI to start
Write-Host "⏳ Waiting for FastAPI to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Start Streamlit frontend
Write-Host "🎨 Starting Streamlit frontend service..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; streamlit run main.py --server.port=8501 --server.address=0.0.0.0" -WindowStyle Normal

Write-Host ""
Write-Host "🎉 All services started successfully!" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
Write-Host "📊 Dashboard: http://localhost:8501" -ForegroundColor Cyan
Write-Host "🔌 API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Services are running in separate windows" -ForegroundColor Yellow
Write-Host "   Close those windows to stop the services" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Enter to open the dashboard in your browser..." -ForegroundColor Yellow
Read-Host

# Open dashboard in default browser
Start-Process "http://localhost:8501"

Write-Host "Dashboard opened in browser!" -ForegroundColor Green
Write-Host "Keep this window open to monitor the services" -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to exit"
