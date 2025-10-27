#!/usr/bin/env python3
"""
Reorder patterns for better matching specificity:
1. Swap Pattern 23 (Ep##) ↔ Pattern 24 (Season # Ep #)
2. Move Pattern 20 (E##) to before Pattern 25
"""

import sys
import json
from pathlib import Path

# Add tests directory to path
tests_dir = Path(__file__).parent / "tests"
json_path = tests_dir / "fixtures" / "pattern_definitions.json"

print("=" * 70)
print("Pattern Reordering for Better Specificity")
print("=" * 70)
print()

# Load pattern definitions
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Backup
backup_path = json_path.with_suffix('.json.backup.reorder')
with open(backup_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)
print(f"[BACKUP] Created: {backup_path.name}")
print()

# Get patterns as a dict by ID for easy lookup
patterns_by_id = {p['id']: p for p in data['patterns']}

print("Step 1: Swap Pattern 23 <-> Pattern 24")
print("  Current 23: Ep##")
print("  Current 24: Season # Ep #")
print()

# Swap IDs
pattern_23 = patterns_by_id[23]
pattern_24 = patterns_by_id[24]

pattern_23['id'] = 24  # Ep## becomes 24
pattern_24['id'] = 23  # Season # Ep # becomes 23

print("  [SWAPPED] Pattern 23 is now: Season # Ep #")
print("  [SWAPPED] Pattern 24 is now: Ep##")
print()

# Rename test directories for swapped patterns
test_files_base = tests_dir / "fixtures" / "pattern_files"
dir_23 = test_files_base / "pattern_23_Ep"
dir_24 = test_files_base / "pattern_24_Season__Ep"

if dir_23.exists() and dir_24.exists():
    # Use temporary name to avoid collision
    temp_dir = test_files_base / "pattern_temp"
    dir_23.rename(temp_dir)
    dir_24.rename(dir_23)
    temp_dir.rename(dir_24)
    print("  [RENAMED] Test directories swapped")
else:
    print("  [SKIP] Test directories not found (will be regenerated)")
print()

print("Step 2: Move Pattern 20 (E##) to before Pattern 25")
print("  Current order: ...24 -> [20] -> 21 -> 22 -> 23 -> 24 -> 25...")
print("  Target order:  ...24 -> 21 -> 22 -> 23 -> 24 -> [25=E##] -> 26...")
print()

# Get the E## pattern (currently ID 20)
pattern_e = patterns_by_id[20]
print(f"  Found Pattern 20: {pattern_e['name']}")

# Shift patterns 21-24 down by 1
# 21->20, 22->21, 23->22, 24->23
for old_id in [24, 23, 22, 21]:  # Process in reverse to avoid conflicts
    p = patterns_by_id[old_id]
    new_id = old_id - 1
    print(f"  [SHIFT] Pattern {old_id} ({p['name']}) -> Pattern {new_id}")
    p['id'] = new_id
    # Rename test directory
    old_dir = test_files_base / f"pattern_{old_id:02d}_{p['name'].replace('#', '').replace(' ', '_').replace('/', '-').replace('\\\\', '-').strip('_')}"
    # Try to find the directory with any naming variation
    matching_dirs = list(test_files_base.glob(f"pattern_{old_id:02d}_*"))
    if matching_dirs:
        old_dir = matching_dirs[0]
        new_name = old_dir.name.replace(f"pattern_{old_id:02d}_", f"pattern_{new_id:02d}_")
        new_dir = old_dir.parent / new_name
        if old_dir.exists():
            old_dir.rename(new_dir)
            print(f"    [RENAMED] {old_dir.name} -> {new_name}")

# Now move E## from 20 to 24
pattern_e['id'] = 24
print(f"  [MOVED] Pattern E## from ID 20 -> ID 24")

# Rename E## test directory
old_e_dir = test_files_base / "pattern_20_E"
if old_e_dir.exists():
    new_e_dir = test_files_base / "pattern_24_E"
    old_e_dir.rename(new_e_dir)
    print(f"    [RENAMED] pattern_20_E -> pattern_24_E")

print()

# Now shift patterns 25-28 up by 1
# 25->26, 26->27, 27->28, 28->29
print("Step 3: Shift remaining patterns")
for old_id in [25, 26, 27, 28]:
    if old_id in patterns_by_id:
        p = patterns_by_id[old_id]
        new_id = old_id + 1
        print(f"  [SHIFT] Pattern {old_id} ({p['name']}) -> Pattern {new_id}")
        p['id'] = new_id
        # Rename test directory
        matching_dirs = list(test_files_base.glob(f"pattern_{old_id:02d}_*"))
        if matching_dirs:
            old_dir = matching_dirs[0]
            new_name = old_dir.name.replace(f"pattern_{old_id:02d}_", f"pattern_{new_id:02d}_")
            new_dir = old_dir.parent / new_name
            if old_dir.exists():
                old_dir.rename(new_dir)
                print(f"    [RENAMED] {old_dir.name} -> {new_name}")

print()

# Re-sort patterns by ID
data['patterns'].sort(key=lambda p: p['id'])

# Update metadata
data['metadata']['total_patterns'] = len(data['patterns'])

# Save
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print("[SUCCESS] Pattern reordering complete!")
print()
print("Final order:")
print("  Pattern 23: Season # Ep # (was 24)")
print("  Pattern 24: E## (was 20)")
print("  Pattern 25: Ep## (was 23, then 24 after swap)")
print("  Pattern 26: ## - ## (was 25)")
print("  Pattern 27: - ## (was 26)")
print("  Pattern 28: [##] (was 27)")
print("  Pattern 29: _## (was 28)")
print()
print("Total patterns: 29")
print()
print("Next steps:")
print("  1. Run: python tests/run_pattern_integration_tests.py")
print("  2. Verify all tests still pass")
print()
