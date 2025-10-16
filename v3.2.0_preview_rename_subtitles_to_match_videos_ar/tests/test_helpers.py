"""
Module: test_helpers.py
Purpose: Shared test utilities for SubFast test suite

Provides reusable utilities for test setup, teardown, assertions,
and file operations. Uses only Python stdlib (no external dependencies).
"""

import tempfile
import shutil
import unittest
from pathlib import Path
from typing import Optional

def create_temp_directory() -> Path:
    """
    Create a temporary directory for test use.
    
    Returns:
        Path: Path to the temporary directory
    
    Example:
        temp_dir = create_temp_directory()
        # Use temp_dir for test files
        cleanup_test_files(temp_dir)
    """
    temp_dir = Path(tempfile.mkdtemp(prefix='subfast_test_'))
    return temp_dir


def cleanup_test_files(path: Path) -> None:
    """
    Remove test artifacts and cleanup temporary files.
    
    Args:
        path: Path to directory or file to remove
    
    Example:
        cleanup_test_files(temp_dir)
    """
    if not path.exists():
        return
    
    try:
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=True)
        else:
            path.unlink(missing_ok=True)
    except Exception:
        # Ignore cleanup errors to prevent test failures
        pass


def create_sample_config(output_path: Path, options: Optional[dict] = None) -> Path:
    """
    Generate a sample config.ini file for testing.
    
    Args:
        output_path: Where to save the config file
        options: Optional dict of config values to override defaults
    
    Returns:
        Path: Path to the created config file
    
    Example:
        config_path = create_sample_config(
            temp_dir / 'config.ini',
            {'General': {'detected_video_extensions': 'mkv, mp4'}}
        )
    """
    default_config = """[General]
detected_video_extensions = mkv, mp4, avi
detected_subtitle_extensions = srt, ass, ssa
CSV_export = true

[SubtitleEmbedding]
delete_subtitle_after_embed = true
language_detection_enabled = true
default_language = eng
"""
    
    # TODO: Merge with options if provided (for future use)
    output_path.write_text(default_config, encoding='utf-8')
    return output_path


def compare_files(file1: Path, file2: Path) -> bool:
    """
    Compare two files for equality (byte-by-byte comparison).
    
    Args:
        file1: Path to first file
        file2: Path to second file
    
    Returns:
        bool: True if files are identical, False otherwise
    
    Example:
        if compare_files(expected_csv, actual_csv):
            # Files match
            pass
    """
    if not file1.exists() or not file2.exists():
        return False
    
    return file1.read_bytes() == file2.read_bytes()


def assert_file_exists(path: Path, msg: Optional[str] = None) -> None:
    """
    Custom assertion to verify file exists.
    
    Args:
        path: Path to file that should exist
        msg: Optional custom error message
    
    Raises:
        AssertionError: If file does not exist
    
    Example:
        assert_file_exists(config_path, "Config file should be created")
    """
    if not path.exists():
        error_msg = msg or f"File should exist: {path}"
        raise AssertionError(error_msg)
    
    if not path.is_file():
        error_msg = msg or f"Path exists but is not a file: {path}"
        raise AssertionError(error_msg)


def assert_directory_empty(path: Path, msg: Optional[str] = None) -> None:
    """
    Custom assertion to verify directory is empty.
    
    Args:
        path: Path to directory that should be empty
        msg: Optional custom error message
    
    Raises:
        AssertionError: If directory is not empty or doesn't exist
    
    Example:
        assert_directory_empty(temp_dir, "Cleanup should remove all files")
    """
    if not path.exists():
        error_msg = msg or f"Directory should exist: {path}"
        raise AssertionError(error_msg)
    
    if not path.is_dir():
        error_msg = msg or f"Path exists but is not a directory: {path}"
        raise AssertionError(error_msg)
    
    files = list(path.iterdir())
    if files:
        error_msg = msg or f"Directory should be empty but contains: {[f.name for f in files]}"
        raise AssertionError(error_msg)


class SubFastTestCase(unittest.TestCase):
    """
    Base test case class with common utilities.
    
    Provides automatic temp directory management and common assertions.
    Inherit from this class for consistent test setup/teardown.
    
    Example:
        class TestMyFeature(SubFastTestCase):
            def test_something(self):
                # self.temp_dir is automatically available
                test_file = self.temp_dir / 'test.txt'
                # Cleanup handled automatically in tearDown
    """
    
    def setUp(self):
        """Set up test fixtures - creates temporary directory."""
        super().setUp()
        self.temp_dir = create_temp_directory()
    
    def tearDown(self):
        """Clean up test artifacts - removes temporary directory."""
        cleanup_test_files(self.temp_dir)
        super().tearDown()
    
    def assertFileExists(self, path: Path, msg: Optional[str] = None):
        """Assert that a file exists."""
        assert_file_exists(path, msg)
    
    def assertDirectoryEmpty(self, path: Path, msg: Optional[str] = None):
        """Assert that a directory is empty."""
        assert_directory_empty(path, msg)
    
    def assertFilesEqual(self, file1: Path, file2: Path, msg: Optional[str] = None):
        """Assert that two files are identical."""
        if not compare_files(file1, file2):
            error_msg = msg or f"Files should be identical: {file1} != {file2}"
            raise AssertionError(error_msg)


# Future utilities for pattern testing (Story 6.2)
def load_pattern_definitions():
    """
    Load pattern definitions from JSON file.
    
    Returns:
        dict: Pattern definitions for data-driven tests
    
    Note: Implementation deferred to Story 6.2
    """
    # TODO: Implement in Story 6.2
    pass


def generate_dummy_file(filename: Path, size_kb: int = 1, file_type: str = 'video'):
    """
    Generate dummy test file (video or subtitle).
    
    Args:
        filename: Path where file should be created
        size_kb: Size of dummy file in KB
        file_type: 'video' or 'subtitle'
    
    Note: Implementation deferred to Story 6.2
    """
    # TODO: Implement in Story 6.2
    pass
