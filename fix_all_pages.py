#!/usr/bin/env python3
"""
Script to remove conflicting CSS from all dashboard pages
"""

import os
import re

# Directory containing the pages
pages_dir = "smartops-ai/dashboard/pages"

def remove_css_from_page(file_path):
    """Remove CSS and JavaScript from a single page file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remove CSS blocks
        css_patterns = [
            (r'# .*CSS.*\n.*st\.markdown\("""\n<style>.*?</style>.*?""', re.DOTALL),
            (r'# .*full-width.*CSS.*\n.*st\.markdown\("""\n<style>.*?</style>.*?""', re.DOTALL),
            (r'# .*Nuclear.*CSS.*\n.*st\.markdown\("""\n<style>.*?</style>.*?""', re.DOTALL),
            (r'# .*Ultra-aggressive.*CSS.*\n.*st\.markdown\("""\n<style>.*?</style>.*?""', re.DOTALL),
            (r'st\.markdown\("""\n<style>.*?</style>.*?""', re.DOTALL),
        ]
        
        for pattern, flags in css_patterns:
            content = re.sub(pattern, '', content, flags=flags)
        
        # Remove JavaScript blocks
        js_patterns = [
            (r'<!-- .*JavaScript.*?-->\s*<script>.*?</script>', re.DOTALL),
            (r'<script>.*?</script>', re.DOTALL),
        ]
        
        for pattern, flags in js_patterns:
            content = re.sub(pattern, '', content, flags=flags)
        
        # Clean up any remaining 100vw references
        content = re.sub(r'max-width:\s*100vw\s*!important', 'max-width: 100% !important', content)
        content = re.sub(r'width:\s*100vw\s*!important', 'width: 100% !important', content)
        content = re.sub(r'min-width:\s*100vw\s*!important', 'min-width: 100% !important', content)
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed CSS in {file_path}")
            return True
        else:
            print(f"ℹ️ No changes needed in {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return False

def main():
    """Main function to fix all page CSS"""
    if not os.path.exists(pages_dir):
        print(f"❌ Pages directory not found: {pages_dir}")
        return
    
    print("🔧 Removing conflicting CSS from all dashboard pages...")
    
    fixed_count = 0
    total_count = 0
    
    # Get all Python files in the pages directory
    for filename in os.listdir(pages_dir):
        if filename.endswith('.py'):
            file_path = os.path.join(pages_dir, filename)
            total_count += 1
            
            if remove_css_from_page(file_path):
                fixed_count += 1
    
    print(f"\n🎉 CSS cleanup complete!")
    print(f"📊 Fixed {fixed_count} out of {total_count} files")
    
    if fixed_count > 0:
        print("\n🚀 All pages now use consistent main layout!")
        print("📋 Next steps:")
        print("1. Commit and push changes")
        print("2. Wait for pipeline deployment")
        print("3. Test all pages for consistent layout")

if __name__ == "__main__":
    main()
