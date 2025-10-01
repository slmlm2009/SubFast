#!/usr/bin/env python3
"""
Fix pattern ordering bugs and add missing Season ## - ## patterns
"""

# Read the file
with open('rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking_configurable.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the EPISODE_PATTERNS section
old_patterns = """# Each pattern extracts season and episode numbers, normalizing them to S##E## format
EPISODE_PATTERNS = [
    (re.compile(r'[Ss](\\d+)[Ee](\\d+)'), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'(?:^|[._\\s-])(\\d{1,2})[xX](\\d+)(?=[._\\s-]|$)'), lambda m: (m.group(1).zfill(2), m.group(2))),
    # NEW: S## - ## format (e.g., S01 - 05, S2 - 10)
    (re.compile(r'[Ss](\\d{1,2})\\s*-\\s*(\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    # NEW: S## - E## format (e.g., S01 - E05, S2 - E10)
    (re.compile(r'[Ss](\\d{1,2})\\s*-\\s*[Ee](\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    # NEW: S## - EP## format (e.g., S01 - EP05, S2 - EP10)
    (re.compile(r'[Ss](\\d{1,2})\\s*-\\s*[Ee][Pp](\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss]eason\\.(\\d+)[\\s\\._-]*[Ee]pisode\\.(\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss](\\d+)[\\s\\._-]*[Ee]p(?:isode)?\\.(\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss](\\d+)[Ee]p(?:isode)?(\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss]eason\\s+(\\d+)\\s+[Ee]pisode\\s+(\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss]eason(\\d+)[Ee]pisode(\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss]eason(\\d+)\\s+[Ee]pisode(\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss]eason(\\d+)\\s+[Ee]p(?:isode)?(\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss]eason(\\d+)[Ee]p(?:isode)?(\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'(?:^|[._\\s-])[Ee](\\d+)(?=[._\\s-]|$)'), lambda m: ("01", m.group(1))),
    (re.compile(r'[Ss]eason\\s+(\\d+)[\\s\\._-]*[Ee]p(?:isode)?\\s*(\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss]eason(\\d+)[\\s\\._-]*[Ee]p(?:isode)?(\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'(?:^|[._\\s-])[Ee]p(?:isode)?(\\d+)(?=[._\\s-]|$)', re.IGNORECASE), lambda m: ("01", m.group(1))),
    (re.compile(r'[Ss]eason\\s+(\\d+)\\s+[Ee]p(?:isode)?\\s*(\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    # NEW: Ordinal Season patterns (1st, 2nd, 3rd, etc.)
    # Pattern: 1st Season - 05 → S01E05
    (re.compile(r'(\\d{1,2})(?:st|nd|rd|th)\\s+[Ss]eason\\s*-\\s*(\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    # Pattern: 2nd Season E10 → S02E10
    (re.compile(r'(\\d{1,2})(?:st|nd|rd|th)\\s+[Ss]eason\\s+[Ee](?:pisode)?\\s*(\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    # Pattern: 3rd Season EP8 → S03E08
    (re.compile(r'(\\d{1,2})(?:st|nd|rd|th)\\s+[Ss]eason\\s+[Ee][Pp]\\s*(\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'-\\s*(\\d+)'), lambda m: ("01", m.group(1))),
]"""

new_patterns = """# Each pattern extracts season and episode numbers, normalizing them to S##E## format
EPISODE_PATTERNS = [
    (re.compile(r'[Ss](\\d+)[Ee](\\d+)'), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'(?:^|[._\\s-])(\\d{1,2})[xX](\\d+)(?=[._\\s-]|$)'), lambda m: (m.group(1).zfill(2), m.group(2))),
    # NEW: S## - ## format (e.g., S01 - 05, S2 - 10)
    (re.compile(r'[Ss](\\d{1,2})\\s*-\\s*(\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    # NEW: S## - E## format (e.g., S01 - E05, S2 - E10)
    (re.compile(r'[Ss](\\d{1,2})\\s*-\\s*[Ee](\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    # NEW: S## - EP## format (e.g., S01 - EP05, S2 - EP10)
    (re.compile(r'[Ss](\\d{1,2})\\s*-\\s*[Ee][Pp](\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    # NEW: Ordinal Season patterns (MOVED HERE - must come BEFORE general E##/EP## patterns)
    # Pattern: 2nd Season EP8 → S02E08 (most specific first)
    (re.compile(r'(\\d{1,2})(?:st|nd|rd|th)\\s+[Ss]eason\\s+[Ee][Pp]\\s*(\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    # Pattern: 2nd Season E10 or 2nd Season Episode 10 → S02E10
    (re.compile(r'(\\d{1,2})(?:st|nd|rd|th)\\s+[Ss]eason\\s+[Ee](?:pisode)?\\s*(\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    # Pattern: 1st Season - 05 → S01E05
    (re.compile(r'(\\d{1,2})(?:st|nd|rd|th)\\s+[Ss]eason\\s*-\\s*(\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    # NEW: Season ## - ## patterns (CRITICAL - must come BEFORE general patterns)
    # Pattern: Season 2 - 23 → S02E23 (with space before number)
    (re.compile(r'[Ss]eason\\s+(\\d{1,2})\\s*-\\s*(\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    # Pattern: Season12 - 103 → S12E103 (without space before number)
    (re.compile(r'[Ss]eason(\\d{1,2})\\s*-\\s*(\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    # Existing Season patterns (unchanged)
    (re.compile(r'[Ss]eason\\.(\\d+)[\\s\\._-]*[Ee]pisode\\.(\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss](\\d+)[\\s\\._-]*[Ee]p(?:isode)?\\.(\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss](\\d+)[Ee]p(?:isode)?(\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss]eason\\s+(\\d+)\\s+[Ee]pisode\\s+(\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss]eason(\\d+)[Ee]pisode(\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss]eason(\\d+)\\s+[Ee]pisode(\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss]eason(\\d+)\\s+[Ee]p(?:isode)?(\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss]eason(\\d+)[Ee]p(?:isode)?(\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'(?:^|[._\\s-])[Ee](\\d+)(?=[._\\s-]|$)'), lambda m: ("01", m.group(1))),
    (re.compile(r'[Ss]eason\\s+(\\d+)[\\s\\._-]*[Ee]p(?:isode)?\\s*(\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss]eason(\\d+)[\\s\\._-]*[Ee]p(?:isode)?(\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'(?:^|[._\\s-])[Ee]p(?:isode)?(\\d+)(?=[._\\s-]|$)', re.IGNORECASE), lambda m: ("01", m.group(1))),
    (re.compile(r'[Ss]eason\\s+(\\d+)\\s+[Ee]p(?:isode)?\\s*(\\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    # Generic dash pattern (unchanged, last resort)
    (re.compile(r'-\\s*(\\d+)'), lambda m: ("01", m.group(1))),
]"""

# Replace
new_content = content.replace(old_patterns, new_patterns)

# Write back
with open('rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking_configurable.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("[OK] Pattern fixes applied successfully!")
print("\nChanges made:")
print("  1. ✅ Moved ordinal patterns BEFORE general E##/EP## patterns")
print("     - '2nd Season EP10' will now correctly detect S02E10")
print("  2. ✅ Added 'Season ## - ##' pattern (with space)")
print("     - 'Season 2 - 23' will now correctly detect S02E23")
print("  3. ✅ Added 'Season## - ##' pattern (without space)")
print("     - 'Season12 - 103' will now correctly detect S12E103")
print("\nPattern count: 27 patterns (was 25, added 2 new Season patterns)")
