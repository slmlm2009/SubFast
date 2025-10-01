#!/usr/bin/env python3
"""Replace get_episode_number calls with cached version"""

content = open('rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking.py', 'r', encoding='utf-8').read()

# Don't replace the function definition itself
# Replace the calls in various functions

# Count occurrences
count_before = content.count('get_episode_number(')

# Replace all calls (but not the definition line)
# Do NOT replace: "def get_episode_number(" or "def get_episode_number_cached("
lines = content.split('\n')
new_lines = []

for line in lines:
    # Skip function definitions
    if 'def get_episode_number(' in line or 'def get_episode_number_cached(' in line:
        new_lines.append(line)
    # Skip calls inside get_episode_number_cached (to avoid infinite recursion)
    elif '_episode_cache[filename] = get_episode_number(filename)' in line:
        new_lines.append(line)
    # Replace all other calls
    else:
        new_lines.append(line.replace('get_episode_number(', 'get_episode_number_cached('))

content = '\n'.join(new_lines)

# Count after
count_after = content.count('get_episode_number_cached(')

open('rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking.py', 'w', encoding='utf-8').write(content)

print(f'Replaced {count_after - 1} calls with cached version')  # -1 for the definition itself
print(f'Kept 2 unchanged: function definition and cache population')
