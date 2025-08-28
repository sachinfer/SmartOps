@echo off
echo 🚀 SmartOps Dashboard Startup Script for Windows
echo ================================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "event_api.py" (
    echo ❌ Please run this script from the dashboard directory
    echo Expected files: event_api.py, misi24x7.py
    pause
    exit /b 1
)

if not exist "misi24x7.py" (
    echo ❌ Please run this script from the dashboard directory
    echo Expected files: event_api.py, misi24x7.py
    pause
    exit /b 1
)

echo ✅ Python found and in correct directory

REM Check dependencies
echo Checking dependencies...
python -c "import fastapi, streamlit, kubernetes" >nul 2>&1
if errorlevel 1 (
    echo ❌ Missing dependencies. Installing...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
    echo ✅ Dependencies installed
) else (
    echo ✅ All required dependencies are available
)

REM Check if ports are available
echo Checking port availability...
netstat -an | findstr ":8000" >nul
if not errorlevel 1 (
    echo ❌ Port 8000 is already in use
    echo Please stop the existing service first
    pause
    exit /b 1
)

netstat -an | findstr ":8501" >nul
if not errorlevel 1 (
    echo ❌ Port 8501 is already in use
    echo Please stop the existing service first
    pause
    exit /b 1
)

echo ✅ Ports 8000 and 8501 are available

REM Start FastAPI backend
echo 🚀 Starting FastAPI backend service...
start "FastAPI Backend" cmd /k "python -m uvicorn event_api:app --host 0.0.0.0 --port 8000 --reload"

REM Wait a moment for FastAPI to start
timeout /t 3 /nobreak >nul

REM Start Streamlit frontend
echo 🎨 Starting Streamlit frontend service...
        start "Streamlit Frontend" cmd /k "streamlit run misi24x7.py --server.port=8501 --server.address=0.0.0.0"

echo.
echo 🎉 All services started successfully!
echo ================================================
echo 📊 Dashboard: http://localhost:8501
echo 🔌 API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo 💡 Services are running in separate windows
echo    Close those windows to stop the services
echo.
echo Press any key to open the dashboard in your browser...
pause >nul

REM Open dashboard in default browser
start http://localhost:8501

echo Dashboard opened in browser!
echo Keep this window open to monitor the services
echo.
pause
