Write-Host "Starting SmartOps Dashboard Services..." -ForegroundColor Green
Write-Host ""

Write-Host "Starting API Service..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; python event_api.py" -WindowStyle Normal

Write-Host "Waiting for API service to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host "Starting Dashboard..." -ForegroundColor Yellow
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; streamlit run page_router.py" -WindowStyle Normal

Write-Host ""
Write-Host "Services started!" -ForegroundColor Green
Write-Host "- API Service: http://localhost:8000" -ForegroundColor Cyan
Write-Host "- Dashboard: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to close this window..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
