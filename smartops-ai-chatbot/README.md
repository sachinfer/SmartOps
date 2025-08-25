# SmartOps AI Chatbot 🤖

A custom AI-powered chatbot specifically designed for SmartOps Kubernetes operations platform. This chatbot provides intelligent responses to user queries and guides users to relevant SmartOps pages and features.

## ✨ Features

- **Intelligent Q&A**: Answers questions about SmartOps features and functionality
- **Navigation Guidance**: Automatically suggests which pages to visit for specific tasks
- **Context Awareness**: Maintains conversation context and provides relevant suggestions
- **Smart Suggestions**: Offers follow-up questions based on user queries
- **Confidence Scoring**: Shows AI confidence level for each response
- **Modern UI**: Beautiful Streamlit interface with responsive design

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
docker build -t smartops-ai-chatbot .

# Run with custom port
docker run -d -p 8080:8501 --name ai-chatbot smartops-ai-chatbot
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: smartops-ai-chatbot
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ai-chatbot
  template:
    metadata:
      labels:
        app: ai-chatbot
    spec:
      containers:
      - name: chatbot
        image: smartops-ai-chatbot:latest
        ports:
        - containerPort: 8501
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
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

---

**Made with ❤️ for SmartOps Kubernetes Operations**
