#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for embed_subtitles_to_match_videos_ar.py

Tests cover:
- Configuration loading (valid, invalid, missing config.ini)
- mkvmerge path resolution (configured vs same directory)
- mkvmerge validation (success and failure cases)
- Command-line argument parsing
"""

import unittest
import tempfile
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
import subprocess

# Add parent directory to path to import the script
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import embed_subtitles_to_match_videos_ar as embed_script


class TestConfigLoading(unittest.TestCase):
    """Test configuration loading functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / 'config.ini'
    
    def tearDown(self):
        """Clean up temporary files"""
        if self.config_path.exists():
            self.config_path.unlink()
        os.rmdir(self.temp_dir)
    
    @patch('embed_subtitles_to_match_videos_ar.Path')
    def test_load_config_missing_file(self, mock_path):
        """Test config loading when config.ini doesn't exist"""
        # Mock Path to return our temp directory
        mock_path.return_value.parent = Path(self.temp_dir)
        mock_path.return_value.parent.__truediv__ = lambda self, other: Path(self.temp_dir) / other
        
        # Ensure config file doesn't exist
        config_file = Path(self.temp_dir) / 'config.ini'
        if config_file.exists():
            config_file.unlink()
        
        config = embed_script.load_config()
        
        # Should return default configuration
        self.assertIsNone(config['mkvmerge_path'])
        self.assertTrue(config['default_track'])
        self.assertIsNone(config['language'])
    
    def test_load_config_valid_file(self):
        """Test config loading with valid config.ini"""
        # Create valid config file
        config_content = """
[Embedding]
mkvmerge_path = C:/Program Files/MKVToolNix/mkvmerge.exe
default_track = false
language = ara
"""
        self.config_path.write_text(config_content)
        
        with patch('embed_subtitles_to_match_videos_ar.Path') as mock_path:
            mock_path.return_value.parent = Path(self.temp_dir)
            mock_path.return_value.parent.__truediv__ = lambda self, other: Path(self.temp_dir) / other
            
            config = embed_script.load_config()
            
            self.assertEqual(config['mkvmerge_path'], 'C:/Program Files/MKVToolNix/mkvmerge.exe')
            self.assertFalse(config['default_track'])
            self.assertEqual(config['language'], 'ara')
    
    def test_load_config_empty_values(self):
        """Test config loading with empty values (should use defaults)"""
        config_content = """
[Embedding]
mkvmerge_path = 
default_track = true
language = 
"""
        self.config_path.write_text(config_content)
        
        with patch('embed_subtitles_to_match_videos_ar.Path') as mock_path:
            mock_path.return_value.parent = Path(self.temp_dir)
            mock_path.return_value.parent.__truediv__ = lambda self, other: Path(self.temp_dir) / other
            
            config = embed_script.load_config()
            
            self.assertIsNone(config['mkvmerge_path'])
            self.assertTrue(config['default_track'])
            self.assertIsNone(config['language'])
    
    def test_load_config_invalid_file(self):
        """Test config loading with invalid/corrupted config.ini"""
        # Create invalid config file
        self.config_path.write_text("This is not valid INI format!!!")
        
        with patch('embed_subtitles_to_match_videos_ar.Path') as mock_path:
            mock_path.return_value.parent = Path(self.temp_dir)
            mock_path.return_value.parent.__truediv__ = lambda self, other: Path(self.temp_dir) / other
            
            config = embed_script.load_config()
            
            # Should return defaults on parse error
            self.assertIsNone(config['mkvmerge_path'])
            self.assertTrue(config['default_track'])


