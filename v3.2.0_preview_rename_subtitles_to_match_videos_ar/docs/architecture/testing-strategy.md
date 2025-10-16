# Testing Strategy

## Testing Philosophy

**Approach:** Manual + Targeted Unit Tests

SubFast is a file-manipulation utility where automated end-to-end testing is complex (requires real video/subtitle files, Windows environment, Registry access). The strategy balances test coverage with practical development efficiency:

1. **Manual Testing:** Primary validation with real-world files
2. **Unit Tests:** Critical components (pattern matching, configuration)
3. **Integration Tests:** Limited scope (file operations with temp directories)
4. **Real-World Validation:** Beta testing with diverse media libraries

**Coverage Goals:**
- Pattern recognition: 100% (all 25+ patterns tested)
- Configuration loading: 100% (all valid and invalid cases)
- File operations: Manual verification
- mkvmerge integration: Manual verification
- Windows Registry: Manual verification

## Test Organization

```plaintext
C:\subfast\
├── tests\                                # Test directory
│   ├── __init__.py
│   ├── test_pattern_engine.py           # Pattern matching tests
│   ├── test_config_loader.py            # Configuration tests
│   ├── test_file_matcher.py             # File discovery and matching tests
│   ├── fixtures\                        # Test data
│   │   ├── sample_episodes.txt          # Filename examples
│   │   ├── test_config.ini              # Test configurations
│   │   └── test_videos\                 # Small test video files
│   └── manual_tests\                    # Manual test scenarios
│       ├── renaming_scenarios.md        # Test cases for renaming
│       └── embedding_scenarios.md       # Test cases for embedding
```

## Unit Tests

### Pattern Recognition Tests

**Framework:** Python `unittest`

**Test Coverage:**
```python
# tests/test_pattern_engine.py
import unittest
from scripts.common.pattern_engine import extract_episode_info, normalize_episode_number

class TestPatternEngine(unittest.TestCase):
    """Test all 25+ episode patterns"""
    
    def test_standard_S##E##(self):
        self.assertEqual(extract_episode_info("Show.S01E05.mkv"), (1, 5))
        self.assertEqual(extract_episode_info("Show.S2E15.mkv"), (2, 15))
    
    def test_alternate_##x##(self):
        self.assertEqual(extract_episode_info("Show.2x8.mkv"), (2, 8))
        # Should NOT match resolution
        self.assertIsNone(extract_episode_info("Show.1920x1080.mkv"))
    
    def test_ordinal_seasons(self):
        self.assertEqual(extract_episode_info("Show.1st.Season.05.mkv"), (1, 5))
        self.assertEqual(extract_episode_info("Show.2nd.Season.E10.mkv"), (2, 10))
    
    def test_normalization(self):
        """Episode numbers should normalize regardless of padding"""
        self.assertEqual(extract_episode_info("Show.S01E05.mkv")[1], 5)
        self.assertEqual(extract_episode_info("Show.S1E5.mkv")[1], 5)
        self.assertEqual(extract_episode_info("Show.S01E005.mkv")[1], 5)
    
    def test_unrecognized_patterns(self):
        """Unrecognized patterns should return None"""
        self.assertIsNone(extract_episode_info("Random.File.Name.mkv"))
        self.assertIsNone(extract_episode_info("Movie.2023.BluRay.mkv"))

    # ... More tests for all pattern variations
```

**Run Tests:**
```bash
py -m unittest discover -s tests -p "test_*.py"
```

---

### Configuration Tests

```python
# tests/test_config_loader.py
import unittest
import tempfile
from pathlib import Path
from scripts.common.config_loader import load_config, generate_default_config

class TestConfigLoader(unittest.TestCase):
    
    def setUp(self):
        """Create temporary config file for each test"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "config.ini"
    
    def test_missing_config_generates_default(self):
        """Missing config.ini should auto-generate"""
        config = load_config(self.config_path)
        self.assertTrue(self.config_path.exists())
        self.assertEqual(config.detected_video_extensions, ['mkv', 'mp4'])
    
    def test_invalid_extensions_use_default(self):
        """Invalid extensions should fallback to defaults"""
        self.config_path.write_text("""
        [General]
        detected_video_extensions = @@@invalid@@@
        """)
        config = load_config(self.config_path)
        self.assertEqual(config.detected_video_extensions, ['mkv', 'mp4'])
    
    def test_boolean_parsing(self):
        """Test various boolean value formats"""
        self.config_path.write_text("""
        [General]
        keep_console_open = true
        [Renaming]
        renaming_report = false
        """)
        config = load_config(self.config_path)
        self.assertTrue(config.keep_console_open)
        self.assertFalse(config.renaming_report)
    
    # ... More config validation tests
```

