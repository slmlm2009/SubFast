#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit Tests for Story 2.2: Backup and Output File Management

Tests the backup workflow functions for the subtitle embedding tool.
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import functions from embed script
from embed_subtitles_to_match_videos_ar import (
    has_sufficient_space,
    ensure_backups_directory,
    backup_originals,
    safe_delete_subtitle,
    rename_embedded_to_final,
    cleanup_failed_merge
)


class TestDiskSpaceChecking(unittest.TestCase):
    """Test disk space checking functionality"""
    
    def setUp(self):
        """Create temporary test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.video_file = self.test_dir / "test_video.mkv"
        self.subtitle_file = self.test_dir / "test_subtitle.srt"
        
        # Create test files with known sizes
        self.video_file.write_bytes(b'V' * (100 * 1024 * 1024))  # 100 MB
        self.subtitle_file.write_bytes(b'S' * (1 * 1024 * 1024))  # 1 MB
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)
    
    def test_disk_space_check_sufficient(self):
        """Test that check passes with sufficient disk space"""
        # Most systems will have sufficient space for test
        result = has_sufficient_space(self.video_file, self.subtitle_file)
        self.assertTrue(result, "Should have sufficient space for small test files")
    
    @patch('shutil.disk_usage')
    def test_disk_space_check_insufficient(self, mock_disk_usage):
        """Test that check fails with insufficient disk space"""
        # Mock disk usage to return insufficient space
        mock_usage = MagicMock()
        mock_usage.free = 1024  # Only 1 KB free
        mock_disk_usage.return_value = mock_usage
        
        result = has_sufficient_space(self.video_file, self.subtitle_file)
        self.assertFalse(result, "Should fail with insufficient disk space")


class TestBackupsDirectoryManagement(unittest.TestCase):
    """Test backups directory creation"""
    
    def setUp(self):
        """Create temporary test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)
    
    def test_ensure_backups_directory_new(self):
        """Test that backups directory is created when it doesn't exist"""
        backups_dir = ensure_backups_directory(self.test_dir)
        
        self.assertTrue(backups_dir.exists(), "Backups directory should be created")
        self.assertTrue(backups_dir.is_dir(), "Backups path should be a directory")
        self.assertEqual(backups_dir.name, "backups", "Directory should be named 'backups'")
    
    def test_ensure_backups_directory_exists(self):
        """Test that function handles existing backups directory"""
        # Create backups directory first
        backups_dir = self.test_dir / "backups"
        backups_dir.mkdir()
        
        # Call function
        result_dir = ensure_backups_directory(self.test_dir)
        
        self.assertEqual(result_dir, backups_dir, "Should return existing backups directory")
        self.assertTrue(result_dir.exists(), "Backups directory should still exist")