class TestMkvmergeValidation(unittest.TestCase):
    """Test mkvmerge validation functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.mkvmerge_path = Path(self.temp_dir) / 'mkvmerge.exe'
    
    def tearDown(self):
        """Clean up temporary files"""
        if self.mkvmerge_path.exists():
            self.mkvmerge_path.unlink()
        os.rmdir(self.temp_dir)
    
    def test_validate_mkvmerge_not_found(self):
        """Test validation when mkvmerge.exe doesn't exist"""
        non_existent_path = str(Path(self.temp_dir) / 'nonexistent.exe')
        success, path, version = embed_script.validate_mkvmerge(non_existent_path)
        
        self.assertFalse(success)
        self.assertIsNone(path)
        self.assertIsNone(version)
    
    @patch('embed_subtitles_to_match_videos_ar.Path')
    @patch('embed_subtitles_to_match_videos_ar.subprocess.run')
    def test_validate_mkvmerge_success(self, mock_run, mock_path):
        """Test successful mkvmerge validation"""
        # Create a dummy file
        self.mkvmerge_path.touch()
        
        # Mock Path to return our test path
        mock_path.return_value.parent = Path(self.temp_dir)
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value.__truediv__ = lambda self, other: mock_path_instance
        
        # Mock subprocess to return success
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "mkvmerge v82.0 ('I'm The President') 64-bit\n"
        mock_run.return_value = mock_result
        
        with patch('embed_subtitles_to_match_videos_ar.os.access', return_value=True):
            success, path, version = embed_script.validate_mkvmerge(str(self.mkvmerge_path))
        
        self.assertTrue(success)
        self.assertIsNotNone(path)
        self.assertIn("mkvmerge", version)
    
    @patch('embed_subtitles_to_match_videos_ar.subprocess.run')
    def test_validate_mkvmerge_not_executable(self, mock_run):
        """Test validation when mkvmerge exists but can't execute"""
        # Create a dummy file
        self.mkvmerge_path.touch()
        
        # Mock subprocess to raise an exception
        mock_run.side_effect = FileNotFoundError("File not found")
        
        with patch('embed_subtitles_to_match_videos_ar.os.access', return_value=True):
            success, path, version = embed_script.validate_mkvmerge(str(self.mkvmerge_path))
        
        self.assertFalse(success)
        self.assertEqual(path, str(self.mkvmerge_path))
        self.assertIsNone(version)
    
    @patch('embed_subtitles_to_match_videos_ar.subprocess.run')
    def test_validate_mkvmerge_timeout(self, mock_run):
        """Test validation when mkvmerge command times out"""
        # Create a dummy file
        self.mkvmerge_path.touch()
        
        # Mock subprocess to timeout
        mock_run.side_effect = subprocess.TimeoutExpired(cmd=['mkvmerge'], timeout=5)
        
        with patch('embed_subtitles_to_match_videos_ar.os.access', return_value=True):
            success, path, version = embed_script.validate_mkvmerge(str(self.mkvmerge_path))
        
        self.assertFalse(success)
        self.assertIsNone(version)


class TestCommandLineParsing(unittest.TestCase):
    """Test command-line argument parsing"""
    
    def test_parse_no_arguments(self):
        """Test parsing with no arguments (should use current directory)"""
        test_args = ['embed_subtitles_to_match_videos_ar.py']
        with patch('sys.argv', test_args):
            args = embed_script.parse_arguments()
            self.assertEqual(args.directory, '.')
            self.assertFalse(args.test_mkvmerge)
    
    def test_parse_directory_argument(self):
        """Test parsing with directory argument"""
        test_args = ['embed_subtitles_to_match_videos_ar.py', '/path/to/videos']
        with patch('sys.argv', test_args):
            args = embed_script.parse_arguments()
            self.assertEqual(args.directory, '/path/to/videos')
            self.assertFalse(args.test_mkvmerge)
    
    def test_parse_test_mkvmerge_flag(self):
        """Test parsing with --test-mkvmerge flag"""
        test_args = ['embed_subtitles_to_match_videos_ar.py', '--test-mkvmerge']
        with patch('sys.argv', test_args):
            args = embed_script.parse_arguments()
            self.assertTrue(args.test_mkvmerge)
    
    def test_parse_version_flag(self):
        """Test parsing with --version flag"""
        test_args = ['embed_subtitles_to_match_videos_ar.py', '--version']
        with patch('sys.argv', test_args):
            with self.assertRaises(SystemExit) as cm:
                embed_script.parse_arguments()
            # --version causes SystemExit with code 0
            self.assertEqual(cm.exception.code, 0)


