@echo off
echo Starting SmartOps Dashboard...
echo.
echo This will start the Streamlit dashboard in a new command window.
echo The dashboard will be available at: http://localhost:8501
echo.
echo Press any key to continue...
pause >nul

echo Starting dashboard...
start "SmartOps Dashboard" cmd /k "cd /d %~dp0 && streamlit run pages/1_Overview.py"
