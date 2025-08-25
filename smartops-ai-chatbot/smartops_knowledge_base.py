"""
SmartOps Knowledge Base for AI Chatbot
Contains information about SmartOps features, pages, and functionality
"""

SMARTOPS_KNOWLEDGE_BASE = {
    "pod_management": {
        "questions": [
            "how to check pods",
            "how can ai check pods",
            "pod status",
            "pod logs",
            "pod explorer",
            "view pods",
            "monitor pods"
        ],
        "answer": "SmartOps provides comprehensive pod management capabilities. You can check pod status, view logs, and explore pod details through the Pod Explorer page.",
        "page": "Pod Explorer and Logs",
        "page_number": 2,
        "features": [
            "Real-time pod status monitoring",
            "Pod logs viewing and analysis",
            "Pod resource usage metrics",
            "Pod health checks"
        ]
    },
    
    "anomaly_detection": {
        "questions": [
            "anomaly detection",
            "ai anomaly",
            "detect issues",
            "find problems",
            "monitoring anomalies"
        ],
        "answer": "SmartOps uses AI-powered anomaly detection to identify potential issues in your Kubernetes cluster. The system monitors metrics and logs to detect unusual patterns.",
        "page": "Anomaly Detection",
        "page_number": 4,
        "features": [
            "AI-powered metric analysis",
            "Log pattern recognition",
            "Real-time anomaly alerts",
            "Historical trend analysis"
        ]
    },
    
    "kubernetes_shell": {
        "questions": [
            "kubernetes shell",
            "kubectl",
            "cluster explorer",
            "run commands",
            "cluster management",
            "how do i access the kubernetes shell",
            "access kubernetes shell"
        ],
        "answer": "Access the Kubernetes Shell and Cluster Explorer to run kubectl commands, explore your cluster resources, and manage your Kubernetes environment directly from SmartOps.",
        "page": "Kubernetes Shell and Cluster Explorer",
        "page_number": 3,
        "features": [
            "Interactive kubectl shell",
            "Cluster resource exploration",
            "Command execution",
            "Resource monitoring"
        ]
    },
    
    "auto_scaling": {
        "questions": [
            "auto scaling",
            "scaling recommendations",
            "scale pods",
            "resource optimization",
            "performance tuning",
            "tell me about auto scaling",
            "auto scaling features"
        ],
        "answer": "Get intelligent auto-scaling recommendations and control pod scaling based on AI analysis of your cluster performance and resource usage patterns.",
        "page": "Auto Scaling Recommendations and Control",
        "page_number": 5,
        "features": [
            "AI-powered scaling recommendations",
            "Automatic pod scaling",
            "Resource optimization suggestions",
            "Performance monitoring"
        ]
    },
    
    "incident_management": {
        "questions": [
            "incident timeline",
            "postmortem report",
            "incident management",
            "troubleshooting",
            "issue tracking",
            "what is the incident management page",
            "incident management features"
        ],
        "answer": "Track incidents, generate postmortem reports, and maintain a comprehensive timeline of cluster events and issues for better incident management.",
        "page": "Incident Timeline and Postmortem Report Generator",
        "page_number": 6,
        "features": [
            "Incident timeline tracking",
            "Automated postmortem reports",
            "Issue correlation analysis",
            "Resolution tracking"
        ]
    },
    
    "ai_actions": {
        "questions": [
            "ai actions",
            "automated actions",
            "ai automation",
            "smart operations"
        ],
        "answer": "Execute AI-powered automated actions to resolve issues, optimize performance, and maintain cluster health without manual intervention.",
        "page": "AI Actions",
        "page_number": 8,
        "features": [
            "Automated issue resolution",
            "Intelligent resource management",
            "Predictive maintenance",
            "Smart operations automation"
        ]
    },
    
    "deployments": {
        "questions": [
            "deployments",
            "deployment events",
            "deployment tracking",
            "rollout status"
        ],
        "answer": "Monitor deployment events, track rollout status, and manage application deployments with comprehensive visibility and control.",
        "page": "Deployments",
        "page_number": 9,
        "features": [
            "Deployment event tracking",
            "Rollout status monitoring",
            "Deployment history",
            "Rollback capabilities"
        ]
    },
    
    "overview": {
        "questions": [
            "overview",
            "dashboard",
            "main page",
            "home",
            "summary"
        ],
        "answer": "Get a comprehensive overview of your Kubernetes cluster with real-time metrics, system health status, and key performance indicators.",
        "page": "Overview",
        "page_number": 1,
        "features": [
            "Cluster health overview",
            "Real-time metrics dashboard",
            "System status monitoring",
            "Performance indicators"
        ]
    }
}

def get_knowledge_base():
    """Return the complete knowledge base"""
    return SMARTOPS_KNOWLEDGE_BASE

def search_knowledge(query):
    """Search the knowledge base for relevant information"""
    query_lower = query.lower()
    results = []
    
    for category, info in SMARTOPS_KNOWLEDGE_BASE.items():
        # Check if any question matches the query
        for question in info["questions"]:
            if question in query_lower or any(word in query_lower for word in question.split()):
                results.append({
                    "category": category,
                    "answer": info["answer"],
                    "page": info["page"],
                    "page_number": info["page_number"],
                    "features": info["features"],
                    "relevance_score": len([word for word in question.split() if word in query_lower])
                })
    
    # Sort by relevance score
    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    return results

def get_page_navigation_info(page_number):
    """Get navigation information for a specific page"""
    page_mapping = {
        1: "Overview",
        2: "Pod Explorer and Logs", 
        3: "Kubernetes Shell and Cluster Explorer",
        4: "Anomaly Detection",
        5: "Auto Scaling Recommendations and Control",
        6: "Incident Timeline and Postmortem Report Generator",
        8: "AI Actions",
        9: "Deployments"
    }
    
    if page_number in page_mapping:
        return {
            "page_name": page_mapping[page_number],
            "navigation_instruction": f"Navigate to page {page_number}: {page_mapping[page_number]}",
            "url_path": f"page_{page_number}"
        }
    return None
