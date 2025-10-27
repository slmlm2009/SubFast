#!/usr/bin/env python3
"""
Test real-world pattern matching with actual show names
"""

from subfast.scripts.common.pattern_engine import extract_episode_info, normalize_episode_number

# Real-world test cases
test_cases = [
    # Pattern 1a: S## Episode ##
    ("[SubsPlease] Attack on Titan S04 Episode 16.mkv", (4, 16), "S04E16"),
    ("My.Hero.Academia.S08 Episode 01.1080p.mkv", (8, 1), "S08E01"),
    
    # Pattern 4a: S##.E##
    ("One.Piece.S01.E1015.720p.WEB-DL.mkv", (1, 1015), "S01E1015"),
    ("[Erai-raws] Demon Slayer S03.E11.mkv", (3, 11), "S03E11"),
    
    # Pattern 4b: S##_E##
    ("Bleach.TYBW.S02_E13.1080p.mkv", (2, 13), "S02E13"),
    ("[HorribleSubs] Naruto S01_E220.mkv", (1, 220), "S01E220"),
    
    # Pattern 5a: S## EP##
    ("Jujutsu Kaisen S02 EP23.mkv", (2, 23), "S02E23"),
    ("[CR] Vinland Saga S02 EP24.1080p.mkv", (2, 24), "S02E24"),
    
    # Pattern 15a: Season## Episode ##
    ("Dr.Stone.Season03 Episode 11.mkv", (3, 11), "S03E11"),
    ("Spy x Family Season02_Episode13.mkv", (2, 13), "S02E13"),
]

print("=" * 70)
print("Testing Real-World Pattern Matching")
print("=" * 70)
print()

all_pass = True

for filename, expected_tuple, expected_normalized in test_cases:
    result = extract_episode_info(filename)
    
    if result:
        normalized = normalize_episode_number(result[0], result[1])
        status = "[PASS]" if result == expected_tuple and normalized == expected_normalized else "[FAIL]"
        
        if result != expected_tuple or normalized != expected_normalized:
            all_pass = False
            
        print(f"{status}")
        print(f"  File: {filename}")
        print(f"  Expected: {expected_tuple} -> {expected_normalized}")
        print(f"  Got:      {result} -> {normalized}")
        print()
    else:
        all_pass = False
        print(f"[FAIL] - NO MATCH")
        print(f"  File: {filename}")
        print(f"  Expected: {expected_tuple} -> {expected_normalized}")
        print(f"  Got:      None")
        print()

print("=" * 70)
if all_pass:
    print("[SUCCESS] All tests PASSED!")
else:
    print("[FAILED] Some tests FAILED - need investigation")
print("=" * 70)
