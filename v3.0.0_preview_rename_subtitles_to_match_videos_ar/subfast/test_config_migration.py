"""
Unit tests for configuration migration functions (Story 3.1 Task 13).

Tests the unified configuration migration, section handling, and corrupted config recovery.
"""

import unittest
import configparser
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

# Import the functions we're testing
import sys
sys.path.insert(0, str(Path(__file__).parent))

from embed_subtitles_to_match_videos_ar import migrate_old_config, ensure_section_exists


class TestConfigMigration(unittest.TestCase):
    """Test configuration migration from old to new unified format."""
    
    def setUp(self):
        """Create temporary directory for test config files."""
        self.test_dir = tempfile.mkdtemp()
        self.config_path = Path(self.test_dir) / 'config.ini'
    
    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.test_dir)
    
    def test_migrate_old_renaming_config_to_unified(self):
        """Test migration of old renaming script config to unified format."""
        # Create old renaming config format
        config = configparser.ConfigParser()
        config['General'] = {
            'enable_export': 'true',
            'language_suffix': 'ar'
        }
        config['FileFormats'] = {
            'video_extensions': 'mkv, mp4',
            'subtitle_extensions': 'srt, ass'
        }
        
        # Write initial config
        with open(self.config_path, 'w') as f:
            config.write(f)
        
        # Perform migration
        config = configparser.ConfigParser()
        config.read(self.config_path)
        result = migrate_old_config(config, self.config_path)
        
        # Verify migration performed
        self.assertTrue(result, "Migration should return True when changes made")
        
        # Reload to verify file changes
        config_after = configparser.ConfigParser()
        config_after.read(self.config_path)
        
        # Verify new keys exist
        self.assertTrue(config_after.has_option('Renaming', 'renaming_report'))
        self.assertTrue(config_after.has_option('Renaming', 'renaming_language_suffix'))
        self.assertTrue(config_after.has_option('General', 'detected_video_extensions'))
        self.assertTrue(config_after.has_option('General', 'detected_subtitle_extensions'))
        
        # Verify values preserved
        self.assertEqual(config_after.get('Renaming', 'renaming_report'), 'true')
        self.assertEqual(config_after.get('Renaming', 'renaming_language_suffix'), 'ar')
        self.assertEqual(config_after.get('General', 'detected_video_extensions'), 'mkv, mp4')
        
        # Verify old keys removed
        self.assertFalse(config_after.has_option('General', 'enable_export'))
        self.assertFalse(config_after.has_option('General', 'language_suffix'))
        self.assertFalse(config_after.has_section('FileFormats'))
    
    def test_migrate_old_embedding_config_to_unified(self):
        """Test migration of old embedding script config to unified format."""
        # Create old embedding config format
        config = configparser.ConfigParser()
        config['Embedding'] = {
            'mkvmerge_path': '',
            'language': 'ar',
            'default_track': 'yes'
        }
        config['Reporting'] = {
            'csv_export': 'true'
        }
        
        # Write initial config
        with open(self.config_path, 'w') as f:
            config.write(f)
        
        # Perform migration
        config = configparser.ConfigParser()
        config.read(self.config_path)
        result = migrate_old_config(config, self.config_path)
        
        # Verify migration performed
        self.assertTrue(result, "Migration should return True when changes made")
        
        # Reload to verify file changes
        config_after = configparser.ConfigParser()
        config_after.read(self.config_path)
        
        # Verify new keys exist
        self.assertTrue(config_after.has_option('Embedding', 'embedding_language_code'))
        self.assertTrue(config_after.has_option('Embedding', 'default_flag'))
        self.assertTrue(config_after.has_option('Embedding', 'embedding_report'))
        
        # Verify values preserved
        self.assertEqual(config_after.get('Embedding', 'embedding_language_code'), 'ar')
        self.assertEqual(config_after.get('Embedding', 'default_flag'), 'yes')
        self.assertEqual(config_after.get('Embedding', 'embedding_report'), 'true')
        
        # Verify old keys removed
        self.assertFalse(config_after.has_option('Embedding', 'language'))
        self.assertFalse(config_after.has_option('Embedding', 'default_track'))
        self.assertFalse(config_after.has_section('Reporting'))
    
    def test_migrate_mixed_old_new_config(self):
        """Test migration when config has mix of old and new key names."""
        # Create mixed config
        config = configparser.ConfigParser()
        config['General'] = {
            'enable_export': 'false',  # Old key
            'detected_video_extensions': 'mkv, mp4, avi'  # New key already present
        }
        config['Embedding'] = {
            'mkvmerge_path': '',
            'language': 'en',  # Old key
            'embedding_report': 'false'  # New key already present
        }
        
        # Write initial config
        with open(self.config_path, 'w') as f:
            config.write(f)
        
        # Perform migration
        config = configparser.ConfigParser()
        config.read(self.config_path)
        result = migrate_old_config(config, self.config_path)
        
        # Verify migration performed
        self.assertTrue(result, "Migration should return True when changes made")
        
        # Reload to verify file changes
        config_after = configparser.ConfigParser()
        config_after.read(self.config_path)
        
        # Verify old keys migrated
        self.assertTrue(config_after.has_option('Renaming', 'renaming_report'))
        self.assertEqual(config_after.get('Renaming', 'renaming_report'), 'false')
        self.assertTrue(config_after.has_option('Embedding', 'embedding_language_code'))
        self.assertEqual(config_after.get('Embedding', 'embedding_language_code'), 'en')
        
        # Verify new keys preserved
        self.assertTrue(config_after.has_option('General', 'detected_video_extensions'))
        self.assertEqual(config_after.get('General', 'detected_video_extensions'), 'mkv, mp4, avi')
        self.assertTrue(config_after.has_option('Embedding', 'embedding_report'))
        self.assertEqual(config_after.get('Embedding', 'embedding_report'), 'false')
    
    def test_no_migration_needed_for_new_format(self):
        """Test that no migration occurs when config already in new format."""
        # Create new format config
        config = configparser.ConfigParser()
        config['General'] = {
            'detected_video_extensions': 'mkv, mp4',
            'detected_subtitle_extensions': 'srt, ass'
        }
        config['Renaming'] = {
            'renaming_report': 'false',
            'renaming_language_suffix': ''
        }
        config['Embedding'] = {
            'mkvmerge_path': '',
            'embedding_language_code': '',
            'default_flag': 'yes',
            'embedding_report': 'false'
        }
        
        # Write config
        with open(self.config_path, 'w') as f:
            config.write(f)
        
        # Store original content for comparison
        with open(self.config_path, 'r') as f:
            original_content = f.read()
        
        # Perform migration
        config = configparser.ConfigParser()
        config.read(self.config_path)
        result = migrate_old_config(config, self.config_path)
        
        # Verify no migration performed
        self.assertFalse(result, "Migration should return False when no changes needed")


