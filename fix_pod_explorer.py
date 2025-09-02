#!/usr/bin/env python3
"""
Script to fix the Pod Explorer page structure
"""

import re

def fix_pod_explorer():
    """Fix the Pod Explorer page by adding proper structure"""
    
    # Read the current file
    with open('smartops-ai/dashboard/pages/2_Pod_Explorer_and_Logs.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the main content section and fix indentation
    # Add proper function wrapper and fix indentation
    lines = content.split('\n')
    fixed_lines = []
    in_main_content = False
    indent_level = 0
    
    for line in lines:
        if 'def show_page():' in line:
            fixed_lines.append(line)
            indent_level = 4
            continue
        elif 'try:' in line and 'Main content with error handling' in lines[lines.index(line)-1]:
            fixed_lines.append('    ' + line)
            indent_level = 8
            continue
        elif 'except Exception:' in line and 'An unexpected error occurred' in lines[lines.index(line)+1]:
            fixed_lines.append('    ' + line)
            continue
        elif line.strip().startswith('st.') or line.strip().startswith('#') or line.strip().startswith('if ') or line.strip().startswith('for ') or line.strip().startswith('with ') or line.strip().startswith('else:') or line.strip().startswith('elif '):
            if 'def show_page():' in '\n'.join(fixed_lines):
                fixed_lines.append('    ' + line)
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    
    # Add the function call at the end
    if 'show_page()' not in '\n'.join(fixed_lines):
        fixed_lines.append('')
        fixed_lines.append('# Call the function to show the page')
        fixed_lines.append('show_page()')
    
    # Write the fixed content
    with open('smartops-ai/dashboard/pages/2_Pod_Explorer_and_Logs.py', 'w', encoding='utf-8') as f:
        f.write('\n'.join(fixed_lines))
    
    print("✅ Fixed Pod Explorer page structure")

if __name__ == "__main__":
    fix_pod_explorer()
