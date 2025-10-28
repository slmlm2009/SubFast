"""Clean up metadata to remove calculated/auto-generated fields."""

import json
from pathlib import Path


def clean_metadata():
    """Remove auto-generated metadata fields, keep only essential user-provided fields."""
    pattern_file = Path(__file__).parent.parent / 'fixtures' / 'pattern_definitions.json'
    
    with open(pattern_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Keep only essential user-provided metadata
    essential_metadata = {
        'version': data['metadata'].get('version', '3.2.1'),
        'description': data['metadata'].get('description', ''),
        'comment': data['metadata'].get('comment', ''),
        'total_patterns': len(data['patterns']),  # Calculate, don't use stale value
        'total_variations': sum(len(p.get('variations', [])) for p in data['patterns'])
    }
    
    data['metadata'] = essential_metadata
    
    with open(pattern_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return {
        'patterns': essential_metadata['total_patterns'],
        'variations': essential_metadata['total_variations']
    }


if __name__ == '__main__':
    result = clean_metadata()
    print(f"SUCCESS: Metadata cleaned:")
    print(f"   Patterns: {result['patterns']}")
    print(f"   Variations: {result['variations']}")
    print("   - Only essential metadata preserved")
    print("   - Zero manual maintenance needed!")
