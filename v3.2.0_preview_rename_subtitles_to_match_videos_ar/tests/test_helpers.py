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


# ============================================================================
# Pattern Extensibility Helpers (Story 6.4)
# ============================================================================

def validate_pattern_definition(pattern_dict: dict) -> tuple[bool, list[str]]:
    """
    Validate a pattern definition matches the required schema.
    
    Args:
        pattern_dict: Dictionary containing pattern definition
    
    Returns:
        Tuple of (is_valid, error_messages)
        - is_valid: True if pattern is valid, False otherwise
        - error_messages: List of validation error messages (empty if valid)
    
    Validation Rules:
        - Must have 'id', 'name', 'description', 'variations' fields
        - ID must be an integer
        - Variations must be a non-empty list
        - Each variation must have: var_id, expected, video_template, subtitle_template
        - Expected format must be S##E## pattern
        - var_id must be unique within variations
    
    Example:
        >>> pattern = {
        ...     "id": 26,
        ...     "name": "Episode.##.Season.##",
        ...     "description": "Reversed order pattern",
        ...     "variations": [
        ...         {
        ...             "var_id": "VAR1",
        ...             "expected": "S02E05",
        ...             "video_template": "Show.Episode.5.Season.2.mkv",
        ...             "subtitle_template": "Show.Episode.5.Season.2.srt"
        ...         }
        ...     ]
        ... }
        >>> is_valid, errors = validate_pattern_definition(pattern)
        >>> print(is_valid)
        True
    """
    import re
    
    errors = []
    
    # Check required top-level fields
    required_fields = ['id', 'name', 'description', 'variations']
    for field in required_fields:
        if field not in pattern_dict:
            errors.append(f"Missing required field: '{field}'")
    
    if errors:
        return (False, errors)
    
    # Validate ID is integer
    if not isinstance(pattern_dict['id'], int):
        errors.append(f"Pattern ID must be an integer, got: {type(pattern_dict['id']).__name__}")
    
    # Validate variations is a list
    if not isinstance(pattern_dict['variations'], list):
        errors.append(f"'variations' must be a list, got: {type(pattern_dict['variations']).__name__}")
        return (False, errors)
    
    # Check variations not empty
    if len(pattern_dict['variations']) == 0:
        errors.append("'variations' list cannot be empty")
        return (False, errors)
    
    # Validate each variation
    var_ids_seen = set()
    expected_pattern = re.compile(r'^S\d{1,2}E\d{1,2}$', re.IGNORECASE)
    
    for idx, variation in enumerate(pattern_dict['variations']):
        # Check required variation fields
        var_required = ['var_id', 'expected', 'video_template', 'subtitle_template']
        for field in var_required:
            if field not in variation:
                errors.append(f"Variation {idx}: Missing required field '{field}'")
        
        # Validate var_id uniqueness
        if 'var_id' in variation:
            var_id = variation['var_id']
            if var_id in var_ids_seen:
                errors.append(f"Variation {idx}: Duplicate var_id '{var_id}'")
            var_ids_seen.add(var_id)
        
        # Validate expected format
        if 'expected' in variation:
            expected = variation['expected']
            if not expected_pattern.match(expected):
                errors.append(f"Variation {idx}: Expected format must be S##E## (e.g., S01E05), got: '{expected}'")
        
        # Validate filenames look reasonable
        if 'video_template' in variation:
            video = variation['video_template']
            if not any(video.endswith(ext) for ext in ['.mkv', '.mp4', '.avi']):
                errors.append(f"Variation {idx}: video_template should end with .mkv, .mp4, or .avi")
        
        if 'subtitle_template' in variation:
            subtitle = variation['subtitle_template']
            if not any(subtitle.endswith(ext) for ext in ['.srt', '.ass']):
                errors.append(f"Variation {idx}: subtitle_template should end with .srt or .ass")
    
    is_valid = len(errors) == 0
    return (is_valid, errors)


