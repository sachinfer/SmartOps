"""
Test script for SmartOps AI Chatbot
Run this to test the chatbot functionality
"""

from ai_chatbot_engine import SmartOpsAIChatbot
from smartops_knowledge_base import search_knowledge, get_knowledge_base

def test_chatbot():
    """Test the chatbot with various queries"""
    print("🤖 Testing SmartOps AI Chatbot")
    print("=" * 50)
    
    # Initialize chatbot
    chatbot = SmartOpsAIChatbot()
    
    # Test queries
    test_queries = [
        "Hello",
        "How can AI check pods?",
        "What is anomaly detection?",
        "How do I access the Kubernetes shell?",
        "Tell me about auto-scaling",
        "What can you do?",
        "Thank you",
        "How do I check pod status?",
        "What is the incident management page?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🧪 Test {i}: '{query}'")
        print("-" * 30)
        
        try:
            response = chatbot.process_query(query)
            
            print(f"✅ Answer: {response['answer']}")
            
            if response.get('navigation_guide'):
                nav = response['navigation_guide']
                print(f"🧭 Navigation: Page {nav['page_number']} - {nav['page_name']}")
            
            if response.get('suggested_questions'):
                print("💡 Suggested Questions:")
                for q in response['suggested_questions'][:2]:
                    print(f"   • {q}")
            
            print(f"🎯 Confidence: {response.get('confidence', 'N/A'):.1%}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("📊 Knowledge Base Statistics:")
    
    kb = get_knowledge_base()
    print(f"   Categories: {len(kb)}")
    print(f"   Total Features: {sum(len(info['features']) for info in kb.values())}")
    
    # Test search functionality
    print("\n🔍 Testing Knowledge Search:")
    search_results = search_knowledge("pods")
    print(f"   Search results for 'pods': {len(search_results)}")
    
    for result in search_results[:2]:
        print(f"   • {result['category']} (Score: {result['relevance_score']})")
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    test_chatbot()
