#!/usr/bin/env python3
"""Add support for directory argument"""

with open('rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking_configurable.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Add target_directory parameter to function
content = content.replace(
    'def rename_subtitles_to_match_videos():\n    directory = os.getcwd()',
    'def rename_subtitles_to_match_videos(target_directory=None):\n    directory = target_directory if target_directory else os.getcwd()'
)

# Fix 2: Pass sys.argv[1] in main
content = content.replace(
    '    renamed_count, movie_mode_detected, original_videos, original_subtitles, rename_map = rename_subtitles_to_match_videos()',
    '    # Get target directory from command line argument if provided\n    target_dir = sys.argv[1] if len(sys.argv) > 1 else None\n    \n    renamed_count, movie_mode_detected, original_videos, original_subtitles, rename_map = rename_subtitles_to_match_videos(target_dir)'
)

with open('rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking_configurable.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Directory argument support added successfully!")
