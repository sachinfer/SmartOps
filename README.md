# 🚀 SmartOps - Intelligent Kubernetes Operations Dashboard

A comprehensive, AI-powered Kubernetes operations dashboard that provides real-time monitoring, anomaly detection, auto-scaling recommendations, and incident management for your Kubernetes clusters.

## ✨ Features

### 🎯 **Core Dashboard Features**
- **Real-time Cluster Overview** - Live pod status, node information, and resource metrics
- **Pod Explorer & Logs** - Browse pods across namespaces and view real-time logs
- **Kubernetes Shell** - Execute kubectl commands directly from the dashboard
- **Cluster Explorer** - Interactive exploration of pods, services, deployments, and nodes
- **Anomaly Detection** - AI-powered detection of unusual patterns and potential issues
- **Auto-scaling Recommendations** - Intelligent HPA settings based on usage patterns
- **Incident Timeline** - Comprehensive incident tracking and postmortem reports
- **AI Actions** - Automated recommendations and action history

### 🔧 **Technical Features**
- **Real-time Data** - Live Kubernetes cluster data without hardcoded values
- **API-First Architecture** - Robust FastAPI backend with graceful fallbacks
- **Smart Error Handling** - User-friendly error messages and automatic fallbacks
- **Responsive UI** - Modern, beautiful interface with dark theme and animations
- **Multi-namespace Support** - View and manage resources across all namespaces
- **Log Management** - Real-time pod log viewing with container selection
- **Resource Monitoring** - CPU, memory, and scaling metrics

## 🏗️ Architecture

```
SmartOps/
├── 📁 dashboard/                 # Streamlit frontend
│   ├── 📄 streamlit_app.py      # Main dashboard application
│   ├── 📁 pages/                # Dashboard pages
│   │   ├── 📄 1_Overview.py     # Cluster overview and metrics
│   │   ├── 📄 2_Pod_Explorer_and_Logs.py  # Pod management and logs
│   │   ├── 📄 3_Kubernetes_Shell_and_Cluster_Explorer.py  # Shell and explorer
│   │   ├── 📄 4_Anomaly_Detection.py      # AI anomaly detection
│   │   ├── 📄 5_Auto_Scaling_Recommendations_and_Control.py  # HPA management
│   │   ├── 📄 6_Incident_Timeline_and_Postmortem_Report_Generator.py  # Incident management
│   │   ├── 📄 8_AI_Actions.py   # AI recommendations and actions
│   │   └── 📄 9_Deployments.py  # Deployment tracking
│   ├── 📄 event_api.py          # FastAPI backend service
│   └── 📄 requirements.txt      # Python dependencies
├── 📁 app/                      # Background services
│   ├── 📄 anomaly_loop.py       # Anomaly detection service
│   └── 📄 monitor_pod_status.py # Pod monitoring service
└── 📁 k8s/                      # Kubernetes manifests
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Kubernetes cluster access
- kubectl configured

### 1. Clone and Setup
```bash
git clone <repository-url>
cd SmartOps/smartops-ai/dashboard
pip install -r requirements.txt
```

### 2. Start the Backend API
```bash
python event_api.py
```
The API will start on `http://localhost:8000`

### 3. Start the Dashboard
```bash
streamlit run streamlit_app.py
```
The dashboard will open at `http://localhost:8501`

### 4. Windows Users (One-Click Start)-
```bash
start_dashboard.bat
```

## 🔌 API Endpoints

### Core Kubernetes Operations
- `GET /` - Health check
- `GET /namespaces` - List all namespaces
- `GET /pods?namespace={ns}` - Get pods in namespace
- `GET /logs?pod={name}&namespace={ns}` - Get pod logs
- `GET /pod-containers?pod_name={name}&namespace={ns}` - Get container names

### Resource Management
- `GET /kubectl_get?resource_type={type}&namespace={ns}` - Get Kubernetes resources
- `POST /kubectl_raw?command={cmd}` - Execute kubectl commands
- `GET /hpa_status` - Get HPA and scaling data
- `POST /update_hpa` - Update HPA settings

### Incident Management
- `GET /incidents` - Get incident data
- `POST /postmortem` - Save postmortem reports