class TestRunCommand(unittest.TestCase):
    """Test command execution functionality"""
    
    @patch('embed_subtitles_to_match_videos_ar.subprocess.run')
    def test_run_command_success(self, mock_run):
        """Test successful command execution"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Success output"
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        success, stdout, stderr = embed_script.run_command(['echo', 'test'])
        
        self.assertTrue(success)
        self.assertEqual(stdout, "Success output")
        self.assertEqual(stderr, "")
    
    @patch('embed_subtitles_to_match_videos_ar.subprocess.run')
    def test_run_command_failure(self, mock_run):
        """Test failed command execution"""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "Error message"
        mock_run.return_value = mock_result
        
        success, stdout, stderr = embed_script.run_command(['false'])
        
        self.assertFalse(success)
        self.assertEqual(stderr, "Error message")
    
    @patch('embed_subtitles_to_match_videos_ar.subprocess.run')
    def test_run_command_timeout(self, mock_run):
        """Test command execution timeout"""
        mock_run.side_effect = subprocess.TimeoutExpired(cmd=['sleep'], timeout=300)
        
        success, stdout, stderr = embed_script.run_command(['sleep', '1000'])
        
        self.assertFalse(success)
        self.assertIn("timed out", stderr)


class TestStubFunctions(unittest.TestCase):
    """Test that stub functions exist and return expected types"""
    
    def test_find_matching_files_stub(self):
        """Test find_matching_files stub returns empty list"""
        result = embed_script.find_matching_files('/some/path')
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
    
    def test_build_mkvmerge_command_stub(self):
        """Test build_mkvmerge_command stub returns empty list"""
        result = embed_script.build_mkvmerge_command('video.mkv', 'subtitle.srt', 'output.mkv', {})
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
    
    def test_generate_report_stub(self):
        """Test generate_report stub doesn't raise exceptions"""
        try:
            embed_script.generate_report([], '/path/to/report.csv')
        except Exception as e:
            self.fail(f"generate_report stub raised exception: {e}")


class TestLanguageDetection(unittest.TestCase):
    """Test language code detection from subtitle filenames."""
    
    def test_detect_language_dot_pattern_2letter(self):
        """Test detection of 2-letter language codes with dot separator."""
        self.assertEqual(embed_script.detect_language_from_filename('episode.ar.srt'), 'ar')
        self.assertEqual(embed_script.detect_language_from_filename('movie.en.srt'), 'en')
        self.assertEqual(embed_script.detect_language_from_filename('show.fr.ass'), 'fr')
    
    def test_detect_language_dot_pattern_3letter(self):
        """Test detection of 3-letter language codes with dot separator."""
        self.assertEqual(embed_script.detect_language_from_filename('episode.ara.srt'), 'ara')
        self.assertEqual(embed_script.detect_language_from_filename('movie.eng.srt'), 'eng')
        self.assertEqual(embed_script.detect_language_from_filename('show.fra.ssa'), 'fra')
    
    def test_detect_language_underscore_pattern(self):
        """Test detection with underscore separator."""
        self.assertEqual(embed_script.detect_language_from_filename('episode_ar.srt'), 'ar')
        self.assertEqual(embed_script.detect_language_from_filename('movie_eng.srt'), 'eng')
    
    def test_detect_language_bracket_pattern(self):
        """Test detection with bracket notation."""
        self.assertEqual(embed_script.detect_language_from_filename('episode[ar].srt'), 'ar')
        self.assertEqual(embed_script.detect_language_from_filename('movie[en].srt'), 'en')
    
    def test_detect_language_no_language(self):
        """Test files without language codes return None."""
        self.assertIsNone(embed_script.detect_language_from_filename('episode.srt'))
        self.assertIsNone(embed_script.detect_language_from_filename('movie.ass'))
        self.assertIsNone(embed_script.detect_language_from_filename('show.ssa'))
    
    def test_detect_language_invalid_code(self):
        """Test invalid language codes are not detected."""
        self.assertIsNone(embed_script.detect_language_from_filename('episode.xx.srt'))
        self.assertIsNone(embed_script.detect_language_from_filename('movie.zzz.srt'))


