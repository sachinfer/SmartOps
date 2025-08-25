# SmartOps AI Chatbot 🤖

A custom AI-powered chatbot specifically designed for SmartOps Kubernetes operations platform. This chatbot provides intelligent responses to user queries and guides users to relevant SmartOps pages and features. **Now fully integrated with SmartOps pipeline for automatic Kubernetes deployment!**

## ✨ Features

- **Intelligent Q&A**: Answers questions about SmartOps features and functionality
- **Navigation Guidance**: Automatically suggests which pages to visit for specific tasks
- **Context Awareness**: Maintains conversation context and provides relevant suggestions
- **Smart Suggestions**: Offers follow-up questions based on user queries
- **Confidence Scoring**: Shows AI confidence level for each response
- **Modern UI**: Beautiful Streamlit interface with responsive design
- **Pipeline Integration**: Automatic deployment via GitHub Actions
- **Kubernetes Ready**: Production-ready with HPA, health checks, and monitoring
- **Misi Widget**: Floating 🤖 icon with popup chat interface

## 🚀 Quick Start

### Option 1: Direct Python Execution

1. **Install Python 3.9+** if not already installed
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the chatbot**:
   ```bash
   streamlit run streamlit_chatbot.py
   ```
4. **Open browser** at `http://localhost:8501`

### Option 2: Windows Batch File

Double-click `start_chatbot.bat` to automatically start the chatbot.

### Option 3: PowerShell Script

Run `start_chatbot.ps1` in PowerShell for enhanced startup experience.

### Option 4: Docker

```bash
# Build and run with Docker
docker build -t smartops-ai-chatbot .
docker run -p 8501:8501 smartops-ai-chatbot

# Or use docker-compose
docker-compose up --build

# Production build
docker build -f Dockerfile.production -t misi-ai-chatbot:prod .
docker run -p 8501:8501 misi-ai-chatbot:prod
```

### Option 5: Local Testing Script

```bash
# Make executable (Linux/Mac)
chmod +x deploy_local.sh
./deploy_local.sh

# Windows PowerShell
.\deploy_local.ps1
```

## 🏗️ Architecture

### Core Components

1. **Knowledge Base** (`smartops_knowledge_base.py`)
   - Comprehensive information about SmartOps features
   - Page mappings and navigation instructions
   - Feature descriptions and capabilities

2. **AI Engine** (`ai_chatbot_engine.py`)
   - Query processing and response generation
   - Context management and conversation history
   - Intelligent response selection

3. **Streamlit Interface** (`streamlit_chatbot.py`)
   - Modern web-based chat interface
   - Real-time conversation display
   - Navigation guidance and suggestions

4. **Misi Widget** (`misi_chatbot_widget.py`)
   - Floating 🤖 icon for any page
   - Popup chat interface
   - Easy integration with existing apps

5. **Integration Utilities** (`misi_integration.py`)
   - One-line integration functions
   - Sidebar and quick help options
   - Multiple position configurations

### File Structure

```
smartops-ai-chatbot/
├── 📁 Core AI Components
│   ├── ai_chatbot_engine.py      # AI logic and response generation
│   ├── smartops_knowledge_base.py # Knowledge base and search
│   └── streamlit_chatbot.py      # Main web interface
├── 📁 Misi Integration
│   ├── misi_chatbot_widget.py    # Floating widget and popup
│   ├── misi_integration.py       # One-line integration functions
│   └── example_page_with_misi.py # Integration example
├── 📁 Kubernetes Deployment
│   ├── k8s/misi-chatbot-deployment.yaml # Complete K8s manifests
│   ├── Dockerfile.production     # Production Docker image
│   └── deploy_local.sh           # Local testing script
├── 📁 Testing & Documentation
│   ├── test_chatbot.py           # Core functionality tests
│   ├── test_misi_integration.py  # Integration tests
│   ├── demo.py                   # Interactive demo
│   └── KUBERNETES_DEPLOYMENT_GUIDE.md # Deployment guide
├── 📁 Development
│   ├── requirements.txt           # Python dependencies
│   ├── docker-compose.yml        # Local development
│   ├── start_chatbot.bat         # Windows startup
│   └── start_chatbot.ps1         # PowerShell startup
└── 📁 Documentation
    ├── README.md                  # This file
    ├── MISI_INTEGRATION_GUIDE.md # Integration guide
    ├── MISI_QUICK_START.md       # Quick start guide
    └── INTEGRATION_GUIDE.md      # General integration guide
```

