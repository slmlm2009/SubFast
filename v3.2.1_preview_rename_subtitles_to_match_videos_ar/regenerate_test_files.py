#!/usr/bin/env python3
"""
Regenerate test files for patterns 20, 21, 23, 24, 25
"""

import sys
from pathlib import Path

tests_dir = Path(__file__).parent / "tests"
sys.path.insert(0, str(tests_dir))

from test_helpers import generate_pattern_test_files

test_files_base = tests_dir / "fixtures" / "pattern_files"

print("=" * 70)
print("Regenerating Test Files for Reordered Patterns")
print("=" * 70)
print()

patterns_to_regenerate = [20, 21, 23, 24, 25]

for pattern_id in patterns_to_regenerate:
    print(f"Regenerating Pattern {pattern_id}...")
    pattern_dir = generate_pattern_test_files(pattern_id, str(test_files_base))
    if pattern_dir:
        print(f"  [SUCCESS] {pattern_dir}")
    else:
        print(f"  [FAILED] Pattern {pattern_id}")
    print()

print("[DONE] Test file regeneration complete!")
print()
