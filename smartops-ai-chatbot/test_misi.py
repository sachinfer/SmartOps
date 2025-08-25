"""
Test Script for Misi AI Chatbot
Verify all components work correctly
"""

import sys
import os

def test_imports():
    """Test if all modules can be imported"""
    try:
        from smartops_knowledge_base import search_knowledge, get_knowledge_base
        from ai_chatbot_engine import SmartOpsAIChatbot
        from misi_chatbot_widget import MisiChatbotWidget, add_misi_to_page
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_knowledge_base():
    """Test knowledge base functionality"""
    try:
        from smartops_knowledge_base import search_knowledge, get_knowledge_base
        
        # Test getting knowledge base
        kb = get_knowledge_base()
        if not kb:
            print("❌ Knowledge base is empty")
            return False
        
        print(f"✅ Knowledge base loaded with {len(kb)} categories")
        
        # Test search functionality
        results = search_knowledge("how can ai check pods")
        if not results:
            print("❌ Search returned no results")
            return False
        
        print(f"✅ Search returned {len(results)} results")
        print(f"   Top result: {results[0]['category']} - {results[0]['page']}")
        
        return True
    except Exception as e:
        print(f"❌ Knowledge base test failed: {e}")
        return False

def test_ai_engine():
    """Test AI chatbot engine"""
    try:
        from ai_chatbot_engine import SmartOpsAIChatbot
        
        chatbot = SmartOpsAIChatbot()
        
        # Test query processing
        response = chatbot.process_query("How can AI check pods?")
        
        if not response:
            print("❌ No response generated")
            return False
        
        print("✅ AI engine response generated:")
        print(f"   Answer: {response['answer'][:100]}...")
        print(f"   Confidence: {response.get('confidence', 'N/A')}")
        
        if response.get('navigation_guide'):
            nav = response['navigation_guide']
            print(f"   Navigation: Page {nav['page_number']} - {nav['page_name']}")
        
        return True
    except Exception as e:
        print(f"❌ AI engine test failed: {e}")
        return False

def test_misi_widget():
    """Test Misi widget creation"""
    try:
        from misi_chatbot_widget import MisiChatbotWidget
        
        widget = MisiChatbotWidget()
        print("✅ Misi widget created successfully")
        
        # Test methods exist
        if hasattr(widget, 'render_misi_icon'):
            print("✅ render_misi_icon method exists")
        else:
            print("❌ render_misi_icon method missing")
            return False
        
        if hasattr(widget, 'render_misi_integration'):
            print("✅ render_misi_integration method exists")
        else:
            print("❌ render_misi_integration method missing")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Misi widget test failed: {e}")
        return False

def test_integration_function():
    """Test the main integration function"""
    try:
        from misi_chatbot_widget import add_misi_to_page
        
        # Test function exists
        if callable(add_misi_to_page):
            print("✅ add_misi_to_page function is callable")
        else:
            print("❌ add_misi_to_page is not callable")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Integration function test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Misi AI Chatbot Components")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Knowledge Base", test_knowledge_base),
        ("AI Engine", test_ai_engine),
        ("Misi Widget", test_misi_widget),
        ("Integration Function", test_integration_function)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Testing {test_name}...")
        if test_func():
            passed += 1
            print(f"✅ {test_name} test passed")
        else:
            print(f"❌ {test_name} test failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Misi AI Chatbot is ready to use.")
        print("\n💡 To use Misi in your pages, add this line:")
        print("   from smartops_ai_chatbot.misi_chatbot_widget import add_misi_to_page")
        print("   add_misi_to_page()")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
