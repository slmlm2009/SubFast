#!/usr/bin/env python3
"""Fix negative count bug in movie mode"""

content = open('rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking.py', 'r', encoding='utf-8').read()

# Fix the calculation to prevent negative values
old = '    unmatched_subtitles = total_subtitles - renamed_count - unidentified_subtitle_count\n'
new = '    unmatched_subtitles = max(0, total_subtitles - renamed_count - unidentified_subtitle_count)\n'

if old in content:
    content = content.replace(old, new)
    open('rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking.py', 'w', encoding='utf-8').write(content)
    print('[OK] Fixed negative count bug - added max(0, ...) to prevent negative values')
else:
    print('[FAIL] Could not find the line to fix')