class TestCommandBuilding(unittest.TestCase):
    """Test mkvmerge command building logic."""
    
    def test_build_command_with_language_and_default(self):
        """Test command building with language tag and default flag."""
        config = {'mkvmerge_path': None, 'default_track': True, 'language': None}
        
        with patch.object(embed_script, 'validate_mkvmerge') as mock_validate:
            mock_validate.return_value = (True, 'C:/tools/mkvmerge.exe', 'v88.0')
            
            command = embed_script.build_mkvmerge_command('video.mkv', 'sub.ar.srt', 'output.mkv', config)
            
            self.assertIn('C:/tools/mkvmerge.exe', command)
            self.assertIn('-o', command)
            self.assertIn('output.mkv', command)
            self.assertIn('video.mkv', command)
            self.assertIn('--language', command)
            self.assertIn('0:ar', command)
            self.assertIn('--default-track', command)
            self.assertIn('0:yes', command)
            self.assertIn('sub.ar.srt', command)
    
    def test_build_command_without_language(self):
        """Test command building when no language is detected or configured."""
        config = {'mkvmerge_path': None, 'default_track': True, 'language': None}
        
        with patch.object(embed_script, 'validate_mkvmerge') as mock_validate:
            mock_validate.return_value = (True, 'C:/tools/mkvmerge.exe', 'v88.0')
            
            command = embed_script.build_mkvmerge_command('video.mkv', 'sub.srt', 'output.mkv', config)
            
            self.assertNotIn('--language', command)
            self.assertIn('--default-track', command)
            self.assertIn('0:yes', command)
    
    def test_build_command_with_config_language_fallback(self):
        """Test language fallback to config when not in filename."""
        config = {'mkvmerge_path': None, 'default_track': True, 'language': 'ar'}
        
        with patch.object(embed_script, 'validate_mkvmerge') as mock_validate:
            mock_validate.return_value = (True, 'C:/tools/mkvmerge.exe', 'v88.0')
            
            command = embed_script.build_mkvmerge_command('video.mkv', 'sub.srt', 'output.mkv', config)
            
            self.assertIn('--language', command)
            self.assertIn('0:ar', command)
    
    def test_build_command_default_track_false(self):
        """Test command building with default_track=False."""
        config = {'mkvmerge_path': None, 'default_track': False, 'language': None}
        
        with patch.object(embed_script, 'validate_mkvmerge') as mock_validate:
            mock_validate.return_value = (True, 'C:/tools/mkvmerge.exe', 'v88.0')
            
            command = embed_script.build_mkvmerge_command('video.mkv', 'sub.srt', 'output.mkv', config)
            
            self.assertNotIn('--default-track', command)
    
    def test_build_command_mkvmerge_not_found(self):
        """Test command building when mkvmerge is not available."""
        config = {'mkvmerge_path': None, 'default_track': True, 'language': None}
        
        with patch.object(embed_script, 'validate_mkvmerge') as mock_validate:
            mock_validate.return_value = (False, None, None)
            
            with self.assertRaises(FileNotFoundError):
                embed_script.build_mkvmerge_command('video.mkv', 'sub.srt', 'output.mkv', config)


class TestFileValidation(unittest.TestCase):
    """Test file pair validation logic."""
    
    @patch('os.access')
    @patch('pathlib.Path.exists')
    def test_validate_nonexistent_video(self, mock_exists, mock_access):
        """Test validation fails for nonexistent video file."""
        mock_exists.return_value = False
        
        success, error = embed_script.validate_file_pair('nonexistent.mkv', 'sub.srt')
        
        self.assertFalse(success)
        self.assertIn('Video file not found', error)
    
    @patch('os.access')
    @patch('pathlib.Path.exists')
    def test_validate_wrong_video_extension(self, mock_exists, mock_access):
        """Test validation fails for non-MKV video files."""
        mock_exists.return_value = True
        mock_access.return_value = True
        
        success, error = embed_script.validate_file_pair('video.avi', 'sub.srt')
        
        self.assertFalse(success)
        self.assertIn('must be .mkv format', error)
    
    @patch('os.access')
    @patch('pathlib.Path.exists')
    def test_validate_wrong_subtitle_extension(self, mock_exists, mock_access):
        """Test validation fails for invalid subtitle extensions."""
        mock_exists.return_value = True
        mock_access.return_value = True
        
        success, error = embed_script.validate_file_pair('video.mkv', 'sub.txt')
        
        self.assertFalse(success)
        self.assertIn('must be .srt, .ass, or .ssa format', error)
    
    @patch('os.access')
    @patch('pathlib.Path.exists')
    def test_validate_success(self, mock_exists, mock_access):
        """Test validation succeeds with valid files."""
        mock_exists.return_value = True
        mock_access.return_value = True
        
        success, error = embed_script.validate_file_pair('video.mkv', 'sub.srt')
        
        self.assertTrue(success)
        self.assertIsNone(error)


