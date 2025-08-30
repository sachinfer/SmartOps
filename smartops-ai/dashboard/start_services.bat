@echo off
echo �� SmartOps Dashboard Services Startup Script
echo =============================================
echo.

echo 📍 Starting Backend API Service...
start "SmartOps API Service" cmd /k "cd /d %~dp0 && python event_api.py"

echo ⏳ Waiting for API service to start...
timeout /t 3 /nobreak >nul

echo 🌐 Starting Dashboard...
echo.

echo Checking required files...
if not exist "event_api.py" (
    echo ❌ ERROR: event_api.py not found!
    echo Expected files: event_api.py, main.py
    pause
    exit /b 1
)

if not exist "main.py" (
    echo ❌ ERROR: main.py not found!
    echo Expected files: event_api.py, main.py
    pause
    exit /b 1
)

echo ✅ All required files found!
echo.

start "Streamlit Frontend" cmd /k "streamlit run main.py --server.port=8501 --server.address=0.0.0.0"

echo.
echo ✅ Both services are starting up!
echo.
echo 📱 Dashboard will open at: http://localhost:8501
echo 🔌 API service runs at: http://localhost:8000
echo.
echo 💡 Keep both terminal windows open while using the dashboard
echo.
pause
