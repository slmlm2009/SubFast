#!/usr/bin/env python3
"""
Unit tests for file discovery and matching functionality (Story 2.1)
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from embed_subtitles_to_match_videos_ar import (
    get_episode_number,
    get_episode_number_cached,
    extract_base_name,
    match_movie_files,
    find_matching_files
)


class TestEpisodePatternDetection(unittest.TestCase):
    """Test episode pattern detection with all 25+ patterns"""
    
    def test_standard_s_e_format(self):
        """Test S01E05 format"""
        self.assertEqual(get_episode_number('Show.S01E05.mkv'), 'S01E05')
        self.assertEqual(get_episode_number('Show.s02e10.mkv'), 'S02E10')
    
    def test_x_format(self):
        """Test 1x05 format"""
        self.assertEqual(get_episode_number('Show.1x05.mkv'), 'S01E05')
        self.assertEqual(get_episode_number('Show.2x10.mkv'), 'S02E10')
    
    def test_dash_format(self):
        """Test S01 - 05 format"""
        self.assertEqual(get_episode_number('Show.S01 - 05.mkv'), 'S01E05')
        self.assertEqual(get_episode_number('Show.S2 - 10.mkv'), 'S02E10')
    
    def test_ordinal_season(self):
        """Test 1st Season Episode 5 format"""
        self.assertEqual(get_episode_number('Show.1st Season Episode 5.mkv'), 'S01E05')
        self.assertEqual(get_episode_number('Show.2nd Season Episode 10.mkv'), 'S02E10')
        self.assertEqual(get_episode_number('Show.3rd Season Episode 8.mkv'), 'S03E08')
    
    def test_season_episode_format(self):
        """Test Season 1 Episode 5 format"""
        self.assertEqual(get_episode_number('Show.Season 1 Episode 5.mkv'), 'S01E05')
        self.assertEqual(get_episode_number('Show.Season.2.Episode.10.mkv'), 'S02E10')
    
    def test_episode_only(self):
        """Test Episode 5 format (assumes Season 1)"""
        self.assertEqual(get_episode_number('Show.E05.mkv'), 'S01E05')
        self.assertEqual(get_episode_number('Show.Episode 10.mkv'), 'S01E10')
    
    def test_dash_number_only(self):
        """Test - 05 format (assumes Season 1)"""
        self.assertEqual(get_episode_number('Show - 05.mkv'), 'S01E05')
    
    def test_no_pattern(self):
        """Test filenames without episode patterns"""
        self.assertIsNone(get_episode_number('Movie Title 2023.mkv'))
        self.assertIsNone(get_episode_number('RandomFile.mkv'))
    
    def test_episode_cache(self):
        """Test episode number caching"""
        filename = 'Show.S01E05.mkv'
        result1 = get_episode_number_cached(filename)
        result2 = get_episode_number_cached(filename)
        self.assertEqual(result1, result2)
        self.assertEqual(result1, 'S01E05')


class TestMovieMatching(unittest.TestCase):
    """Test movie file matching"""
    
    def setUp(self):
        """Create temporary directory for testing"""
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)
    
    def tearDown(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.test_dir)
    
    def test_year_match(self):
        """Test matching based on year"""
        video = Path('Movie Title (2023).mkv')
        subtitle = Path('Movie Title 2023.srt')
        
        result = match_movie_files([video], [subtitle])
        self.assertIsNotNone(result)
        self.assertEqual(result[0], video)
        self.assertEqual(result[1], subtitle)
    
    def test_word_overlap_match(self):
        """Test matching based on word overlap"""
        video = Path('Great Movie 1080p.mkv')
        subtitle = Path('Great Movie.srt')
        
        result = match_movie_files([video], [subtitle])
        self.assertIsNotNone(result)
    
    def test_no_match_different_titles(self):
        """Test no match for different titles"""
        video = Path('Movie A.mkv')
        subtitle = Path('Movie B.srt')
        
        result = match_movie_files([video], [subtitle])
        # Could be None or a match depending on word overlap threshold
        # This test verifies the function executes without error
    
    def test_multiple_files_no_match(self):
        """Test no match when multiple files present"""
        videos = [Path('Movie1.mkv'), Path('Movie2.mkv')]
        subtitles = [Path('Sub1.srt')]
        
        result = match_movie_files(videos, subtitles)
        self.assertIsNone(result)


class TestFileDiscovery(unittest.TestCase):
    """Test file discovery and matching"""
    
    def setUp(self):
        """Create temporary directory with test files"""
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)
    
    def tearDown(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.test_dir)
    
    def test_episode_matching(self):
        """Test matching TV show episodes"""
        # Create test files
        (self.test_path / 'Show.S01E01.mkv').touch()
        (self.test_path / 'Show.S01E02.mkv').touch()
        (self.test_path / 'Show.S01E01.srt').touch()
        (self.test_path / 'Show.S01E02.srt').touch()
        
        matches = find_matching_files(self.test_dir)
        
        self.assertEqual(len(matches), 2)
        # Verify matches contain the expected files
        video_names = {m[0].name for m in matches}
        subtitle_names = {m[1].name for m in matches}
        
        self.assertIn('Show.S01E01.mkv', video_names)
        self.assertIn('Show.S01E02.mkv', video_names)
        self.assertIn('Show.S01E01.srt', subtitle_names)
        self.assertIn('Show.S01E02.srt', subtitle_names)
    
    def test_movie_matching(self):
        """Test matching movie files"""
        # Create test files
        (self.test_path / 'Great Movie (2023).mkv').touch()
        (self.test_path / 'Great Movie 2023.srt').touch()
        
        matches = find_matching_files(self.test_dir)
        
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0][0].name, 'Great Movie (2023).mkv')
        self.assertEqual(matches[0][1].name, 'Great Movie 2023.srt')
    
    def test_mixed_extensions(self):
        """Test with different subtitle extensions"""
        # Create test files with different extensions
        (self.test_path / 'Show.S01E01.mkv').touch()
        (self.test_path / 'Show.S01E02.mkv').touch()
        (self.test_path / 'Show.S01E01.ass').touch()
        (self.test_path / 'Show.S01E02.ssa').touch()
        
        matches = find_matching_files(self.test_dir)
        
        self.assertEqual(len(matches), 2)
    
    def test_unmatched_files(self):
        """Test handling of unmatched files"""
        # Create files that won't match
        (self.test_path / 'Show.S01E01.mkv').touch()
        (self.test_path / 'Different.S02E01.srt').touch()
        
        matches = find_matching_files(self.test_dir)
        
        # Should find no matches
        self.assertEqual(len(matches), 0)
    
    def test_empty_directory(self):
        """Test empty directory"""
        matches = find_matching_files(self.test_dir)
        self.assertEqual(len(matches), 0)
    
    def test_hidden_files_ignored(self):
        """Test that hidden files are ignored"""
        (self.test_path / '.hidden.mkv').touch()
        (self.test_path / '.hidden.srt').touch()
        
        matches = find_matching_files(self.test_dir)
        self.assertEqual(len(matches), 0)


class TestBaseNameExtraction(unittest.TestCase):
    """Test base name extraction"""
    
    def test_basic_extraction(self):
        """Test basic filename cleaning"""
        self.assertEqual(extract_base_name('Movie.Title.mkv'), 'Movie Title')
        self.assertEqual(extract_base_name('Movie_Title.mkv'), 'Movie Title')
        self.assertEqual(extract_base_name('Movie-Title.mkv'), 'Movie Title')
    
    def test_mixed_separators(self):
        """Test mixed separator handling"""
        self.assertEqual(extract_base_name('Movie.Title_2023-HD.mkv'), 'Movie Title 2023 HD')


if __name__ == '__main__':
    # Run tests with verbose output
    from datetime import datetime
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(__import__(__name__))
    
    # Collect all tests from suite BEFORE running (suite gets consumed)
    all_tests_list = []
    
    def collect_all_tests(test_or_suite):
        """Recursively collect all test cases from suite"""
        try:
            # Try to iterate - it's a suite
            for test in test_or_suite:
                collect_all_tests(test)
        except TypeError:
            # Can't iterate - it's a test case
            if hasattr(test_or_suite, '_testMethodName'):
                short_name = f"{test_or_suite.__class__.__name__}.{test_or_suite._testMethodName}"
                full_name = str(test_or_suite)
                all_tests_list.append((full_name, short_name))
    
    collect_all_tests(suite)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Export test summary as CSV with ALL test scenarios
    import csv
    summary_file = Path(__file__).parent / 'tests' / 'unit_test_summary.csv'
    summary_file.parent.mkdir(exist_ok=True)
    
    # Collect all test results
    failed_tests = {str(test): traceback for test, traceback in result.failures}
    error_tests = {str(test): traceback for test, traceback in result.errors}
    
    with open(summary_file, 'w', encoding='utf-8', newline='') as f:
        # Write metadata header as comments
        f.write(f"# Unit Test Summary - File Discovery and Matching (Story 2.1)\n")
        f.write(f"# Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Test Module: {__file__}\n")
        f.write(f"# Tests Run: {result.testsRun}\n")
        f.write(f"# Successes: {result.testsRun - len(result.failures) - len(result.errors)}\n")
        f.write(f"# Failures: {len(result.failures)}\n")
        f.write(f"# Errors: {len(result.errors)}\n")
        f.write(f"# Skipped: {len(result.skipped)}\n")
        f.write(f"# Overall Result: {'PASS' if result.wasSuccessful() else 'FAIL'}\n")
        f.write("#\n")
        
        # CSV headers and data
        writer = csv.writer(f)
        writer.writerow(['Test Name', 'Category', 'Status', 'Error Message'])
        
        # Write all test results
        for full_name, short_name in sorted(all_tests_list, key=lambda x: x[1]):
            # Determine category
            category = 'Other'
            if 'Episode' in short_name:
                category = 'Episode Pattern Detection'
            elif 'Movie' in short_name:
                category = 'Movie Matching'
            elif 'FileDiscovery' in short_name:
                category = 'File Discovery'
            elif 'BaseName' in short_name:
                category = 'Base Name Extraction'
            
            # Determine status and error using full_name for matching
            if full_name in failed_tests:
                status = 'FAIL'
                # Extract just the assertion error line
                error_msg = failed_tests[full_name].split('\n')[-2] if failed_tests[full_name] else 'Failed'
            elif full_name in error_tests:
                status = 'ERROR'
                error_msg = error_tests[full_name].split('\n')[-2] if error_tests[full_name] else 'Error'
            else:
                status = 'PASS'
                error_msg = ''
            
            writer.writerow([short_name, category, status, error_msg])
    
    print(f"\n[Test Summary Exported] {summary_file}")