class TestIntelligentBackupLogic(unittest.TestCase):
    """Test intelligent backup collision handling"""
    
    def setUp(self):
        """Create temporary test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.backups_dir = self.test_dir / "backups"
        self.backups_dir.mkdir()
        
        self.video_file = self.test_dir / "test_video.mkv"
        self.subtitle_file = self.test_dir / "test_subtitle.srt"
        
        self.video_file.write_text("video content")
        self.subtitle_file.write_text("subtitle content")
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)
    
    def test_backup_originals_both_new(self):
        """Test that both files are backed up when neither exists in backups"""
        video_backed_up, subtitle_backed_up = backup_originals(
            self.video_file, self.subtitle_file, self.backups_dir
        )
        
        self.assertTrue(video_backed_up, "Video should be backed up")
        self.assertTrue(subtitle_backed_up, "Subtitle should be backed up")
        
        # Verify files moved to backups
        self.assertTrue((self.backups_dir / "test_video.mkv").exists())
        self.assertTrue((self.backups_dir / "test_subtitle.srt").exists())
        
        # Verify files removed from working dir
        self.assertFalse(self.video_file.exists())
        self.assertFalse(self.subtitle_file.exists())
    
    def test_backup_originals_video_exists(self):
        """Test that only subtitle is backed up when video already in backups"""
        # Pre-create video backup
        video_backup = self.backups_dir / "test_video.mkv"
        video_backup.write_text("existing video backup")
        
        video_backed_up, subtitle_backed_up = backup_originals(
            self.video_file, self.subtitle_file, self.backups_dir
        )
        
        self.assertFalse(video_backed_up, "Video should NOT be backed up (already exists)")
        self.assertTrue(subtitle_backed_up, "Subtitle should be backed up")
        
        # Verify video still in working dir (not moved)
        self.assertTrue(self.video_file.exists(), "Video should remain in working dir")
        
        # Verify subtitle moved
        self.assertTrue((self.backups_dir / "test_subtitle.srt").exists())
        self.assertFalse(self.subtitle_file.exists())
    
    def test_backup_originals_subtitle_exists(self):
        """Test that only video is backed up when subtitle already in backups"""
        # Pre-create subtitle backup
        subtitle_backup = self.backups_dir / "test_subtitle.srt"
        subtitle_backup.write_text("existing subtitle backup")
        
        video_backed_up, subtitle_backed_up = backup_originals(
            self.video_file, self.subtitle_file, self.backups_dir
        )
        
        self.assertTrue(video_backed_up, "Video should be backed up")
        self.assertFalse(subtitle_backed_up, "Subtitle should NOT be backed up (already exists)")
        
        # Verify video moved
        self.assertTrue((self.backups_dir / "test_video.mkv").exists())
        self.assertFalse(self.video_file.exists())
        
        # Verify subtitle still in working dir (not moved)
        self.assertTrue(self.subtitle_file.exists(), "Subtitle should remain in working dir")
    
    def test_backup_originals_both_exist(self):
        """Test that neither file is backed up when both already in backups"""
        # Pre-create both backups
        video_backup = self.backups_dir / "test_video.mkv"
        subtitle_backup = self.backups_dir / "test_subtitle.srt"
        video_backup.write_text("existing video backup")
        subtitle_backup.write_text("existing subtitle backup")
        
        video_backed_up, subtitle_backed_up = backup_originals(
            self.video_file, self.subtitle_file, self.backups_dir
        )
        
        self.assertFalse(video_backed_up, "Video should NOT be backed up (already exists)")
        self.assertFalse(subtitle_backed_up, "Subtitle should NOT be backed up (already exists)")
        
        # Verify both still in working dir (not moved)
        self.assertTrue(self.video_file.exists(), "Video should remain in working dir")
        self.assertTrue(self.subtitle_file.exists(), "Subtitle should remain in working dir")


class TestSafeSubtitleDeletion(unittest.TestCase):
    """Test safe subtitle deletion with backup verification"""
    
    def setUp(self):
        """Create temporary test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.backups_dir = self.test_dir / "backups"
        self.backups_dir.mkdir()
        
        self.subtitle_file = self.test_dir / "test_subtitle.srt"
        self.subtitle_file.write_text("subtitle content")
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)
    
    def test_safe_delete_subtitle_in_backups(self):
        """Test that subtitle is deleted when confirmed in backups"""
        # Create backup
        subtitle_backup = self.backups_dir / "test_subtitle.srt"
        subtitle_backup.write_text("subtitle backup")
        
        # Delete safely
        safe_delete_subtitle(self.subtitle_file, self.backups_dir)
        
        # Verify subtitle deleted from working dir
        self.assertFalse(self.subtitle_file.exists(), "Subtitle should be deleted")
        
        # Verify backup still exists
        self.assertTrue(subtitle_backup.exists(), "Backup should remain")
    
    def test_safe_delete_subtitle_not_in_backups(self):
        """Test that subtitle is kept when not in backups"""
        # No backup exists
        
        # Attempt safe delete
        safe_delete_subtitle(self.subtitle_file, self.backups_dir)
        
        # Verify subtitle still in working dir (safety check prevented deletion)
        self.assertTrue(self.subtitle_file.exists(), "Subtitle should be kept (not in backups)")


class TestFileRenamingAndCleanup(unittest.TestCase):
    """Test file renaming and cleanup functions"""
    
    def setUp(self):
        """Create temporary test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.embedded_file = self.test_dir / "test.embedded.mkv"
        self.final_file = self.test_dir / "test.mkv"
        
        self.embedded_file.write_text("embedded content")
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)
    
    def test_rename_embedded_to_final(self):
        """Test renaming .embedded.mkv to final name"""
        rename_embedded_to_final(self.embedded_file, self.final_file)
        
        # Verify embedded file gone
        self.assertFalse(self.embedded_file.exists(), "Embedded file should be renamed")
        
        # Verify final file exists
        self.assertTrue(self.final_file.exists(), "Final file should exist")
        self.assertEqual(self.final_file.read_text(), "embedded content")
    
    def test_cleanup_failed_merge(self):
        """Test cleanup of temporary .embedded.mkv file"""
        cleanup_failed_merge(self.embedded_file)
        
        # Verify temp file deleted
        self.assertFalse(self.embedded_file.exists(), "Temp file should be deleted")
    
    def test_cleanup_failed_merge_nonexistent(self):
        """Test cleanup handles non-existent file gracefully"""
        nonexistent = self.test_dir / "nonexistent.embedded.mkv"
        
        # Should not raise exception
        try:
            cleanup_failed_merge(nonexistent)
        except Exception as e:
            self.fail(f"Cleanup should handle non-existent file: {e}")


if __name__ == '__main__':
    unittest.main(verbosity=2)
