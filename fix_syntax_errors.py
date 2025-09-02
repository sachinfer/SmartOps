#!/usr/bin/env python3
"""
Script to fix syntax errors in dashboard pages
"""

import os
import re

# Directory containing the pages
pages_dir = "smartops-ai/dashboard/pages"

def fix_syntax_errors(file_path):
    """Fix syntax errors in a single page file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remove broken lines at the beginning
        content = re.sub(r'^", unsafe_allow_html=True\)\s*\n', '', content, flags=re.MULTILINE)
        
        # Remove any remaining broken st.markdown calls
        content = re.sub(r'^", unsafe_allow_html=True\)\s*\n', '', content, flags=re.MULTILINE)
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed syntax errors in {file_path}")
            return True
        else:
            print(f"ℹ️ No syntax errors found in {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return False

def main():
    """Main function to fix all page syntax errors"""
    if not os.path.exists(pages_dir):
        print(f"❌ Pages directory not found: {pages_dir}")
        return
    
    print("🔧 Fixing syntax errors in all dashboard pages...")
    
    fixed_count = 0
    total_count = 0
    
    # Get all Python files in the pages directory
    for filename in os.listdir(pages_dir):
        if filename.endswith('.py'):
            file_path = os.path.join(pages_dir, filename)
            total_count += 1
            
            if fix_syntax_errors(file_path):
                fixed_count += 1
    
    print(f"\n🎉 Syntax error fixes complete!")
    print(f"📊 Fixed {fixed_count} out of {total_count} files")
    
    if fixed_count > 0:
        print("\n🚀 All pages should now load without syntax errors!")
        print("📋 Next steps:")
        print("1. Commit and push changes")
        print("2. Wait for pipeline deployment")
        print("3. Test all pages")

if __name__ == "__main__":
    main()
