#!/usr/bin/env python3
"""Fix config caching issue - corrected version"""

with open('rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking_configurable.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Change module-level CONFIG loading
old_module = "# Configuration loaded in main() to avoid caching issues\nCONFIG = None"
# It might already be fixed, let's check original
if "# Load configuration at module level\nCONFIG = load_configuration()" in content:
    content = content.replace(
        "# Load configuration at module level\nCONFIG = load_configuration()",
        "# Configuration loaded in main() to avoid caching issues\nCONFIG = None"
    )
    print("Fixed module-level CONFIG loading")
elif "CONFIG = None" in content:
    print("Module-level CONFIG already set to None")

# Fix 2: The main block is broken - let's fix the entire main block section
# Find and replace the broken section
old_main_broken = """    # Track execution time
    start_time = time.time()
    
    # Get target directory from command line argument if provided
    target_dir = sys.argv[1] if len(sys.argv) > 1 else None
    
    
    # Load configuration FRESH on each run (avoids Python module caching)
    global CONFIG
    CONFIG = load_configuration()
    renamed_count, movie_mode_detected, original_videos, original_subtitles, rename_map, processed_directory = rename_subtitles_to_match_videos(target_dir)"""

new_main_fixed = """    # Get target directory from command line argument if provided
    target_dir = sys.argv[1] if len(sys.argv) > 1 else None
    
    # Load configuration FRESH on each run (avoids Python module caching)
    global CONFIG
    CONFIG = load_configuration()
    
    # Track execution time
    start_time = time.time()
    
    renamed_count, movie_mode_detected, original_videos, original_subtitles, rename_map, processed_directory = rename_subtitles_to_match_videos(target_dir)"""

if old_main_broken in content:
    content = content.replace(old_main_broken, new_main_fixed)
    print("Fixed main block - reordered to load config after target_dir")
else:
    print("Main block structure not as expected, checking alternative...")
    # Try to find the issue and fix it differently
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'CONFIG = load_configuration()' in line and 'renamed_count' in line:
            # Found the broken line
            # Split it
            lines[i] = '    CONFIG = load_configuration()'
            # Insert the renamed_count line after with proper spacing
            lines.insert(i + 1, '    ')
            lines.insert(i + 2, '    # Track execution time')
            lines.insert(i + 3, '    start_time = time.time()')
            lines.insert(i + 4, '    ')
            lines.insert(i + 5, '    renamed_count, movie_mode_detected, original_videos, original_subtitles, rename_map, processed_directory = rename_subtitles_to_match_videos(target_dir)')
            # Remove Track execution time if it appears before
            for j in range(max(0, i - 10), i):
                if '# Track execution time' in lines[j]:
                    # Remove this and the next line (start_time = ...)
                    del lines[j:j+2]
                    break
            content = '\n'.join(lines)
            print(f"Fixed broken line at position {i}")
            break

# Write back
with open('rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking_configurable.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Config caching fix completed!")
