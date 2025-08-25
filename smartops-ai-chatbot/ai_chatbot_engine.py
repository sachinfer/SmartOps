"""
SmartOps AI Chatbot Engine
Core AI logic for processing queries and generating intelligent responses
"""

import re
from typing import Dict, List, Optional
from datetime import datetime
from smartops_knowledge_base import search_knowledge, get_knowledge_base

class SmartOpsAIChatbot:
    def __init__(self):
        self.conversation_history = []
        self.knowledge_base = get_knowledge_base()
        
    def process_query(self, user_query: str) -> Dict:
        """
        Process user query and generate comprehensive response
        """
        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_query,
            "timestamp": datetime.now()
        })
        
        # Search knowledge base
        search_results = search_knowledge(user_query, top_k=3)
        
        if not search_results:
            # No relevant information found
            response = self._generate_general_response(user_query)
        else:
            # Generate response based on best match
            best_match = search_results[0]
            response = self._generate_knowledge_response(best_match, search_results)
        
        # Add response to conversation history
        self.conversation_history.append({
            "role": "assistant",
            "content": response["answer"],
            "timestamp": datetime.now()
        })
        
        return response
    
    def _generate_general_response(self, query: str) -> Dict:
        """
        Generate response when no specific knowledge is found
        """
        return {
            "answer": f"I understand you're asking about '{query}'. While I don't have specific information about this, I can help you with SmartOps features like pod management, anomaly detection, Kubernetes shell access, and more. What would you like to know about?",
            "confidence": 0.3,
            "suggested_questions": [
                "How can I check pod status?",
                "What is anomaly detection?",
                "How do I access the Kubernetes shell?",
                "Tell me about auto-scaling"
            ],
            "navigation_guide": None
        }
    
    def _generate_knowledge_response(self, best_match: Dict, all_results: List[Dict]) -> Dict:
        """
        Generate response based on knowledge base match
        """
        # Calculate confidence based on relevance score
        max_score = max(result["relevance_score"] for result in all_results)
        confidence = min(best_match["relevance_score"] / max_score, 1.0)
        
        # Generate navigation guide
        navigation_guide = {
            "page_name": best_match["page"],
            "page_number": best_match["page_number"],
            "instruction": f"Navigate to {best_match['page']} to access {', '.join(best_match['features'][:2])}."
        }
        
        # Generate suggested questions
        suggested_questions = self._generate_suggested_questions(best_match, all_results)
        
        return {
            "answer": best_match["answer"],
            "confidence": confidence,
            "suggested_questions": suggested_questions,
            "navigation_guide": navigation_guide,
            "features": best_match["features"]
        }
    
    def _generate_suggested_questions(self, best_match: Dict, all_results: List[Dict]) -> List[str]:
        """
        Generate relevant follow-up questions
        """
        suggestions = []
        
        # Add related questions from other categories
        for result in all_results[:3]:  # Top 3 results
            if result["category"] != best_match["category"]:
                # Get a sample question from this category
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
        """
        Get conversation history
        """
        return self.conversation_history
    
    def clear_conversation_history(self):
        """
        Clear conversation history
        """
        self.conversation_history = []
    
    def get_available_features(self) -> List[str]:
        """
        Get list of available SmartOps features
        """
        features = []
        for category, info in self.knowledge_base.items():
            features.extend(info["features"])
        return list(set(features))  # Remove duplicates
    
    def get_page_summary(self, page_number: int) -> Optional[Dict]:
        """
        Get summary of a specific page
        """
        for category, info in self.knowledge_base.items():
            if info["page_number"] == page_number:
                return {
                    "page_name": info["page"],
                    "page_number": info["page_number"],
                    "description": info["answer"],
                    "key_features": info["features"]
                }
        return None
