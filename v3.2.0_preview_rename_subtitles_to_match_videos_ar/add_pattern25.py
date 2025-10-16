#!/usr/bin/env python3
"""
Add Pattern 25 (## - ##) to pattern_definitions.json using helper functions.
Story 6.4 Task 6 - Pattern Extensibility Framework Validation
"""

import sys
from pathlib import Path

# Add tests directory to path
tests_dir = Path(__file__).parent / "tests"
sys.path.insert(0, str(tests_dir))

from test_helpers import (
    validate_pattern_definition,
    add_pattern_to_definitions,
    generate_pattern_test_files
)

# Pattern 25 Definition
pattern_25 = {
    "id": 25,
    "name": "## - ##",
    "description": "Season and episode numbers separated by dash, no S/E prefix (e.g., '3 - 04')",
    "variations": [
        {
            "var_id": "VAR1",
            "expected": "S03E04",
            "video_template": "[VAR1]-Show 3 - 04.mkv",
            "subtitle_template": "[VAR1]-Show 3 - 04.srt"
        },
        {
            "var_id": "VAR2",
            "expected": "S02E10",
            "video_template": "[VAR2]-Series 2-10.720p.mkv",
            "subtitle_template": "[VAR2]-Series 2-10.srt"
        },
        {
            "var_id": "VAR3",
            "expected": "S01E25",
            "video_template": "[VAR3]-Example 1 - 25.BluRay.mkv",
            "subtitle_template": "[VAR3]-Example 1 - 25.srt"
        }
    ]
}

print("=" * 70)
print("Adding Pattern 25: ## - ## (Season-Episode Dash Format)")
print("=" * 70)
print()

# Step 1: Validate
print("Step 1: Validating pattern definition...")
is_valid, errors = validate_pattern_definition(pattern_25)

if not is_valid:
    print("[FAIL] Validation FAILED:")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)

print("[PASS] Pattern definition is valid!")
print()

# Step 2: Renumber existing Pattern 25 → 26, then add new Pattern 25
print("Step 2: Adding to pattern_definitions.json...")
json_path = tests_dir / "fixtures" / "pattern_definitions.json"

# First, manually handle the renumbering
import json
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find and renumber existing Pattern 25 to 26
for pattern in data['patterns']:
    if pattern['id'] == 25:
        print("  - Renumbering existing Pattern 25 (- ##) -> Pattern 26")
        pattern['id'] = 26
        # Rename test directory
        old_dir = tests_dir / "fixtures" / "pattern_files" / "pattern_25_dash"
        new_dir = tests_dir / "fixtures" / "pattern_files" / "pattern_26_dash"
        if old_dir.exists():
            old_dir.rename(new_dir)
            print(f"  - Renamed test directory: {old_dir.name} -> {new_dir.name}")
        break

# Insert new Pattern 25 at the correct position (after Pattern 24)
# Find the index of Pattern 24
insert_index = None
for i, pattern in enumerate(data['patterns']):
    if pattern['id'] == 24:
        insert_index = i + 1
        break

if insert_index is None:
    print("[FAIL] Could not find Pattern 24 to insert after")
    sys.exit(1)

# Insert new Pattern 25
data['patterns'].insert(insert_index, pattern_25)
print(f"  - Inserted new Pattern 25 (## - ##) at position {insert_index}")

# Update metadata
data['metadata']['total_patterns'] = len(data['patterns'])

# Save the updated JSON
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print("[PASS] Pattern added to definitions!")
success = True

print("[PASS] Pattern added to definitions!")
print()

# Step 3: Generate test files
print("Step 3: Generating test files...")
test_files_base = tests_dir / "fixtures" / "pattern_files"

pattern_dir = generate_pattern_test_files(25, str(test_files_base))

if pattern_dir:
    print(f"[PASS] Test files created in: {pattern_dir}")
else:
    print("[FAIL] Failed to generate test files")
    sys.exit(1)

print()
print("=" * 70)
print("Pattern 25 Added Successfully!")
print("=" * 70)
print()
print("Next steps:")
print("  1. Run: python tests/run_pattern_integration_tests.py")
print("  2. Verify Pattern 25 tests pass")
print()
