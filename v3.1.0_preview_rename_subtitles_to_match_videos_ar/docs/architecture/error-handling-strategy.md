# Error Handling Strategy

## Error Categories and Responses

### 1. Configuration Errors

**Type:** Non-Fatal (Use Defaults)

**Examples:**
- Missing config.ini
- Invalid file extensions
- Invalid boolean values
- Malformed INI syntax

**Handling:**
```python
try:
    config = load_config('config.ini')
except FileNotFoundError:
    logger.warning("config.ini not found. Generating default configuration.")
    config = generate_default_config()
    save_config(config)
except ConfigParseError as e:
    logger.warning(f"Invalid config.ini: {e}. Using defaults.")
    config = get_default_config()
```

**User Experience:**
- Console warning logged
- Default values used
- Script continues execution
- Default config.ini auto-generated if missing

---

### 2. File System Errors

**Type:** Per-File Fatal (Skip File, Continue Batch)

**Examples:**
- Permission denied
- Disk full
- File in use by another process
- Invalid filename characters

**Handling:**
```python
for matched_pair in matched_pairs:
    try:
        result = process_file(matched_pair)
    except PermissionError as e:
        logger.error(f"Permission denied: {matched_pair.video.path}")
        result = ProcessingResult(status='failed', error=str(e))
    except OSError as e:
        logger.error(f"File system error: {e}")
        result = ProcessingResult(status='failed', error=str(e))
    
    results.append(result)
    # Continue with next file
```

**User Experience:**
- Error logged to console with affected file
- File skipped
- Batch processing continues
- Error included in summary and CSV report
- Specific troubleshooting hint provided

---

### 3. mkvmerge Errors

**Type:** Per-File Fatal (Skip File, Continue Batch)

**Examples:**
- mkvmerge.exe not found
- Invalid MKV file
- Corrupted subtitle file
- mkvmerge crash
- Timeout (>5 minutes)

**Handling:**
```python
# At startup
if not mkvmerge_path.exists():
    console_error("mkvmerge.exe not found. Please check config.ini")
    sys.exit(3)

# During processing
try:
    exit_code, stdout, stderr = run_mkvmerge(command, timeout=300)
    if exit_code != 0:
        raise MKVMergeError(f"mkvmerge failed: {stderr}")
except subprocess.TimeoutExpired:
    logger.error(f"mkvmerge timeout (>5min) for {video.path}")
    result = ProcessingResult(status='failed', error='Timeout: Process took longer than 5 minutes')
except MKVMergeError as e:
    logger.error(f"mkvmerge error: {e}")
    result = ProcessingResult(status='failed', error=str(e))
```

**User Experience:**
- Startup validation prevents "tool not found" mid-batch
- Per-file errors logged with mkvmerge's stderr output
- Timeout prevents hanging on problematic files
- Failed files noted in summary
- Temporary `.embedded.mkv` cleaned up

---

### 4. Pattern Matching Failures

**Type:** Non-Fatal (Skip File Pair)

**Examples:**
- Unrecognized filename pattern
- No matching video for subtitle
- Multiple possible matches (ambiguous)

**Handling:**
```python
episode_info = extract_episode_info(filename)
if episode_info is None:
    logger.info(f"Unrecognized pattern, skipping: {filename}")
    return None  # File not included in matched pairs

if len(potential_matches) > 1:
    logger.warning(f"Ambiguous match for {subtitle.path}: {potential_matches}")
    # Take first match and log warning
```

**User Experience:**
- Informational log (not error)
- File simply not processed
- No impact on other files
- Logged in summary: "X files processed, Y unmatched"

---

## Error Logging Format

**Console Output:**
```plaintext
[ERROR] <Category>: <Specific Issue>
File: <affected_filename>
Details: <error_details>
Suggestion: <troubleshooting_hint>
```

**Example:**
```plaintext
[ERROR] File System: Insufficient disk space for embedding
File: LargeMovie.mkv
Details: Required 5.2GB, available 2.1GB on drive C:\
Suggestion: Free up disk space or move file to drive with more space
```

**CSV Report Error Recording:**
```csv
Original Video,Original Subtitle,Status,Error Message,Timestamp
LargeMovie.mkv,LargeMovie.srt,Failed,"Insufficient disk space: Required 5.2GB, available 2.1GB",2025-01-12T10:45:00
```

## Exit Codes

```python
# Script exit codes for automation/scripting
EXIT_SUCCESS = 0          # All operations successful
EXIT_CONFIG_ERROR = 1     # Critical config issue (e.g., mkvmerge not found)
EXIT_FILE_ERROR = 2       # All files failed (permissions, disk full)
EXIT_MKVMERGE_ERROR = 3   # mkvmerge tool error (not found, invalid)
EXIT_USER_ABORT = 130     # User pressed Ctrl+C
```

---
