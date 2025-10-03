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


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
