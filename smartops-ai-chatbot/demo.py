"""
SmartOps AI Chatbot Demo
Demonstrates the chatbot's capabilities with interactive examples
"""

from ai_chatbot_engine import SmartOpsAIChatbot
from smartops_knowledge_base import get_knowledge_base
import time

def print_separator():
    print("=" * 80)

def print_header(title):
    print(f"\n{'='*20} {title} {'='*20}")

def demo_basic_functionality():
    """Demonstrate basic chatbot functionality"""
    print_header("Basic Functionality Demo")
    
    chatbot = SmartOpsAIChatbot()
    
    # Test basic queries
    test_queries = [
        "Hello",
        "What can you do?",
        "Thank you"
    ]
    
    for query in test_queries:
        print(f"\n👤 User: {query}")
        response = chatbot.process_query(query)
        print(f"🤖 AI: {response['answer']}")
        print(f"🎯 Confidence: {response['confidence']:.1%}")
        time.sleep(1)

def demo_knowledge_queries():
    """Demonstrate knowledge-based queries"""
    print_header("Knowledge Queries Demo")
    
    chatbot = SmartOpsAIChatbot()
    
    # Test knowledge queries
    knowledge_queries = [
        "How can AI check pods?",
        "What is anomaly detection?",
        "How do I access the Kubernetes shell?",
        "Tell me about auto-scaling"
    ]
    
    for query in knowledge_queries:
        print(f"\n👤 User: {query}")
        response = chatbot.process_query(query)
        print(f"🤖 AI: {response['answer']}")
        
        if response.get('navigation_guide'):
            nav = response['navigation_guide']
            print(f"🧭 Navigation: Page {nav['page_number']} - {nav['page_name']}")
        
        if response.get('suggested_questions'):
            print("💡 Suggested Questions:")
            for q in response['suggested_questions'][:2]:
                print(f"   • {q}")
        
        print(f"🎯 Confidence: {response['confidence']:.1%}")
        time.sleep(1)

def demo_navigation_guidance():
    """Demonstrate navigation guidance"""
    print_header("Navigation Guidance Demo")
    
    chatbot = SmartOpsAIChatbot()
    
    # Test navigation queries
    nav_queries = [
        "I want to check pod status",
        "Show me anomaly detection",
        "How do I run kubectl commands?",
        "Where can I see auto-scaling recommendations?"
    ]
    
    for query in nav_queries:
        print(f"\n👤 User: {query}")
        response = chatbot.process_query(query)
        
        if response.get('navigation_guide'):
            nav = response['navigation_guide']
            print(f"🧭 AI suggests: Navigate to Page {nav['page_number']}")
            print(f"   Page Name: {nav['page_name']}")
            print(f"   Instruction: {nav['instruction']}")
        else:
            print("❌ No navigation guidance available")
        
        print(f"🎯 Confidence: {response['confidence']:.1%}")
        time.sleep(1)

def demo_conversation_context():
    """Demonstrate conversation context maintenance"""
    print_header("Conversation Context Demo")
    
    chatbot = SmartOpsAIChatbot()
    
    # Simulate a conversation
    conversation = [
        "Hello",
        "I need help with pods",
        "What about logs?",
        "How do I check resource usage?"
    ]
    
    print("🔄 Simulating a conversation...")
    
    for i, query in enumerate(conversation, 1):
        print(f"\n--- Turn {i} ---")
        print(f"👤 User: {query}")
        
        response = chatbot.process_query(query)
        print(f"🤖 AI: {response['answer'][:100]}...")
        
        # Show context
        if i > 1:
            context = chatbot.get_context_summary()
            print(f"📋 Context: {len(chatbot.get_conversation_history())} messages")
        
        time.sleep(1)
    
    # Show final context
    print(f"\n📊 Final conversation has {len(chatbot.get_conversation_history())} messages")

def demo_knowledge_base():
    """Show knowledge base statistics"""
    print_header("Knowledge Base Overview")
    
    kb = get_knowledge_base()
    
    print(f"📚 Total Categories: {len(kb)}")
    print(f"🔧 Total Features: {sum(len(info['features']) for info in kb.values())}")
    
    print("\n📋 Available Categories:")
    for category, info in kb.items():
        print(f"   • {info['page']} (Page {info['page_number']})")
        print(f"     Features: {len(info['features'])}")
        print(f"     Questions: {len(info['questions'])}")

def demo_search_functionality():
    """Demonstrate search functionality"""
    print_header("Search Functionality Demo")
    
    from smartops_knowledge_base import search_knowledge
    
    search_terms = ["pods", "anomaly", "shell", "scaling"]
    
    for term in search_terms:
        print(f"\n🔍 Searching for: '{term}'")
        results = search_knowledge(term)
        
        print(f"   Found {len(results)} results:")
        for result in results[:3]:  # Show top 3
            print(f"     • {result['category']} (Score: {result['relevance_score']})")

def main():
    """Run all demos"""
    print("🚀 SmartOps AI Chatbot Demo")
    print("This demo showcases the chatbot's capabilities")
    
    try:
        # Run all demos
        demo_basic_functionality()
        demo_knowledge_queries()
        demo_navigation_guidance()
        demo_conversation_context()
        demo_knowledge_base()
        demo_search_functionality()
        
        print_header("Demo Completed Successfully!")
        print("✅ All functionality working correctly")
        print("🎯 The chatbot is ready for integration!")
        
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
        print("Please check the installation and try again")

if __name__ == "__main__":
    main()
