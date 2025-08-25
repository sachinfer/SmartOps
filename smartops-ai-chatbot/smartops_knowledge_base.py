"""
SmartOps Knowledge Base for AI Chatbot
Contains comprehensive information about SmartOps features, pages, and navigation
"""

import re
from typing import Dict, List, Optional

# Comprehensive SmartOps Knowledge Base
SMARTOPS_KNOWLEDGE_BASE = {
    "overview": {
        "questions": [
            "how to get overview",
            "cluster overview",
            "dashboard overview",
            "what is smartops",
            "main dashboard",
            "cluster health",
            "system status"
        ],
        "answer": "SmartOps provides a comprehensive overview of your Kubernetes cluster. The main dashboard shows cluster health, resource usage, and system status at a glance.",
        "page": "Overview",
        "page_number": 1,
        "features": [
            "Real-time cluster health monitoring",
            "Resource usage metrics",
            "System status overview",
            "Performance analytics"
        ]
    },
    "pod_management": {
        "questions": [
            "how to check pods",
            "how can ai check pods",
            "pod status",
            "pod logs",
            "pod explorer",
            "view pods",
            "monitor pods",
            "pod health"
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
    "kubernetes_shell": {
        "questions": [
            "how to access kubernetes shell",
            "kubernetes shell",
            "cluster explorer",
            "kubectl commands",
            "cluster access",
            "shell access",
            "command line access"
        ],
        "answer": "SmartOps includes a built-in Kubernetes shell for direct cluster access. You can run kubectl commands, explore resources, and manage your cluster directly from the interface.",
        "page": "Kubernetes Shell and Cluster Explorer",
        "page_number": 3,
        "features": [
            "Built-in kubectl access",
            "Cluster resource exploration",
            "Command execution",
            "Resource management"
        ]
    },
    "anomaly_detection": {
        "questions": [
            "what is anomaly detection",
            "anomaly detection",
            "ai monitoring",
            "intelligent monitoring",
            "issue detection",
            "problem identification",
            "smart monitoring"
        ],
        "answer": "SmartOps uses AI-powered anomaly detection to automatically identify issues in your Kubernetes cluster. It monitors metrics, logs, and behavior patterns to detect potential problems before they become critical.",
        "page": "Anomaly Detection",
        "page_number": 4,
        "features": [
            "AI-powered issue detection",
            "Automated problem identification",
            "Predictive analytics",
            "Intelligent alerting"
        ]
    },
    "auto_scaling": {
        "questions": [
            "auto scaling",
            "scaling recommendations",
            "resource scaling",
            "pod scaling",
            "cluster scaling",
            "scaling control",
            "automatic scaling"
        ],
        "answer": "SmartOps provides intelligent auto-scaling recommendations and control for your Kubernetes cluster. It analyzes resource usage patterns and suggests optimal scaling strategies.",
        "page": "Auto Scaling Recommendations and Control",
        "page_number": 5,
        "features": [
            "Intelligent scaling recommendations",
            "Resource usage analysis",
            "Automated scaling control",
            "Performance optimization"
        ]
    },
    "incident_management": {
        "questions": [
            "incident management",
            "timeline tracking",
            "postmortem reports",
            "incident tracking",
            "problem resolution",
            "incident history",
            "resolution tracking"
        ],
        "answer": "SmartOps includes comprehensive incident management with timeline tracking and automated postmortem report generation. Track issues from detection to resolution.",
        "page": "Incident Timeline and Postmortem Report Generator",
        "page_number": 6,
        "features": [
            "Incident timeline tracking",
            "Automated postmortem reports",
            "Resolution tracking",
            "Historical analysis"
        ]
    },
    "ai_actions": {
        "questions": [
            "ai actions",
            "automated operations",
            "ai automation",
            "smart operations",
            "automated tasks",
            "ai workflows"
        ],
        "answer": "SmartOps AI Actions provide automated operations and intelligent workflows for common Kubernetes tasks. Let AI handle routine operations while you focus on strategic decisions.",
        "page": "AI Actions",
        "page_number": 8,
        "features": [
            "Automated operations",
            "Intelligent workflows",
            "Smart task execution",
            "AI-powered automation"
        ]
    },
    "deployments": {
        "questions": [
            "deployments",
            "deployment monitoring",
            "deployment status",
            "deployment management",
            "app deployments",
            "deployment tracking"
        ],
        "answer": "SmartOps provides comprehensive deployment monitoring and management. Track deployment status, manage rollouts, and monitor application health across your cluster.",
        "page": "Deployments",
        "page_number": 9,
        "features": [
            "Deployment status monitoring",
            "Rollout management",
            "Application health tracking",
            "Deployment history"
        ]
    }
}

def search_knowledge(query: str, top_k: int = 3) -> List[Dict]:
    """
    Search the knowledge base for relevant information
    """
    query_lower = query.lower()
    results = []
    
    for category, info in SMARTOPS_KNOWLEDGE_BASE.items():
        relevance_score = 0
        
        # Check questions for exact matches
        for question in info["questions"]:
            if query_lower in question.lower():
                relevance_score += 10
            elif any(word in question.lower() for word in query_lower.split()):
                relevance_score += 5
        
        # Check answer content
        if query_lower in info["answer"].lower():
            relevance_score += 3
        
        # Check category name
        if query_lower in category.lower():
            relevance_score += 2
        
        if relevance_score > 0:
            results.append({
                "category": category,
                "answer": info["answer"],
                "page": info["page"],
                "page_number": info["page_number"],
                "features": info["features"],
                "relevance_score": relevance_score
            })
    
    # Sort by relevance score and return top results
    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    return results[:top_k]

def get_knowledge_base() -> Dict:
    """
    Get the complete knowledge base
    """
    return SMARTOPS_KNOWLEDGE_BASE

def get_page_info(page_number: int) -> Optional[Dict]:
    """
    Get information about a specific page
    """
    for category, info in SMARTOPS_KNOWLEDGE_BASE.items():
        if info["page_number"] == page_number:
            return info
    return None

def get_navigation_guide(page_number: int) -> Dict:
    """
    Get navigation instructions for a specific page
    """
    page_info = get_page_info(page_number)
    if page_info:
        return {
            "page_name": page_info["page"],
            "page_number": page_info["page_number"],
            "instruction": f"Navigate to {page_info['page']} to access {', '.join(page_info['features'][:2])}."
        }
    return None
