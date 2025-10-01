#!/usr/bin/env python3
"""Fix CSV export to use target directory instead of cwd()"""

with open('rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking_configurable.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Add directory parameter to export function signature
old_sig = 'def export_analysis_to_csv(renamed_count=0, movie_mode=False, original_videos=None, original_subtitles=None, rename_map=None, execution_time=None):'
new_sig = 'def export_analysis_to_csv(renamed_count=0, movie_mode=False, original_videos=None, original_subtitles=None, rename_map=None, execution_time=None, target_directory=None):'

content = content.replace(old_sig, new_sig)

# Fix 2: Update directory assignment in export function
old_dir = '    directory = os.getcwd()'
new_dir = '    directory = target_directory if target_directory else os.getcwd()'

content = content.replace(old_dir, new_dir)

# Fix 3: Update export call to pass directory parameter
old_call = '        export_analysis_to_csv(renamed_count, movie_mode_detected, original_videos, original_subtitles, rename_map, time_str)'
new_call = '        export_analysis_to_csv(renamed_count, movie_mode_detected, original_videos, original_subtitles, rename_map, time_str, target_dir)'

content = content.replace(old_call, new_call)

# Fix 4: Update return statement to include directory
old_return = '    return renamed_count, movie_mode_detected, original_video_files, original_subtitle_files, rename_mapping'
new_return = '    return renamed_count, movie_mode_detected, original_video_files, original_subtitle_files, rename_mapping, directory'

content = content.replace(old_return, new_return)

# Fix 5: Update main block to receive directory in return
old_main_call = '    renamed_count, movie_mode_detected, original_videos, original_subtitles, rename_map = rename_subtitles_to_match_videos(target_dir)'
new_main_call = '    renamed_count, movie_mode_detected, original_videos, original_subtitles, rename_map, processed_directory = rename_subtitles_to_match_videos(target_dir)'

content = content.replace(old_main_call, new_main_call)

with open('rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking_configurable.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("CSV export path fixed successfully!")
print("  - CSV will now be exported to target directory (not cwd)")
print("  - config.ini remains in script directory")
