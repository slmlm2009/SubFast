#!/usr/bin/env python3
"""Fix episode number zero-padding in all patterns"""

with open('rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking_configurable.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all lambda formatters to add .zfill(2) to episode numbers
# Pattern: m.group(2) → m.group(2).zfill(2)
# BUT keep m.group(1).zfill(2) as is (season already padded)

replacements = [
    # Single capture group (episode only, season defaults to "01")
    ('lambda m: ("01", m.group(1))', 'lambda m: ("01", m.group(1).zfill(2))'),
    
    # Two capture groups (season and episode)
    ('lambda m: (m.group(1).zfill(2), m.group(2))', 'lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))'),
]

for old, new in replacements:
    content = content.replace(old, new)

# Write back
with open('rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking_configurable.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("[SUCCESS] Fixed episode number zero-padding in all patterns!")
print("All single-digit episodes will now be formatted as E0#")
print("Examples:")
print("  S03E8 → S03E08")
print("  S01E5 → S01E05")
print("  S01E1 → S01E01")
