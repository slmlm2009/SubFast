#!/usr/bin/env python3
"""
Quick integration test for Pattern 30 (FINAL SEASON) matching logic.
Tests the actual logic used in subfast_rename.py and subfast_embed.py.
"""

import sys
from pathlib import Path

# Add subfast to path
sys.path.insert(0, str(Path(__file__).parent / 'subfast' / 'scripts'))

from common import pattern_engine

def test_pattern_30_integration():
    """Test all Pattern 30 scenarios using the actual integration logic."""
    
    print("=" * 70)
    print("PATTERN 30 (FINAL SEASON) INTEGRATION TEST")
    print("=" * 70)
    print()
    
    test_cases = [
        {
            "name": "VAR1: Subtitle FINAL SEASON -> Infer from Video S08",
            "video": "My.Hero.Academia.S08E01.Toshinori.Yagi.Rising-Origin.1080p.mkv",
            "subtitle": "[Heroacainarabic] Boku no Hero Academia FINAL SEASON - 01.ass",
            "expected_sub": "S08E01",
            "expected_vid": "S08E01"
        },
        {
            "name": "VAR2: Subtitle FINAL SEASON -> Infer from Video S08 (E02)",
            "video": "My.Hero.Academia.S08E02.Toshinori.Yagi.Rising-Origin.1080p.mkv",
            "subtitle": "[Heroacainarabic] Boku no Hero Academia FINAL SEASON - 02.ass",
            "expected_sub": "S08E02",
            "expected_vid": "S08E02"
        },
        {
            "name": "VAR3: Subtitle FINAL SEASON -> Infer from Video S04",
            "video": "Attack.on.Titan.S04E05.1080p.mkv",
            "subtitle": "Attack on Titan FINAL SEASON - 05.ass",
            "expected_sub": "S04E05",
            "expected_vid": "S04E05"
        },
        {
            "name": "VAR4: Video FINAL SEASON -> Infer from Subtitle S08",
            "video": "My.Hero.Academia.FINAL.SEASON.E01.mkv",
            "subtitle": "Boku no Hero Academia S08E01.ass",
            "expected_sub": "S08E01",
            "expected_vid": "S08E01"
        },
        {
            "name": "VAR5: Video FINAL SEASON -> Infer from Subtitle S04",
            "video": "Attack.on.Titan.FINAL.SEASON - 03.mkv",
            "subtitle": "Attack.on.Titan.S04E03.ass",
            "expected_sub": "S04E03",
            "expected_vid": "S04E03"
        },
        {
            "name": "VAR6: Both FINAL SEASON -> No inference (both default S01)",
            "video": "Show.FINAL.SEASON.E01.mkv",
            "subtitle": "Show.FINAL.SEASON - 01.ass",
            "expected_sub": "S01E01",
            "expected_vid": "S01E01"
        }
    ]
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"Test {i}: {test['name']}")
        print(f"  Video:    {test['video']}")
        print(f"  Subtitle: {test['subtitle']}")
        
        # Detect FINAL SEASON keyword
        sub_has_final = pattern_engine.detect_final_season_keyword(test['subtitle'])
        vid_has_final = pattern_engine.detect_final_season_keyword(test['video'])
        print(f"  Detection: Subtitle={sub_has_final}, Video={vid_has_final}")
        
        # Match using the same logic as the scripts
        sub_ep, vid_ep = pattern_engine.match_subtitle_to_video(
            test['subtitle'], 
            test['video']
        )
        
        print(f"  Result:   Subtitle={sub_ep}, Video={vid_ep}")
        print(f"  Expected: Subtitle={test['expected_sub']}, Video={test['expected_vid']}")
        
        # Verify
        if sub_ep == test['expected_sub'] and vid_ep == test['expected_vid']:
            print("  [PASS]")
            passed += 1
        else:
            print("  [FAIL]")
            failed += 1
        
        print()
    
    print("=" * 70)
    print(f"RESULTS: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 70)
    
    return failed == 0

if __name__ == "__main__":
    success = test_pattern_30_integration()
    sys.exit(0 if success else 1)
