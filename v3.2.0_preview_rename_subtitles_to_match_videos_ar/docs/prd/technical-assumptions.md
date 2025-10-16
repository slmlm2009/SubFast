# Technical Assumptions

## Repository Structure: Monorepo

SubFast is a standalone Windows utility with all components in a single repository structure:

```
C:\subfast\
├── scripts/
│   ├── subfast_rename.py
│   └── subfast_embed.py
├── bin/
│   └── mkvmerge.exe
├── resources/
│   ├── subfast_logo.ico
│   └── docs/
│       └── CONFIGURATION_README.md
├── config.ini
├── add_subfast_menu.reg
└── remove_subfast_menu.reg
```

## Service Architecture

**Architecture Type:** Monolithic Local Scripts

- Two independent Python scripts (`subfast_rename.py`, `subfast_embed.py`)
- No client-server architecture
- Direct file system operations
- Command-line tool invoked via Windows Shell integration

## Testing Requirements

**Testing Strategy:** Manual + Unit Testing Convenience Methods

- Primary testing: Manual testing during development
- Unit tests for critical pattern matching regex
- File operation tests with temporary directories
- Integration testing with sample video/subtitle files
- Real-world testing with diverse episode naming patterns

**Rationale:** As a local utility tool, extensive automated testing infrastructure would add unnecessary complexity. Focus on robust pattern matching tests and real-world validation.

## Language and Runtime

- **Primary Language:** Python 3.7+
- **Rationale:** Cross-platform capabilities, strong file system libraries, easy scripting, subprocess management
- **Constraint:** Python Launcher must be available at `C:\Windows\py.exe`

## External Dependencies

- **MKVToolNix (mkvmerge.exe):**
  - Purpose: Subtitle embedding into MKV containers
  - Bundled in `bin/` directory
  - Configurable path for user-provided installations
  - Latest stable version recommended

## Subprocess Execution Pattern

**Critical Windows Compatibility Requirement:**

All subprocess calls to `mkvmerge.exe` must use list-based arguments without `shell=True` to ensure compatibility with all Windows shell configurations:

```python
# CORRECT - Windows-compatible
result = subprocess.run(
    [str(mkvmerge_path), '-o', str(output), str(video), str(subtitle)],
    capture_output=True,
    text=True,
    timeout=300
)
```

**Rationale:** Avoids issues with non-standard COMSPEC environment variables and ensures proper argument escaping.

## Configuration Management

- **Format:** INI file (`config.ini`)
- **Sections:** `[General]`, `[Renaming]`, `[Embedding]`
- **Behavior:** Auto-generate with defaults if missing
- **Rationale:** Human-readable, simple parsing, unified configuration for both features

## Performance Optimizations

- Episode number caching with dictionary lookups
- Regex precompilation at script initialization
- Optional CSV export for speed-critical scenarios
- Memory-efficient processing (42% reduction achieved in v2.5.0)

## Additional Technical Assumptions

1. **Windows Registry Integration:** Uses `.reg` files for context menu registration (admin privileges may be required)

2. **File System Operations:** Direct file I/O using Python's `pathlib` and `shutil` modules

3. **Character Encoding:** UTF-8 for all file operations and console output

4. **Collision Detection:** Filename-based collision checking before write operations

5. **Backup Strategy:** Move-based backups (not copy) to save disk space

6. **Progress Reporting:** Console-based real-time status updates (no GUI required)

7. **Error Logging:** Console output only (no separate log files by default)

---
