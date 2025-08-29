# 🚀 SmartOps Dashboard Startup Script
# ======================================

Write-Host "Starting SmartOps Dashboard..." -ForegroundColor Green
Write-Host ""

Write-Host "This will start the Streamlit dashboard in a new PowerShell window." -ForegroundColor Yellow
Write-Host "The dashboard will be available at: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""

Write-Host "Press any key to continue..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host "Starting dashboard..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; streamlit run pages/1_Overview.py" -WindowStyle Normal