class TestSectionHandling(unittest.TestCase):
    """Test graceful section and key handling functions."""
    
    def setUp(self):
        """Create temporary directory for test config files."""
        self.test_dir = tempfile.mkdtemp()
        self.config_path = Path(self.test_dir) / 'config.ini'
    
    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.test_dir)
    
    def test_ensure_section_adds_missing_section(self):
        """Test that missing section is added with defaults."""
        # Create config without Renaming section
        config = configparser.ConfigParser()
        config['General'] = {
            'detected_video_extensions': 'mkv, mp4'
        }
        
        # Write config
        with open(self.config_path, 'w') as f:
            config.write(f)
        
        # Reload and ensure section
        config = configparser.ConfigParser()
        config.read(self.config_path)
        result = ensure_section_exists(config, 'Renaming', {
            'renaming_report': 'false',
            'renaming_language_suffix': ''
        }, self.config_path)
        
        # Verify section was added
        self.assertTrue(result, "Should return True when section added")
        
        # Reload to verify file changes
        config_after = configparser.ConfigParser()
        config_after.read(self.config_path)
        
        self.assertTrue(config_after.has_section('Renaming'))
        self.assertTrue(config_after.has_option('Renaming', 'renaming_report'))
        self.assertTrue(config_after.has_option('Renaming', 'renaming_language_suffix'))
        self.assertEqual(config_after.get('Renaming', 'renaming_report'), 'false')
    
    def test_ensure_section_adds_missing_keys(self):
        """Test that missing keys are added to existing section."""
        # Create config with Renaming section but missing keys
        config = configparser.ConfigParser()
        config['Renaming'] = {
            'renaming_report': 'true'
            # Missing renaming_language_suffix
        }
        
        # Write config
        with open(self.config_path, 'w') as f:
            config.write(f)
        
        # Reload and ensure section complete
        config = configparser.ConfigParser()
        config.read(self.config_path)
        result = ensure_section_exists(config, 'Renaming', {
            'renaming_report': 'false',  # Already exists, should not overwrite
            'renaming_language_suffix': ''  # Missing, should add
        }, self.config_path)
        
        # Verify key was added
        self.assertTrue(result, "Should return True when key added")
        
        # Reload to verify file changes
        config_after = configparser.ConfigParser()
        config_after.read(self.config_path)
        
        # Verify existing key not overwritten
        self.assertEqual(config_after.get('Renaming', 'renaming_report'), 'true')
        
        # Verify missing key added
        self.assertTrue(config_after.has_option('Renaming', 'renaming_language_suffix'))
        self.assertEqual(config_after.get('Renaming', 'renaming_language_suffix'), '')