## 📊 Dashboard Pages

### 1. Overview 📈
- Real-time cluster metrics
- Pod status across namespaces
- Node information and health
- Resource utilization

### 2. Pod Explorer & Logs 🔍
- Browse pods by namespace
- Real-time log viewing
- Container selection
- Pod status monitoring

### 3. Kubernetes Shell 💻
- Execute kubectl commands
- Command history navigation
- Real-time output display
- Parsed table views

### 4. Anomaly Detection 🚨
- AI-powered anomaly detection
- Real-time monitoring
- Alert management
- Pattern analysis

### 5. Auto-scaling Control ⚖️
- HPA recommendations
- CPU/memory analysis
- Scaling policies
- One-click HPA updates

### 6. Incident Management 📋
- Incident timeline
- Postmortem reports
- Root cause analysis
- Audit trail

### 7. AI Actions 🤖
- Automated recommendations
- Action history
- Smart suggestions
- Performance insights

### 8. Deployments 🚀
- Deployment tracking
- Rollout status
- Version management
- Rollback capabilities

## 🎨 UI Features

- **Dark Theme** - Modern, eye-friendly interface
- **Responsive Design** - Works on all screen sizes
- **Smooth Animations** - Professional user experience
- **Intuitive Navigation** - Easy-to-use sidebar navigation
- **Real-time Updates** - Live data without page refreshes
- **Error Handling** - Graceful fallbacks and user-friendly messages

## 🔧 Configuration

### Environment Variables
```bash
# Telegram Bot (for alerts)
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# Kubernetes
KUBECONFIG=path_to_kubeconfig
```

### API Configuration
- **Host**: `0.0.0.0` (accessible from any IP)
- **Port**: `8000`
- **CORS**: Enabled for local development
- **Timeout**: 30 seconds for kubectl commands

## 🚨 Troubleshooting

### Common Issues

#### 1. API Connection Errors
```bash
# Check if API is running
curl http://localhost:8000/

# Restart API service
python event_api.py
```

#### 2. Dashboard Not Loading
```bash
# Check Streamlit
streamlit run streamlit_app.py

# Verify port 8501 is available
netstat -an | findstr :8501
```

#### 3. Kubernetes Access Issues
```bash
# Test kubectl access
kubectl get nodes

# Check cluster context
kubectl config current-context
```

#### 4. Missing Dependencies
```bash
# Install requirements
pip install -r requirements.txt

# Check Python version
python --version
```

### Debug Mode
Enable debug logging by setting environment variables:
```bash
export LOG_LEVEL=DEBUG
export STREAMLIT_LOG_LEVEL=debug
```

## 🔒 Security

- **CORS Configuration** - Configured for development
- **API Authentication** - Ready for production auth integration
- **Kubernetes RBAC** - Respects cluster permissions
- **Input Validation** - All API inputs are validated
- **Error Sanitization** - No sensitive data in error messages

## 🚀 Production Deployment

### Docker Deployment
```bash
# Build image
docker build -t smartops-dashboard .

# Run container
docker run -p 8501:8501 -p 8000:8000 smartops-dashboard
```

### Kubernetes Deployment
```bash
# Apply manifests
kubectl apply -f k8s/

# Check status
kubectl get pods -n smartops
```

### Environment Variables
```bash
# Production settings
export PRODUCTION=true
export KUBERNETES_SERVICE_HOST=your-cluster-ip
export KUBERNETES_SERVICE_PORT=443
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Code formatting
black .
flake8 .
```

## 📝 Changelog

### v2.0.0 (Current)
- ✨ Complete dashboard rewrite with modern UI
- 🔧 Fixed all API endpoints and error handling
- 🚀 Added real-time Kubernetes data integration
- 🎯 Implemented AI-powered recommendations
- 📊 Added comprehensive incident management
- ⚖️ Added auto-scaling control features

### v1.0.0
- Initial release with basic functionality

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Kubernetes community for excellent APIs
- Streamlit team for the amazing dashboard framework
- FastAPI for the robust backend framework
- All contributors and users

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)
- **Documentation**: [Wiki](https://github.com/your-repo/wiki)

---

**Made with ❤️ for the Kubernetes community**

