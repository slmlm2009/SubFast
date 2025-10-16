# SubFast Testing Framework

## Testing Philosophy

SubFast's testing framework is designed to:
- **Ensure Pattern Accuracy**: All 25 episode patterns validated with realistic test data
- **Zero Dependencies**: Uses Python's built-in `unittest` module only
- **Comprehensive Reporting**: Detailed, bordered table reports generated automatically
- **Self-Contained**: All tests include necessary context and cleanup
- **Extensible**: Easy to add new tests and patterns

## Quick Start

### Running All Tests

```bash
# From project root
python tests/run_tests.py

# Using unittest directly
python -m unittest discover tests/

# Includes: Unit tests + Integration tests (pattern + embedding)
```

### Running Specific Tests

```bash
# Run specific test module
python tests/run_tests.py test_config_loader

# Run specific test class
python -m unittest tests.test_config_loader.TestConfigLoader

# Run specific test method
python -m unittest tests.test_config_loader.TestConfigLoader.test_default_config
```

### Verbose Output

```bash
python tests/run_tests.py -v
```

## Test Reports

### Automatic Report Generation

**Every test run automatically generates a comprehensive report** saved to `tests/reports/`.

Report includes:
- ✅ **Summary Statistics**: Total tests, passed, failed, skipped with percentages
- ✅ **Pattern Test Results**: Shows all pattern IDs, names, variations, status
- ✅ **Failed Tests Details**: Exact failure information with pattern context
- ✅ **Detailed Results**: Complete test listing with durations
- ✅ **Bordered Tables**: Clear, readable format matching SubFast console style

### Report Format

Reports use **bordered table format** for clarity:

```
================================================================================
                          TEST EXECUTION REPORT                               
================================================================================
Test Run: 2025-01-16 10:30:15
Total Duration: 3.24 seconds

--------------------------------------------------------------------------------
                            SUMMARY STATISTICS                                 
--------------------------------------------------------------------------------
| Metric                    | Count  | Percentage |
|---------------------------|--------|------------|
| Total Tests Run           | 50     | 100.00%    |
| Tests Passed              | 47     | 94.00%     |
| Tests Failed              | 2      | 4.00%      |
--------------------------------------------------------------------------------
```

### Viewing Reports

Reports are saved with timestamps:
```bash
tests/reports/test-results-20250116-103015.txt
tests/reports/test-results-20250116-143022.txt
```

Open in any text editor to review results.

## Test Structure

### Directory Organization

```
tests/
├── run_tests.py                      # Custom test runner with unified reporting
├── README.md                         # This file
├── test_helpers.py                   # Shared test utilities
├── test_config_loader.py             # Config module tests (14 tests)
├── test_csv_reporter.py              # CSV reporter tests (10 tests)
├── run_pattern_integration_tests.py  # Pattern integration tests (Story 6.2)
├── test_embedding_integration.py     # Embedding workflow tests (Story 6.3) ⭐ NEW
├── EMBEDDING_INTEGRATION_TESTS.md    # Embedding test documentation ⭐ NEW
├── fixtures/                         # Test data
│   ├── pattern_definitions.json      # Pattern specs (Story 6.2)
│   └── pattern_files/                # Dummy test files (77 variations, 25 patterns)
├── reports/                          # Generated test reports
├── 1- Renaming/
│   └── episode_patterns_guide.md     # Pattern specification
└── 2- Embedding/
    └── integration_testing_files/    # Real video/subtitle samples (Story 6.3) ⭐
```

### Naming Conventions

**Test Files**: `test_<module_name>.py`
- Example: `test_config_loader.py`, `test_pattern_matching.py`

**Test Classes**: `Test<Functionality>`
- Example: `TestConfigLoader`, `TestPatternMatching`

**Test Methods**: `test_<specific_behavior>`
- Example: `test_default_config_generation`, `test_pattern_01_s_e_format`

### Example Test Structure

```python
import unittest
from pathlib import Path

class TestConfigLoader(unittest.TestCase):
    """Test configuration loading and generation."""
    
    def setUp(self):
        """Set up test fixtures before each test."""
        # Create temp directory, sample data, etc.
        pass
    
    def test_default_config_generation(self):
        """Test that default configuration is generated correctly."""
        # Arrange
        # Act
        # Assert
        pass
    
    def tearDown(self):
        """Clean up after each test."""
        # Remove temp files, restore state
        pass

if __name__ == '__main__':
    unittest.main()
```

## Writing New Tests

### Step 1: Create Test File

```python
# tests/test_my_module.py
import unittest
from tests.test_helpers import create_temp_directory, cleanup_test_files

class TestMyModule(unittest.TestCase):
    """Test description."""
    
    def setUp(self):
        self.temp_dir = create_temp_directory()
    
    def test_specific_behavior(self):
        """Test specific behavior description."""
        # Test implementation
        pass
    
    def tearDown(self):
        cleanup_test_files(self.temp_dir)
```

