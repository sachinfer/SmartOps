# 🚀 SmartOps Dashboard Startup Script for Windows PowerShell
# =========================================================

Write-Host "🚀 SmartOps Dashboard Startup Script for Windows PowerShell" -ForegroundColor Green
Write-Host "=========================================================" -ForegroundColor Green

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
if (-not (Test-Path "event_api.py")) {
    Write-Host "❌ Please run this script from the dashboard directory" -ForegroundColor Red
    Write-Host "Expected files: event_api.py, pages/1_Overview.py" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

if (-not (Test-Path "main_app.py")) {
    Write-Host "❌ Please run this script from the dashboard directory" -ForegroundColor Red
    Write-Host "Expected files: event_api.py, main_app.py" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ In correct directory" -ForegroundColor Green

# Check dependencies
Write-Host "Checking dependencies..." -ForegroundColor Yellow
try {
    python -c "import fastapi, streamlit, kubernetes" 2>$null
    Write-Host "✅ All required dependencies are available" -ForegroundColor Green
} catch {
    Write-Host "❌ Missing dependencies. Installing..." -ForegroundColor Yellow
    try {
        pip install -r requirements.txt
        Write-Host "✅ Dependencies installed" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
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
$fastapiJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    python -m uvicorn event_api:app --host 0.0.0.0 --port 8000 --reload
}

# Wait a moment for FastAPI to start
Start-Sleep -Seconds 3

# Start Streamlit frontend
Write-Host "🎨 Starting Streamlit frontend service..." -ForegroundColor Yellow
$streamlitJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    streamlit run main_app.py --server.port=8501 --server.address=0.0.0.0
}

Write-Host ""
Write-Host "🎉 All services started successfully!" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
Write-Host "📊 Dashboard: http://localhost:8501" -ForegroundColor Cyan
Write-Host "🔌 API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Services are running in background jobs" -ForegroundColor Yellow
Write-Host "   Use Get-Job to see running jobs" -ForegroundColor Yellow
Write-Host "   Use Stop-Job to stop services" -ForegroundColor Yellow
Write-Host ""

# Wait for services to be ready
Write-Host "Waiting for services to be ready..." -ForegroundColor Yellow
$maxAttempts = 30
$attempts = 0

while ($attempts -lt $maxAttempts) {
    try {
        $apiResponse = Invoke-RestMethod -Uri "http://localhost:8000/" -Method Get -TimeoutSec 2
        $streamlitResponse = Invoke-WebRequest -Uri "http://localhost:8501/" -Method Get -TimeoutSec 2
        
        if ($apiResponse.status -eq "healthy" -and $streamlitResponse.StatusCode -eq 200) {
            Write-Host "✅ All services are ready!" -ForegroundColor Green
            break
        }
    } catch {
        # Service not ready yet
    }
    
    $attempts++
    Start-Sleep -Seconds 1
    Write-Progress -Activity "Starting services" -Status "Attempt $attempts of $maxAttempts" -PercentComplete (($attempts / $maxAttempts) * 100)
}

if ($attempts -ge $maxAttempts) {
    Write-Host "⚠️ Services may not be fully ready yet" -ForegroundColor Yellow
}

# Open dashboard in default browser
Write-Host "Opening dashboard in browser..." -ForegroundColor Yellow
Start-Process "http://localhost:8501"

Write-Host ""
Write-Host "Dashboard opened in browser!" -ForegroundColor Green
Write-Host "Keep this window open to monitor the services" -ForegroundColor Yellow
Write-Host ""

# Show job status
Write-Host "Current job status:" -ForegroundColor Cyan
Get-Job | Format-Table -AutoSize

Write-Host ""
Write-Host "Commands:" -ForegroundColor Yellow
Write-Host "  Get-Job                    - Show all jobs" -ForegroundColor White
Write-Host "  Receive-Job <JobId>        - Show job output" -ForegroundColor White
Write-Host "  Stop-Job <JobId>           - Stop a specific job" -ForegroundColor White
Write-Host "  Stop-Job -Name *           - Stop all jobs" -ForegroundColor White
Write-Host "  Remove-Job <JobId>         - Remove a job" -ForegroundColor White
Write-Host ""

Read-Host "Press Enter to exit (services will continue running)"
