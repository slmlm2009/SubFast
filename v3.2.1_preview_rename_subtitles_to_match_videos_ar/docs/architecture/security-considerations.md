# Security Considerations

## Input Validation

**File Path Validation:**
- All paths resolved to absolute paths using `pathlib.Path.resolve()`
- No path traversal vulnerabilities (operations scoped to provided directory)
- File extension validation against whitelist from config

**Configuration Validation:**
- All config values validated with safe defaults
- No arbitrary code execution from configuration
- Invalid values logged and replaced with defaults

**User Input:**
- No direct user input during execution (folder path from Explorer)
- Command-line arguments only used for directory path

## Subprocess Security

**mkvmerge Execution:**
```python
# SECURE: List-based arguments prevent injection
subprocess.run([str(mkvmerge), '-o', str(output), str(video), str(subtitle)])

# INSECURE: Shell command concatenation (NOT USED)
subprocess.run(f'{mkvmerge} -o {output} {video} {subtitle}', shell=True)
```

**Security Measures:**
- Never use `shell=True`
- All paths explicitly converted to strings
- No user-controllable command construction
- mkvmerge path validated at startup
- Timeout enforced to prevent hanging processes

## File System Security

**Permissions:**
- Scripts run with user's Windows permissions
- No privilege escalation
- No modification of system files
- All operations in user-writable directories

**Backup Safety:**
- Original files moved (not deleted) to backups/
- Backup directory created in same location (no cross-drive issues)
- Collision detection prevents accidental overwrites

**Data Integrity:**
- Atomic file operations (rename complete or not at all)
- Temporary files (`.embedded.mkv`) deleted on failure
- No partial file states

## Privacy

**No External Communication:**
- No network requests
- No telemetry or analytics
- No data sent to external servers
- Completely offline operation

**Local Data Only:**
- All processing local to user's machine
- CSV reports stored locally
- No cloud storage or syncing

## Registry Integration Security

**User-Level Registry:**
- Context menu registered in user scope when possible
- No system-wide changes unless run as administrator
- Registry keys limited to Windows Explorer context menu

**Registry Content:**
```reg
; Only modifies Explorer context menu for folders
[HKEY_CLASSES_ROOT\Directory\shell\SubFast]
; No script execution paths in registry (uses .py association)
```

---