def add_pattern_to_definitions(pattern_dict: dict, json_path: Optional[Path] = None) -> bool:
    """
    Add a new pattern to pattern_definitions.json file.
    
    Args:
        pattern_dict: Dictionary containing pattern definition
        json_path: Path to pattern_definitions.json (defaults to tests/fixtures/pattern_definitions.json)
    
    Returns:
        True if pattern was added successfully, False otherwise
    
    Notes:
        - Validates pattern before adding
        - Checks for duplicate IDs
        - Inserts pattern in correct position (sorted by ID)
        - Creates backup of original file before modification
        - Preserves JSON formatting and metadata
    
    Example:
        >>> pattern = {
        ...     "id": 26,
        ...     "name": "Episode.##.Season.##",
        ...     "description": "Reversed order pattern",
        ...     "variations": [...]
        ... }
        >>> success = add_pattern_to_definitions(pattern)
        >>> if success:
        ...     print("Pattern added successfully!")
    """
    import json
    import shutil
    
    # Default path
    if json_path is None:
        json_path = Path(__file__).parent / 'fixtures' / 'pattern_definitions.json'
    else:
        json_path = Path(json_path)
    
    # Validate pattern first
    is_valid, errors = validate_pattern_definition(pattern_dict)
    if not is_valid:
        print(f"[ERROR] Pattern validation failed:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    # Check file exists
    if not json_path.exists():
        print(f"[ERROR] Pattern definitions file not found: {json_path}")
        return False
    
    # Read existing patterns
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON in {json_path}: {e}")
        return False
    
    # Check for duplicate ID
    pattern_id = pattern_dict['id']
    existing_ids = [p['id'] for p in data.get('patterns', [])]
    if pattern_id in existing_ids:
        print(f"[ERROR] Pattern ID {pattern_id} already exists in pattern_definitions.json")
        return False
    
    # Create backup
    backup_path = json_path.with_suffix('.json.backup')
    try:
        shutil.copy2(json_path, backup_path)
        print(f"[INFO] Created backup: {backup_path.name}")
    except Exception as e:
        print(f"[WARNING] Could not create backup: {e}")
    
    # Insert pattern in sorted position
    patterns = data.get('patterns', [])
    patterns.append(pattern_dict)
    patterns.sort(key=lambda p: p['id'])
    data['patterns'] = patterns
    
    # Update metadata
    if 'metadata' in data:
        data['metadata']['total_patterns'] = len(patterns)
    
    # Write back to file
    try:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[SUCCESS] Pattern {pattern_id} added to {json_path.name}")
        print(f"[INFO] Total patterns: {len(patterns)}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to write pattern definitions: {e}")
        # Restore from backup
        if backup_path.exists():
            shutil.copy2(backup_path, json_path)
            print(f"[INFO] Restored from backup")
        return False


def generate_pattern_test_files(pattern_id: int, base_path: Optional[Path] = None) -> Optional[Path]:
    """
    Generate test files for a specific pattern from pattern_definitions.json.
    
    Args:
        pattern_id: ID of the pattern to generate files for
        base_path: Base path for pattern_files directory (defaults to tests/fixtures/pattern_files)
    
    Returns:
        Path to created pattern directory, or None if generation failed
    
    Notes:
        - Reads pattern definition from pattern_definitions.json
        - Creates pattern_XX_name/ directory
        - Generates dummy video and subtitle files based on variations
        - Creates backup/ subdirectory
        - Uses VAR-based file naming ([VAR1], [VAR2], etc.)
    
    Example:
        >>> pattern_dir = generate_pattern_test_files(26)
        >>> if pattern_dir:
        ...     print(f"Files created in: {pattern_dir}")
        ...     print(f"Files: {list(pattern_dir.glob('*'))}")
    """
    import json
    
    # Default paths
    if base_path is None:
        base_path = Path(__file__).parent / 'fixtures' / 'pattern_files'
    else:
        base_path = Path(base_path)
    
    json_path = Path(__file__).parent / 'fixtures' / 'pattern_definitions.json'
    
    # Read pattern definitions
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to read pattern definitions: {e}")
        return None
    
    # Find pattern by ID
    pattern = None
    for p in data.get('patterns', []):
        if p['id'] == pattern_id:
            pattern = p
            break
    
    if not pattern:
        print(f"[ERROR] Pattern ID {pattern_id} not found in pattern_definitions.json")
        return None
    
    # Create pattern directory
    pattern_name_safe = pattern['name'].replace('#', '').replace('/', '-').replace('\\', '-').replace(' ', '_').strip('_')
    pattern_dir = base_path / f"pattern_{pattern_id:02d}_{pattern_name_safe}"
    pattern_dir.mkdir(parents=True, exist_ok=True)
    
    # Create backup subdirectory
    backup_dir = pattern_dir / 'backup'
    backup_dir.mkdir(exist_ok=True)
    
    # Generate files for each variation
    files_created = []
    for variation in pattern['variations']:
        var_id = variation['var_id']
        video_template = variation['video_template']
        subtitle_template = variation['subtitle_template']
        
        # Prepend [VAR#] to filenames
        video_filename = f"[{var_id}]-{video_template}"
        subtitle_filename = f"[{var_id}]-{subtitle_template}"
        
        # Create dummy video file (supports .mkv, .mp4, etc.)
        video_path = pattern_dir / video_filename
        video_ext = video_path.suffix.lower()
        
        if video_ext == '.mkv':
            header = b'\x1a\x45\xdf\xa3'  # EBML header
        elif video_ext == '.mp4':
            header = b'\x00\x00\x00\x20\x66\x74\x79\x70\x69\x73\x6f\x6d'  # MP4 ftyp
        else:
            header = b'\x00\x00\x00\x01'
        
        content = header + b'\x00' * (1024 - len(header))  # 1KB file
        video_path.write_bytes(content)
        files_created.append(video_filename)
        
        # Create dummy subtitle file (supports .srt, .ass, etc.)
        subtitle_path = pattern_dir / subtitle_filename
        subtitle_ext = subtitle_path.suffix.lower()
        
        if subtitle_ext == '.srt':
            subtitle_content = f"1\n00:00:01,000 --> 00:00:05,000\nDummy subtitle for {var_id}\n\n"
        elif subtitle_ext == '.ass':
            subtitle_content = f"""[Script Info]
Title: Test {var_id}

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:01.00,0:00:05.00,Default,,0,0,0,,Dummy subtitle for {var_id}
"""
        else:
            subtitle_content = f"Dummy subtitle for {var_id}\n"
        
        subtitle_path.write_text(subtitle_content, encoding='utf-8')
        files_created.append(subtitle_filename)
    
    print(f"[SUCCESS] Generated {len(files_created)} test files in: {pattern_dir.name}")
    for filename in files_created:
        print(f"  - {filename}")
    
    return pattern_dir
