"""
Module: update_pattern_metadata.py
Purpose: Automatically update pattern_definitions.json metadata to match actual pattern/variation counts.
"""

import json
from pathlib import Path
from datetime import datetime


def update_metadata():
    """Update the metadata section of pattern_definitions.json with actual counts."""
    pattern_file = Path(__file__).parent / 'fixtures' / 'pattern_definitions.json'
    
    if not pattern_file.exists():
        print(f"[ERROR] Pattern file not found: {pattern_file}")
        return False
    
    # Read the current file
    with open(pattern_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Calculate actual counts
    patterns = data.get('patterns', [])
    total_patterns = len(patterns)
    total_variations = sum(len(p.get('variations', [])) for p in patterns)
    
    # Update metadata
    if 'metadata' not in data:
        data['metadata'] = {}
    
    data['metadata']['total_patterns'] = total_patterns
    data['metadata']['total_variations'] = total_variations
    data['metadata']['last_updated'] = datetime.now().isoformat()
    
    # Write updated file
    with open(pattern_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"[OK] Updated pattern metadata:")
    print(f"   Total patterns: {total_patterns}")
    print(f"   Total variations: {total_variations}")
    print(f"   File: {pattern_file}")
    
    return True


if __name__ == '__main__':
    success = update_metadata()
    if not success:
        exit(1)
