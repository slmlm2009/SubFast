#!/usr/bin/env python3
"""Fix remaining filename building locations in CSV export section"""

with open('rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking_configurable.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Target lines: 767, 782, 859, 886 (approximate, may have shifted)
# These are all in CSV export section with different indentation

changes_made = 0

i = 0
while i < len(lines):
    line = lines[i]
    
    # Look for the exact pattern that needs replacement
    if 'new_name = f"{base_name}.{CONFIG[\'language_suffix\']}{subtitle_ext}"' in line:
        # Check if already fixed
        if i > 0 and '# Build filename with optional language suffix' in lines[i-1]:
            i += 1
            continue
        
        # Determine indentation from current line
        indent = len(line) - len(line.lstrip())
        indent_str = ' ' * indent
        
        # Replace with conditional version
        lines[i] = f"{indent_str}# Build filename with optional language suffix\n"
        lines.insert(i + 1, f"{indent_str}if CONFIG['language_suffix']:\n")
        lines.insert(i + 2, f"{indent_str}    new_name = f\"{{base_name}}.{{CONFIG['language_suffix']}}{{subtitle_ext}}\"\n")
        lines.insert(i + 3, f"{indent_str}else:\n")
        lines.insert(i + 4, f"{indent_str}    new_name = f\"{{base_name}}{{subtitle_ext}}\"\n")
        
        changes_made += 1
        i += 5  # Skip the lines we just inserted
    else:
        i += 1

# Write back
with open('rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking_configurable.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"[SUCCESS] Fixed {changes_made} additional filename building locations")
