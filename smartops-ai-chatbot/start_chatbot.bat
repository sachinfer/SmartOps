@echo off
echo Starting SmartOps AI Chatbot...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.9+ and try again
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo Starting AI Chatbot...
echo.
echo The chatbot will open in your browser at: http://localhost:8501
echo Press Ctrl+C to stop the chatbot
echo.

REM Start the chatbot
streamlit run streamlit_chatbot.py --server.port=8501

pause