---

## Manual Testing Scenarios

### Renaming Test Cases

**File:** `tests/manual_tests/renaming_scenarios.md`

**Test Scenarios:**

1. **Basic Episode Matching**
   - Setup: 3 videos `Show.S01E0{1,2,3}.mkv`, 3 subtitles `subtitle-{1,2,3}.srt`
   - Expected: Subtitles renamed to `Show.S01E0{1,2,3}.srt`

2. **Inconsistent Zero-Padding**
   - Setup: Video `Show.S2E8.mkv`, Subtitle `Show.S02E008.srt`
   - Expected: Context-aware match succeeds

3. **Language Suffix**
   - Setup: Config with `renaming_language_suffix = ar`
   - Expected: Renamed to `Show.S01E01.ar.srt`

4. **Collision Handling**
   - Setup: Target file already exists
   - Expected: Skip with warning, original untouched

5. **Movie Mode**
   - Setup: Single video + single subtitle
   - Expected: Direct 1:1 match without episode detection

6. **Unrecognized Patterns**
   - Setup: Video with standard pattern, subtitle with random name
   - Expected: No match, subtitle skipped

7. **CSV Report Verification**
   - Setup: Enable `renaming_report = true`
   - Expected: `renaming_report.csv` generated with accurate data

**Execution:**
```bash
# Create test directory, add files, run script, verify results
```

---

### Embedding Test Cases

**File:** `tests/manual_tests/embedding_scenarios.md`

**Test Scenarios:**

1. **Basic Subtitle Embedding**
   - Setup: MKV video + matching subtitle
   - Expected: Subtitle embedded, backup created, original moved

2. **Language Detection from Filename**
   - Setup: Subtitle named `Show.S01E01.ar.srt`
   - Expected: Embedded with language code `ara`

3. **Language Fallback to Config**
   - Setup: No language in filename, config has `embedding_language_code = eng`
   - Expected: Embedded with `eng` language tag

4. **Default Track Flag**
   - Setup: `default_flag = true` in config
   - Expected: mkvmerge command includes `--default-track 0:yes`

5. **Disk Space Check**
   - Setup: Process large file with insufficient disk space
   - Expected: Skip with clear disk space error

6. **mkvmerge Failure**
   - Setup: Corrupted video file
   - Expected: Error logged, `.embedded.mkv` deleted, originals untouched

7. **Backup Collision**
   - Setup: Process same file twice
   - Expected: First creates backup, second skips backup and updates file

8. **Non-MKV Files**
   - Setup: MP4 video + subtitle
   - Expected: Skipped with message "Embedding only supports MKV"

9. **CSV Report Verification**
   - Setup: Enable `embedding_report = true`
   - Expected: `embedding_report.csv` with accurate language detection and timing

**Verification Tools:**
```bash
# Verify embedded subtitle
mkvmerge --identify output.mkv

# Verify subtitle track properties
mkvinfo output.mkv | grep -A5 "Track type: subtitles"
```

---

## Real-World Validation

**Beta Testing Checklist:**

1. **Diverse Episode Patterns**
   - Test with TV shows using different naming conventions
   - Verify all 25+ patterns work in practice

2. **Large Batch Processing**
   - Process 1000+ file dataset
   - Verify <1 second renaming performance
   - Monitor memory usage during embedding

3. **Various Subtitle Formats**
   - Test with .srt, .ass files
   - Different character encodings

4. **Different Video Formats**
   - Test with .mkv, .mp4 (renaming)
   - Verify MKV-only constraint (embedding)

5. **Windows Environment Variations**
   - Windows 10 and Windows 11
   - Different Python versions (3.7, 3.8, 3.10, 3.12)
   - User and Administrator accounts

6. **Edge Cases**
   - Files with special characters in names
   - Very long filenames
   - Unicode characters (Arabic, Chinese, etc.)

---
