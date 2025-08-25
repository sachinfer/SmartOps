"""
Test Misi AI Chatbot Integration
Run this to test that Misi can be integrated into pages
"""

import sys
import os

# Add current directory to path
sys.path.append('.')

def test_misi_imports():
    """Test that all Misi components can be imported"""
    print("🧪 Testing Misi imports...")
    
    try:
        from misi_chatbot_widget import MisiChatbotWidget
        print("✅ MisiChatbotWidget imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import MisiChatbotWidget: {e}")
        return False
    
    try:
        from misi_integration import add_misi_to_page, add_misi_to_sidebar
        print("✅ Misi integration functions imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Misi integration: {e}")
        return False
    
    try:
        from ai_chatbot_engine import SmartOpsAIChatbot
        print("✅ AI chatbot engine imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import AI chatbot engine: {e}")
        return False
    
    try:
        from smartops_knowledge_base import get_knowledge_base
        print("✅ Knowledge base imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import knowledge base: {e}")
        return False
    
    return True

def test_misi_widget_creation():
    """Test that Misi widget can be created"""
    print("\n🧪 Testing Misi widget creation...")
    
    try:
        from misi_chatbot_widget import MisiChatbotWidget
        
        # Create widget
        misi = MisiChatbotWidget()
        print("✅ MisiChatbotWidget created successfully")
        
        # Test chatbot functionality
        response = misi.chatbot.process_query("Hello")
        print(f"✅ Chatbot response test: {response['answer'][:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create Misi widget: {e}")
        return False

def test_misi_integration_functions():
    """Test that Misi integration functions work"""
    print("\n🧪 Testing Misi integration functions...")
    
    try:
        from misi_integration import (
            add_misi_to_page, 
            add_misi_to_sidebar, 
            add_misi_quick_help,
            add_misi_top_right,
            add_misi_bottom_left,
            add_misi_top_left,
            add_misi_bottom_right
        )
        
        print("✅ All Misi integration functions imported successfully")
        
        # Test convenience functions
        functions = [
            add_misi_top_right,
            add_misi_bottom_left,
            add_misi_top_left,
            add_misi_bottom_right
        ]
        
        for func in functions:
            print(f"✅ {func.__name__} function available")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to test Misi integration functions: {e}")
        return False

def test_knowledge_base():
    """Test that knowledge base is working"""
    print("\n🧪 Testing knowledge base...")
    
    try:
        from smartops_knowledge_base import get_knowledge_base, search_knowledge
        
        # Get knowledge base
        kb = get_knowledge_base()
        print(f"✅ Knowledge base loaded: {len(kb)} categories")
        
        # Test search
        results = search_knowledge("pods")
        print(f"✅ Search test: Found {len(results)} results for 'pods'")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to test knowledge base: {e}")
        return False

def test_chatbot_functionality():
    """Test that chatbot functionality works"""
    print("\n🧪 Testing chatbot functionality...")
    
    try:
        from ai_chatbot_engine import SmartOpsAIChatbot
        
        # Create chatbot
        chatbot = SmartOpsAIChatbot()
        
        # Test queries
        test_queries = [
            "Hello",
            "How can AI check pods?",
            "What is anomaly detection?"
        ]
        
        for query in test_queries:
            response = chatbot.process_query(query)
            print(f"✅ Query '{query}': Response length {len(response['answer'])} chars")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to test chatbot functionality: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Misi AI Chatbot Integration")
    print("=" * 50)
    
    tests = [
        test_misi_imports,
        test_misi_widget_creation,
        test_misi_integration_functions,
        test_knowledge_base,
        test_chatbot_functionality
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        else:
            print(f"❌ Test {test.__name__} failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Misi integration is ready to use.")
        print("\n💡 To use Misi in your pages, add this line:")
        print("   from smartops_ai_chatbot.misi_integration import add_misi_to_page")
        print("   add_misi_to_page()")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
