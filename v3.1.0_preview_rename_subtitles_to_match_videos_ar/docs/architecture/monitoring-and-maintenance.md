# Monitoring and Maintenance

## Monitoring Capabilities

SubFast is a local utility without centralized monitoring infrastructure. Observability is achieved through:

### 1. Console Output
- Real-time progress reporting during batch operations
- Success/failure status for each file
- Final summary statistics
- Error messages with affected filenames

### 2. CSV Reports (Optional)
- Complete record of all operations
- Timestamps and execution times
- Status and error messages
- Useful for post-execution audit

### 3. Windows Event Log (Not Implemented)
- Future consideration: Log critical errors to Windows Event Log
- Would enable centralized monitoring for IT administrators

## Maintenance Considerations

### Pattern Updates

**Adding New Episode Patterns:**
```python
# In pattern_engine.py COMPILED_PATTERNS list
COMPILED_PATTERNS.append((
    'NewPattern',
    re.compile(r'YourRegexHere', re.IGNORECASE)
))
```

**Testing New Patterns:**
```python
# Add test case to tests/test_pattern_engine.py
def test_new_pattern(self):
    result = extract_episode_info("Example.NewFormat.mkv")
    self.assertEqual(result, (season, episode))
```

### mkvmerge Updates

**Updating Bundled mkvmerge:**
1. Download latest MKVToolNix portable version
2. Extract `mkvmerge.exe` to `C:\subfast\bin\`
3. Test embedding workflow with sample files
4. Update version in README

**User-Provided mkvmerge:**
```ini
[Embedding]
# User can specify custom mkvmerge path
mkvmerge_path = C:\Program Files\MKVToolNix\mkvmerge.exe
```

### Configuration Schema Evolution

**Adding New Config Options:**
```python
# In config_loader.py
def get_default_config():
    return {
        # Existing options...
        'new_option': 'default_value'  # Add new with default
    }
```

**Backward Compatibility:**
- Always provide defaults for new options
- Never remove existing options (deprecate if needed)
- Document changes in CHANGELOG.md

### Python Version Migration

**Future Python 3.11+ Migration:**
- Update README requirements
- Test all subprocess calls (potential changes)
- Test Windows compatibility
- Consider new features (e.g., improved error messages)

## Known Limitations

1. **MKV-Only Embedding:** mkvmerge constraint, no MP4 support
2. **No Parallel Processing:** Sequential to avoid disk I/O contention
3. **Windows-Only:** Registry integration and `py.exe` dependency
4. **No GUI:** By design (context menu is the interface)
5. **No Undo:** Backups provide recovery, but no built-in undo

## Future Enhancement Ideas

1. **GUI Configuration Tool:** For users uncomfortable with INI files
2. **Batch Report Viewer:** HTML report instead of CSV
3. **Auto-Update Checker:** Check for new SubFast versions
4. **Pattern Suggestion:** Machine learning to suggest new patterns
5. **Multi-Language Subtitle Embedding:** Embed multiple subtitle tracks at once

---
