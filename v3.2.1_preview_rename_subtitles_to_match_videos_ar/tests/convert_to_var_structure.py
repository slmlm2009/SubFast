"""
Convert pattern_definitions.json to VAR-based structure

This script converts the old structure to the new VAR-based structure
where each variation has a unique VAR ID and expected result.
"""

import json
from pathlib import Path

def convert_pattern_definitions():
    """Convert old structure to new VAR-based structure."""
    
    # Load old structure
    old_file = Path(__file__).parent / 'fixtures' / 'pattern_definitions.json'
    with open(old_file, 'r', encoding='utf-8') as f:
        old_data = json.load(f)
    
    # Create new structure
    new_data = {
        "metadata": {
            "version": "3.2.0",
            "description": "Pattern definitions for SubFast episode matching tests with VAR-based structure",
            "total_patterns": 25,
            "comment": "Each variation has [VAR#] prefix for stable reference during manual testing"
        },
        "patterns": []
    }
    
    # Convert each pattern
    for pattern in old_data['patterns']:
        pattern_id = pattern['id']
        pattern_name = pattern['name']
        description = pattern['description']
        expected_matches = pattern.get('expected_match', {})
        
        # Create variations list
        variations = []
        var_counter = 1
        
        # Group files by expected result
        for expected_episode, files in expected_matches.items():
            # Find video and subtitle for this variation
            video_file = None
            subtitle_file = None
            
            for file in files:
                if file.endswith('.mkv'):
                    video_file = file
                elif file.endswith('.srt'):
                    subtitle_file = file
            
            if video_file and subtitle_file:
                variations.append({
                    "var_id": f"VAR{var_counter}",
                    "expected": expected_episode,
                    "video_template": video_file,
                    "subtitle_template": subtitle_file
                })
                var_counter += 1
        
        # Add pattern to new structure
        new_pattern = {
            "id": pattern_id,
            "name": pattern_name,
            "description": description,
            "variations": variations
        }
        
        new_data['patterns'].append(new_pattern)
    
    # Save new structure
    new_file = Path(__file__).parent / 'fixtures' / 'pattern_definitions_new.json'
    with open(new_file, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=2, ensure_ascii=False)
    
    print(f"[SUCCESS] Converted {len(new_data['patterns'])} patterns")
    print(f"[SUCCESS] Saved to: {new_file}")
    
    # Show sample
    print("\nSample Pattern Structure:")
    print(json.dumps(new_data['patterns'][0], indent=2))
    
    return new_file


if __name__ == '__main__':
    convert_pattern_definitions()
