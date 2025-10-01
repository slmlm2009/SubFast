#!/usr/bin/env python3
"""Simple caching optimization - most critical performance gain"""

with open('rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Step 1: Add cache variable after COMMON_INDICATORS dict
old_1 = '''}\n\ndef get_episode_number(filename):'''
new_1 = '''}\n\n# Performance optimization: Episode number cache\n_episode_cache = {}\n\ndef get_episode_number(filename):'''

if old_1 in content:
    content = content.replace(old_1, new_1, 1)
    print("[OK] Added episode cache variable")
else:
    print("[FAIL] Could not find insertion point for cache variable")
    exit(1)

# Step 2: Add cached wrapper function after get_episode_number
old_2 = '''    return None\n\ndef extract_season_episode_numbers(episode_string):'''
new_2 = '''    return None\n\ndef get_episode_number_cached(filename):\n    """Cached wrapper - extracts episode once per filename."""\n    if filename not in _episode_cache:\n        _episode_cache[filename] = get_episode_number(filename)\n    return _episode_cache[filename]\n\ndef extract_season_episode_numbers(episode_string):'''

if old_2 in content:
    content = content.replace(old_2, new_2, 1)
    print("[OK] Added cached wrapper function")
else:
    print("[FAIL] Could not find insertion point for cached function")
    exit(1)

# Step 3: Replace all get_episode_number calls with cached version
# BUT exclude: 
# - The function definition itself  
# - The call inside get_episode_number_cached (to avoid infinite recursion)

# Split by lines to be selective
lines = content.split('\n')
in_get_episode_func = False
in_cached_func = False
replacements = 0

new_lines = []
for i, line in enumerate(lines):
    # Track which function we're in
    if 'def get_episode_number(filename):' in line:
        in_get_episode_func = True
        in_cached_func = False
    elif 'def get_episode_number_cached(filename):' in line:
        in_cached_func = True
        in_get_episode_func = False
    elif line.startswith('def ') and not line.startswith('    def'):
        in_get_episode_func = False
        in_cached_func = False
    
    # Don't replace inside the original function or the cache update line
    if in_get_episode_func or (in_cached_func and 'get_episode_number(filename)' in line):
        new_lines.append(line)
    elif 'get_episode_number(' in line:
        new_line = line.replace('get_episode_number(', 'get_episode_number_cached(')
        if new_line != line:
            replacements += 1
        new_lines.append(new_line)
    else:
        new_lines.append(line)

content = '\n'.join(new_lines)

print(f"[OK] Replaced {replacements} calls with cached version")

# Write back
with open('rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n[SUCCESS] Caching optimization applied!")
print("Expected performance gain: 40-50% on Long_Anime scenario")
print("\nNext step: Run benchmark to verify improvement")