### Step 2: Run Your Tests

```bash
python tests/run_tests.py test_my_module
```

### Step 3: Review Report

Check `tests/reports/test-results-*.txt` for detailed results.

## Test Helpers

The `test_helpers.py` module provides useful utilities:

- `create_temp_directory()` - Creates temporary test directory
- `create_sample_config()` - Generates sample config.ini
- `compare_files()` - Compares two files for equality
- `cleanup_test_files()` - Removes test artifacts
- `assert_file_exists()` - Custom assertion for file existence
- `assert_directory_empty()` - Checks directory is empty

See `test_helpers.py` for complete documentation.

## Pattern Testing (Story 6.2)

Pattern tests use **dummy video and subtitle files** with realistic variations.

**Pattern Definition**: `tests/fixtures/pattern_definitions.json`
- Data-driven test design
- Easy to add new patterns
- Multiple filename variations per pattern

**Example Pattern Test**:
```python
def test_pattern_01_s_e_format(self):
    """Test Pattern 1: S##E## format."""
    result = get_episode_number_cached("Show.S01E05.mkv")
    self.assertEqual(result, "S01E05")
```

See Story 6.2 for comprehensive pattern testing documentation.

## Integration Testing (Story 6.3)

Integration tests use **real video and subtitle files** from:
```
tests/2- Embedding/integration_testing_files/
```

These tests validate end-to-end embedding workflow.

## Performance Targets

- Individual tests: < 1 second
- Full test suite (Story 6.1): < 2 seconds
- Full suite (all stories): < 10 seconds

## Troubleshooting

### Tests Not Discovered

Ensure:
- Test files start with `test_`
- Test classes inherit from `unittest.TestCase`
- Test methods start with `test_`

### Import Errors

Run tests from project root:
```bash
cd C:\...\v3.2.0_preview_rename_subtitles_to_match_videos_ar
python tests/run_tests.py
```

### Report Not Generated

Check:
- `tests/reports/` directory exists (auto-created)
- File permissions allow writing
- Disk space available

## Embedding Integration Tests (Story 6.3)

### Overview

Tests for the complete embedding workflow using real video/subtitle files.

**Location**: `test_embedding_integration.py`  
**Test Files**: `tests/2- Embedding/integration_testing_files/`  
**Documentation**: `EMBEDDING_INTEGRATION_TESTS.md`

### Features

✅ **11 Integration Tests**  
✅ **Works with or without mkvmerge**  
✅ **Auto-skips tests requiring mkvmerge if not available**  
✅ **Real video files** (~36 MB and ~28 MB)  
✅ **Complete workflow validation**

### Running Embedding Tests

```bash
# Run all embedding integration tests
python -m unittest test_embedding_integration -v

# Run only tests that don't need mkvmerge (9 tests)
python -m unittest test_embedding_integration.TestEmbeddingIntegration -v

# Run only mkvmerge-specific tests (2 tests, requires mkvmerge)
python -m unittest test_embedding_integration.TestEmbeddingWorkflowWithMkvmerge -v
```

### Test Coverage

**Workflow Steps Tested:**
1. Scan directory for video/subtitle files
2. Match video with subtitle files
3. Detect language codes
4. Create backup directory
5. Run mkvmerge (if available)
6. Move originals to backup
7. Generate CSV report

**Scenarios:**
- Basic embedding workflow
- Movie mode matching
- Missing mkvmerge handling
- Backup creation
- Dynamic timeout calculation
- Error cleanup and rollback

### mkvmerge Status

Tests automatically detect and report mkvmerge availability:

```
[INFO] mkvmerge is available - full integration tests will run
```
or
```
[WARNING] mkvmerge not available - embedding tests will be limited
```

Tests requiring mkvmerge are automatically SKIPPED if not installed.

### See Also

Full documentation: `tests/EMBEDDING_INTEGRATION_TESTS.md`

## Additional Resources

- **Coding Standards**: `docs/architecture/coding-standards.md`
- **Tech Stack**: `docs/architecture/tech-stack.md`
- **Story 6.1**: Test framework setup (this implementation)
- **Story 6.2**: Pattern test suite with dummy files (COMPLETE)
- **Story 6.3**: Embedding integration tests (COMPLETE) ⭐
- **Story 6.4**: Test data management and extensibility

## Contributing

When adding new tests:
1. Follow naming conventions
2. Include docstrings
3. Clean up test artifacts in `tearDown()`
4. Keep tests fast and focused
5. Use test helpers for common operations
6. Document pattern-specific test logic

---

**Zero Dependencies | Comprehensive Reports | Pattern-Focused Testing**