class TestIntegrationWithRealMkvmerge(unittest.TestCase):
    """Integration test with real mkvmerge and test files."""
    
    def setUp(self):
        """Set up test environment."""
        from pathlib import Path
        self.test_dir = Path(__file__).parent / 'tests'
        self.video_file = self.test_dir / 'demo.mkv'
        self.subtitle_file = self.test_dir / 'demo.ar.srt'
        self.output_file = self.test_dir / 'demo.embedded.mkv'
        
        # Clean up any previous test output
        if self.output_file.exists():
            self.output_file.unlink()
    
    def tearDown(self):
        """Clean up test files."""
        if self.output_file.exists():
            self.output_file.unlink()
    
    def test_real_mkvmerge_embedding(self):
        """Test actual subtitle embedding with real mkvmerge."""
        # Skip if mkvmerge not available
        config = embed_script.load_config()
        success, mkvmerge_path, version = embed_script.validate_mkvmerge(config.get('mkvmerge_path'))
        
        if not success:
            self.skipTest("mkvmerge not available for integration testing")
        
        # Verify test files exist
        self.assertTrue(self.video_file.exists(), f"Test video not found: {self.video_file}")
        self.assertTrue(self.subtitle_file.exists(), f"Test subtitle not found: {self.subtitle_file}")
        
        # Run embedding
        success, output_path, error = embed_script.embed_subtitle_pair(
            self.video_file,
            self.subtitle_file,
            config
        )
        
        # Verify success
        self.assertTrue(success, f"Embedding failed: {error}")
        self.assertIsNotNone(output_path, "Output path is None")
        self.assertTrue(output_path.exists(), f"Output file not created: {output_path}")
        
        # Verify output file has content
        self.assertGreater(output_path.stat().st_size, 0, "Output file is empty")
        
        # Verify subtitle track using mkvmerge --identify
        identify_command = [str(mkvmerge_path), '--identify', str(output_path)]
        result = subprocess.run(identify_command, capture_output=True, text=True, timeout=30)
        
        self.assertEqual(result.returncode, 0, "mkvmerge --identify failed")
        
        # Check for subtitle track in output
        output_text = result.stdout
        self.assertIn('subtitles', output_text.lower(), "No subtitle track found in output")
        
        print(f"\n[Integration Test] Successfully created: {output_path}")
        print(f"[Integration Test] File size: {output_path.stat().st_size} bytes")
        print(f"[Integration Test] mkvmerge identify output:\n{output_text}")


class TestOperationSummary(unittest.TestCase):
    """Test operation summary display functionality"""
    
    @patch('builtins.print')
    def test_print_operation_summary_all_success(self, mock_print):
        """Test summary with all successful operations"""
        results = [
            {
                'video': Path('video1.mkv'),
                'subtitle': Path('sub1.srt'),
                'success': True,
                'output': Path('video1.embedded.mkv'),
                'error': None
            },
            {
                'video': Path('video2.mkv'),
                'subtitle': Path('sub2.srt'),
                'success': True,
                'output': Path('video2.embedded.mkv'),
                'error': None
            }
        ]
        
        embed_script.print_operation_summary(results)
        
        # Verify summary was printed
        call_args = [str(call) for call in mock_print.call_args_list]
        output_text = ' '.join(call_args)
        
        self.assertIn('Total Processed: 2', output_text)
        self.assertIn('Successful: 2', output_text)
        self.assertIn('Failed: 0', output_text)
    
    @patch('builtins.print')
    def test_print_operation_summary_with_failures(self, mock_print):
        """Test summary with mixed success and failures"""
        results = [
            {
                'video': Path('video1.mkv'),
                'subtitle': Path('sub1.srt'),
                'success': True,
                'output': Path('video1.embedded.mkv'),
                'error': None
            },
            {
                'video': Path('video2.mkv'),
                'subtitle': Path('sub2.srt'),
                'success': False,
                'output': None,
                'error': 'File not found'
            },
            {
                'video': Path('video3.mkv'),
                'subtitle': Path('sub3.ass'),
                'success': False,
                'output': None,
                'error': 'Permission denied'
            }
        ]
        
        embed_script.print_operation_summary(results)
        
        # Verify summary was printed
        call_args = [str(call) for call in mock_print.call_args_list]
        output_text = ' '.join(call_args)
        
        self.assertIn('Total Processed: 3', output_text)
        self.assertIn('Successful: 1', output_text)
        self.assertIn('Failed: 2', output_text)
        self.assertIn('FAILURES:', output_text)
        self.assertIn('video2.mkv', output_text)
        self.assertIn('File not found', output_text)
        self.assertIn('video3.mkv', output_text)
        self.assertIn('Permission denied', output_text)
    
    @patch('builtins.print')
    def test_print_operation_summary_all_failures(self, mock_print):
        """Test summary with all operations failed"""
        results = [
            {
                'video': Path('video1.mkv'),
                'subtitle': Path('sub1.srt'),
                'success': False,
                'output': None,
                'error': 'mkvmerge execution failed'
            }
        ]
        
        embed_script.print_operation_summary(results)
        
        # Verify failure details
        call_args = [str(call) for call in mock_print.call_args_list]
        output_text = ' '.join(call_args)
        
        self.assertIn('Total Processed: 1', output_text)
        self.assertIn('Successful: 0', output_text)
        self.assertIn('Failed: 1', output_text)