### Knowledge Categories

- **Pod Management** (Page 2): Pod status, logs, monitoring
- **Anomaly Detection** (Page 4): AI-powered issue identification
- **Kubernetes Shell** (Page 3): Cluster exploration and commands
- **Auto Scaling** (Page 5): Intelligent scaling recommendations
- **Incident Management** (Page 6): Timeline tracking and reports
- **AI Actions** (Page 8): Automated operations
- **Deployments** (Page 9): Deployment monitoring and management
- **Overview** (Page 1): Cluster health and metrics

## 💬 Usage Examples

### Example 1: Pod Management
**User**: "How can AI check pods?"
**AI Response**: 
- Explains pod management capabilities
- Guides to Page 2: Pod Explorer and Logs
- Suggests related questions

### Example 2: Anomaly Detection
**User**: "What is anomaly detection?"
**AI Response**:
- Explains AI-powered monitoring
- Guides to Page 4: Anomaly Detection
- Lists key features

### Example 3: Navigation Help
**User**: "How do I access the Kubernetes shell?"
**AI Response**:
- Explains shell capabilities
- Guides to Page 3: Kubernetes Shell
- Provides navigation instructions

## 🔧 Configuration

### Environment Variables

- `STREAMLIT_SERVER_PORT`: Port for the chatbot (default: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Server address (default: 0.0.0.0)

### Customization

1. **Add New Knowledge**: Edit `smartops_knowledge_base.py`
2. **Modify Responses**: Update `ai_chatbot_engine.py`
3. **Change UI**: Modify `streamlit_chatbot.py`

## 🧪 Testing

Run the test script to verify functionality:

```bash
python test_chatbot.py
```

This will test various queries and show response quality.

### Testing Misi Integration

```bash
# Test Misi widget and integration
python test_misi_integration.py

# Test local deployment
./deploy_local.sh  # Linux/Mac
# or
.\deploy_local.ps1  # Windows
```

## 📊 Performance

- **Response Time**: < 100ms for most queries
- **Memory Usage**: ~50MB RAM
- **CPU Usage**: Minimal during idle, spikes during processing
- **Scalability**: Can handle multiple concurrent users

## 🚀 Deployment

### Local Development
```bash
streamlit run streamlit_chatbot.py --server.port=8501
```

### Production Deployment
```bash
# Build Docker image
docker build -f Dockerfile.production -t misi-ai-chatbot:prod .
docker run -d -p 8080:8501 --name misi-chatbot misi-ai-chatbot:prod
```

### 🚀 **Pipeline Integration (Recommended)**

The chatbot is now fully integrated with your SmartOps GitHub Actions pipeline! 

**Automatic Deployment:**
- ✅ Builds on every push to `main`, `gcp`, `gcp2`, `dash`, or `ai` branches
- ✅ Parallel Docker builds with layer caching
- ✅ Automatic deployment to GKE cluster in `smartops` namespace
- ✅ Health checks and auto-scaling (2-10 replicas)
- ✅ Telegram notifications on success/failure

**Pipeline Features:**
- **Parallel Builds**: Misi builds alongside other SmartOps services
- **Auto-scaling**: HPA scales based on CPU (70%) and memory (80%) usage
- **Health Monitoring**: Liveness and readiness probes
- **Load Balancing**: ClusterIP service with ingress support
- **Resource Management**: 256Mi-512Mi RAM, 250m-500m CPU

**To Deploy:**
```bash
# Just commit and push!
git add .
git commit -m "feat: Update Misi AI chatbot"
git push origin main

# Pipeline automatically:
# 1. Builds Docker image
# 2. Pushes to GCP Artifact Registry  
# 3. Deploys to Kubernetes
# 4. Scales and monitors
```

### Manual Kubernetes Deployment
```yaml
# Apply the complete deployment
kubectl apply -f k8s/misi-chatbot-deployment.yaml -n smartops

# Check status
kubectl get pods -n smartops -l app=misi-ai-chatbot
kubectl get svc misi-ai-chatbot-service -n smartops
kubectl get hpa misi-ai-chatbot-hpa -n smartops
```

## 🔒 Security Considerations

- No external API calls (fully self-contained)
- Local knowledge base (no data leakage)
- Session-based conversation storage
- No persistent user data storage

## 🛠️ Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Change port
   streamlit run streamlit_chatbot.py --server.port=8502
   ```

2. **Dependencies Missing**
   ```bash
   pip install -r requirements.txt
   ```

3. **Python Version Issues**
   - Ensure Python 3.9+ is installed
   - Check PATH environment variable

### Debug Mode

```bash
streamlit run streamlit_chatbot.py --logger.level=debug
```

## 🔌 Misi Integration

### One-Line Integration

Add Misi to any Streamlit page with just one line:

```python
from smartops_ai_chatbot.misi_integration import add_misi_to_page

# Add floating 🤖 icon (bottom-right corner)
add_misi_to_page()

# Or customize position
add_misi_to_page("top-left")
add_misi_to_page("bottom-left")
add_misi_to_page("top-right")
```

### Integration Options

1. **Floating Icon** (`add_misi_to_page()`)
   - Floating 🤖 icon in any corner
   - Click to open popup chat
   - Non-intrusive design

2. **Sidebar Integration** (`add_misi_to_sidebar()`)
   - Chat interface in sidebar
   - Navigation guidance
   - Suggested questions

3. **Quick Help** (`add_misi_quick_help()`)
   - Compact help section
   - Common questions
   - Quick navigation

### Example Integration

```python
import streamlit as st
from smartops_ai_chatbot.misi_integration import add_misi_to_page

# Your page content
st.title("My SmartOps Page")
st.write("Welcome to SmartOps!")

# Add Misi (floating icon)
add_misi_to_page()

# Misi will appear as a floating 🤖 icon
# Users can click to chat and get navigation help
```

## 📈 Future Enhancements

- **Machine Learning**: Train on user interactions
- **Multi-language Support**: Internationalization
- **Voice Interface**: Speech-to-text integration
- **Advanced Analytics**: Usage patterns and insights
- **API Integration**: External service connectivity
- **Mobile App**: Native mobile application

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is part of SmartOps and follows the same licensing terms.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the test output
3. Check Streamlit logs
4. Contact the SmartOps team

## 🚀 Pipeline Integration Status

### ✅ **Fully Integrated with SmartOps Pipeline**

**Current Status:** Misi AI Chatbot is now fully integrated with your existing SmartOps GitHub Actions pipeline!

**What Happens on Every Push:**
1. **Automatic Build**: Docker image built with production optimizations
2. **Registry Push**: Image pushed to GCP Artifact Registry
3. **Kubernetes Deploy**: Automatic deployment to `smartops` namespace
4. **Health Monitoring**: Health checks and auto-scaling enabled
5. **Notifications**: Telegram updates on deployment status

**Pipeline Triggers:**
- `main` branch → Production deployment
- `gcp`, `gcp2`, `dash`, `ai` branches → Development deployment
- Manual trigger via GitHub Actions

**Deployment Resources:**
- **Namespace**: `smartops`
- **Replicas**: 2-10 (auto-scaling)
- **Resources**: 256Mi-512Mi RAM, 250m-500m CPU
- **Health Checks**: Liveness and readiness probes
- **Auto-scaling**: CPU > 70% or Memory > 80%

**Access Information:**
- **Service**: `misi-ai-chatbot-service.smartops.svc.cluster.local:80`
- **Health Endpoint**: `/_stcore/health`
- **External Access**: Configure ingress for custom domain

---

**Made with ❤️ for SmartOps Kubernetes Operations**

**🚀 Misi AI Chatbot: Your Intelligent Kubernetes Assistant!**
