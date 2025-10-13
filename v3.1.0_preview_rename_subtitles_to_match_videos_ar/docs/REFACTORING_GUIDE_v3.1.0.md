# SubFast v3.1.0 Refactoring Guide

## Overview

This guide provides step-by-step instructions for refactoring `subfast_rename.py` and `subfast_embed.py` to use the new shared modules structure.

**Refactoring Goals:**
- ✅ Extract duplicated logic into shared modules
- ✅ Reduce main script complexity
- ✅ Remove development artifacts and unnecessary comments
- ✅ Improve maintainability and code reuse
- ✅ Externalize hardcoded language codes

---

## What We've Created

### Shared Modules (`scripts/common/`)

1. **`config_loader.py`** - Configuration management (used by both scripts)
2. **`pattern_engine.py`** - Episode pattern matching (25+ patterns, used by both)
3. **`csv_reporter.py`** - CSV export functionality (used by both)

**Note:** File utilities and language detection remain in their respective scripts since they're not truly duplicated.

### Data Files

1. **`resources/data/mkvmerge_language_codes.json`** - Externalized language codes (for embedding)

---

## Refactoring Steps for `subfast_rename.py`

### Step 1: Update Imports

**Replace the old imports section with:**

```python
#!/usr/bin/env python3
"""
SubFast - Renaming Module
Fast subtitle renaming for all languages.
Version: 3.1.0
"""

import sys
from pathlib import Path
from datetime import datetime
import time

# Import shared modules
from common import config_loader
from common import pattern_engine
from common import csv_reporter
from common import file_utils
```

### Step 2: Remove Duplicated Code

