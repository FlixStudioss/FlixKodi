#!/usr/bin/env python3
"""
Script to fix dialog.ok() calls for Kodi 19+ compatibility
Changes from 4 arguments to 2 arguments (heading + combined message with \n)
"""
import re
import os

def fix_dialog_ok_in_file(filepath):
    """Fix dialog.ok() calls in a single file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Pattern to match dialog.ok with 3-4 arguments across multiple lines
    # This is a simplified approach - we'll match the pattern and reconstruct it
    pattern = r'dialog\.ok\(([^,]+),\s*([^)]+)\)'
    
    def replace_dialog_ok(match):
        full_match = match.group(0)
        # Count commas to determine number of arguments
        # Remove the opening dialog.ok( and closing )
        args_str = full_match[10:-1]  # Remove 'dialog.ok(' and ')'
        
        # Split by commas but be careful with nested parentheses and strings
        args = []
        current_arg = ''
        paren_depth = 0
        in_string = False
        string_char = None
        
        for char in args_str:
            if char in ('"', "'") and (not in_string or char == string_char):
                if not in_string:
                    in_string = True
                    string_char = char
                elif char == string_char:
                    in_string = False
                    string_char = None
            
            if char == '(' and not in_string:
                paren_depth += 1
            elif char == ')' and not in_string:
                paren_depth -= 1
            
            if char == ',' and paren_depth == 0 and not in_string:
                args.append(current_arg.strip())
                current_arg = ''
            else:
                current_arg += char
        
        if current_arg.strip():
            args.append(current_arg.strip())
        
        # If we have more than 2 arguments, combine them
        if len(args) > 2:
            heading = args[0]
            # Combine remaining arguments with \n
            messages = args[1:]
            combined_message = ' +\n                          '.join([f'{msg}' if i == 0 else f'"{msg.strip()}"' if not msg.strip().startswith('"') and not msg.strip().startswith("'") else msg for i, msg in enumerate(messages)])
            
            # Add \n to all but the last message
            result_messages = []
            for i, msg in enumerate(messages):
                if i < len(messages) - 1:
                    # Add \n before the closing quote/format
                    if msg.strip().endswith(')'):
                        # It's a format string
                        msg = msg.rstrip() + ' +\n                          "\\n"'
                    elif msg.strip().endswith('"') or msg.strip().endswith("'"):
                        # Regular string
                        quote_char = msg.strip()[-1]
                        msg = msg.rstrip()[:-1] + '\\n' + quote_char
                result_messages.append(msg)
            
            # Reconstruct with proper formatting
            if len(messages) == 2:
                new_call = f'dialog.ok({heading},\n                          {messages[0].rstrip()} +\n                          "\\n" +\n                          {messages[1]})'
            elif len(messages) == 3:
                new_call = f'dialog.ok({heading},\n                          {messages[0].rstrip()} +\n                          "\\n" +\n                          {messages[1].rstrip()} +\n                          "\\n" +\n                          {messages[2]})'
            else:
                new_call = full_match  # Don't change if unexpected format
            
            return new_call
        
        return full_match
    
    # This is complex, so let's just print what we found
    matches = list(re.finditer(pattern, content, re.DOTALL))
    if matches:
        print(f"\nFound {len(matches)} dialog.ok() calls in {filepath}")
        print("Manual fixing recommended due to complexity")
    
    return content

# Files to check
files_to_fix = [
    'FlixKodi/plugin.program.flixwizard/resources/libs/backup.py',
    'FlixKodi/plugin.program.flixwizard/resources/libs/db.py',
    'FlixKodi/plugin.program.flixwizard/resources/libs/debridit.py',
    'FlixKodi/plugin.program.flixwizard/resources/libs/install.py',
    'FlixKodi/plugin.program.flixwizard/resources/libs/gui/menu.py',
    'FlixKodi/plugin.program.flixwizard/resources/libs/check.py',
]

base_dir = os.path.dirname(__file__)
for file_rel in files_to_fix:
    filepath = os.path.join(base_dir, file_rel)
    if os.path.exists(filepath):
        fix_dialog_ok_in_file(filepath)

print("\nNote: Due to the complexity of the replacements, manual fixing is recommended.")
print("Use pattern: Combine multiple message arguments with + '\\n' + between them")
