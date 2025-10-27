#!/usr/bin/env python3
"""
Reorder patterns - FIXED VERSION:
1. Swap Pattern 23 (Ep##) ↔ Pattern 24 (Season # Ep #)
2. Move Pattern 20 (E##) to position 25
   - Shift 21-22 down to 20-21
   - Keep 23-24 in place (they're correct after swap)
   - Shift 25-28 up to 26-29
"""

import sys
import json
from pathlib import Path

tests_dir = Path(__file__).parent / "tests"
json_path = tests_dir / "fixtures" / "pattern_definitions.json"
test_files_base = tests_dir / "fixtures" / "pattern_files"

print("=" * 70)
print("Pattern Reordering - FIXED VERSION")
print("=" * 70)
print()

# Load
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Backup
backup_path = json_path.with_suffix('.json.backup.reorder2')
with open(backup_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)
print(f"[BACKUP] Created: {backup_path.name}")
print()

patterns_by_id = {p['id']: p for p in data['patterns']}

# === STEP 1: Swap 23 and 24 ===
print("Step 1: Swap Pattern 23 <-> Pattern 24")
p23 = patterns_by_id[23]
p24 = patterns_by_id[24]

print(f"  Before: ID 23={p23['name']}, ID 24={p24['name']}")

# Swap IDs
p23['id'] = 24
p24['id'] = 23

print(f"  After:  ID 23={p24['name']}, ID 24={p23['name']}")

# Rename test directories
dir_23_old = list(test_files_base.glob("pattern_23_*"))
dir_24_old = list(test_files_base.glob("pattern_24_*"))

if dir_23_old and dir_24_old:
    temp_dir = test_files_base / "pattern_temp_swap"
    dir_23_old[0].rename(temp_dir)
    dir_24_old[0].rename(test_files_base / dir_23_old[0].name)
    temp_dir.rename(test_files_base / dir_24_old[0].name)
    print("  [RENAMED] Test directories swapped")
print()

# === STEP 2: Move E## from 20 to 25 ===
print("Step 2: Move Pattern 20 (E##) to position 25")

p20 = patterns_by_id[20]
print(f"  Pattern 20: {p20['name']}")

# Change E##'s ID to 25
p20['id'] = 25
print(f"  [MOVED] E## from ID 20 -> ID 25")

# Shift 21-22 down to 20-21
for old_id in [22, 21]:  # Reverse order to avoid conflicts
    p = patterns_by_id[old_id]
    new_id = old_id - 1
    print(f"  [SHIFT] Pattern {old_id} ({p['name']}) -> Pattern {new_id}")
    p['id'] = new_id
    
    # Rename test directory
    old_dirs = list(test_files_base.glob(f"pattern_{old_id:02d}_*"))
    if old_dirs:
        old_dir = old_dirs[0]
        new_name = old_dir.name.replace(f"pattern_{old_id:02d}_", f"pattern_{new_id:02d}_")
        new_dir = old_dir.parent / new_name
        if old_dir.exists() and not new_dir.exists():
            old_dir.rename(new_dir)
            print(f"    [RENAMED] {old_dir.name} -> {new_name}")

# Patterns 23-24 stay in place (already correct after swap)
print(f"  [KEEP] Pattern 23 ({patterns_by_id[23]['name']}) stays at 23")
print(f"  [KEEP] Pattern 24 ({patterns_by_id[24]['name']}) stays at 24")

# Shift 25-28 up to 26-29
print()
print("Step 3: Shift patterns 25-28 up to 26-29")
for old_id in [28, 27, 26, 25]:  # Reverse order
    if old_id in patterns_by_id:
        p = patterns_by_id[old_id]
        new_id = old_id + 1
        print(f"  [SHIFT] Pattern {old_id} ({p['name']}) -> Pattern {new_id}")
        p['id'] = new_id
        
        # Rename test directory
        old_dirs = list(test_files_base.glob(f"pattern_{old_id:02d}_*"))
        if old_dirs:
            old_dir = old_dirs[0]
            new_name = old_dir.name.replace(f"pattern_{old_id:02d}_", f"pattern_{new_id:02d}_")
            new_dir = old_dir.parent / new_name
            if old_dir.exists() and not new_dir.exists():
                old_dir.rename(new_dir)
                print(f"    [RENAMED] {old_dir.name} -> {new_name}")

# Rename E## test directory (20 -> 25)
e_dir = list(test_files_base.glob("pattern_20_E"))
if e_dir:
    new_dir = test_files_base / "pattern_25_E"
    if e_dir[0].exists() and not new_dir.exists():
        e_dir[0].rename(new_dir)
        print(f"  [RENAMED] pattern_20_E -> pattern_25_E")

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
print("Final order (20-29):")
for p in sorted(data['patterns'], key=lambda x: x['id'])[19:29]:
    print(f"  Pattern {p['id']}: {p['name']}")
print()
print(f"Total patterns: {len(data['patterns'])}")
print()
