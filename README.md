# 🚀 SmartOps by Misi 24x7 - Intelligent Kubernetes Operations Dashboard

A comprehensive, AI-powered Kubernetes operations dashboard that provides real-time monitoring, anomaly detection, auto-scaling recommendations, incident management, and an intelligent AI chatbot assistant for your Kubernetes clusters.

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
- **Deployment Monitoring** - Track deployments, rollouts, and version management

### 🤖 **Misi AI Chatbot Assistant**
- **Intelligent Navigation** - Ask Misi to guide you through dashboard features
- **Smart Q&A** - Get instant answers about SmartOps by Misi 24x7 functionality
- **Page Navigation** - Quick access to all dashboard pages
- **Contextual Help** - AI-powered assistance for Kubernetes operations
- **Beautiful Full-Screen Interface** - Immersive chat experience with glassmorphism design
- **Floating Widget** - Always accessible from any dashboard page
- **Smart Suggestions** - Pre-built queries for common tasks

### 🔧 **Technical Features**
- **Real-time Data** - Live Kubernetes cluster data without hardcoded values
- **API-First Architecture** - Robust FastAPI backend with graceful fallbacks
- **Smart Error Handling** - User-friendly error messages and automatic fallbacks
- **Responsive UI** - Modern, beautiful interface with dark theme and animations
- **Multi-namespace Support** - View and manage resources across all namespaces
- **Log Management** - Real-time pod log viewing with container selection
- **Resource Monitoring** - CPU, memory, and scaling metrics
- **Glassmorphism Design** - Modern UI with backdrop blur and transparency effects

## 🏗️ Architecture

```
SmartOps by Misi 24x7/
├── 📁 dashboard/                 # Streamlit frontend
│   ├── 📄 streamlit_app.py      # Main dashboard application
│   ├── 📄 misi_chatbot_widget.py # AI chatbot widget
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
│   ├── 📄 check_anomalies_db.py # Database anomaly checking
│   ├── 📄 collect_real_metrics.py # Real-time metrics collection
│   └── 📄 monitor_pod_status.py # Pod monitoring service
├── 📁 model/                    # AI models
│   └── 📄 isolation_forest.pkl  # Anomaly detection model
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
cd SmartOps by Misi 24x7/smartops-ai/dashboard
pip install -r requirements.txt
```

### 2. Start the Backend API-
```bash
python event_api.py
```
The API will start on `http://localhost:8000`

### 3. Start the Dashboard
```bash
streamlit run streamlit_app.py
```
The dashboard will open at `http://localhost:8501`

### 4. Windows Users (One-Click Start)
```bash
start_dashboard.bat
# or
start_dashboard.ps1
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

### Anomaly Detection
- `GET /anomalies` - Get detected anomalies
- `POST /train_model` - Train anomaly detection model
- `GET /metrics` - Get real-time cluster metrics

## 📊 Dashboard Pages & Functions

### 1. Overview 📈
**Functions:**
- Real-time cluster metrics display
- Pod status visualization across namespaces
- Node information and health monitoring
- Resource utilization charts
- Namespace overview with pod counts
- Cluster health indicators

**Features:**
- Live data updates every 30 seconds
- Interactive charts and graphs
- Color-coded status indicators
- Responsive grid layout

### 2. Pod Explorer & Logs 🔍
**Functions:**
- Browse pods by namespace
- Real-time log viewing with container selection
- Pod status monitoring and filtering
- Pod details and specifications
- Container information display
- Log search and filtering

**Features:**
- Multi-container pod support
- Real-time log streaming
- Log level filtering (INFO, WARN, ERROR)
- Pod restart count tracking
- Resource usage display

### 3. Kubernetes Shell & Cluster Explorer 💻
**Functions:**
- Execute kubectl commands directly
- Command history navigation
- Real-time output display
- Parsed table views for common resources
- Resource exploration (pods, services, deployments, nodes)
- Namespace switching

**Features:**
- Command autocompletion
- Output formatting
- Error handling and display
- Resource type filtering
- Interactive command execution

### 4. Anomaly Detection 🚨
**Functions:**
- AI-powered anomaly detection using Isolation Forest
- Real-time monitoring of cluster metrics
- Pattern analysis and alerting
- Anomaly history and trends
- Custom threshold configuration
- Alert management and notifications

**Features:**
- Machine learning model training
- Real-time data processing
- Visual anomaly indicators
- Historical anomaly tracking
- Configurable sensitivity levels

### 5. Auto-scaling Control ⚖️
**Functions:**
- HPA (Horizontal Pod Autoscaler) recommendations
- CPU and memory usage analysis
- Scaling policy optimization
- One-click HPA updates
- Resource utilization monitoring
- Scaling history tracking

**Features:**
- AI-powered scaling suggestions
- Resource threshold configuration
- Scaling policy templates
- Performance impact analysis
- Automated scaling recommendations

### 6. Incident Timeline & Postmortem 📋
**Functions:**
- Incident timeline tracking
- Postmortem report generation
- Root cause analysis tools
- Audit trail maintenance
- Incident categorization
- Resolution tracking

**Features:**
- Timeline visualization
- Report templates
- Search and filtering
- Export capabilities
- Collaboration tools

### 7. AI Actions 🤖
**Functions:**
- Automated recommendations
- Action history tracking
- Smart suggestions for operations
- Performance insights
- Predictive analytics
- Automated task execution

**Features:**
- AI-powered insights
- Action automation
- Performance optimization
- Resource optimization
- Intelligent alerts

### 8. Deployments 🚀
**Functions:**
- Deployment tracking and monitoring
- Rollout status visualization
- Version management
- Rollback capabilities
- Deployment history
- Resource allocation tracking

**Features:**
- Real-time deployment status
- Rollback controls
- Version comparison
- Resource monitoring
- Performance metrics

## 🤖 Misi AI Chatbot Features

### **Core Capabilities**
- **Smart Navigation** - Ask Misi to show specific pages or features
- **Contextual Help** - Get help with any SmartOps by Misi 24x7 functionality
- **Quick Actions** - Execute common tasks through conversation
- **Feature Discovery** - Learn about available dashboard capabilities

### **Available Commands**
- `"show pages"` - Display all available dashboard pages
- `"check pods"` - Get guidance on pod management
- `"anomaly detection"` - Learn about AI monitoring features
- `"auto scaling"` - Get help with HPA management
- `"kubernetes shell"` - Access cluster exploration tools
- `"incident management"` - Learn about incident tracking
- `"test chat"` - Verify chatbot functionality

### **UI Features**
- **Floating Icon** - Always accessible from bottom-right corner
- **Full-Screen Chat** - Immersive chat experience
- **Glassmorphism Design** - Modern, beautiful interface
- **Responsive Layout** - Works on all screen sizes
- **Smooth Animations** - Professional user experience
- **Smart Suggestions** - Pre-built query buttons

## 🎨 UI Features

- **Dark Theme** - Modern, eye-friendly interface
- **Glassmorphism Design** - Backdrop blur and transparency effects
- **Responsive Design** - Works on all screen sizes
- **Smooth Animations** - Professional user experience
- **Intuitive Navigation** - Easy-to-use sidebar navigation
- **Real-time Updates** - Live data without page refreshes
- **Error Handling** - Graceful fallbacks and user-friendly messages
- **Modern Icons** - Beautiful iconography throughout the interface
- **Hover Effects** - Interactive elements with smooth transitions
- **Custom Scrollbars** - Styled scrollbars for better aesthetics

## 🔧 Configuration

### Environment Variables
```bash
# Telegram Bot (for alerts)
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# Kubernetes
KUBECONFIG=path_to_kubeconfig