class TestExitCodeDetermination(unittest.TestCase):
    """Test exit code determination logic"""
    
    def test_determine_exit_code_all_success(self):
        """Test exit code when all operations succeed"""
        results = [
            {'success': True},
            {'success': True}
        ]
        
        code = embed_script.determine_exit_code(results)
        self.assertEqual(code, embed_script.EXIT_SUCCESS)
    
    def test_determine_exit_code_partial_failure(self):
        """Test exit code when some operations fail"""
        results = [
            {'success': True},
            {'success': False},
            {'success': True}
        ]
        
        code = embed_script.determine_exit_code(results)
        self.assertEqual(code, embed_script.EXIT_PARTIAL_FAILURE)
    
    def test_determine_exit_code_complete_failure(self):
        """Test exit code when all operations fail"""
        results = [
            {'success': False},
            {'success': False}
        ]
        
        code = embed_script.determine_exit_code(results)
        self.assertEqual(code, embed_script.EXIT_COMPLETE_FAILURE)
    
    def test_determine_exit_code_no_results(self):
        """Test exit code when no files were processed"""
        results = []
        
        code = embed_script.determine_exit_code(results)
        self.assertEqual(code, embed_script.EXIT_SUCCESS)
    
    def test_determine_exit_code_mkvmerge_invalid(self):
        """Test exit code when mkvmerge validation failed"""
        results = []
        
        code = embed_script.determine_exit_code(results, mkvmerge_valid=False)
        self.assertEqual(code, embed_script.EXIT_FATAL_ERROR)


class TestMainBatchProcessing(unittest.TestCase):
    """Test main function batch processing logic"""
    
    @patch('embed_subtitles_to_match_videos_ar.parse_arguments')
    @patch('embed_subtitles_to_match_videos_ar.load_config')
    @patch('embed_subtitles_to_match_videos_ar.validate_mkvmerge')
    @patch('embed_subtitles_to_match_videos_ar.find_matching_files')
    @patch('embed_subtitles_to_match_videos_ar.embed_subtitle_pair')
    @patch('embed_subtitles_to_match_videos_ar.print_operation_summary')
    @patch('builtins.print')
    def test_main_batch_partial_failure(self, mock_print, mock_summary, mock_embed,
                                        mock_find, mock_validate, mock_config, mock_args):
        """Test main function with batch processing and partial failures"""
        # Setup mocks
        mock_args.return_value = MagicMock(directory='.', test_mkvmerge=False)
        mock_config.return_value = {'mkvmerge_path': None}
        mock_validate.return_value = (True, Path('/usr/bin/mkvmerge'), 'mkvmerge v1.0.0')
        
        # Mock file pairs
        video1 = Path('video1.mkv')
        sub1 = Path('sub1.srt')
        video2 = Path('video2.mkv')
        sub2 = Path('sub2.srt')
        mock_find.return_value = [(video1, sub1), (video2, sub2)]
        
        # Mock embed results: first succeeds, second fails
        mock_embed.side_effect = [
            (True, Path('video1.embedded.mkv'), None),
            (False, None, 'Permission denied')
        ]
        
        # Run main
        with patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.is_dir', return_value=True), \
             patch('pathlib.Path.resolve', return_value=Path('.')):
            exit_code = embed_script.main()
        
        # Verify exit code is PARTIAL_FAILURE
        self.assertEqual(exit_code, embed_script.EXIT_PARTIAL_FAILURE)
        
        # Verify embed was called twice
        self.assertEqual(mock_embed.call_count, 2)
        
        # Verify summary was called
        mock_summary.assert_called_once()
    
    @patch('embed_subtitles_to_match_videos_ar.parse_arguments')
    @patch('embed_subtitles_to_match_videos_ar.load_config')
    @patch('embed_subtitles_to_match_videos_ar.validate_mkvmerge')
    @patch('builtins.print')
    def test_main_mkvmerge_not_found(self, mock_print, mock_validate, mock_config, mock_args):
        """Test main function when mkvmerge is not found"""
        # Setup mocks
        mock_args.return_value = MagicMock(directory='.', test_mkvmerge=False)
        mock_config.return_value = {'mkvmerge_path': None}
        mock_validate.return_value = (False, None, None)
        
        # Run main
        exit_code = embed_script.main()
        
        # Verify exit code is FATAL_ERROR
        self.assertEqual(exit_code, embed_script.EXIT_FATAL_ERROR)
    
    @patch('embed_subtitles_to_match_videos_ar.parse_arguments')
    @patch('embed_subtitles_to_match_videos_ar.load_config')
    @patch('embed_subtitles_to_match_videos_ar.validate_mkvmerge')
    @patch('embed_subtitles_to_match_videos_ar.find_matching_files')
    @patch('builtins.print')
    def test_main_no_matching_files(self, mock_print, mock_find, mock_validate, mock_config, mock_args):
        """Test main function when no matching files are found"""
        # Setup mocks
        mock_args.return_value = MagicMock(directory='.', test_mkvmerge=False)
        mock_config.return_value = {'mkvmerge_path': None}
        mock_validate.return_value = (True, Path('/usr/bin/mkvmerge'), 'mkvmerge v1.0.0')
        mock_find.return_value = []  # No files found
        
        # Run main
        with patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.is_dir', return_value=True), \
             patch('pathlib.Path.resolve', return_value=Path('.')):
            exit_code = embed_script.main()
        
        # Verify exit code is SUCCESS (no files to process is not an error)
        self.assertEqual(exit_code, embed_script.EXIT_SUCCESS)


