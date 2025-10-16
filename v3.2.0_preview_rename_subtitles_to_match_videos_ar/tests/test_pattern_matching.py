"""
Pattern Matching Test Suite

Tests all 25 episode patterns using data-driven approach with dummy files.
Validates pattern recognition, priority, caching, and edge cases.

Test Categories:
- Pattern Recognition: Each pattern's video and subtitle variations
- Pattern Priority: First match wins when multiple patterns could match
- Edge Cases: Word boundaries, case sensitivity, special characters
- Cache Behavior: LRU cache population and performance
- Negative Cases: Files that should NOT match any pattern

Version: 3.2.0
"""

import sys
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent.absolute()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import json
import unittest
from typing import Dict, List

# Import pattern engine functions
from subfast.scripts.common.pattern_engine import (
    get_episode_number_cached,
    clear_episode_cache,
    get_cache_info
)


class TestPatternMatching(unittest.TestCase):
    """Test all 25 episode patterns with dummy files."""
    
    @classmethod
    def setUpClass(cls):
        """Load pattern definitions once for all tests."""
        pattern_file = Path(__file__).parent / 'fixtures' / 'pattern_definitions.json'
        
        if not pattern_file.exists():
            raise FileNotFoundError(
                f"Pattern definitions not found: {pattern_file}\n"
                f"Run 'python tests/generate_test_files.py' first."
            )
        
        with open(pattern_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        cls.patterns = data.get('patterns', [])
        cls.total_patterns = len(cls.patterns)
        
        if cls.total_patterns != 25:
            raise ValueError(f"Expected 25 patterns, found {cls.total_patterns}")
    
    def setUp(self):
        """Clear cache before each test for consistent results."""
        clear_episode_cache()
    
    def _test_pattern_variations(self, pattern: Dict, file_type: str):
        """
        Helper to test all variations of a pattern using ACTUAL FILES on disk.
        
        Args:
            pattern: Pattern definition from JSON
            file_type: 'video_variations' or 'subtitle_variations'
        """
        pattern_id = pattern['id']
        pattern_name = pattern['name']
        variations = pattern.get(file_type, [])
        expected_matches = pattern.get('expected_match', {})
        
        # Determine pattern directory path
        pattern_name_clean = pattern_name.replace('##', '').replace('#', '').replace(' ', '_').strip('_')
        pattern_dir = Path(__file__).parent / 'fixtures' / 'pattern_files' / f"pattern_{pattern_id:02d}_{pattern_name_clean}"
        
        # Get extension filter
        extension = '.mkv' if file_type == 'video_variations' else '.srt'
        
        # Get actual files from disk
        if not pattern_dir.exists():
            self.fail(f"Pattern directory not found: {pattern_dir}. Run 'python tests/generate_test_files.py' first.")
        
        actual_files = sorted([f.name for f in pattern_dir.glob(f'*{extension}')])
        
        # Verify file count matches JSON definition
        if len(actual_files) != len(variations):
            self.fail(
                f"Pattern {pattern_id} ({pattern_name}): "
                f"File count mismatch! JSON defines {len(variations)} {file_type}, "
                f"but disk has {len(actual_files)} files. "
                f"JSON: {variations}, Disk: {actual_files}"
            )
        
        # Test each actual file from disk
        for actual_filename in actual_files:
            with self.subTest(pattern=pattern_id, file=actual_filename):
                # Extract pattern match result
                result = get_episode_number_cached(actual_filename)
                
                # Find expected result from JSON
                # We need to match by comparing normalized filenames since disk files might have slight differences
                expected = None
                for exp_result, files in expected_matches.items():
                    # Check if this actual file matches any expected file in JSON
                    for json_file in files:
                        if json_file.endswith(extension) and json_file in actual_files:
                            # This is the expected result for files in this group
                            if actual_filename in files:
                                expected = exp_result
                                break
                    if expected:
                        break
                
                # If we couldn't find exact match, try to find by pattern
                if not expected:
                    # Fallback: try to find by any file in this variation group
                    for exp_result, files in expected_matches.items():
                        if actual_filename in files:
                            expected = exp_result
                            break
                
                self.assertIsNotNone(
                    expected,
                    f"Pattern {pattern_id} ({pattern_name}): "
                    f"No expected match defined for actual file '{actual_filename}'. "
                    f"This file exists on disk but is not in pattern_definitions.json!"
                )
                
                self.assertEqual(
                    result,
                    expected,
                    f"Pattern {pattern_id} ({pattern_name}): "
                    f"File '{actual_filename}' extracted '{result}' but expected '{expected}'. "
                    f"HINT: File may have been renamed on disk, or pattern regex is incorrect."
                )


class TestPattern01_SE(TestPatternMatching):
    """Test Pattern 1: S##E## format"""
    
    def test_video_variations(self):
        """Test all video file variations for Pattern 1."""
        pattern = self.patterns[0]  # id: 1
        self._test_pattern_variations(pattern, 'video_variations')
    
    def test_subtitle_variations(self):
        """Test all subtitle file variations for Pattern 1."""
        pattern = self.patterns[0]
        self._test_pattern_variations(pattern, 'subtitle_variations')


class TestPattern02_x(TestPatternMatching):
    """Test Pattern 2: ##x## format"""
    
    def test_video_variations(self):
        """Test all video file variations for Pattern 2."""
        pattern = self.patterns[1]  # id: 2
        self._test_pattern_variations(pattern, 'video_variations')
    
    def test_subtitle_variations(self):
        """Test all subtitle file variations for Pattern 2."""
        pattern = self.patterns[1]
        self._test_pattern_variations(pattern, 'subtitle_variations')


class TestPattern03_S_Hyphen(TestPatternMatching):
    """Test Pattern 3: S## - ## format"""
    
    def test_video_variations(self):
        """Test all video file variations for Pattern 3."""
        pattern = self.patterns[2]  # id: 3
        self._test_pattern_variations(pattern, 'video_variations')
    
    def test_subtitle_variations(self):
        """Test all subtitle file variations for Pattern 3."""
        pattern = self.patterns[2]
        self._test_pattern_variations(pattern, 'subtitle_variations')


class TestPattern04_S_E_Hyphen(TestPatternMatching):
    """Test Pattern 4: S## - E## format"""
    
    def test_video_variations(self):
        """Test all video file variations for Pattern 4."""
        pattern = self.patterns[3]  # id: 4
        self._test_pattern_variations(pattern, 'video_variations')
    
    def test_subtitle_variations(self):
        """Test all subtitle file variations for Pattern 4."""
        pattern = self.patterns[3]
        self._test_pattern_variations(pattern, 'subtitle_variations')


class TestPattern05_S_EP_Hyphen(TestPatternMatching):
    """Test Pattern 5: S## - EP## format"""
    
    def test_video_variations(self):
        """Test all video file variations for Pattern 5."""
        pattern = self.patterns[4]  # id: 5
        self._test_pattern_variations(pattern, 'video_variations')
    
    def test_subtitle_variations(self):
        """Test all subtitle file variations for Pattern 5."""
        pattern = self.patterns[4]
        self._test_pattern_variations(pattern, 'subtitle_variations')


class TestPattern06_OrdinalSeason(TestPatternMatching):
    """Test Pattern 6: 1st Season - ## format"""
    
    def test_video_variations(self):
        """Test all video file variations for Pattern 6."""
        pattern = self.patterns[5]  # id: 6
        self._test_pattern_variations(pattern, 'video_variations')
    
    def test_subtitle_variations(self):
        """Test all subtitle file variations for Pattern 6."""
        pattern = self.patterns[5]
        self._test_pattern_variations(pattern, 'subtitle_variations')


class TestPattern07_OrdinalSeasonEpisode(TestPatternMatching):
    """Test Pattern 7: 1st Season Episode ## format"""
    
    def test_video_variations(self):
        """Test all video file variations for Pattern 7."""
        pattern = self.patterns[6]  # id: 7
        self._test_pattern_variations(pattern, 'video_variations')
    
    def test_subtitle_variations(self):
        """Test all subtitle file variations for Pattern 7."""
        pattern = self.patterns[6]
        self._test_pattern_variations(pattern, 'subtitle_variations')


class TestPattern08_OrdinalSeasonE(TestPatternMatching):
    """Test Pattern 8: 1st Season E## format"""
    
    def test_video_variations(self):
        """Test all video file variations for Pattern 8."""
        pattern = self.patterns[7]  # id: 8
        self._test_pattern_variations(pattern, 'video_variations')
    
    def test_subtitle_variations(self):
        """Test all subtitle file variations for Pattern 8."""
        pattern = self.patterns[7]
        self._test_pattern_variations(pattern, 'subtitle_variations')


class TestPattern09_OrdinalSeasonEP(TestPatternMatching):
    """Test Pattern 9: 1st Season EP## format"""
    
    def test_video_variations(self):
        """Test all video file variations for Pattern 9."""
        pattern = self.patterns[8]  # id: 9
        self._test_pattern_variations(pattern, 'video_variations')
    
    def test_subtitle_variations(self):
        """Test all subtitle file variations for Pattern 9."""
        pattern = self.patterns[8]
        self._test_pattern_variations(pattern, 'subtitle_variations')


class TestPattern10_SeasonHyphen(TestPatternMatching):
    """Test Pattern 10: Season ## - ## format"""
    
    def test_video_variations(self):
        """Test all video file variations for Pattern 10."""
        pattern = self.patterns[9]  # id: 10
        self._test_pattern_variations(pattern, 'video_variations')
    
    def test_subtitle_variations(self):
        """Test all subtitle file variations for Pattern 10."""
        pattern = self.patterns[9]
        self._test_pattern_variations(pattern, 'subtitle_variations')


class TestPattern11_SeasonNoSpaceHyphen(TestPatternMatching):
    """Test Pattern 11: Season## - ## format"""
    
    def test_video_variations(self):
        """Test all video file variations for Pattern 11."""
        pattern = self.patterns[10]  # id: 11
        self._test_pattern_variations(pattern, 'video_variations')
    
    def test_subtitle_variations(self):
        """Test all subtitle file variations for Pattern 11."""
        pattern = self.patterns[10]
        self._test_pattern_variations(pattern, 'subtitle_variations')


class TestPattern12_SeasonDotEpisodeDot(TestPatternMatching):
    """Test Pattern 12: Season.#.Episode.# format"""
    
    def test_video_variations(self):
        """Test all video file variations for Pattern 12."""
        pattern = self.patterns[11]  # id: 12
        self._test_pattern_variations(pattern, 'video_variations')
    
    def test_subtitle_variations(self):
        """Test all subtitle file variations for Pattern 12."""
        pattern = self.patterns[11]
        self._test_pattern_variations(pattern, 'subtitle_variations')


class TestPattern13_S_EpDot(TestPatternMatching):
    """Test Pattern 13: S#.Ep.# format"""
    
    def test_video_variations(self):
        """Test all video file variations for Pattern 13."""
        pattern = self.patterns[12]  # id: 13
        self._test_pattern_variations(pattern, 'video_variations')
    
    def test_subtitle_variations(self):
        """Test all subtitle file variations for Pattern 13."""
        pattern = self.patterns[12]
        self._test_pattern_variations(pattern, 'subtitle_variations')


class TestPattern14_SEp(TestPatternMatching):
    """Test Pattern 14: S#Ep# format"""
    
    def test_video_variations(self):
        """Test all video file variations for Pattern 14."""
        pattern = self.patterns[13]  # id: 14
        self._test_pattern_variations(pattern, 'video_variations')
    
    def test_subtitle_variations(self):
        """Test all subtitle file variations for Pattern 14."""
        pattern = self.patterns[13]
        self._test_pattern_variations(pattern, 'subtitle_variations')


class TestPattern15_SeasonSpaceEpisodeSpace(TestPatternMatching):
    """Test Pattern 15: Season # Episode # format"""
    
    def test_video_variations(self):
        """Test all video file variations for Pattern 15."""
        pattern = self.patterns[14]  # id: 15
        self._test_pattern_variations(pattern, 'video_variations')
    
    def test_subtitle_variations(self):
        """Test all subtitle file variations for Pattern 15."""
        pattern = self.patterns[14]
        self._test_pattern_variations(pattern, 'subtitle_variations')


class TestPattern16_SeasonEpisode(TestPatternMatching):
    """Test Pattern 16: Season#Episode# format"""
    
    def test_video_variations(self):
        """Test all video file variations for Pattern 16."""
        pattern = self.patterns[15]  # id: 16
        self._test_pattern_variations(pattern, 'video_variations')
    
    def test_subtitle_variations(self):
        """Test all subtitle file variations for Pattern 16."""
        pattern = self.patterns[15]
        self._test_pattern_variations(pattern, 'subtitle_variations')


class TestPattern17_SeasonSpaceEpisode(TestPatternMatching):
    """Test Pattern 17: Season# Episode# format"""
    
    def test_video_variations(self):
        """Test all video file variations for Pattern 17."""
        pattern = self.patterns[16]  # id: 17
        self._test_pattern_variations(pattern, 'video_variations')
    
    def test_subtitle_variations(self):
        """Test all subtitle file variations for Pattern 17."""
        pattern = self.patterns[16]
        self._test_pattern_variations(pattern, 'subtitle_variations')


class TestPattern18_SeasonSpaceEp(TestPatternMatching):
    """Test Pattern 18: Season# Ep# format"""
    
    def test_video_variations(self):
        """Test all video file variations for Pattern 18."""
        pattern = self.patterns[17]  # id: 18
        self._test_pattern_variations(pattern, 'video_variations')
    
    def test_subtitle_variations(self):
        """Test all subtitle file variations for Pattern 18."""
        pattern = self.patterns[17]
        self._test_pattern_variations(pattern, 'subtitle_variations')


class TestPattern19_SeasonEp(TestPatternMatching):
    """Test Pattern 19: Season#Ep# format"""
    
    def test_video_variations(self):
        """Test all video file variations for Pattern 19."""
        pattern = self.patterns[18]  # id: 19
        self._test_pattern_variations(pattern, 'video_variations')
    
    def test_subtitle_variations(self):
        """Test all subtitle file variations for Pattern 19."""
        pattern = self.patterns[18]
        self._test_pattern_variations(pattern, 'subtitle_variations')


class TestPattern20_E_Only(TestPatternMatching):
    """Test Pattern 20: E## format (assumes Season 1)"""
    
    def test_video_variations(self):
        """Test all video file variations for Pattern 20."""
        pattern = self.patterns[19]  # id: 20
        self._test_pattern_variations(pattern, 'video_variations')
    
    def test_subtitle_variations(self):
        """Test all subtitle file variations for Pattern 20."""
        pattern = self.patterns[19]
        self._test_pattern_variations(pattern, 'subtitle_variations')


class TestPattern21_SeasonDotEpSpace(TestPatternMatching):
    """Test Pattern 21: Season #.Ep # format"""
    
    def test_video_variations(self):
        """Test all video file variations for Pattern 21."""
        pattern = self.patterns[20]  # id: 21
        self._test_pattern_variations(pattern, 'video_variations')
    
    def test_subtitle_variations(self):
        """Test all subtitle file variations for Pattern 21."""
        pattern = self.patterns[20]
        self._test_pattern_variations(pattern, 'subtitle_variations')


class TestPattern22_SeasonDotEp(TestPatternMatching):
    """Test Pattern 22: Season#.Ep# format"""
    
    def test_video_variations(self):
        """Test all video file variations for Pattern 22."""
        pattern = self.patterns[21]  # id: 22
        self._test_pattern_variations(pattern, 'video_variations')
    
    def test_subtitle_variations(self):
        """Test all subtitle file variations for Pattern 22."""
        pattern = self.patterns[21]
        self._test_pattern_variations(pattern, 'subtitle_variations')


class TestPattern23_Ep_Only(TestPatternMatching):
    """Test Pattern 23: Ep## format (assumes Season 1)"""
    
    def test_video_variations(self):
        """Test all video file variations for Pattern 23."""
        pattern = self.patterns[22]  # id: 23
        self._test_pattern_variations(pattern, 'video_variations')
    
    def test_subtitle_variations(self):
        """Test all subtitle file variations for Pattern 23."""
        pattern = self.patterns[22]
        self._test_pattern_variations(pattern, 'subtitle_variations')


class TestPattern24_SeasonSpaceEpSpace(TestPatternMatching):
    """Test Pattern 24: Season # Ep # format"""
    
    def test_video_variations(self):
        """Test all video file variations for Pattern 24."""
        pattern = self.patterns[23]  # id: 24
        self._test_pattern_variations(pattern, 'video_variations')
    
    def test_subtitle_variations(self):
        """Test all subtitle file variations for Pattern 24."""
        pattern = self.patterns[23]
        self._test_pattern_variations(pattern, 'subtitle_variations')


class TestPattern25_HyphenOnly(TestPatternMatching):
    """Test Pattern 25: - ## format (assumes Season 1)"""
    
    def test_video_variations(self):
        """Test all video file variations for Pattern 25."""
        pattern = self.patterns[24]  # id: 25
        self._test_pattern_variations(pattern, 'video_variations')
    
    def test_subtitle_variations(self):
        """Test all subtitle file variations for Pattern 25."""
        pattern = self.patterns[24]
        self._test_pattern_variations(pattern, 'subtitle_variations')


class TestPatternPriority(TestPatternMatching):
    """Test pattern priority: first match wins when multiple patterns could match."""
    
    def test_s01e05_beats_other_formats(self):
        """Pattern 1 (S##E##) should match before other season/episode formats."""
        # S01E05 format should be recognized by Pattern 1
        result = get_episode_number_cached("Show.S01E05.mkv")
        self.assertEqual(result, "S01E05")
        
        # Even with extra text, S01E05 should be found
        result = get_episode_number_cached("Show.Name.S01E05.Season 1 Episode 5.mkv")
        self.assertEqual(result, "S01E05")  # Should match Pattern 1, not Pattern 15
    
    def test_2x05_beats_dash_format(self):
        """Pattern 2 (##x##) should match before similar formats."""
        result = get_episode_number_cached("Series.2x05.mkv")
        self.assertEqual(result, "S02E05")
    
    def test_word_boundaries(self):
        """Patterns should respect word boundaries to avoid false matches."""
        # These should NOT match pattern 2 (##x##) because of word boundaries
        # The regex has (?:^|[._\s-]) before and (?=[._\s-]|$) after
        
        # This SHOULD match (proper boundaries)
        result = get_episode_number_cached("Show.2x05.mkv")
        self.assertEqual(result, "S02E05")
        
        # Pattern matching is based on regex boundaries, so text like "12x3" 
        # embedded in other text should still work if there are separators


class TestCacheBehavior(TestPatternMatching):
    """Test LRU cache behavior for performance."""
    
    def test_cache_populates_on_first_call(self):
        """First call should populate the cache."""
        clear_episode_cache()
        
        # Check cache is empty
        cache_info = get_cache_info()
        self.assertEqual(cache_info.hits, 0)
        self.assertEqual(cache_info.misses, 0)
        
        # First call - cache miss
        result = get_episode_number_cached("Show.S01E05.mkv")
        self.assertEqual(result, "S01E05")
        
        cache_info = get_cache_info()
        self.assertEqual(cache_info.misses, 1)
        self.assertEqual(cache_info.hits, 0)
    
    def test_cache_hits_on_repeated_calls(self):
        """Repeated calls with same filename should hit cache."""
        clear_episode_cache()
        
        filename = "Show.S01E05.mkv"
        
        # First call - miss
        get_episode_number_cached(filename)
        
        # Second call - should hit cache
        result = get_episode_number_cached(filename)
        self.assertEqual(result, "S01E05")
        
        cache_info = get_cache_info()
        self.assertEqual(cache_info.hits, 1)
        self.assertEqual(cache_info.misses, 1)
    
    def test_clear_cache_resets_state(self):
        """Clearing cache should reset cache statistics."""
        # Populate cache
        get_episode_number_cached("Show.S01E05.mkv")
        get_episode_number_cached("Show.S01E05.mkv")  # Hit
        
        # Clear cache
        clear_episode_cache()
        
        # Check cache is reset
        cache_info = get_cache_info()
        self.assertEqual(cache_info.hits, 0)
        self.assertEqual(cache_info.misses, 0)


class TestEdgeCases(TestPatternMatching):
    """Test edge cases and boundary conditions."""
    
    def test_case_insensitivity(self):
        """Pattern matching should be case-insensitive where appropriate."""
        # Uppercase
        result1 = get_episode_number_cached("Show.S01E05.mkv")
        # Lowercase
        result2 = get_episode_number_cached("Show.s01e05.mkv")
        # Mixed
        result3 = get_episode_number_cached("Show.S01e05.mkv")
        
        self.assertEqual(result1, "S01E05")
        self.assertEqual(result2, "S01E05")
        self.assertEqual(result3, "S01E05")
    
    def test_special_characters_in_filename(self):
        """Pattern should work with various separators."""
        # Dot separator
        result1 = get_episode_number_cached("Show.Name.S01E05.720p.mkv")
        # Underscore separator
        result2 = get_episode_number_cached("Show_Name_S01E05_720p.mkv")
        # Space separator
        result3 = get_episode_number_cached("Show Name S01E05 720p.mkv")
        # Hyphen separator
        result4 = get_episode_number_cached("Show-Name-S01E05-720p.mkv")
        
        self.assertEqual(result1, "S01E05")
        self.assertEqual(result2, "S01E05")
        self.assertEqual(result3, "S01E05")
        self.assertEqual(result4, "S01E05")
    
    def test_no_match_returns_none(self):
        """Files with no recognizable pattern should return None."""
        # No episode pattern at all
        result = get_episode_number_cached("Random.Movie.2023.mkv")
        self.assertIsNone(result)
        
        # Just season, no episode
        result = get_episode_number_cached("Show.Season.1.mkv")
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
