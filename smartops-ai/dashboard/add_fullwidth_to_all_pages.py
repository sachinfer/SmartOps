#!/usr/bin/env python3
"""
Script to add ultra-aggressive full-width CSS to all dashboard pages
"""

import os
import glob

# Ultra-aggressive full-width CSS template
FULLWIDTH_CSS = '''# Ultra-aggressive full-width CSS
st.markdown("""
<style>
/* Force full width on ALL elements */
* {
    max-width: 100vw !important;
}

/* Streamlit specific overrides */
.main .block-container,
.block-container,
.stApp > div,
[data-testid="stAppViewContainer"],
.stApp > div > div,
.stApp > div > div > div {
    max-width: 100vw !important;
    width: 100vw !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
    margin-left: 0 !important;
    margin-right: 0 !important;
}

/* Force full width on all containers */
.stApp > div > div > div > div,
.stApp > div > div > div > div > div,
.stApp > div > div > div > div > div > div {
    max-width: 100vw !important;
    width: 100vw !important;
}

/* Override any remaining constraints */
.main .block-container > div,
.main .block-container > div > div {
    max-width: 100vw !important;
    width: 100vw !important;
}

/* Force full width on page content */
.main .block-container > div > div {
    max-width: 100vw !important;
    width: 100vw !important;
    padding: 0 !important;
    margin: 0 !important;
}
</style>
""", unsafe_allow_html=True)

'''

def add_fullwidth_to_page(file_path):
    """Add full-width CSS to a page file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if full-width CSS already exists
        if 'max-width: 100vw !important' in content:
            print(f"✅ {os.path.basename(file_path)} - Already has full-width CSS")
            return False
        
        # Find the right place to insert CSS (after imports, before main logic)
        lines = content.split('\n')
        
        # Look for the first function definition or main logic
        insert_index = 0
        for i, line in enumerate(lines):
            if line.strip().startswith('def ') or line.strip().startswith('st.'):
                insert_index = i
                break
        
        # Insert the CSS before the first function or Streamlit call
        lines.insert(insert_index, '')
        lines.insert(insert_index, FULLWIDTH_CSS)
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print(f"✅ {os.path.basename(file_path)} - Added full-width CSS")
        return True
        
    except Exception as e:
        print(f"❌ {os.path.basename(file_path)} - Error: {e}")
        return False

def main():
    """Main function to process all page files"""
    print("🚀 Adding ultra-aggressive full-width CSS to all dashboard pages...")
    print()
    
    # Get all Python files in pages directory
    pages_dir = "pages"
    if not os.path.exists(pages_dir):
        print(f"❌ Pages directory not found: {pages_dir}")
        return
    
    page_files = glob.glob(os.path.join(pages_dir, "*.py"))
    
    if not page_files:
        print("❌ No page files found")
        return
    
    print(f"Found {len(page_files)} page files:")
    for file_path in page_files:
        print(f"  - {os.path.basename(file_path)}")
    
    print()
    
    # Process each page file
    updated_count = 0
    for file_path in page_files:
        if add_fullwidth_to_page(file_path):
            updated_count += 1
    
    print()
    print(f"🎉 Updated {updated_count} out of {len(page_files)} page files")
    print("All pages now have ultra-aggressive full-width CSS!")

if __name__ == "__main__":
    main()
