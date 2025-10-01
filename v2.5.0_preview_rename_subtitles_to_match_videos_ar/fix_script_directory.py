#!/usr/bin/env python3
"""Fix get_script_directory() to use __file__ instead of cwd()"""

with open('rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking_configurable.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the function
old_function = '''def get_script_directory():
    """Get the current working directory where the script will look for config.ini"""
    return Path.cwd()'''

new_function = '''def get_script_directory():
    """
    Get the directory where the script file is located.
    This ensures config.ini is always in the same folder as the script,
    regardless of where the script is called from (e.g., right-click context menu).
    
    Returns:
        Path: Absolute path to the directory containing the script file
    """
    return Path(__file__).parent.resolve()'''

if old_function in content:
    content = content.replace(old_function, new_function)
    
    with open('rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking_configurable.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ Successfully updated get_script_directory() function")
    print("  - Changed from: Path.cwd()")
    print("  - Changed to: Path(__file__).parent.resolve()")
else:
    print("✗ Could not find the function to replace")
    print("  Function may have already been modified")