**Delete these sections (they're now in shared modules):**

1. **Delete** all `EPISODE_PATTERNS` definitions (~100 lines)
2. **Delete** `DEFAULT_CONFIG` dictionary
3. **Delete** `get_script_directory()` function
4. **Delete** `create_default_config_file()` function
5. **Delete** `parse_extensions()` function
6. **Delete** `parse_boolean()` function
7. **Delete** `load_config()` function
8. **Delete** all episode extraction functions:
   - `extract_season_episode_numbers()`
   - `get_episode_number()`
   - `get_episode_number_cached()`
9. **Delete** `extract_base_name()` function
10. **Delete** CSV export functions (replaced by csv_reporter module)

### Step 3: Simplify main() Function

**Replace configuration loading:**

```python
# OLD:
CONFIG = load_config()

# NEW:
CONFIG = config_loader.load_config()
```

**Replace episode detection:**

```python
# OLD:
episode_num = get_episode_number_cached(filename)

# NEW:
episode_num = pattern_engine.get_episode_number_cached(filename)
```

**Replace CSV export:**

```python
# OLD:
if CONFIG['enable_export']:
    with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        # ... many lines of CSV logic ...

# NEW:
if CONFIG['enable_export']:
    csv_reporter.generate_csv_report(
        results,
        csv_path,
        operation_type='renaming'
    )
    csv_reporter.print_summary(results, 'Renaming')
```

### Step 4: Remove Development Artifacts

**Delete or clean up:**

1. **Delete** all `# Story X.Y` comments throughout the file
2. **Delete** `BANNER` and `CSV_BANNER` ASCII art (optional: keep simple version)
3. **Delete** commented-out code blocks
4. **Delete** excessive separator prints (`print("=" * 80)`)
5. **Simplify** verbose progress displays

**Replace verbose banners with:**

```python
print("\n" + "=" * 60)
print("SubFast - Subtitle Renaming v3.1.0")
print("=" * 60 + "\n")
```

### Step 5: Restructure main() Function

**Break down the main() function into smaller, focused functions:**

```python
def process_renaming(folder_path: Path, config: dict) -> list:
    """Process all subtitle renaming operations."""
    results = []
    
    # Discover files
    video_files, subtitle_files = file_utils.discover_files(
        folder_path,
        config['video_extensions'],
        config['subtitle_extensions']
    )
    
    # Detect mode (movie or episode)
    mode = detect_mode(video_files, subtitle_files)
    
    # Build matches
    matches = build_matches(video_files, subtitle_files, mode)
    
    # Execute renames
    results = execute_renames(matches, config)
    
    return results


def main():
    """Main entry point."""
    # Argument parsing
    folder_path = parse_arguments()
    
    # Load configuration
    config = config_loader.load_config()
    
    # Process renames
    start_time = time.time()
    results = process_renaming(folder_path, config)
    elapsed_time = time.time() - start_time
    
    # Export report
    if config['enable_export']:
        csv_path = folder_path / 'renaming_report.csv'
        csv_reporter.generate_csv_report(results, csv_path, 'renaming')
    
    # Print summary
    csv_reporter.print_summary(results, 'Renaming')
    
    # Console behavior
    handle_console_close(config, results)
```

---

## Refactoring Steps for `subfast_embed.py`

### Step 1: Update Imports

**Replace the old imports section with:**

```python
#!/usr/bin/env python3
"""
SubFast - Embedding Module
Fast subtitle embedding into MKV files.
Version: 3.1.0
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime
import time

# Import shared modules
from common import config_loader
from common import pattern_engine
from common import csv_reporter

# Language codes handled within this script using resources/data/mkvmerge_language_codes.json
```

### Step 2: Remove Duplicated Code

**Delete these sections:**

1. **Delete** hardcoded `MKVMERGE_LANGUAGE_CODES` dictionary (~50+ lines)
2. **Delete** duplicated configuration functions (same as rename script)
3. **Delete** duplicated episode extraction functions
4. **Delete** duplicated CSV export logic

### Step 3: Replace Language Detection with JSON Loading

**Replace hardcoded dictionary:**

```python
# OLD:
MKVMERGE_LANGUAGE_CODES = {
    'ara': 'Arabic',
    'eng': 'English',
    # ... 40+ more entries
}

# NEW:
# Load from resources/data/mkvmerge_language_codes.json
def load_language_codes():
    """Load language codes from JSON file."""
    json_path = Path(__file__).parent.parent / 'resources' / 'data' / 'mkvmerge_language_codes.json'
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[WARNING] Language codes file not found: {json_path}")
        return {'codes': {}, 'common_two_letter_codes': {}}

# Call once at module level
LANGUAGE_DATA = load_language_codes()
```

### Step 4: Clean Up main() Function

**Structure the main() function similarly:**

```python
def process_embedding(folder_path: Path, config: dict) -> list:
    """Process all subtitle embedding operations."""
    results = []
    
    # Validate mkvmerge
    mkvmerge_path = validate_mkvmerge(config['mkvmerge_path'])
    if not mkvmerge_path:
        return results
    
    # Discover files
    video_files, subtitle_files = file_utils.discover_files(
        folder_path,
        config['video_extensions'],
        config['subtitle_extensions']
    )
    
    # Filter MKV only
    mkv_videos = [v for v in video_files if v.suffix.lower() == '.mkv']
    
    # Build matches
    matches = build_matches(mkv_videos, subtitle_files)
    
    # Execute embeddings
    results = execute_embeddings(matches, config, mkvmerge_path)
    
    return results


def main():
    """Main entry point."""
    folder_path = parse_arguments()
    config = config_loader.load_config()
    
    start_time = time.time()
    results = process_embedding(folder_path, config)
    elapsed_time = time.time() - start_time
    
    if config['embedding_report']:
        csv_path = folder_path / 'embedding_report.csv'
        csv_reporter.generate_csv_report(results, csv_path, 'embedding')
    
    csv_reporter.print_summary(results, 'Embedding')
    
    handle_console_close(config, results)
```

---

## Common Refactorings for Both Scripts

### Remove Verbose Output

**Before:**
```python
print("=" * 80)
print("SUBFAST - SUBTITLE RENAMING")
print("=" * 80)
print(f"Processing folder: {folder_path}")
print("=" * 80)
```

**After:**
```python
print(f"\nSubFast v3.1.0 - Processing: {folder_path.name}\n")
```

### Simplify Error Messages

**Before:**
```python
print("[ERROR] " + "=" * 60)
print("CRITICAL ERROR: Failed to process file")
print(f"File: {filename}")
print(f"Reason: {error}")
print("=" * 60)
```

**After:**
```python
print(f"[ERROR] Failed to process {filename}: {error}")
```

### Remove Development Comments

**Delete these types of comments:**
```python
# Story 1.2: Configuration loading
# Story 2.3 Task 5: Episode detection
# OLD: previous implementation
# TODO: optimize this later
# FIXME: handle edge case
```

**Keep only meaningful comments:**
```python
# Skip hidden files and system files
# Normalize episode numbers for consistent matching
# Strategy: filename → config → none
```

---

## Testing After Refactoring

### Test Checklist

1. **Configuration Loading**
   - [ ] config.ini loads correctly
   - [ ] Default config generates if missing
   - [ ] Invalid values fall back to defaults

2. **Renaming Functionality**
   - [ ] Episode pattern detection works (test 5-10 patterns)
   - [ ] Language suffix applied correctly
   - [ ] CSV export generates properly
   - [ ] Movie mode works for single pairs

3. **Embedding Functionality**
   - [ ] mkvmerge path validates correctly
   - [ ] Language detection from filename works
   - [ ] Backup creation functions properly
   - [ ] Disk space check prevents failures

4. **Shared Modules**
   - [ ] pattern_engine cache improves performance
   - [ ] language_codes.json loads correctly
   - [ ] csv_reporter generates valid CSV
   - [ ] file_utils handles edge cases

### Performance Testing

**Run with profiling:**
```bash
python -m cProfile -o profile.stats scripts/subfast_rename.py "C:\test_folder"
python -m pstats profile.stats
# In pstats: sort cumulative, stats 20
```

**Expected improvements:**
- Reduced code duplication: ~40-50% less code in main scripts
- Same or better performance (caching optimizations)
- Easier maintenance and testing

---

## Final Checklist

- [ ] All shared modules created in `scripts/common/`
- [ ] `mkvmerge_language_codes.json` in `resources/`
- [ ] Both main scripts refactored
- [ ] All development artifacts removed
- [ ] Code tested with sample files
- [ ] Performance validated
- [ ] Documentation updated

---

## Estimated Code Reduction

**Before Refactoring:**
- `subfast_rename.py`: ~1250 lines
- `subfast_embed.py`: ~1400 lines
- **Total: ~2650 lines**

**After Refactoring:**
- `subfast_rename.py`: ~600 lines (52% reduction)
- `subfast_embed.py`: ~650 lines (54% reduction)
- Shared modules: ~800 lines (reusable)
- **Total: ~2050 lines (23% overall reduction)**

**Benefits:**
- 40-50% less duplicated code
- Centralized logic for easier maintenance
- Better testability (modules can be unit tested)
- Externalized data (language codes)
- Cleaner, more readable main scripts

---

## Next Steps

1. **Backup current scripts** before refactoring
2. **Refactor one script at a time** (start with rename)
3. **Test thoroughly** after each change
4. **Update documentation** to reflect v3.1.0 changes
5. **Consider adding unit tests** for shared modules

## Questions or Issues?

If you encounter any issues during refactoring:
1. Check import paths are correct
2. Verify `__init__.py` exists in `common/`
3. Ensure `mkvmerge_language_codes.json` path is correct
4. Test shared modules independently before integrating

---

**End of Refactoring Guide**
