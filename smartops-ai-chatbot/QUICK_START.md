# 🚀 Quick Start Guide

## ⚡ Get Started in 5 Minutes

### 1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 2. **Test the Chatbot**
```bash
python test_chatbot.py
```

### 3. **Run the Web Interface**
```bash
streamlit run streamlit_chatbot.py
```

### 4. **Open Browser**
Navigate to: `http://localhost:8501`

## 🎯 Try These Questions

- "Hello"
- "How can AI check pods?"
- "What is anomaly detection?"
- "How do I access the Kubernetes shell?"
- "Tell me about auto-scaling"

## 🔧 Integration Options

### **Option A: Add to Main Dashboard**
Copy the chatbot files to your main SmartOps dashboard and import them.

### **Option B: Run as Separate Service**
Run on different port and communicate via API calls.

### **Option C: Docker Deployment**
```bash
docker build -t smartops-ai-chatbot .
docker run -p 8501:8501 smartops-ai-chatbot
```

## 📁 File Structure
```
smartops-ai-chatbot/
├── ai_chatbot_engine.py      # AI logic and response generation
├── smartops_knowledge_base.py # Knowledge base and search
├── streamlit_chatbot.py      # Web interface
├── test_chatbot.py           # Test script
├── demo.py                   # Demo script
├── requirements.txt          # Dependencies
├── Dockerfile               # Container configuration
├── docker-compose.yml       # Local development
├── start_chatbot.bat        # Windows startup
├── start_chatbot.ps1        # PowerShell startup
└── README.md                # Full documentation
```

## 🎉 You're Ready!

The chatbot is fully functional and ready to:
- Answer SmartOps questions
- Guide users to relevant pages
- Provide intelligent suggestions
- Maintain conversation context

**Next Step**: Choose your integration method and deploy!
