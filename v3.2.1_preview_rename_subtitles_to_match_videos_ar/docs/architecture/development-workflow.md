# Development Workflow

## Local Development Setup

**Prerequisites:**
```bash
# Verify Python installation
py --version  # Should show Python 3.7 or higher

# Verify Python Launcher location
where py  # Should show C:\Windows\py.exe

# Install development tools (optional)
py -m pip install pytest  # For unit testing
```

**Initial Setup:**
```bash
# 1. Clone or extract project
cd C:\subfast\

# 2. Verify directory structure
dir  # Should show scripts/, bin/, resources/, config.ini

# 3. Test configuration loading
py scripts\subfast_rename.py --help  # Should show usage

# 4. Verify mkvmerge bundled correctly
bin\mkvmerge.exe --version  # Should show version info
```

## Manual Testing

**Test Renaming:**
```bash
# Create test directory with sample files
mkdir C:\temp\subfast_test
cd C:\temp\subfast_test

# Add test video: "Show.S01E05.mkv"
# Add test subtitle: "subtitle-05.srt"

# Run rename script directly
py C:\subfast\scripts\subfast_rename.py "C:\temp\subfast_test"

# Verify: subtitle-05.srt renamed to Show.S01E05.srt (or with language suffix)
```

**Test Embedding:**
```bash
# Using same test directory with MKV video and subtitle
py C:\subfast\scripts\subfast_embed.py "C:\temp\subfast_test"

# Verify: 
# - backups/ directory created
# - Original files moved to backups/
# - New Show.S01E05.mkv contains embedded subtitle
```

**Test Context Menu:**
```bash
# 1. Install context menu
# Double-click: add_subfast_menu.reg

# 2. Verify in Explorer
# Right-click in C:\temp\subfast_test
# Should see "SubFast" menu with two options

# 3. Test via context menu
# Right-click → SubFast → Rename subtitles
# Observe console window behavior
```

## Unit Testing

**Pattern Recognition Tests:**
```python
# tests/test_pattern_engine.py
import unittest
from scripts.common.pattern_engine import extract_episode_info

class TestPatternEngine(unittest.TestCase):
    def test_standard_format(self):
        result = extract_episode_info("Show.S01E05.mkv")
        self.assertEqual(result.season_number, 1)
        self.assertEqual(result.episode_number, 5)
    
    def test_alternate_format(self):
        result = extract_episode_info("Show.2x8.mkv")
        self.assertEqual(result.season_number, 2)
        self.assertEqual(result.episode_number, 8)
    
    def test_resolution_not_episode(self):
        result = extract_episode_info("Show.1920x1080.mkv")
        self.assertIsNone(result)
```

**Run Tests:**
```bash
py -m pytest tests/
```

## Configuration Testing

**Test Config Validation:**
```python
# Temporarily rename config.ini
# Run script - should auto-generate default config
py scripts\subfast_rename.py "C:\temp\test"

# Verify config.ini created with default values
```

**Test Invalid Config:**
```python
# Edit config.ini with invalid values
# detected_video_extensions = @@@invalid@@@

# Run script - should log warning and use defaults
py scripts\subfast_rename.py "C:\temp\test"
```

---
