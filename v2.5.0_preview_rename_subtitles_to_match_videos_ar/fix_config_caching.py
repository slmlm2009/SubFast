#!/usr/bin/env python3
"""Fix config caching issue by moving CONFIG loading to main block"""

with open('rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking_configurable.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix 1: Change module-level CONFIG loading (around line 211-212)
for i, line in enumerate(lines):
    if line.strip() == '# Load configuration at module level':
        lines[i] = '# Configuration loaded in main() to avoid caching issues\n'
        if i + 1 < len(lines) and 'CONFIG = load_configuration()' in lines[i + 1]:
            lines[i + 1] = 'CONFIG = None\n'
        print(f"Fixed module-level CONFIG at line {i+1}")
        break

# Fix 2: Add config loading to main block (after target_dir line)
for i, line in enumerate(lines):
    if 'target_dir = sys.argv[1] if len(sys.argv) > 1 else None' in line:
        # Found the target_dir line, insert config loading after it
        # Find the next non-empty line
        j = i + 1
        while j < len(lines) and lines[j].strip() == '':
            j += 1
        
        # Insert config loading before the next statement
        config_loading = [
            '    \n',
            '    # Load configuration FRESH on each run (avoids Python module caching)\n',
            '    global CONFIG\n',
            '    CONFIG = load_configuration()\n'
        ]
        
        lines = lines[:j] + config_loading + lines[j:]
        print(f"Added config loading to main block at line {j+1}")
        break

# Write back
with open('rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking_configurable.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Config caching fix applied successfully!")
print("- Module-level CONFIG set to None")
print("- Config loading moved to main block")
print("- Changes to config.ini will now be detected immediately")
