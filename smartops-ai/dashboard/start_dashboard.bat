@echo off
echo Starting SmartOps Dashboard Services...
echo.

echo Starting API Service...
start "SmartOps API" cmd /k "cd /d %~dp0 && python event_api.py"

echo Waiting for API service to start...
timeout /t 5 /nobreak >nul

echo Starting Dashboard...
start "SmartOps Dashboard" cmd /k "cd /d %~dp0 && streamlit run streamlit_app.py"

echo.
echo Services started! 
echo - API Service: http://localhost:8000
echo - Dashboard: http://localhost:8501
echo.
echo Press any key to close this window...
pause >nul
