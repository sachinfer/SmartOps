@echo off
echo 🚀 SmartOps Dashboard Startup Script
echo ======================================
echo.

echo 📍 Starting Backend API Service...
echo.
start "SmartOps API Service" cmd /k "cd /d %~dp0 && python event_api.py"

echo ⏳ Waiting for API service to start...
timeout /t 3 /nobreak >nul

echo 🌐 Starting Dashboard...
echo.
        start "SmartOps Dashboard" cmd /k "cd /d %~dp0 && streamlit run main_app.py"

echo.
echo ✅ Both services are starting up!
echo.
echo 📱 Dashboard will open at: http://localhost:8501
echo 🔌 API service runs at: http://localhost:8000
echo.
echo 💡 Keep both terminal windows open while using the dashboard
echo.
pause
