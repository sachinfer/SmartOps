# SmartOps AI Chatbot Startup Script
Write-Host "Starting SmartOps AI Chatbot..." -ForegroundColor Green
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.9+ and try again" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if requirements are installed
Write-Host "Checking dependencies..." -ForegroundColor Yellow
try {
    $streamlitInstalled = pip show streamlit 2>&1
    Write-Host "✅ Streamlit is installed" -ForegroundColor Green
} catch {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    try {
        pip install -r requirements.txt
        Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green
    } catch {
        Write-Host "❌ Error: Failed to install dependencies" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host ""
Write-Host "🚀 Starting AI Chatbot..." -ForegroundColor Green
Write-Host ""
Write-Host "The chatbot will open in your browser at: http://localhost:8501" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the chatbot" -ForegroundColor Yellow
Write-Host ""

# Start the chatbot
try {
    streamlit run streamlit_chatbot.py --server.port=8501
} catch {
    Write-Host "❌ Error starting chatbot: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
}
