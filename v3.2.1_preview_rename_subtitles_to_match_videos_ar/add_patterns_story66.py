#!/usr/bin/env python3
"""
Story 6.6: Add 7 new patterns (2 new IDs + 5 variations to existing patterns)
"""

import sys
import json
from pathlib import Path

# Add tests directory to path
tests_dir = Path(__file__).parent / "tests"
sys.path.insert(0, str(tests_dir))

from test_helpers import generate_pattern_test_files

# Load pattern definitions
json_path = tests_dir / "fixtures" / "pattern_definitions.json"
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 70)
print("Story 6.6: Adding 7 New Patterns")
print("=" * 70)
print()

# Backup
backup_path = json_path.with_suffix('.json.backup')
with open(backup_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)
print(f"[BACKUP] Created: {backup_path.name}")
print()

# ===== Add Variations to Existing Patterns =====

print("Adding variations to existing patterns...")
print()

# Pattern 1: Add VAR6 (S## Episode ##)
pattern_1 = [p for p in data['patterns'] if p['id'] == 1][0]
pattern_1['variations'].append({
    "var_id": "VAR6",
    "expected": "S02E08",
    "video_template": "Show.S02 Episode 08.mkv",
    "subtitle_template": "Show.S02 Episode 08.srt"
})
print("[ADDED] Pattern 1 VAR6: S## Episode ##")

# Pattern 4: Add VAR4 and VAR5 (S##.E##, S##_E##)
pattern_4 = [p for p in data['patterns'] if p['id'] == 4][0]
pattern_4['variations'].extend([
    {
        "var_id": "VAR4",
        "expected": "S02E12",
        "video_template": "Show.S02.E12.mkv",
        "subtitle_template": "Show.S02.E12.srt"
    },
    {
        "var_id": "VAR5",
        "expected": "S03E07",
        "video_template": "Show.S03_E07.mkv",
        "subtitle_template": "Show.S03_E07.srt"
    }
])
print("[ADDED] Pattern 4 VAR4: S##.E##")
print("[ADDED] Pattern 4 VAR5: S##_E##")

# Pattern 5: Add VAR4 (S## EP##)
pattern_5 = [p for p in data['patterns'] if p['id'] == 5][0]
pattern_5['variations'].append({
    "var_id": "VAR4",
    "expected": "S01E15",
    "video_template": "Show.S01 EP15.mkv",
    "subtitle_template": "Show.S01 EP15.srt"
})
print("[ADDED] Pattern 5 VAR4: S## EP##")

# Pattern 15: Add VAR4 (Season## Episode ##)
pattern_15 = [p for p in data['patterns'] if p['id'] == 15][0]
pattern_15['variations'].append({
    "var_id": "VAR4",
    "expected": "S02E20",
    "video_template": "Show.Season02 Episode 20.mkv",
    "subtitle_template": "Show.Season02 Episode 20.srt"
})
print("[ADDED] Pattern 15 VAR4: Season## Episode ##")

print()

# ===== Add New Pattern IDs =====

print("Adding new pattern IDs...")
print()

# Pattern 27: [##]
pattern_27 = {
    "id": 27,
    "name": "[##]",
    "description": "Bracket-enclosed episode number, assumes Season 1 (e.g., '[07].mkv')",
    "variations": [
        {
            "var_id": "VAR1",
            "expected": "S01E07",
            "video_template": "[VCB-Studio] IS Infinite Stratos [07][Ma10p_1080p][x265_flac_aac].mkv",
            "subtitle_template": "[VCB-Studio] IS Infinite Stratos [07].srt"
        },
        {
            "var_id": "VAR2",
            "expected": "S01E12",
            "video_template": "Show.Name.[12].720p.mkv",
            "subtitle_template": "Show.Name.[12].srt"
        },
        {
            "var_id": "VAR3",
            "expected": "S01E05",
            "video_template": "Series [5] Episode.mkv",
            "subtitle_template": "Series [5] Episode.srt"
        }
    ]
}
data['patterns'].append(pattern_27)
print("[ADDED] Pattern 27: [##]")

# Pattern 28: _##
pattern_28 = {
    "id": 28,
    "name": "_##",
    "description": "Underscore with episode number, assumes Season 1 (e.g., 'Show_09.mkv'). LAST PATTERN.",
    "variations": [
        {
            "var_id": "VAR1",
            "expected": "S01E09",
            "video_template": "[DB]Maoyuu Maou Yuusha_-_09_(10bit_BD1080p_x265).mkv",
            "subtitle_template": "[DB]Maoyuu Maou Yuusha_09.srt"
        },
        {
            "var_id": "VAR2",
            "expected": "S01E15",
            "video_template": "Show_15.mkv",
            "subtitle_template": "Show_15.srt"
        },
        {
            "var_id": "VAR3",
            "expected": "S01E03",
            "video_template": "Example_3.720p.mkv",
            "subtitle_template": "Example_3.srt"
        }
    ]
}
data['patterns'].append(pattern_28)
print("[ADDED] Pattern 28: _##")

print()

# Update metadata
data['metadata']['total_patterns'] = len(data['patterns'])

# Save
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f"[SUCCESS] Updated pattern_definitions.json")
print(f"  Total patterns: {len(data['patterns'])}")
print()

# ===== Generate Test Files =====

print("=" * 70)
print("Generating Test Files")
print("=" * 70)
print()

test_files_base = tests_dir / "fixtures" / "pattern_files"

# Regenerate test files for patterns with new variations
patterns_to_regenerate = [1, 4, 5, 15, 27, 28]

for pattern_id in patterns_to_regenerate:
    print(f"Generating files for Pattern {pattern_id}...")
    pattern_dir = generate_pattern_test_files(pattern_id, str(test_files_base))
    if pattern_dir:
        print(f"  [SUCCESS] {pattern_dir}")
    else:
        print(f"  [FAILED] Pattern {pattern_id}")
    print()

print("=" * 70)
print("Story 6.6 Complete!")
print("=" * 70)
print()
print("Next steps:")
print("  1. Run: python tests/run_pattern_integration_tests.py")
print("  2. Verify all tests pass")
print()
