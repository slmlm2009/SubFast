#!/usr/bin/env python3
"""Comprehensive pattern verification test - All 25 patterns"""

import re
import sys

# Complete enhanced pattern list (25 patterns)
EPISODE_PATTERNS = [
    (re.compile(r'[Ss](\d+)[Ee](\d+)'), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'(?:^|[._\s-])(\d{1,2})[xX](\d+)(?=[._\s-]|$)'), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    # NEW: S## - ## format (e.g., S01 - 05, S2 - 10)
    (re.compile(r'[Ss](\d{1,2})\s*-\s*(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    # NEW: S## - E## format (e.g., S01 - E05, S2 - E10)
    (re.compile(r'[Ss](\d{1,2})\s*-\s*[Ee](\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    # NEW: S## - EP## format (e.g., S01 - EP05, S2 - EP10)
    (re.compile(r'[Ss](\d{1,2})\s*-\s*[Ee][Pp](\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    # NEW: Ordinal Season patterns (placed HERE to match before generic patterns)
    # Pattern: 1st Season - 05 → S01E05
    (re.compile(r'(\d{1,2})(?:st|nd|rd|th)\s+[Ss]eason\s*-\s*(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    # Pattern: 3rd Season Episode 8 → S03E08 (FIXES THE BUG!)
    (re.compile(r'(\d{1,2})(?:st|nd|rd|th)\s+[Ss]eason\s+[Ee]pisode\s+(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    # Pattern: 2nd Season E10 → S02E10
    (re.compile(r'(\d{1,2})(?:st|nd|rd|th)\s+[Ss]eason\s+[Ee]\s*(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    # Pattern: 2nd Season EP10 → S02E10
    (re.compile(r'(\d{1,2})(?:st|nd|rd|th)\s+[Ss]eason\s+[Ee][Pp]\s*(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    # NEW: Season ## - ## format (e.g., Season 2 - 23, Season 12 - 103)
    (re.compile(r'[Ss]eason\s+(\d{1,2})\s*-\s*(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'[Ss]eason(\d{1,2})\s*-\s*(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'[Ss]eason\.(\d+)[\s\._-]*[Ee]pisode\.(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'[Ss](\d+)[\s\._-]*[Ee]p(?:isode)?\.(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'[Ss](\d+)[Ee]p(?:isode)?(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'[Ss]eason\s+(\d+)\s+[Ee]pisode\s+(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'[Ss]eason(\d+)[Ee]pisode(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'[Ss]eason(\d+)\s+[Ee]pisode(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'[Ss]eason(\d+)\s+[Ee]p(?:isode)?(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'[Ss]eason(\d+)[Ee]p(?:isode)?(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'(?:^|[._\s-])[Ee](\d+)(?=[._\s-]|$)'), lambda m: ("01", m.group(1).zfill(2))),
    (re.compile(r'[Ss]eason\s+(\d+)[\s\._-]*[Ee]p(?:isode)?\s*(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'[Ss]eason(\d+)[\s\._-]*[Ee]p(?:isode)?(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'(?:^|[._\s-])[Ee]p(?:isode)?(\d+)(?=[._\s-]|$)', re.IGNORECASE), lambda m: ("01", m.group(1).zfill(2))),
    (re.compile(r'[Ss]eason\s+(\d+)\s+[Ee]p(?:isode)?\s*(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'-\s*(\d+)'), lambda m: ("01", m.group(1).zfill(2))),
]

def get_episode_number(filename):
    """Extract episode from filename using all patterns"""
    for pattern, formatter in EPISODE_PATTERNS:
        match = pattern.search(filename)
        if match:
            season, episode = formatter(match)
            return f"S{season}E{episode}"
    return None

# Comprehensive test cases covering ALL 25 patterns
test_cases = [
    # Original S##E## patterns
    ("ShowName S01E05.mkv", "S01E05", "Basic S##E##"),
    ("ShowName S12E149.mkv", "S12E149", "Basic S##E## (multi-digit)"),
    
    # ##x## format
    ("ShowName 2x10.mp4", "S02E10", "##x## format"),
    ("ShowName 1x03.mkv", "S01E03", "##x## format"),
    
    # NEW: S## - ## patterns
    ("ShowName S01 - 07.mkv", "S01E07", "S## - ## format"),
    ("ShowName S12 - 149.mkv", "S12E149", "S## - ## format (multi-digit)"),
    
    # NEW: S## - E## patterns
    ("ShowName S01 - E08.mkv", "S01E08", "S## - E## format"),
    ("ShowName S2 - E23.mp4", "S02E23", "S## - E## format"),
    
    # NEW: S## - EP## patterns
    ("ShowName S01 - EP09.mkv", "S01E09", "S## - EP## format"),
    ("ShowName S2 - EP25.mp4", "S02E25", "S## - EP## format"),
    
    # NEW: Ordinal Season patterns (THE BUG FIXES!)
    ("ShowName 1st Season - 05.mkv", "S01E05", "Ordinal - ##"),
    ("ShowName 3rd Season Episode 8.srt", "S03E08", "Ordinal Episode ## (BUG FIX!)"),
    ("ShowName 3rd Season Episode 8 (3840x2160).mkv", "S03E08", "Ordinal Episode ## with resolution (BUG FIX!)"),
    ("ShowName 2nd Season E10.mp4", "S02E10", "Ordinal E##"),
    ("ShowName 2nd Season EP10.ass", "S02E10", "Ordinal EP##"),
    ("ShowName 12th Season - 103.mkv", "S12E103", "Ordinal - ## (multi-digit)"),
    ("SomeShow 2nd Season E17.ass", "S02E17", "Ordinal E##"),
    
    # NEW: Season ## - ## patterns
    ("ShowName Season 2 - 23.mkv", "S02E23", "Season ## - ## (with space)"),
    ("ShowName Season 12 - 103.mkv", "S12E103", "Season ## - ## (multi-digit)"),
    ("ShowName Season12 - 103.ass", "S12E103", "Season## - ## (no space)"),
    
    # Season.Episode formats
    ("Show.Season.1.Episode.5.mkv", "S01E05", "Season.Episode"),
    
    # SeasonEpisode formats
    ("ShowName Season 1 Episode 5.mp4", "S01E05", "Season # Episode #"),
    ("ShowName Season1Episode5.mkv", "S01E05", "Season#Episode#"),
    
    # S##Ep## formats
    ("ShowName S1Ep5.mkv", "S01E05", "S#Ep#"),
    ("ShowName S01Episode05.mkv", "S01E05", "S##Episode##"),
    
    # Standalone E## (assumes S01)
    ("Detective Conan - 03.mp4", "S01E03", "Standalone - ##"),
    ("Naruto Shippuden EP156.mp4", "S01E156", "Standalone EP##"),
    
    # Resolution conflict test (ensure still works)
    ("ShowName S2 - 14 - 1920x1080.mp4", "S02E14", "Resolution NOT mistaken for episode"),
    
    # Edge cases
    ("ShowName.1x1.mkv", "S01E01", "Minimal ##x##"),
    ("Show S99E999.mkv", "S99E999", "Large numbers"),
]

# Run tests
print("=" * 80)
print("COMPREHENSIVE PATTERN VERIFICATION TEST")
print("=" * 80)
print(f"Testing {len(EPISODE_PATTERNS)} patterns against {len(test_cases)} test cases")
print("=" * 80)
print()

passed = 0
failed = 0
failures = []

for filename, expected, description in test_cases:
    result = get_episode_number(filename)
    status = "PASS" if result == expected else "FAIL"
    
    if result == expected:
        print(f"[OK] {description:45} | {filename}")
        print(f"     Result: {result}")
        passed += 1
    else:
        print(f"[FAIL] {description:45} | {filename}")
        print(f"       Expected: {expected}")
        print(f"       Got: {result}")
        failed += 1
        failures.append((filename, expected, result, description))
    print()

print("=" * 80)
print(f"RESULTS: {passed} passed, {failed} failed out of {len(test_cases)} tests")
print("=" * 80)

if failed > 0:
    print("\nFAILED TESTS:")
    print("-" * 80)
    for filename, expected, got, desc in failures:
        print(f"  {desc}")
        print(f"    File: {filename}")
        print(f"    Expected: {expected}, Got: {got}")
        print()
    sys.exit(1)
else:
    print("\n*** ALL TESTS PASSED ***")
    print("Script is production ready with all 25 episode detection patterns!")
    sys.exit(0)
