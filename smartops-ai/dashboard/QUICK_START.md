# �� SmartOps Dashboard - Quick Start Guide

## 📋 Prerequisites

- Python 3.8+
- Kubernetes cluster access
- kubectl configured
- Docker (optional, for containerized deployment)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
cd smartops-ai/dashboard
pip install -r requirements.txt
```

### 2. Start Services

#### Option A: Using Startup Scripts (Recommended)

**Windows:**
```bash
start_dashboard.bat
```

**PowerShell:**
```powershell
.\start_dashboard.ps1
```

**Python:**
```bash
python start_services.py
```

#### Option B: Manual Start

```bash
# Terminal 1: Start API backend
python event_api.py

# Terminal 2: Start dashboard (in new terminal)
streamlit run main_app.py
```

### 3. Access Dashboard

- **Dashboard**: http://localhost:8501
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🔧 Configuration

### Port Configuration

- **API Port**: Default 8000
- **Dashboard Port**: Use `streamlit run pages/1_Overview.py --server.port 8502`

### Environment Variables

Create `config.env` from `config.env.example`:

```bash
cp config.env.example config.env
# Edit config.env with your settings
```

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**: Stop existing services or change ports
2. **Dependencies missing**: Run `pip install -r requirements.txt`
3. **Kubernetes access**: Ensure kubectl is configured

### Debug Mode

```bash
streamlit run pages/1_Overview.py --logger.level debug
```

## 📚 Next Steps

- Check the [STARTUP_GUIDE.md](STARTUP_GUIDE.md) for detailed setup
- Review [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
- Explore the dashboard features and pages
