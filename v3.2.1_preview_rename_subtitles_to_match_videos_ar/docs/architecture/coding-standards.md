# Coding Standards

## Python Version and Compatibility

**Target:** Python 3.7+ (for Windows 10/11 compatibility)

**Rationale:** Python 3.7 is widely available and provides:
- `pathlib` for modern path handling
- f-strings for readable string formatting
- subprocess enhancements
- Type hints (optional use)

**Constraint:** No features from Python 3.8+ to maintain compatibility

---

## Code Style and Linting

**Style Guide:** PEP 8 (Python Enhancement Proposal 8)

**Linting:** Optional (not enforced via CI for simplicity)

**Key Conventions:**
- 4 spaces for indentation (no tabs)
- Max line length: 100 characters (flexible for readability)
- Snake_case for functions and variables
- PascalCase for classes
- UPPER_CASE for constants

---

## Critical Rules for AI Agents

These rules are MANDATORY for any AI agent modifying SubFast code:

### 1. Subprocess Pattern

**Rule:** ALL subprocess calls MUST use list-based arguments without `shell=True`

**Correct:**
```python
subprocess.run(
    [str(mkvmerge_path), '-o', str(output), str(video), str(subtitle)],
    capture_output=True,
    text=True,
    timeout=300
)
```

**Incorrect:**
```python
# DO NOT USE - Shell injection risk and Windows compatibility issues
subprocess.run(f'{mkvmerge} -o {output} {video} {subtitle}', shell=True)
```

**Rationale:** List-based calls work reliably on all Windows shell configurations

---

### 2. Path Handling

**Rule:** ALWAYS use `pathlib.Path` for file paths, NEVER string concatenation

**Correct:**
```python
from pathlib import Path

video_path = Path(directory) / "video.mkv"
backup_path = Path(directory) / "backups" / video_path.name
```

**Incorrect:**
```python
# DO NOT USE - Breaks on Windows with backslashes
video_path = directory + "/video.mkv"
```

**Rationale:** `pathlib` handles Windows vs. Unix path differences automatically

---

### 3. Error Handling

**Rule:** File operations MUST have try-except blocks; batch processing MUST continue on individual failures

**Correct:**
```python
for matched_pair in matched_pairs:
    try:
        result = process_file(matched_pair)
    except (OSError, PermissionError) as e:
        logger.error(f"Failed to process {matched_pair.video.path}: {e}")
        result = ProcessingResult(status='failed', error=str(e))
    results.append(result)
    # Continue with next file
```

**Incorrect:**
```python
# DO NOT USE - One error stops entire batch
for matched_pair in matched_pairs:
    result = process_file(matched_pair)  # Unhandled exception halts all processing
```

**Rationale:** User expects partial success; one bad file shouldn't stop all processing

---

### 4. Configuration Defaults

**Rule:** Missing or invalid config values MUST use safe defaults, NEVER fail

**Correct:**
```python
try:
    video_exts = config.get('General', 'detected_video_extensions', fallback='mkv, mp4')
except Exception:
    video_exts = 'mkv, mp4'
    logger.warning("Config error, using default video extensions")
```

**Incorrect:**
```python
# DO NOT USE - Crashes on invalid config
video_exts = config.get('General', 'detected_video_extensions')  # Raises if missing
```

**Rationale:** Tool should work out-of-the-box even with missing/corrupt config

---

### 5. Logging vs. Printing

**Rule:** Use `print()` for user-facing console output; use `logger` for debugging (not implemented yet)

**Usage:**
```python
# User-facing messages
print("Processing file 3/10: ShowName.S01E03.mkv")
print("[ERROR] Disk space insufficient")

# Future: Debugging info (if logging implemented)
logger.debug(f"Matched episode S{season}E{episode}")
```

**Rationale:** Clean console output for users; logs for developers when debugging

---

### 6. Atomic File Operations

**Rule:** Use temporary files for multi-step operations; finalize only on success

**Correct:**
```python
temp_output = video.parent / f"{video.stem}.embedded.mkv"
run_mkvmerge(command, output=temp_output)

if mkvmerge_succeeded:
    backup_original(video)
    temp_output.rename(video)  # Atomic rename
else:
    temp_output.unlink()  # Clean up failed temp file
```

**Incorrect:**
```python
# DO NOT USE - Overwrites original before verifying success
run_mkvmerge(command, output=video)  # Destroys original on failure!
```

**Rationale:** Prevents data loss if operation fails mid-process

---

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Script files | snake_case | `subfast_rename.py` |
| Functions | snake_case | `load_config()`, `extract_episode_info()` |
| Classes | PascalCase | `VideoFile`, `EpisodeInfo` |
| Constants | UPPER_CASE | `DEFAULT_VIDEO_EXTENSIONS` |
| Private functions | _leading_underscore | `_validate_extension()` |
| Modules | snake_case | `config_loader.py`, `pattern_engine.py` |

---

## Documentation Standards

**Module Docstrings:**
```python
"""
Module: subfast_rename.py
Purpose: Intelligent subtitle renaming with pattern matching

This module implements the core renaming workflow: directory scanning,
episode pattern recognition, file matching, and safe renaming operations.
"""
```

**Function Docstrings:**
```python
def extract_episode_info(filename: str) -> Optional[EpisodeInfo]:
    """
    Extract normalized episode information from filename.
    
    Args:
        filename: Filename to parse (without path)
    
    Returns:
        EpisodeInfo if pattern matched, None otherwise
    
    Examples:
        >>> extract_episode_info("Show.S01E05.mkv")
        EpisodeInfo(season=1, episode=5, pattern='S##E##')
    """
```

---
