#!/usr/bin/env python3
"""Restore complete enhanced pattern list to configurable script"""

with open('rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking_configurable.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the EPISODE_PATTERNS section
start_idx = None
end_idx = None

for i, line in enumerate(lines):
    if 'EPISODE_PATTERNS = [' in line:
        start_idx = i
    elif start_idx is not None and line.strip() == ']':
        end_idx = i + 1
        break

if start_idx is None or end_idx is None:
    print("ERROR: Could not find EPISODE_PATTERNS section")
    exit(1)

print(f"Found EPISODE_PATTERNS at lines {start_idx+1} to {end_idx}")

# Complete enhanced pattern list (25 patterns total)
new_patterns = '''EPISODE_PATTERNS = [
    (re.compile(r'[Ss](\d+)[Ee](\d+)'), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'(?:^|[._\s-])(\d{1,2})[xX](\d+)(?=[._\s-]|$)'), lambda m: (m.group(1).zfill(2), m.group(2))),
    # NEW: S## - ## format (e.g., S01 - 05, S2 - 10)
    (re.compile(r'[Ss](\d{1,2})\s*-\s*(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    # NEW: S## - E## format (e.g., S01 - E05, S2 - E10)
    (re.compile(r'[Ss](\d{1,2})\s*-\s*[Ee](\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    # NEW: S## - EP## format (e.g., S01 - EP05, S2 - EP10)
    (re.compile(r'[Ss](\d{1,2})\s*-\s*[Ee][Pp](\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    # NEW: Ordinal Season patterns (placed HERE to match before generic patterns)
    # Pattern: 1st Season - 05 → S01E05
    (re.compile(r'(\d{1,2})(?:st|nd|rd|th)\s+[Ss]eason\s*-\s*(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    # Pattern: 3rd Season Episode 8 → S03E08 (FIXES THE BUG!)
    (re.compile(r'(\d{1,2})(?:st|nd|rd|th)\s+[Ss]eason\s+[Ee]pisode\s+(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    # Pattern: 2nd Season E10 → S02E10
    (re.compile(r'(\d{1,2})(?:st|nd|rd|th)\s+[Ss]eason\s+[Ee]\s*(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    # Pattern: 2nd Season EP10 → S02E10
    (re.compile(r'(\d{1,2})(?:st|nd|rd|th)\s+[Ss]eason\s+[Ee][Pp]\s*(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    # NEW: Season ## - ## format (e.g., Season 2 - 23, Season 12 - 103)
    (re.compile(r'[Ss]eason\s+(\d{1,2})\s*-\s*(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss]eason(\d{1,2})\s*-\s*(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss]eason\.(\d+)[\s\._-]*[Ee]pisode\.(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss](\d+)[\s\._-]*[Ee]p(?:isode)?\.(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss](\d+)[Ee]p(?:isode)?(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss]eason\s+(\d+)\s+[Ee]pisode\s+(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss]eason(\d+)[Ee]pisode(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss]eason(\d+)\s+[Ee]pisode(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss]eason(\d+)\s+[Ee]p(?:isode)?(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss]eason(\d+)[Ee]p(?:isode)?(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'(?:^|[._\s-])[Ee](\d+)(?=[._\s-]|$)'), lambda m: ("01", m.group(1))),
    (re.compile(r'[Ss]eason\s+(\d+)[\s\._-]*[Ee]p(?:isode)?\s*(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss]eason(\d+)[\s\._-]*[Ee]p(?:isode)?(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'(?:^|[._\s-])[Ee]p(?:isode)?(\d+)(?=[._\s-]|$)', re.IGNORECASE), lambda m: ("01", m.group(1))),
    (re.compile(r'[Ss]eason\s+(\d+)\s+[Ee]p(?:isode)?\s*(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'-\s*(\d+)'), lambda m: ("01", m.group(1))),
]
'''

# Replace the old pattern list with the complete enhanced list
lines = lines[:start_idx] + [new_patterns] + lines[end_idx:]

# Write back
with open('rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking_configurable.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\n[SUCCESS] Restored complete enhanced pattern list!")
print("Total patterns: 25")
print("\nKey additions:")
print("  - S## - ## format (3 variants)")
print("  - Ordinal Season patterns (4 variants) - FIXES 3rd Season Episode 8 BUG")
print("  - Season ## - ## format (2 variants)")
print("\nPattern ordering optimized for correct matching priority.")
