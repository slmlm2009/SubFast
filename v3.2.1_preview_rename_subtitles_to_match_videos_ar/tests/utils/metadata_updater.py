"""Automatic metadata updater for pattern_definitions.json.

Eliminates manual metadata maintenance - calculates from actual patterns.
"""

import json
from pathlib import Path
from datetime import datetime


def update_pattern_metadata():
    """Automatically recalculate and update metadata from actual patterns."""
    pattern_file = Path(__file__).parent.parent / 'fixtures' / 'pattern_definitions.json'
    
    if not pattern_file.exists():
        raise FileNotFoundError(f"Pattern file not found: {pattern_file}")
    
    # Read current JSON
    with open(pattern_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Calculate from actual patterns (NO manual updates needed!)
    patterns = data.get('patterns', [])
    metadata = data.get('metadata', {})
    
    # Update calculated values - preserve user metadata only
    calculated_metadata = {
        'version': metadata.get('version', '3.2.1'),  # Keep user version
        'description': metadata.get('description', 'Pattern definitions for SubFast episode matching tests'),  # Keep user description
        'comment': metadata.get('comment', 'Pattern definitions comment'),  # Keep user comment
        'total_patterns': len(patterns),  # Calculate automatically
        'total_variations': sum(len(p.get('variations', [])) for p in patterns),  # Calculate automatically
        'auto_updated_at': datetime.now().isoformat()  # Tracking only
    }
    
    # Preserve essential user metadata, update calculated values only
    essential_metadata = {
        'version': metadata.get('version', '3.2.1'),
        'description': metadata.get('description', 'Pattern definitions for SubFast episode matching tests'),
        'comment': metadata.get('comment', 'Pattern definitions comment'),
        **calculated_metadata  # Override with calculated values
    }
        
    # Update only if calculated values changed
    if (metadata.get('total_patterns') != calculated_metadata['total_patterns'] or
        metadata.get('total_variations') != calculated_metadata['total_variations']):
        
        data['metadata'] = essential_metadata
        
        # Write updated JSON
        with open(pattern_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return {
            'updated': True,
            'old_counts': {
                'patterns': metadata.get('total_patterns', 0),
                'variations': metadata.get('total_variations', 0)
            },
            'new_counts': {
                'patterns': calculated_metadata['total_patterns'],
                'variations': calculated_metadata['total_variations']
            }
        }
    
    return {'updated': False, 'current_counts': calculated_metadata}


if __name__ == '__main__':
    result = update_pattern_metadata()
    
    if result['updated']:
        print(f"SUCCESS: Auto-updated my metadata:")
        print(f"   Patterns: {result['old_counts']['patterns']} → {result['new_counts']['patterns']}")
        print(f"   Variations: {result['old_counts']['variations']} → {result['new_counts']['variations']}")
        print("   - No manual editing required!")
    else:
        counts = result['current_counts']
        print(f"SUCCESS: No metadata updates needed")
        print(f"   Current: {counts['total_patterns']} patterns, {counts['total_variations']} variations")
        print(f"   Maintenance-free!")
