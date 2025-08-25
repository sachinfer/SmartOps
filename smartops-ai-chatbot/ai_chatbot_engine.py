"""
SmartOps AI Chatbot Engine
Processes user queries and provides intelligent responses with navigation guidance
"""

import re
from typing import Dict, List, Tuple
from smartops_knowledge_base import search_knowledge, get_page_navigation_info

class SmartOpsAIChatbot:
    def __init__(self):
        self.conversation_history = []
        self.context = {}
        
    def process_query(self, user_query: str) -> Dict:
        """
        Process user query and return AI response with navigation guidance
        """
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": user_query})
        
        # Search knowledge base
        knowledge_results = search_knowledge(user_query)
        
        # Generate response
        response = self._generate_response(user_query, knowledge_results)
        
        # Add response to history
        self.conversation_history.append({"role": "assistant", "content": response["answer"]})
        
        return response
    
    def _generate_response(self, query: str, knowledge_results: List[Dict]) -> Dict:
        """
        Generate intelligent response based on knowledge base results
        """
        query_lower = query.lower()
        
        # Check for specific patterns
        if self._is_greeting(query_lower):
            return self._generate_greeting_response()
        
        if self._is_help_request(query_lower):
            return self._generate_help_response()
        
        if self._is_thanks(query_lower):
            return self._generate_thanks_response()
        
        # Process knowledge-based queries
        if knowledge_results:
            best_match = knowledge_results[0]
            return self._generate_knowledge_response(best_match, knowledge_results)
        
        # Fallback response
        return self._generate_fallback_response(query)
    
    def _is_greeting(self, query: str) -> bool:
        """Check if query is a greeting"""
        greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
        return any(greeting in query for greeting in greetings)
    
    def _is_help_request(self, query: str) -> bool:
        """Check if query is asking for help"""
        help_terms = ["help", "what can you do", "how does this work", "guide me"]
        return any(term in query for term in help_terms)
    
    def _is_thanks(self, query: str) -> bool:
        """Check if query is expressing thanks"""
        thanks_terms = ["thank", "thanks", "appreciate", "grateful"]
        return any(term in query for term in thanks_terms)
    
    def _generate_greeting_response(self) -> Dict:
        """Generate greeting response"""
        return {
            "answer": "Hello! I'm your SmartOps AI assistant. I can help you with Kubernetes cluster management, pod monitoring, anomaly detection, and much more. How can I assist you today?",
            "navigation_guide": None,
            "suggested_questions": [
                "How can I check pod status?",
                "What is anomaly detection?",
                "How do I access the Kubernetes shell?",
                "Can you help with auto-scaling?"
            ],
            "confidence": 1.0
        }
    
    def _generate_help_response(self) -> Dict:
        """Generate help response"""
        return {
            "answer": "I'm here to help you navigate SmartOps! I can assist with:\n\n• **Pod Management**: Check pod status, view logs, monitor resources\n• **Anomaly Detection**: AI-powered issue identification\n• **Kubernetes Operations**: Shell access, cluster exploration\n• **Auto-scaling**: Intelligent scaling recommendations\n• **Incident Management**: Timeline tracking and reports\n\nJust ask me about any of these features!",
            "navigation_guide": None,
            "suggested_questions": [
                "How do I check pods?",
                "What is the anomaly detection page?",
                "How can I access the Kubernetes shell?",
                "Tell me about auto-scaling"
            ],
            "confidence": 1.0
        }
    
    def _generate_thanks_response(self) -> Dict:
        """Generate thanks response"""
        return {
            "answer": "You're welcome! I'm here to help make your Kubernetes operations smarter and more efficient. Feel free to ask me anything about SmartOps features or if you need help navigating to specific pages.",
            "navigation_guide": None,
            "suggested_questions": [
                "How can I monitor my cluster?",
                "What features are available?",
                "How do I get started?"
            ],
            "confidence": 1.0
        }
    
    def _generate_knowledge_response(self, best_match: Dict, all_results: List[Dict]) -> Dict:
        """Generate response based on knowledge base match"""
        page_info = get_page_navigation_info(best_match["page_number"])
        
        # Build comprehensive answer
        answer = f"{best_match['answer']}\n\n"
        
        if best_match["features"]:
            answer += "**Key Features:**\n"
            for feature in best_match["features"]:
                answer += f"• {feature}\n"
        
        # Add navigation guidance
        if page_info:
            answer += f"\n**Navigation:** {page_info['navigation_instruction']}"
            navigation_guide = {
                "page_number": best_match["page_number"],
                "page_name": page_info["page_name"],
                "instruction": page_info["navigation_instruction"]
            }
        else:
            navigation_guide = None
        
        # Generate suggested follow-up questions
        suggested_questions = self._generate_suggested_questions(best_match, all_results)
        
        return {
            "answer": answer,
            "navigation_guide": navigation_guide,
            "suggested_questions": suggested_questions,
            "confidence": min(0.9, 0.5 + (best_match["relevance_score"] * 0.1))
        }
    
    def _generate_fallback_response(self, query: str) -> Dict:
        """Generate fallback response when no knowledge match is found"""
        return {
            "answer": f"I understand you're asking about '{query}', but I need more specific information to help you effectively. Could you please rephrase your question or ask about specific SmartOps features like:\n\n• Pod management and monitoring\n• Anomaly detection\n• Kubernetes operations\n• Auto-scaling\n• Incident management\n\nI'm here to guide you to the right pages and explain how SmartOps can help!",
            "navigation_guide": None,
            "suggested_questions": [
                "How do I check pod status?",
                "What is anomaly detection?",
                "How can I access the Kubernetes shell?",
                "Tell me about SmartOps features"
            ],
            "confidence": 0.3
        }
    
    def _generate_suggested_questions(self, best_match: Dict, all_results: List[Dict]) -> List[str]:
        """Generate relevant follow-up questions"""
        suggestions = []
        
        # Add related questions from other categories
        for result in all_results[:3]:  # Top 3 results
            if result["category"] != best_match["category"]:
                # Get a sample question from this category
                # Since search results don't have questions, we'll use the category name
                category_name = result["category"].replace("_", " ").title()
                suggestions.append(f"What about {category_name}?")
        
        # Add general SmartOps questions
        general_questions = [
            "How do I get an overview of my cluster?",
            "What other features does SmartOps offer?",
            "How can I automate operations?"
        ]
        
        suggestions.extend(general_questions[:2])
        
        return suggestions[:4]  # Return max 4 suggestions
    
    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history
    
    def clear_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_context_summary(self) -> str:
        """Get summary of current conversation context"""
        if not self.conversation_history:
            return "No conversation context available."
        
        recent_messages = self.conversation_history[-4:]  # Last 4 messages
        context = "Recent conversation:\n"
        
        for msg in recent_messages:
            role = "You" if msg["role"] == "user" else "AI"
            content = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
            context += f"{role}: {content}\n"
        
        return context
