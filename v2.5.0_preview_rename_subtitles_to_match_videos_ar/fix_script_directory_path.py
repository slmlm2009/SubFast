#!/usr/bin/env python3
"""Fix get_script_directory to use __file__ instead of cwd()"""

with open('rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking_configurable.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and replace the get_script_directory function
for i in range(len(lines)):
    if 'def get_script_directory():' in lines[i]:
        # Replace next 2 lines
        if 'Get the current working directory' in lines[i + 1]:
            lines[i + 1] = '    """Get the script\'s directory where config.ini should be located"""\n'
        if 'return Path.cwd()' in lines[i + 2]:
            lines[i + 2] = '    return Path(__file__).parent\n'
        print("Fixed get_script_directory() to use __file__")
        break

# Write back
with open('rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking_configurable.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("[SUCCESS] Script directory path fixed!")
print("- config.ini will now be loaded from script directory")
print("- CSV will still be exported to target directory")
