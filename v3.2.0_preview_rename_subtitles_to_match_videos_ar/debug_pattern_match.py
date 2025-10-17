#!/usr/bin/env python3
"""Debug which pattern matches which filename"""

import re

# Import patterns from pattern_engine
from subfast.scripts.common.pattern_engine import EPISODE_PATTERNS

test_files = [
    'Sword.Art.Online.s02.ep13.sub.srt',
]

print("=" * 70)
print("Pattern Matching Debug")
print("=" * 70)

for filename in test_files:
    print(f"\nFile: {filename}")
    print("-" * 70)
    
    matched = False
    for idx, (name, regex, extractor) in enumerate(EPISODE_PATTERNS, 1):
        match = regex.search(filename)
        if match:
            result = extractor(match)
            print(f"Pattern {idx}: {name}")
            print(f"  Regex: {regex.pattern}")
            print(f"  Match: {match.group(0)}")
            print(f"  Result: S{result[0]:02d}E{result[1]:02d}")
            
            if not matched:
                print(f"  >>> FIRST MATCH (will be used)")
                matched = True
            else:
                print(f"  >>> Would match but pattern {idx} matched first")
            print()
    
    if not matched:
        print("  NO MATCH FOUND")
