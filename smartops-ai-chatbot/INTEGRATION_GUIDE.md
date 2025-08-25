# SmartOps AI Chatbot Integration Guide 🔗

This guide explains how to integrate the AI chatbot with your main SmartOps dashboard and how to deploy it as a separate service.

## 🎯 Integration Options

### Option 1: Embedded Integration (Recommended)
Integrate the chatbot directly into your existing SmartOps dashboard as a new page.

### Option 2: Standalone Service
Run the chatbot as a separate service and communicate via API calls.

### Option 3: Sidebar Integration
Add the chatbot as a sidebar widget in your existing dashboard.

## 🔧 Option 1: Embedded Integration

### Step 1: Add to Main Dashboard
Add the chatbot as a new page in your existing Streamlit dashboard:

```python
# In your main dashboard file (e.g., streamlit_app.py)
import sys
import os
sys.path.append('./smartops-ai-chatbot')

from smartops_ai_chatbot.ai_chatbot_engine import SmartOpsAIChatbot
from smartops_ai_chatbot.smartops_knowledge_base import get_knowledge_base

# Add to your page selection
if selected == "AI Assistant":
    st.title("🤖 SmartOps AI Assistant")
    
    # Initialize chatbot
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = SmartOpsAIChatbot()
    
    # Chat interface
    user_input = st.chat_input("Ask me anything about SmartOps...")
    
    if user_input:
        response = st.session_state.chatbot.process_query(user_input)
        
        # Display response
        st.write(response["answer"])
        
        # Show navigation guide if available
        if response.get("navigation_guide"):
            nav = response["navigation_guide"]
            st.info(f"Navigate to: Page {nav['page_number']} - {nav['page_name']}")
```

### Step 2: Navigation Integration
Add navigation buttons to jump between pages:

```python
# Add navigation buttons
if st.button(f"Go to Page {nav['page_number']}"):
    st.session_state.current_page = nav['page_number']
    st.rerun()
```

## 🚀 Option 2: Standalone Service

### Step 1: Run as Separate Service
```bash
cd smartops-ai-chatbot
streamlit run streamlit_chatbot.py --server.port=8502
```

### Step 2: API Integration
Create an API wrapper for the chatbot:

```python
# api_wrapper.py
from fastapi import FastAPI
from pydantic import BaseModel
from smartops_ai_chatbot.ai_chatbot_engine import SmartOpsAIChatbot

app = FastAPI()
chatbot = SmartOpsAIChatbot()

class ChatRequest(BaseModel):
    message: str
    user_id: str = None

class ChatResponse(BaseModel):
    answer: str
    navigation_guide: dict = None
    suggested_questions: list = None
    confidence: float

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    response = chatbot.process_query(request.message)
    return ChatResponse(**response)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "SmartOps AI Chatbot"}
```

### Step 3: Call from Main Dashboard
```python
import requests

def ask_ai(message):
    response = requests.post("http://localhost:8000/chat", 
                           json={"message": message})
    return response.json()

# Usage
ai_response = ask_ai("How can I check pods?")
st.write(ai_response["answer"])
```

## 🎨 Option 3: Sidebar Integration

### Step 1: Add to Sidebar
```python
# In your main dashboard sidebar
with st.sidebar:
    st.markdown("## 🤖 AI Assistant")
    
    # Quick chat input
    ai_question = st.text_input("Quick AI Question:")
    if ai_question:
        response = chatbot.process_query(ai_question)
        st.info(response["answer"][:200] + "...")
        
        if response.get("navigation_guide"):
            nav = response["navigation_guide"]
            if st.button(f"Go to {nav['page_name']}"):
                st.session_state.current_page = nav['page_number']
                st.rerun()
```

## 🔄 Real-time Integration

### WebSocket Integration
For real-time chat updates:

```python
import asyncio
import websockets

async def chat_websocket(websocket, path):
    chatbot = SmartOpsAIChatbot()
    
    async for message in websocket:
        response = chatbot.process_query(message)
        await websocket.send(json.dumps(response))

# Start WebSocket server
start_server = websockets.serve(chat_websocket, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
```

## 🌐 External DNS Integration

### Step 1: Deploy to External Server
```bash
# Build Docker image
docker build -t smartops-ai-chatbot .

# Push to registry
docker tag smartops-ai-chatbot your-registry/smartops-ai-chatbot:latest
docker push your-registry/smartops-ai-chatbot:latest
```