class TestBatchProcessingIntegration(unittest.TestCase):
    """Integration test for batch processing with multiple real files"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = Path(__file__).parent / 'tests'
        self.config = embed_script.load_config()
        
        # Skip if mkvmerge not available
        success, self.mkvmerge_path, version = embed_script.validate_mkvmerge(
            self.config.get('mkvmerge_path')
        )
        if not success:
            self.skipTest("mkvmerge not available for integration testing")
        
        print(f"\n[Batch Integration Test] Using {version}")
        print(f"[Batch Integration Test] Test directory: {self.test_dir}")
    
    def tearDown(self):
        """Keep embedded files for verification (will be overwritten on next run)"""
        print(f"\n[Test Files Preserved] Output files kept in: {self.test_dir}")
        print(f"[Test Files Preserved] Re-running test will overwrite existing .embedded.mkv files")
    
    def test_batch_processing_with_multiple_files(self):
        """Test batch processing with multiple file pairs (some succeed, some fail)"""
        print("\n" + "="*80)
        print("BATCH PROCESSING INTEGRATION TEST")
        print("="*80)
        
        # Test both subdirectories: episodes and movies
        episodes_dir = self.test_dir / 'episodes'
        movie_dir = self.test_dir / 'movie'
        
        print(f"\n[Test Setup] Using find_matching_files() to auto-discover pairs...")
        print(f"[Test Setup] Testing episodes directory: {episodes_dir}")
        episodes_pairs = embed_script.find_matching_files(str(episodes_dir)) if episodes_dir.exists() else []
        
        print(f"[Test Setup] Testing movie directory: {movie_dir}")
        movie_pairs = embed_script.find_matching_files(str(movie_dir)) if movie_dir.exists() else []
        
        # Combine all pairs
        file_pairs = episodes_pairs + movie_pairs
        
        print(f"[Test Setup] Found {len(episodes_pairs)} episode pair(s), {len(movie_pairs)} movie pair(s)")
        
        # Verify we found matching pairs
        self.assertGreater(len(file_pairs), 0, "No matching file pairs found by find_matching_files()")
        
        print(f"\n[Test] Processing {len(file_pairs)} file pair(s)...")
        
        # Process each pair using embed_subtitle_pair
        results = []
        for idx, (video_file, subtitle_file) in enumerate(file_pairs, 1):
            print(f"\n[{idx}/{len(file_pairs)}] Processing: {video_file.name}")
            print(f"           Subtitle: {subtitle_file.name}")
            
            success, output_file, error_message = embed_script.embed_subtitle_pair(
                video_file,
                subtitle_file,
                self.config
            )
            
            results.append({
                'video': video_file,
                'subtitle': subtitle_file,
                'success': success,
                'output': output_file,
                'error': error_message
            })
            
            if success:
                print(f"  [OK] Success: {output_file.name}")
                # Verify output file exists
                self.assertTrue(output_file.exists(), f"Output file not created: {output_file}")
                self.assertGreater(output_file.stat().st_size, 0, "Output file is empty")
            else:
                print(f"  [FAIL] Failed: {error_message}")
        
        # Test operation summary display
        print("\n[Test] Displaying operation summary...")
        embed_script.print_operation_summary(results)
        
        # Test exit code determination
        exit_code = embed_script.determine_exit_code(results, mkvmerge_valid=True)
        print(f"\n[Test] Exit code: {exit_code}")
        
        # Verify results
        successful_count = sum(1 for r in results if r['success'])
        failed_count = len(results) - successful_count
        
        print(f"\n[Test Results]")
        print(f"  Total processed: {len(results)}")
        print(f"  Successful: {successful_count}")
        print(f"  Failed: {failed_count}")
        
        # Assertions
        self.assertGreater(len(results), 0, "No results recorded")
        
        # Verify exit code logic
        if failed_count == 0:
            self.assertEqual(exit_code, embed_script.EXIT_SUCCESS, 
                           "Exit code should be EXIT_SUCCESS when all operations succeed")
        elif successful_count == 0:
            self.assertEqual(exit_code, embed_script.EXIT_COMPLETE_FAILURE,
                           "Exit code should be EXIT_COMPLETE_FAILURE when all operations fail")
        else:
            self.assertEqual(exit_code, embed_script.EXIT_PARTIAL_FAILURE,
                           "Exit code should be EXIT_PARTIAL_FAILURE when some operations fail")
        
        # Verify at least one successful embedding
        self.assertGreater(successful_count, 0, 
                          "At least one file pair should embed successfully")
        
        # Verify embedded files have subtitle tracks
        for result in results:
            if result['success']:
                output_path = result['output']
                # Use mkvmerge --identify to verify subtitle track
                identify_cmd = [str(self.mkvmerge_path), '--identify', str(output_path)]
                identify_result = subprocess.run(identify_cmd, capture_output=True, text=True, timeout=30)
                
                self.assertEqual(identify_result.returncode, 0, 
                               f"mkvmerge --identify failed for {output_path.name}")
                self.assertIn('subtitles', identify_result.stdout.lower(),
                            f"No subtitle track found in {output_path.name}")
                
                print(f"[Verified] {output_path.name} - Subtitle track present")
        
        print("\n" + "="*80)
        print("BATCH PROCESSING INTEGRATION TEST: PASSED")
        print("="*80)
        
        # Export test summary as CSV
        from datetime import datetime
        summary_file = self.test_dir / 'integration_test_summary.csv'
        with open(summary_file, 'w', encoding='utf-8', newline='') as f:
            import csv
            
            # Write metadata header
            f.write(f"# Integration Test Summary\n")
            f.write(f"# Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Test Directory: {self.test_dir}\n")
            
            # Get mkvmerge version
            success, mkvmerge_path, version = embed_script.validate_mkvmerge(
                self.config.get('mkvmerge_path')
            )
            f.write(f"# mkvmerge Version: {version}\n")
            f.write(f"# Total Processed: {len(results)}\n")
            f.write(f"# Successful: {successful_count}\n")
            f.write(f"# Failed: {failed_count}\n")
            f.write(f"# Exit Code: {exit_code}\n")
            f.write("#\n")
            
            # CSV headers and data
            writer = csv.writer(f)
            writer.writerow(['Index', 'Video File', 'Subtitle File', 'Status', 'Output File', 'File Size (bytes)', 'Subtitle Track', 'Error Message'])
            
            for idx, result in enumerate(results, 1):
                if result['success']:
                    writer.writerow([
                        idx,
                        result['video'].name,
                        result['subtitle'].name,
                        'SUCCESS',
                        result['output'].name,
                        result['output'].stat().st_size,
                        'Verified Present',
                        ''
                    ])
                else:
                    writer.writerow([
                        idx,
                        result['video'].name,
                        result['subtitle'].name,
                        'FAILED',
                        '',
                        '',
                        '',
                        result['error']
                    ])
        
        print(f"\n[Test Summary Exported] {summary_file}")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
