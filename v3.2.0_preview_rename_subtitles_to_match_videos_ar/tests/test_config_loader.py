"""
Test Suite for config_loader module

Tests configuration loading, generation, validation, and fallback behavior.
"""

import unittest
from pathlib import Path
from subfast.scripts.common import config_loader
from tests.test_helpers import SubFastTestCase, create_sample_config


class TestConfigGeneration(SubFastTestCase):
    """Test default configuration file generation."""
    
    def test_default_config_creation(self):
        """Test that default configuration file is created correctly."""
        config_path = self.temp_dir / 'config.ini'
        
        # Create default config
        config_loader.create_default_config_file(config_path)
        
        # Verify file exists
        self.assertFileExists(config_path, "Config file should be created")
        
        # Verify file is not empty
        content = config_path.read_text()
        self.assertTrue(len(content) > 100, "Config file should have substantial content")
        
        # Verify it contains expected sections
        self.assertIn('[General]', content)
        self.assertIn('[Renaming]', content)
        self.assertIn('[Embedding]', content)
    
    def test_default_config_has_all_keys(self):
        """Test that generated config includes all required keys."""
        config_path = self.temp_dir / 'config.ini'
        config_loader.create_default_config_file(config_path)
        
        # Read generated config
        content = config_path.read_text()
        
        # Check for essential configuration keys
        self.assertIn('detected_video_extensions', content)
        self.assertIn('detected_subtitle_extensions', content)
        self.assertIn('keep_console_open', content)
        self.assertIn('renaming_report', content)
        self.assertIn('mkvmerge_path', content)
        self.assertIn('embedding_language_code', content)
        self.assertIn('default_flag', content)


class TestConfigLoading(SubFastTestCase):
    """Test configuration file loading and parsing."""
    
    def test_load_valid_config(self):
        """Test loading a valid configuration file."""
        config_path = self.temp_dir / 'config.ini'
        config_loader.create_default_config_file(config_path)
        
        # Load the config
        config = config_loader.load_config(config_path)
        
        # Verify config is a dictionary
        self.assertIsInstance(config, dict, "Loaded config should be a dictionary")
        
        # Verify contains expected keys from DEFAULT_CONFIG
        self.assertIn('video_extensions', config)
        self.assertIn('subtitle_extensions', config)
        self.assertIn('renaming_report', config)
    
    def test_load_missing_config_uses_defaults(self):
        """Test that missing config file falls back to defaults."""
        non_existent_path = self.temp_dir / 'does_not_exist.ini'
        
        # Load config from non-existent file
        config = config_loader.load_config(non_existent_path)
        
        # Should still return a valid config (defaults)
        self.assertIsInstance(config, dict)
        self.assertIn('video_extensions', config)
        
        # Should match DEFAULT_CONFIG values
        self.assertEqual(config['video_extensions'], config_loader.DEFAULT_CONFIG['video_extensions'])


class TestExtensionParsing(SubFastTestCase):
    """Test file extension parsing functionality."""
    
    def test_parse_extensions_basic(self):
        """Test parsing basic comma-separated extensions."""
        result = config_loader.parse_extensions('mkv, mp4, avi')
        
        self.assertEqual(result, ['mkv', 'mp4', 'avi'])
    
    def test_parse_extensions_with_dots(self):
        """Test that leading dots are stripped from extensions."""
        result = config_loader.parse_extensions('.mkv, .mp4, .avi')
        
        self.assertEqual(result, ['mkv', 'mp4', 'avi'])
    
    def test_parse_extensions_mixed_case(self):
        """Test that extensions are converted to lowercase."""
        result = config_loader.parse_extensions('MKV, Mp4, AVI')
        
        self.assertEqual(result, ['mkv', 'mp4', 'avi'])
    
    def test_parse_extensions_empty_string(self):
        """Test parsing empty extension string returns empty list."""
        result = config_loader.parse_extensions('')
        
        self.assertEqual(result, [])
    
    def test_parse_extensions_with_whitespace(self):
        """Test that extra whitespace is handled correctly."""
        result = config_loader.parse_extensions('  mkv  ,  mp4  ,  avi  ')
        
        self.assertEqual(result, ['mkv', 'mp4', 'avi'])


class TestBooleanParsing(SubFastTestCase):
    """Test boolean value parsing with fallback."""
    
    def test_parse_boolean_true_values(self):
        """Test that 'true' and '1' are parsed as True."""
        self.assertTrue(config_loader.parse_boolean('true'))
        self.assertTrue(config_loader.parse_boolean('True'))
        self.assertTrue(config_loader.parse_boolean('TRUE'))
        self.assertTrue(config_loader.parse_boolean('1'))
    
    def test_parse_boolean_false_values(self):
        """Test that 'false' and '0' are parsed as False."""
        self.assertFalse(config_loader.parse_boolean('false'))
        self.assertFalse(config_loader.parse_boolean('False'))
        self.assertFalse(config_loader.parse_boolean('FALSE'))
        self.assertFalse(config_loader.parse_boolean('0'))
    
    def test_parse_boolean_invalid_falls_back_to_default(self):
        """Test that invalid boolean values fall back to default."""
        # Invalid values should use the default (True in this case)
        result = config_loader.parse_boolean('maybe', default=True)
        self.assertTrue(result)
        
        # 'maybe' with False default should return False
        result = config_loader.parse_boolean('maybe', default=False)
        self.assertFalse(result)
        
        # Empty string should use default
        result = config_loader.parse_boolean('', default=True)
        self.assertTrue(result)


class TestConfigValidation(SubFastTestCase):
    """Test configuration validation and error handling."""
    
    def test_empty_extension_lists_handled(self):
        """Test that empty extension lists don't cause errors."""
        result = config_loader.parse_extensions('')
        self.assertEqual(result, [])
    
    def test_invalid_characters_in_extensions_filtered(self):
        """Test that extensions with invalid characters are filtered out."""
        # This test assumes parse_extensions filters invalid extensions
        result = config_loader.parse_extensions('mkv, mp4, @#$')
        
        # Should only include valid extensions
        self.assertIn('mkv', result)
        self.assertIn('mp4', result)
        # Invalid extension should be filtered
        self.assertNotIn('@#$', result)


if __name__ == '__main__':
    unittest.main()