### Step 2: Kubernetes Deployment
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
        image: your-registry/smartops-ai-chatbot:latest
        ports:
        - containerPort: 8501
        env:
        - name: STREAMLIT_SERVER_PORT
          value: "8501"
        - name: STREAMLIT_SERVER_ADDRESS
          value: "0.0.0.0"
---
apiVersion: v1
kind: Service
metadata:
  name: smartops-ai-chatbot-service
spec:
  selector:
    app: ai-chatbot
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8501
  type: LoadBalancer
```

### Step 3: DNS Configuration
```bash
# Example DNS configuration
# ai.yourdomain.com -> LoadBalancer IP
# chatbot.smartops.com -> LoadBalancer IP
```

## 🔐 Security Integration

### Authentication
```python
# Add authentication to chatbot
def require_auth():
    if 'authenticated' not in st.session_state:
        st.error("Please log in to access the AI Assistant")
        st.stop()

# In chatbot page
if selected == "AI Assistant":
    require_auth()
    # ... rest of chatbot code
```

### API Key Protection
```python
# For API integration
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def verify_token(credentials = Depends(security)):
    if credentials.credentials != "your-api-key":
        raise HTTPException(status_code=403, detail="Invalid API key")
    return credentials.credentials

@app.post("/chat")
async def chat(request: ChatRequest, token: str = Depends(verify_token)):
    # ... chatbot logic
```

## 📊 Monitoring Integration

### Health Checks
```python
# Add health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "SmartOps AI Chatbot",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }
```

### Metrics Collection
```python
# Add Prometheus metrics
from prometheus_client import Counter, Histogram

chat_requests = Counter('chat_requests_total', 'Total chat requests')
response_time = Histogram('chat_response_time_seconds', 'Chat response time')

@app.post("/chat")
async def chat(request: ChatRequest):
    chat_requests.inc()
    start_time = time.time()
    
    response = chatbot.process_query(request.message)
    
    response_time.observe(time.time() - start_time)
    return response
```

## 🧪 Testing Integration

### Test Script
```python
# test_integration.py
import requests
import time

def test_chatbot_integration():
    base_url = "http://localhost:8501"
    
    # Test basic functionality
    test_queries = [
        "Hello",
        "How can AI check pods?",
        "What is anomaly detection?"
    ]
    
    for query in test_queries:
        print(f"Testing: {query}")
        # Test via Streamlit interface or API
        time.sleep(1)
    
    print("Integration test completed!")

if __name__ == "__main__":
    test_chatbot_integration()
```

## 🚀 Production Deployment

### Environment Variables
```bash
# .env file
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
CHATBOT_LOG_LEVEL=INFO
ENABLE_METRICS=true
API_KEY=your-secure-api-key
```

### Docker Compose Production
```yaml
version: '3.8'
services:
  smartops-ai-chatbot:
    build: .
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
    restart: unless-stopped
    networks:
      - smartops-network
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - smartops-ai-chatbot
    networks:
      - smartops-network

networks:
  smartops-network:
    driver: bridge
```

## 🔄 Update and Maintenance

### Automated Updates
```bash
#!/bin/bash
# update_chatbot.sh
cd /opt/smartops-ai-chatbot
git pull origin main
docker-compose down
docker-compose up --build -d
echo "Chatbot updated successfully!"
```

### Backup and Restore
```bash
# Backup chatbot data
docker exec smartops-ai-chatbot tar czf /app/backup.tar.gz /app/data

# Restore chatbot data
docker exec smartops-ai-chatbot tar xzf /app/backup.tar.gz -C /app/
```

## 📈 Performance Optimization

### Caching
```python
import functools
from cachetools import TTLCache

# Cache responses for 5 minutes
response_cache = TTLCache(maxsize=100, ttl=300)

@functools.lru_cache(maxsize=128)
def cached_chat_response(query: str):
    return chatbot.process_query(query)
```

### Load Balancing
```yaml
# Kubernetes HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: smartops-ai-chatbot-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: smartops-ai-chatbot
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

---

**This integration guide provides multiple options for integrating the AI chatbot with your SmartOps platform. Choose the approach that best fits your architecture and requirements.**
