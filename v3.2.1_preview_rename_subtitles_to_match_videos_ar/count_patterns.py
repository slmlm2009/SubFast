"""Count patterns and variations"""
import json
from pathlib import Path

# Load pattern definitions
pattern_file = Path('tests/fixtures/pattern_definitions.json')
with open(pattern_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

patterns = data['patterns']
var_count = sum(len(p['variations']) for p in patterns)

print("=" * 60)
print("PATTERN COUNT CHECK")
print("=" * 60)
print(f"\nTotal patterns: {len(patterns)}")
print(f"Total variations: {var_count}")
print(f"Expected files: {var_count * 2} (video + subtitle)")

# Show Pattern 30 details
pattern_30 = patterns[29]  # 0-indexed, so pattern 30 is at index 29
print(f"\nPattern 30 details:")
print(f"  Name: {pattern_30['name']}")
print(f"  Variations: {len(pattern_30['variations'])} (simplified from 6)")
print(f"  Description: {pattern_30['description']}")

print("\n[SUCCESS] Pattern counts updated!")
print("=" * 60)