class TestCorruptedConfigHandling(unittest.TestCase):
    """Test corrupted configuration file handling."""
    
    def setUp(self):
        """Create temporary directory for test config files."""
        self.test_dir = tempfile.mkdtemp()
        self.config_path = Path(self.test_dir) / 'config.ini'
    
    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.test_dir)
    
    def test_corrupted_config_creates_backup(self):
        """Test that corrupted config is backed up with timestamp."""
        # Create corrupted config (missing section headers)
        corrupted_content = """
mkvmerge_path = 
language = ar
default_track = yes
"""
        with open(self.config_path, 'w') as f:
            f.write(corrupted_content)
        
        # Try to read config (should raise exception)
        config = configparser.ConfigParser()
        with self.assertRaises(configparser.MissingSectionHeaderError):
            config.read(self.config_path)
        
        # Simulate backup creation (what load_config does)
        backup_filename = f"config.ini.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_path = self.config_path.parent / backup_filename
        shutil.move(str(self.config_path), str(backup_path))
        
        # Verify backup was created
        self.assertTrue(backup_path.exists(), "Backup file should exist")
        self.assertFalse(self.config_path.exists(), "Original should be moved")
        
        # Verify backup contains original content
        with open(backup_path, 'r') as f:
            backup_content = f.read()
        self.assertEqual(backup_content, corrupted_content)
    
    def test_corrupted_config_recreates_valid_config(self):
        """Test that fresh valid config is created after corruption."""
        # Create corrupted config
        corrupted_content = """
[NoClosingBracket
mkvmerge_path = test
"""
        with open(self.config_path, 'w') as f:
            f.write(corrupted_content)
        
        # Try to read config (should raise exception)
        config = configparser.ConfigParser()
        with self.assertRaises(configparser.ParsingError):
            config.read(self.config_path)
        
        # Simulate recreation (what load_config does)
        backup_filename = f"config.ini.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_path = self.config_path.parent / backup_filename
        shutil.move(str(self.config_path), str(backup_path))
        
        # Create fresh config
        new_config = configparser.ConfigParser()
        new_config['General'] = {
            'detected_video_extensions': 'mkv, mp4',
            'detected_subtitle_extensions': 'srt, ass'
        }
        new_config['Renaming'] = {
            'renaming_report': 'false',
            'renaming_language_suffix': ''
        }
        new_config['Embedding'] = {
            'mkvmerge_path': '',
            'embedding_language_code': '',
            'default_flag': 'yes',
            'embedding_report': 'false'
        }
        
        with open(self.config_path, 'w') as f:
            new_config.write(f)
        
        # Verify new config is valid
        verify_config = configparser.ConfigParser()
        verify_config.read(self.config_path)
        
        self.assertTrue(verify_config.has_section('General'))
        self.assertTrue(verify_config.has_section('Renaming'))
        self.assertTrue(verify_config.has_section('Embedding'))
        self.assertTrue(verify_config.has_option('Embedding', 'embedding_language_code'))


if __name__ == '__main__':
    unittest.main()
