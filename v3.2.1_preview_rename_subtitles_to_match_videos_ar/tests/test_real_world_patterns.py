#!/usr/bin/env python3
"""
Real-world pattern matching test cases
Tests patterns with actual anime/show filenames from user reports
"""

import unittest
from subfast.scripts.common.pattern_engine import extract_episode_info, normalize_episode_number


class TestRealWorldPatterns(unittest.TestCase):
    """Test patterns with real-world anime/show filenames"""
    
    def test_pattern_1a_s_episode_space(self):
        """Test S## Episode ## with space (Pattern 1a)"""
        test_cases = [
            ("[SubsPlease] Attack on Titan S04 Episode 16.mkv", (4, 16), "S04E16"),
            ("My.Hero.Academia.S08 Episode 01.1080p.mkv", (8, 1), "S08E01"),
            ("Show.S02 Episode 08.mkv", (2, 8), "S02E08"),
        ]
        
        for filename, expected_tuple, expected_normalized in test_cases:
            with self.subTest(filename=filename):
                result = extract_episode_info(filename)
                self.assertIsNotNone(result, f"No match for {filename}")
                self.assertEqual(result, expected_tuple)
                self.assertEqual(normalize_episode_number(*result), expected_normalized)
    
    def test_pattern_4a_s_dot_e(self):
        """Test S##.E## with dot separator (Pattern 4a)"""
        test_cases = [
            ("One.Piece.S01.E1015.720p.WEB-DL.mkv", (1, 1015), "S01E1015"),
            ("[Erai-raws] Demon Slayer S03.E11.mkv", (3, 11), "S03E11"),
            ("Mob.Psycho.100.S03.E11.1080p.mkv", (3, 11), "S03E11"),
            ("Monogatari.Series.S04.E47.1080p.mkv", (4, 47), "S04E47"),
        ]
        
        for filename, expected_tuple, expected_normalized in test_cases:
            with self.subTest(filename=filename):
                result = extract_episode_info(filename)
                self.assertIsNotNone(result, f"No match for {filename}")
                self.assertEqual(result, expected_tuple)
                self.assertEqual(normalize_episode_number(*result), expected_normalized)
    
    def test_pattern_4b_s_underscore_e(self):
        """Test S##_E## with underscore separator (Pattern 4b)"""
        test_cases = [
            ("Bleach.TYBW.S02_E13.1080p.mkv", (2, 13), "S02E13"),
            ("[HorribleSubs] Naruto S01_E220.mkv", (1, 220), "S01E220"),
        ]
        
        for filename, expected_tuple, expected_normalized in test_cases:
            with self.subTest(filename=filename):
                result = extract_episode_info(filename)
                self.assertIsNotNone(result, f"No match for {filename}")
                self.assertEqual(result, expected_tuple)
                self.assertEqual(normalize_episode_number(*result), expected_normalized)
    
    def test_pattern_5a_s_ep_space(self):
        """Test S## EP## with space before episode (Pattern 5a - FIXED)"""
        test_cases = [
            ("Jujutsu Kaisen S02 EP23.mkv", (2, 23), "S02E23"),
            ("[CR] Vinland Saga S02 EP24.1080p.mkv", (2, 24), "S02E24"),
            ("Neon.Genesis.Evangelion s2 ep 08 ENG.srt", (2, 8), "S02E08"),  # User reported issue
        ]
        
        for filename, expected_tuple, expected_normalized in test_cases:
            with self.subTest(filename=filename):
                result = extract_episode_info(filename)
                self.assertIsNotNone(result, f"No match for {filename}")
                self.assertEqual(result, expected_tuple)
                self.assertEqual(normalize_episode_number(*result), expected_normalized)
    
    def test_pattern_15a_season_episode_space(self):
        """Test Season## Episode ## (Pattern 15a)"""
        test_cases = [
            ("Dr.Stone.Season03 Episode 11.mkv", (3, 11), "S03E11"),
            ("Spy x Family Season02_Episode13.mkv", (2, 13), "S02E13"),
        ]
        
        for filename, expected_tuple, expected_normalized in test_cases:
            with self.subTest(filename=filename):
                result = extract_episode_info(filename)
                self.assertIsNotNone(result, f"No match for {filename}")
                self.assertEqual(result, expected_tuple)
                self.assertEqual(normalize_episode_number(*result), expected_normalized)
    
    def test_pattern_19a_season_concatenated_e(self):
        """Test season## e## with concatenated season (Pattern 19a - NEW)"""
        test_cases = [
            ("Gintama season2 e21.srt", (2, 21), "S02E21"),  # User reported issue
            ("Show season3 e05.mkv", (3, 5), "S03E05"),
        ]
        
        for filename, expected_tuple, expected_normalized in test_cases:
            with self.subTest(filename=filename):
                result = extract_episode_info(filename)
                self.assertIsNotNone(result, f"No match for {filename}")
                self.assertEqual(result, expected_tuple)
                self.assertEqual(normalize_episode_number(*result), expected_normalized)


if __name__ == '__main__':
    unittest.main(verbosity=2)
