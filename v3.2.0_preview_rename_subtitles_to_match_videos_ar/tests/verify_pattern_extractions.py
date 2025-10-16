"""
Pattern Extraction Verification Script

This script shows what season/episode is extracted from each dummy file.
Use this to manually verify that pattern matching is working correctly.

Usage:
    python tests/verify_pattern_extractions.py
    python tests/verify_pattern_extractions.py --pattern 21
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.absolute()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import json
import argparse
from subfast.scripts.common.pattern_engine import (
    get_episode_number_cached,
    extract_episode_info
)


def verify_pattern_files(pattern_filter=None):
    """
    Verify all pattern files and show what was extracted.
    
    Args:
        pattern_filter: Optional pattern ID to filter (e.g., 21)
    """
    # Load pattern definitions
    pattern_file = Path(__file__).parent / 'fixtures' / 'pattern_definitions.json'
    with open(pattern_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    patterns = data.get('patterns', [])
    
    if pattern_filter:
        patterns = [p for p in patterns if p['id'] == pattern_filter]
        if not patterns:
            print(f"[ERROR] Pattern {pattern_filter} not found!")
            return
    
    print("=" * 120)
    print("PATTERN EXTRACTION VERIFICATION")
    print("=" * 120)
    print()
    
    total_files = 0
    correct_extractions = 0
    failed_extractions = 0
    
    for pattern in patterns:
        pattern_id = pattern['id']
        pattern_name = pattern['name']
        expected_matches = pattern.get('expected_match', {})
        
        # Determine pattern directory
        pattern_name_clean = pattern_name.replace('##', '').replace('#', '').replace(' ', '_').strip('_')
        pattern_dir = Path(__file__).parent / 'fixtures' / 'pattern_files' / f"pattern_{pattern_id:02d}_{pattern_name_clean}"
        
        if not pattern_dir.exists():
            print(f"[SKIP] Pattern {pattern_id:02d}: {pattern_name} - Directory not found")
            continue
        
        print(f"Pattern {pattern_id:02d}: {pattern_name}")
        print("-" * 120)
        
        # Get all files (videos and subtitles)
        all_files = sorted(list(pattern_dir.glob('*.mkv')) + list(pattern_dir.glob('*.srt')))
        
        for file_path in all_files:
            filename = file_path.name
            total_files += 1
            
            # Extract using pattern engine
            extracted = get_episode_number_cached(filename)
            
            # Get detailed extraction
            if extracted:
                season, episode = extract_episode_info(filename)
                extraction_detail = f"S{season:02d}E{episode:02d}"
            else:
                season, episode = None, None
                extraction_detail = "NO MATCH"
            
            # Find expected result
            expected = None
            for exp_result, files in expected_matches.items():
                if filename in files:
                    expected = exp_result
                    break
            
            # Determine status
            if extracted == expected:
                status = "[PASS]"
                correct_extractions += 1
            else:
                status = "[FAIL]"
                failed_extractions += 1
            
            # Format output
            print(f"  {status} | {filename:<40} | Extracted: {extraction_detail:<8} | Expected: {expected or 'N/A':<8}")
        
        print()
    
    # Summary
    print("=" * 120)
    print("SUMMARY")
    print("=" * 120)
    print(f"Total Files Checked: {total_files}")
    print(f"Correct Extractions: {correct_extractions} ({correct_extractions/total_files*100:.1f}%)")
    print(f"Failed Extractions:  {failed_extractions} ({failed_extractions/total_files*100:.1f}%)")
    print("=" * 120)
    
    if failed_extractions > 0:
        print()
        print("[WARNING] Some files failed extraction!")
        print("Possible reasons:")
        print("  1. File was renamed on disk (doesn't match pattern_definitions.json)")
        print("  2. Pattern regex is incorrect")
        print("  3. Pattern priority issue (earlier pattern matched instead)")
        print()
        print("Fix: Run 'python tests/reset_test_files.py' to restore original filenames")
        return 1
    
    return 0


def main():
    parser = argparse.ArgumentParser(
        description='Verify pattern extraction from dummy files',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--pattern',
        type=int,
        help='Filter by specific pattern ID (1-25)'
    )
    
    args = parser.parse_args()
    
    result = verify_pattern_files(args.pattern)
    sys.exit(result)


if __name__ == '__main__':
    main()