# Anomaly Detection
ANOMALY_SENSITIVITY=0.1
ANOMALY_THRESHOLD=0.8

# Logging
LOG_LEVEL=INFO
STREAMLIT_LOG_LEVEL=info
```

### API Configuration
- **Host**: `0.0.0.0` (accessible from any IP)
- **Port**: `8000`
- **CORS**: Enabled for local development
- **Timeout**: 30 seconds for kubectl commands
- **Rate Limiting**: Configurable request limits
- **Authentication**: Ready for production auth integration

## 🚨 Troubleshooting

### Common Issues

#### 1. API Connection Errors
```bash
# Check if API is running
curl http://localhost:8000/

# Restart API service
python event_api.py

# Check API logs
tail -f api.log
```

#### 2. Dashboard Not Loading
```bash
# Check Streamlit
streamlit run streamlit_app.py

# Verify port 8501 is available
netstat -an | findstr :8501

# Check Streamlit logs
streamlit run streamlit_app.py --logger.level debug
```

#### 3. Kubernetes Access Issues
```bash
# Test kubectl access
kubectl get nodes

# Check cluster context
kubectl config current-context

# Verify permissions
kubectl auth can-i get pods
```

#### 4. Missing Dependencies
```bash
# Install requirements
pip install -r requirements.txt

# Check Python version
python --version

# Update pip
pip install --upgrade pip
```

#### 5. Misi Chatbot Issues
```bash
# Check browser console for JavaScript errors
# Verify Streamlit components are working
# Check if misi_chatbot_widget.py is properly loaded
```

### Debug Mode
Enable debug logging by setting environment variables:
```bash
export LOG_LEVEL=DEBUG
export STREAMLIT_LOG_LEVEL=debug
export ANOMALY_DEBUG=true
```

## 🔒 Security

- **CORS Configuration** - Configured for development
- **API Authentication** - Ready for production auth integration
- **Kubernetes RBAC** - Respects cluster permissions
- **Input Validation** - All API inputs are validated
- **Error Sanitization** - No sensitive data in error messages
- **Rate Limiting** - Protection against abuse
- **Secure Headers** - Security headers configuration
- **Input Sanitization** - XSS protection

## 🚀 Production Deployment

### Docker Deployment
```bash
# Build image
docker build -t smartops-dashboard .

# Run container
docker run -p 8501:8501 -p 8000:8000 smartops-dashboard

# With environment variables
docker run -e KUBECONFIG=/path/to/kubeconfig -p 8501:8501 -p 8000:8000 smartops-dashboard
```

### Kubernetes Deployment
```bash
# Apply manifests
kubectl apply -f k8s/

# Check status
kubectl get pods -n smartops

# View logs
kubectl logs -n smartops deployment/smartops-dashboard
```

### Environment Variables
```bash
# Production settings
export PRODUCTION=true
export KUBERNETES_SERVICE_HOST=your-cluster-ip
export KUBERNETES_SERVICE_PORT=443
export SECURE_COOKIES=true
export HTTPS_ONLY=true
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

# Type checking
mypy .
```

## 📝 Changelog

### v2.1.0 (Current)
- ✨ Added Misi AI Chatbot Assistant
- 🎨 Implemented glassmorphism UI design
- 🚀 Enhanced full-screen chat interface
- 📱 Improved responsive design
- 🔧 Enhanced error handling and debugging
- 📊 Added comprehensive function documentation

### v2.0.0
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
- AI/ML community for anomaly detection algorithms
- All contributors and users

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)
- **Documentation**: [Wiki](https://github.com/your-repo/wiki)
- **AI Assistant**: Use Misi chatbot in the dashboard

---

**Made with ❤️ by Misi 24x7 for the Kubernetes community**

**Powered by AI 🤖 and modern web technologies**

