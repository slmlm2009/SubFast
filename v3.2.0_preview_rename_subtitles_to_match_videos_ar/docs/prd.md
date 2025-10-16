# SubFast Product Requirements Document (PRD)

**Version:** 3.0.0  
**Last Updated:** January 2025  
**Product:** SubFast - Fast subtitle renaming and embedding for all languages

---

## Goals and Background Context

### Goals

- Provide Windows users with a fast, automated solution for managing subtitles with their video files
- Eliminate manual, time-consuming subtitle renaming through intelligent pattern matching
- Enable seamless subtitle embedding into MKV videos through right-click context menu integration
- Support all language codes and subtitle formats with configurable options
- Deliver exceptional performance capable of processing 1000+ files in under 1 second
- Maintain simplicity through Windows Explorer integration requiring no GUI or command-line knowledge
- Ensure safe operations through automatic backups and collision handling
- Support batch processing for efficient management of large media libraries

### Background Context

SubFast (formerly "Subtitle Renamer Tool [AR]") has evolved from a simple renaming utility into a comprehensive dual-feature subtitle management system for Windows. The product addresses a critical pain point for media library managers: organizing and integrating subtitles with video files.

**Evolution Context:**
- v1.0.0: Basic episode detection and renaming
- v2.0.0: Windows context menu integration with enhanced pattern recognition
- v2.5.0: Configuration system with 12x performance improvement and 25+ episode patterns
- v3.0.0: Complete rebranding to "SubFast" with new MKV subtitle embedding feature

The v3.0.0 release represents a major milestone, transforming SubFast from a single-purpose renaming tool into a complete subtitle workflow solution. Users previously had to rename subtitles, then manually open GUI applications to embed them - a disconnected, time-consuming process. SubFast now provides a unified, one-click workflow for both operations through Windows Explorer's context menu.

### Change Log

| Date | Version | Description | Author |
|------|---------|-------------|--------|
| January 2025 | 3.0.0 | Complete PRD rewrite for SubFast v3.0.0 reflecting dual-feature product | PM Team |
| October 2024 | 2.0.0 | Initial PRD for embedding feature addition | PM Team |

---

## Requirements

### Functional Requirements

**FR1: Dual-Feature Context Menu Integration**
- SubFast must provide a cascading Windows context menu accessible via right-click in any folder
- Menu structure: "SubFast" parent menu → "Rename subtitles" + "Embed subtitles" sub-options
- Both features must be invokable from the same folder without requiring separate navigation

**FR2: Intelligent Subtitle Renaming**
- Automatically detect and match video/subtitle file pairs in the same directory
- Rename subtitle files to match their corresponding video filenames exactly
- Support configurable language suffix (e.g., `.ar`, `.en`, `.es`) appended to renamed files
- Preserve original subtitle file extensions during renaming

**FR3: Advanced Episode Pattern Recognition**
- Recognize 25+ episode naming patterns including:
  - Standard: `S##E##` (e.g., S01E05, S2E15)
  - Alternate: `##x##` with smart resolution detection
  - Variations: `S## - ##`, `S## - E##`, `S## - EP##`
  - Text-based: `Season # Episode #` with various separators
  - Ordinal: `1st Season`, `2nd Season`, `3rd Season` patterns
  - Simple: `E##`, `Ep##`, `- ##` patterns
- Context-aware matching that handles inconsistent zero-padding (e.g., `S2E8` matches `S02E008`)

**FR4: Movie Mode Detection**
- Automatically detect folders with single video/subtitle pairs
- Apply simple 1:1 matching for movie scenarios without episode pattern analysis

**FR5: MKV Subtitle Embedding**
- Embed external subtitle files directly into MKV video files using mkvmerge
- Preserve all original video and audio tracks without re-encoding (stream copy only)
- Support automatic subtitle/video match identification using same pattern matching as renaming feature
- Create embedded videos with soft subtitles for seamless playback

**FR6: Language Code Detection and Configuration**
- Extract language codes from subtitle filenames (e.g., `.ar.srt` → Arabic)
- Apply detected language codes to embedded subtitle tracks
- Fall back to configured default language when filename detection fails
- Support ISO 639-2 three-letter language codes (e.g., `ara`, `eng`, `fra`)

**FR7: Default Subtitle Track Control**
- Allow configuration of whether embedded subtitles are marked as "default" track
- Default behavior: Mark embedded subtitle as default track for automatic player selection

**FR8: Automatic Backup Management**
- Create `backups/` directory on first successful embedding operation
- Move original video and subtitle files to backups before creating embedded version
- Skip backup if files already exist (prevents duplicate backups during re-processing)
- Remove subtitle files from working directory after successful backup

**FR9: Collision Handling**
- Detect and prevent file overwrites during renaming operations
- Apply smart naming strategies when target filename already exists
- Never overwrite existing files without explicit user configuration

**FR10: Configuration System**
- Provide `config.ini` file for centralized configuration management
- Support `[General]`, `[Renaming]`, and `[Embedding]` sections
- Auto-generate default `config.ini` if missing with sensible defaults
- Allow configuration of:
  - Detected file extensions (video and subtitle)
  - Language suffixes and codes
  - Console behavior (auto-close vs. stay open)
  - Report generation (enable/disable CSV export)
  - mkvmerge executable path

**FR11: CSV Reporting**
- Generate detailed CSV reports for both renaming and embedding operations
- Include original filenames, new filenames, operation status, and execution metrics
- Make CSV generation configurable (enable/disable) for performance optimization
- Track execution time and performance metrics

**FR12: Batch Processing**
- Process all matched video-subtitle pairs in a directory in a single execution
- Display real-time progress for embedding operations
- Continue processing remaining files if individual operations fail
- Provide summary of successful and failed operations at completion

**FR13: Smart Console Behavior**
- Auto-close console window on successful completion (default behavior)
- Keep console window open on errors for user review
- Allow override via `keep_console_open` configuration
- Display clear, informative status messages during operation

### Non-Functional Requirements

**NFR1: Performance**
- Renaming operations must process 1000+ files in under 1 second
- Utilize episode number caching for 12x performance improvement
- Support regex precompilation optimizations
- Embedding speed dependent on disk I/O (SSD significantly faster than HDD)
- CSV export must be optional for 14% additional speed improvement on large datasets

**NFR2: Platform and Dependencies**
- Target platform: Windows 10/11 (64-bit)
- Require Python 3.7+ with Python Launcher `py.exe` at `C:\Windows\py.exe`
- Require mkvmerge.exe (MKVToolNix) for embedding functionality
- Bundle mkvmerge.exe in `subfast/bin/` directory or allow custom path configuration
- Use Windows Registry (.reg files) for context menu integration

**NFR3: Installation Path**
- Fixed installation path: `C:\subfast\` (required for registry file compatibility)
- Organized directory structure: `scripts/`, `bin/`, `resources/` folders
- Registry files at root level for easy installation/uninstallation

**NFR4: File Format Support**
- Default video formats: `.mkv`, `.mp4` (configurable)
- Default subtitle formats: `.srt`, `.ass` (configurable)
- Embedding limited to `.mkv` containers (mkvmerge constraint)
- Support extensible configuration for additional formats

**NFR5: Error Handling and Reliability**
- Validate mkvmerge.exe existence before operations
- Provide clear error messages with affected filenames
- Gracefully handle partial failures during batch processing
- Check disk space before embedding operations
- Validate file permissions before read/write operations
- Return appropriate exit codes (0 for success, non-zero for errors)

**NFR6: Maintainability**
- Use modular Python script architecture
- Separate concerns: configuration, file matching, command building, execution, reporting
- Reuse file matching logic between rename and embed scripts
- Document all episode pattern regex for future maintenance

**NFR7: User Experience**
- Require no technical knowledge (GUI-free, menu-driven)
- Provide immediate visual feedback through console output
- Include comprehensive README and configuration documentation
- Support troubleshooting through detailed error messages

---

## Technical Assumptions

### Repository Structure: Monorepo

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

### Service Architecture

**Architecture Type:** Monolithic Local Scripts

- Two independent Python scripts (`subfast_rename.py`, `subfast_embed.py`)
- No client-server architecture
- Direct file system operations
- Command-line tool invoked via Windows Shell integration

### Testing Requirements

**Testing Strategy:** Manual + Unit Testing Convenience Methods

- Primary testing: Manual testing during development
- Unit tests for critical pattern matching regex
- File operation tests with temporary directories
- Integration testing with sample video/subtitle files
- Real-world testing with diverse episode naming patterns

**Rationale:** As a local utility tool, extensive automated testing infrastructure would add unnecessary complexity. Focus on robust pattern matching tests and real-world validation.

### Language and Runtime

- **Primary Language:** Python 3.7+
- **Rationale:** Cross-platform capabilities, strong file system libraries, easy scripting, subprocess management
- **Constraint:** Python Launcher must be available at `C:\Windows\py.exe`

### External Dependencies

- **MKVToolNix (mkvmerge.exe):**
  - Purpose: Subtitle embedding into MKV containers
  - Bundled in `bin/` directory
  - Configurable path for user-provided installations
  - Latest stable version recommended

### Subprocess Execution Pattern

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

### Configuration Management

- **Format:** INI file (`config.ini`)
- **Sections:** `[General]`, `[Renaming]`, `[Embedding]`
- **Behavior:** Auto-generate with defaults if missing
- **Rationale:** Human-readable, simple parsing, unified configuration for both features

### Performance Optimizations

- Episode number caching with dictionary lookups
- Regex precompilation at script initialization
- Optional CSV export for speed-critical scenarios
- Memory-efficient processing (42% reduction achieved in v2.5.0)

### Additional Technical Assumptions

1. **Windows Registry Integration:** Uses `.reg` files for context menu registration (admin privileges may be required)

2. **File System Operations:** Direct file I/O using Python's `pathlib` and `shutil` modules

3. **Character Encoding:** UTF-8 for all file operations and console output

4. **Collision Detection:** Filename-based collision checking before write operations

5. **Backup Strategy:** Move-based backups (not copy) to save disk space

6. **Progress Reporting:** Console-based real-time status updates (no GUI required)

7. **Error Logging:** Console output only (no separate log files by default)

---

## Epic List

### Epic 1: Foundation & Project Setup
**Goal:** Establish the SubFast project structure, Windows integration, and configuration system to provide a working foundation for both renaming and embedding features.

### Epic 2: Intelligent Subtitle Renaming System
**Goal:** Implement the comprehensive subtitle renaming engine with advanced episode pattern recognition, movie mode detection, and CSV reporting capabilities.

### Epic 3: MKV Subtitle Embedding System
**Goal:** Build the complete subtitle embedding workflow using mkvmerge integration, including language detection, backup management, and batch processing.

### Epic 4: Configuration, Documentation & Polish
**Goal:** Deliver production-ready documentation, configuration flexibility, and comprehensive error handling to ensure SubFast is user-friendly and reliable.

---

## Epic 1: Foundation & Project Setup

**Epic Goal:** Establish the SubFast project structure with proper Windows integration, configuration management, and foundational utilities. This epic delivers a working context menu integration and configuration system that both features will build upon, along with a simple health-check capability to verify the installation.

### Story 1.1: Project Structure and Installation System

**Story:**
As a SubFast user,
I want a clear directory structure and easy installation process,
so that I can quickly set up SubFast on my Windows machine.

**Acceptance Criteria:**

1. Project directory structure created at `C:\subfast\` with `scripts/`, `bin/`, and `resources/` folders
2. Python scripts placed in `scripts/` directory (`subfast_rename.py`, `subfast_embed.py`)
3. `mkvmerge.exe` bundled in `bin/` directory
4. `subfast_logo.ico` placed in `resources/` directory
5. Registry files (`add_subfast_menu.reg`, `remove_subfast_menu.reg`) created at root level
6. Registry files correctly reference `C:\subfast\` installation path
7. README documentation includes step-by-step installation instructions
8. Installation can be verified by checking for SubFast context menu in Windows Explorer

### Story 1.2: Windows Context Menu Integration

**Story:**
As a SubFast user,
I want to access SubFast features via right-click in any folder,
so that I can quickly process subtitles without opening command-line tools.

**Acceptance Criteria:**

1. `add_subfast_menu.reg` registry file creates cascading "SubFast" parent menu
2. Parent menu displays SubFast icon from `resources/subfast_logo.ico`
3. Submenu includes "Rename subtitles" option invoking `scripts/subfast_rename.py`
4. Submenu includes "Embed subtitles" option invoking `scripts/subfast_embed.py`
5. Both menu items pass the current folder path as an argument to respective scripts
6. `remove_subfast_menu.reg` registry file cleanly removes all SubFast menu entries
7. Registry changes take effect after running .reg file (may require Explorer restart)
8. Context menu appears when right-clicking in empty space within any folder

### Story 1.3: Configuration System with Auto-Generation

**Story:**
As a SubFast user and developer,
I want a centralized configuration file with sensible defaults,
so that I can customize behavior without modifying code and the tool works out-of-the-box.

**Acceptance Criteria:**

1. `config.ini` file created at project root with `[General]`, `[Renaming]`, and `[Embedding]` sections
2. If `config.ini` is missing, scripts automatically generate it with default values
3. `[General]` section includes: `detected_video_extensions`, `detected_subtitle_extensions`, `keep_console_open`
4. `[Renaming]` section includes: `renaming_report`, `renaming_language_suffix`
5. `[Embedding]` section includes: `mkvmerge_path`, `embedding_language_code`, `default_flag`, `embedding_report`
6. Default video extensions: `mkv, mp4`
7. Default subtitle extensions: `srt, ass`
8. Configuration validation performed at script startup with clear error messages for invalid values
9. Documentation (`CONFIGURATION_README.md`) explains all configuration options with examples

### Story 1.4: Smart Console Behavior System

**Story:**
As a SubFast user,
I want the console window to automatically close on success but stay open on errors,
so that I don't have to manually close windows but can review error messages when needed.

**Acceptance Criteria:**

1. When operations complete successfully, console window auto-closes after 2 seconds
2. When any error occurs, console window stays open with "Press any key to continue..." prompt
3. Behavior controlled by `keep_console_open` configuration option
4. When `keep_console_open = true`, console always waits for keypress before closing
5. When `keep_console_open = false`, smart behavior applied (auto-close on success)
6. Success message displayed before auto-close (e.g., "Operation completed successfully. Closing in 2 seconds...")
7. Error messages clearly displayed with affected filenames and troubleshooting hints
8. Exit codes properly set: 0 for success, non-zero for errors

### Story 1.5: Common Utilities and File Discovery Module

**Story:**
As a developer,
I want shared utility functions for file discovery and validation,
so that both renaming and embedding scripts use consistent, tested logic.

**Acceptance Criteria:**

1. Common utilities module created for shared functionality between scripts
2. File discovery function scans directory for files matching configured extensions
3. File extension filtering case-insensitive (e.g., `.MKV` and `.mkv` both match)
4. File validation checks for read permissions before processing
5. Path resolution handles relative and absolute paths correctly
6. Utility functions include disk space checking capability
7. File discovery returns sorted lists for consistent processing order
8. Python Launcher validation confirms `py.exe` exists at `C:\Windows\py.exe`
9. Module includes basic health-check function to verify installation components

---

## Epic 2: Intelligent Subtitle Renaming System

**Epic Goal:** Build the comprehensive subtitle renaming engine with advanced episode pattern recognition, context-aware matching, movie mode detection, collision handling, and optional CSV reporting. This epic delivers the complete renaming workflow accessible via Windows context menu.

### Story 2.1: Core Episode Pattern Recognition Engine

**Story:**
As a SubFast user,
I want the tool to recognize 25+ different episode naming patterns,
so that my subtitles match correctly regardless of source naming conventions.

**Acceptance Criteria:**

1. Regex patterns compiled for all supported formats at script initialization
2. Support `S##E##` format (e.g., S01E05, S2E15) with flexible zero-padding
3. Support `##x##` format (e.g., 2x05, 1x10) with smart resolution conflict detection
4. Support `S## - ##`, `S## - E##`, `S## - EP##` formats with flexible spacing
5. Support `Season # Episode #` format with various separators (space, dash, dot)
6. Support ordinal season patterns: `1st Season`, `2nd Season`, `3rd Season` + episode number
7. Support simple patterns: `E##`, `Ep##`, `- ##` (assumes Season 1)
8. Episode numbers extracted and normalized (e.g., "05", "5", "005" all become 5)
9. Season numbers extracted and normalized similarly
10. Pattern matching case-insensitive
11. First matching pattern wins (patterns ordered by specificity)
12. Unrecognized files logged and skipped without errors

### Story 2.2: Context-Aware File Matching

**Story:**
As a SubFast user,
I want the tool to intelligently match videos and subtitles even with inconsistent formatting,
so that files with different zero-padding or slight format differences still pair correctly.

**Acceptance Criteria:**

1. Episode number caching implemented with dictionary for 12x performance improvement
2. Match pairs by comparing normalized episode/season numbers (not raw strings)
3. `S2E8` (video) successfully matches `S02E008` (subtitle)
4. `2x05` (video) successfully matches `S02E05` (subtitle)
5. `Season 1 Episode 3` successfully matches `S01E03`
6. Matching logic ignores extra whitespace and separator variations
7. When multiple subtitles match same video, first match wins (logged as potential conflict)
8. When no match found, files remain unprocessed and logged
9. Matching performed in memory before any file operations
10. Match summary displayed: "Found X video files, Y subtitle files, Z matched pairs"

### Story 2.3: Movie Mode Detection and Simple Matching

**Story:**
As a SubFast user,
I want single video/subtitle pairs to match automatically without complex pattern matching,
so that my movie subtitles rename correctly without needing episode numbers.

**Acceptance Criteria:**

1. Movie mode automatically detected when exactly 1 video and 1 subtitle file found in directory
2. In movie mode, skip all episode pattern analysis
3. Direct 1:1 matching applied for single pair
4. Movie mode logged to console: "Movie mode detected: 1 video, 1 subtitle"
5. Movie detection performed before episode pattern processing
6. Multiple video or subtitle files automatically trigger episode mode
7. Empty directories handled gracefully with clear message
8. Movie mode respects language suffix configuration

### Story 2.4: Subtitle Renaming with Language Suffix

**Story:**
As a SubFast user,
I want renamed subtitles to include a configurable language suffix,
so that I can identify subtitle language from filename (e.g., `ShowName.S01E05.ar.srt`).

**Acceptance Criteria:**

1. Language suffix read from `config.ini` → `[Renaming]` → `renaming_language_suffix`
2. If suffix configured (e.g., `ar`), append `.{suffix}` before subtitle extension
3. If suffix empty or not configured, no suffix added
4. Renamed format: `{video_base_name}.{language_suffix}.{subtitle_extension}`
5. Example: Video `Show.S01E05.mkv` + subtitle with suffix `ar` → `Show.S01E05.ar.srt`
6. Example without suffix: Video `Show.S01E05.mkv` → `Show.S01E05.srt`
7. Original subtitle extension preserved (`.srt` stays `.srt`, `.ass` stays `.ass`)
8. Suffix validation: only alphanumeric characters and dashes allowed
9. Invalid suffix configuration logged as warning and ignored

### Story 2.5: Collision Detection and Safe Renaming

**Story:**
As a SubFast user,
I want the tool to prevent overwriting existing files during renaming,
so that I never lose data due to filename conflicts.

**Acceptance Criteria:**

1. Before renaming, check if target filename already exists
2. If target exists, skip rename operation for that pair
3. Log collision: "Skipped: Target file already exists - {target_filename}"
4. Collision count included in final summary
5. Original subtitle file remains unchanged when collision detected
6. Process continues with remaining pairs after collision
7. All operations atomic: no partial renames on errors
8. Collision handling works for both movie and episode modes
9. Summary displays: "X files renamed, Y collisions skipped"

### Story 2.6: Batch Processing and Progress Reporting

**Story:**
As a SubFast user,
I want to process all subtitle files in a folder with one context menu click,
so that I can efficiently manage large media libraries.

**Acceptance Criteria:**

1. All matched pairs processed in single script execution
2. Real-time console output for each rename operation
3. Progress format: "Renaming: {subtitle_filename} → {new_filename}"
4. Failures logged individually without stopping batch process
5. Final summary displays counts: matched pairs, successful renames, failures, collisions
6. Empty directories handled gracefully: "No video or subtitle files found"
7. Processing order deterministic (sorted by filename)
8. Total execution time reported in summary
9. All operations complete before console auto-close (on success)

### Story 2.7: CSV Reporting for Renaming Operations

**Story:**
As a SubFast user,
I want optional CSV reports of renaming operations,
so that I can audit changes and track batch processing results.

**Acceptance Criteria:**

1. CSV reporting controlled by `config.ini` → `[Renaming]` → `renaming_report`
2. When enabled, generate `renaming_report.csv` in processed directory
3. CSV columns: Original Filename, New Filename, Status, Timestamp, Execution Time
4. Status values: "Success", "Collision Skipped", "Error"
5. Timestamp in ISO 8601 format
6. Execution time tracked per file
7. CSV overwrites previous report in same directory
8. When disabled, no CSV generated (14% performance improvement on 1000+ files)
9. CSV generation errors logged but don't stop renaming operations
10. UTF-8 encoding with BOM for Excel compatibility

---

## Epic 3: MKV Subtitle Embedding System

**Epic Goal:** Implement the complete subtitle embedding workflow using mkvmerge integration, including automatic language detection, backup management, disk space validation, and batch processing with progress tracking. This epic delivers seamless soft-subtitle embedding accessible via Windows context menu.

### Story 3.1: mkvmerge Integration and Validation

**Story:**
As a SubFast developer and user,
I want reliable integration with mkvmerge for subtitle embedding,
so that the tool can embed subtitles into MKV files without errors.

**Acceptance Criteria:**

1. mkvmerge executable path read from `config.ini` → `[Embedding]` → `mkvmerge_path`
2. If path empty or not configured, default to `bin\mkvmerge.exe` (relative to config.ini)
3. Support both relative and absolute paths for mkvmerge
4. Validate mkvmerge exists and is executable before any operations
5. If mkvmerge not found, display clear error with troubleshooting steps and exit
6. Test mkvmerge connectivity with `--version` command at script startup
7. mkvmerge version logged to console for troubleshooting
8. Path resolution handles Windows backslashes and forward slashes
9. Full mkvmerge path cached after validation for subprocess calls
10. Configuration documentation includes mkvmerge setup instructions

### Story 3.2: Language Code Detection and Configuration

**Story:**
As a SubFast user,
I want subtitle tracks to have correct language tags,
so that media players can properly identify and display subtitle languages.

**Acceptance Criteria:**

1. Language detection implements strategy pattern: filename detection → config fallback → none
2. Extract language code from subtitle filename patterns: `.{lang}.{ext}`, `.{lang}.forced.{ext}`
3. Supported language code positions: `Movie.en.srt`, `Show.S01E05.ar.srt`, `Video.fra.forced.ass`
4. Detected codes converted to ISO 639-2 three-letter format if necessary
5. If no language detected in filename, fall back to `config.ini` → `[Embedding]` → `embedding_language_code`
6. If config also empty, no language tag applied (mkvmerge default behavior)
7. Language code validation: only valid ISO codes accepted
8. Invalid codes logged as warning and treated as "not detected"
9. Language detection logged for each file: "Detected language: {code}" or "No language detected"
10. Configuration documentation includes common ISO 639-2 codes reference

### Story 3.3: Default Subtitle Track Configuration

**Story:**
As a SubFast user,
I want control over whether embedded subtitles are marked as default track,
so that media players automatically select them based on my preference.

**Acceptance Criteria:**

1. Default track flag read from `config.ini` → `[Embedding]` → `default_flag`
2. When `default_flag = true`, mkvmerge command includes `--default-track 0:yes` for subtitle
3. When `default_flag = false`, mkvmerge command includes `--default-track 0:no`
4. Default value if not configured: `true` (mark as default)
5. Setting applies to all embedded subtitle tracks in batch operation
6. Configuration validation: only `true` or `false` accepted
7. Invalid values logged and treated as `true` (safe default)
8. Default flag behavior documented with examples in CONFIGURATION_README.md

### Story 3.4: mkvmerge Command Building with List-Based Arguments

**Story:**
As a developer,
I want mkvmerge commands built using list-based subprocess arguments,
so that commands work reliably on all Windows shell configurations.

**Acceptance Criteria:**

1. All subprocess calls use list of strings (not concatenated command string)
2. Never use `shell=True` in subprocess.run calls
3. All file paths converted to strings using `str(Path(...))` for proper handling
4. Command structure: `[mkvmerge_path, '-o', output_file, video_file, language_options, subtitle_file]`
5. Language options added only when language detected: `['--language', '0:{code}']`
6. Default flag options added: `['--default-track', '0:{yes|no}']`
7. Output filename: `{video_basename}.embedded.mkv` (temporary until successful)
8. Command building logged for debugging: "Command: [arg1, arg2, ...]"
9. Timeout set for mkvmerge execution: 300 seconds (5 minutes) per file
10. Windows path compatibility verified in all command arguments

### Story 3.5: Disk Space Validation and Embedded File Creation

**Story:**
As a SubFast user,
I want the tool to check available disk space before embedding,
so that operations don't fail mid-process due to insufficient space.

**Acceptance Criteria:**

1. Before each mkvmerge operation, check available disk space on target drive
2. Estimate required space: video file size + subtitle file size + 10% buffer
3. If insufficient space, skip file with clear error message
4. Space check logged: "Available: {X}GB, Required: {Y}GB"
5. mkvmerge creates temporary file: `{video_basename}.embedded.mkv`
6. mkvmerge configured for stream copy (no re-encoding of video/audio)
7. All original video and audio tracks preserved in output
8. Subtitle track added as additional track (doesn't replace existing tracks)
9. mkvmerge stdout/stderr captured for error diagnosis
10. Temporary `.embedded.mkv` file deleted if mkvmerge fails

### Story 3.6: Backup Management and File Operations

**Story:**
As a SubFast user,
I want automatic backups of original files before embedding,
so that I can recover originals if needed and understand what was processed.

**Acceptance Criteria:**

1. On first successful embedding, create `backups/` directory in processed folder
2. After successful mkvmerge operation, move original video to `backups/{original_video_name}`
3. After backup video, move original subtitle to `backups/{original_subtitle_name}`
4. If backup files already exist, skip backup and log: "Backup exists, updating file"
5. Remove subtitle from working directory after successful backup (not needed anymore)
6. After backup complete, rename `{video}.embedded.mkv` → `{original_video_name}.mkv`
7. If backup fails (permissions, space), keep original files and delete `.embedded.mkv`
8. Backup operations logged: "Backed up: {filename} → backups/{filename}"
9. All file operations atomic: no partial states on errors
10. Working directory contains only the new embedded MKV after successful operation

### Story 3.7: Batch Embedding with Progress Tracking

**Story:**
As a SubFast user,
I want to embed all matched subtitle/video pairs with real-time progress feedback,
so that I can efficiently process large media libraries and monitor status.

**Acceptance Criteria:**

1. Reuse file matching logic from renaming script for consistency
2. All matched `.mkv` video + subtitle pairs processed in single execution
3. Non-MKV videos skipped with log message: "Skipping {filename}: Embedding only supports MKV"
4. Real-time progress displayed: "Processing {X}/{Y}: {video_filename}"
5. Per-file status logged: "Success: {filename}" or "Failed: {filename} - {error}"
6. Individual failures don't stop batch processing
7. Final summary displays: matched pairs, successful embeds, failures, skipped files
8. Total execution time reported
9. Disk space checked before each file (not just at start)
10. Process completion triggers smart console behavior (auto-close on success)

### Story 3.8: CSV Reporting for Embedding Operations

**Story:**
As a SubFast user,
I want optional CSV reports of embedding operations,
so that I can audit which files were processed and track any failures.

**Acceptance Criteria:**

1. CSV reporting controlled by `config.ini` → `[Embedding]` → `embedding_report`
2. When enabled, generate `embedding_report.csv` in processed directory
3. CSV columns: Original Video, Original Subtitle, Language Code, Status, Timestamp, Execution Time
4. Status values: "Success", "Failed - Insufficient Space", "Failed - mkvmerge Error", "Skipped - Not MKV"
5. Language code column shows detected/configured language or "None"
6. Timestamp in ISO 8601 format
7. Execution time per file (mkvmerge operation duration)
8. CSV overwrites previous report in same directory
9. When disabled, no CSV generated (performance optimization)
10. UTF-8 encoding with BOM for Excel compatibility

---

## Epic 4: Configuration, Documentation & Polish

**Epic Goal:** Deliver comprehensive documentation, advanced configuration flexibility, robust error handling, and production-ready polish. This epic ensures SubFast is user-friendly, reliable, and maintainable with clear troubleshooting guidance and configuration examples.

### Story 4.1: Comprehensive README Documentation

**Story:**
As a SubFast user,
I want clear, comprehensive documentation,
so that I can understand features, install correctly, configure options, and troubleshoot issues.

**Acceptance Criteria:**

1. README includes product overview with feature highlights
2. Feature section covers both renaming and embedding with animated GIF examples
3. Requirements section lists: Windows 10/11, Python 3.7+, Python Launcher location
4. Installation section provides step-by-step instructions with exact paths
5. Usage section demonstrates both features with before/after examples
6. Configuration section explains all `config.ini` options with examples
7. Episode pattern recognition documented with comprehensive examples
8. Performance metrics included: "Renames 1000+ files in under 1 second"
9. Troubleshooting section covers common issues: context menu not appearing, Python not found, mkvmerge errors
10. Version history documents all major releases with feature highlights
11. Contributing section encourages issue reports with CSV exports
12. License section included

### Story 4.2: Configuration Documentation and Examples

**Story:**
As a SubFast user,
I want detailed configuration documentation with examples,
so that I can customize SubFast behavior to my exact needs.

**Acceptance Criteria:**

1. `CONFIGURATION_README.md` created in `resources/docs/` directory
2. Document structure: Overview → Section-by-section breakdown → Examples → Troubleshooting
3. Each configuration option documented with: purpose, valid values, default, impact
4. `[General]` section explained: file extensions, console behavior
5. `[Renaming]` section explained: CSV reports, language suffixes with examples
6. `[Embedding]` section explained: mkvmerge path, language codes, default flag, CSV reports
7. Common configuration scenarios provided: Arabic setup, multi-language setup, performance-optimized
8. ISO 639-2 language code reference table included
9. Configuration validation errors explained with solutions
10. Examples show complete config.ini files for different use cases

### Story 4.3: Advanced Error Handling and Recovery

**Story:**
As a SubFast user,
I want robust error handling with clear messages,
so that I understand problems and can take corrective action without data loss.

**Acceptance Criteria:**

1. All file system operations wrapped in try-except blocks
2. Errors categorized: Configuration, File System, mkvmerge, Permission, Disk Space
3. Each error displays: error type, affected file, specific issue, suggested action
4. Configuration errors detected at startup before file operations
5. Permission errors provide specific path and required permission level
6. Disk space errors display available vs. required space
7. mkvmerge errors include mkvmerge's stderr output for diagnosis
8. Partial batch failures logged individually with full batch summary
9. All errors logged to console with clear formatting (color-coding if supported)
10. Exit codes properly set for automation/scripting: 0 = success, 1 = config error, 2 = file error, 3 = mkvmerge error

### Story 4.4: Configuration Validation and Safe Defaults

**Story:**
As a developer and user,
I want configuration validation with safe defaults,
so that SubFast works reliably even with missing or invalid configuration.

**Acceptance Criteria:**

1. At startup, validate all configuration sections and keys
2. Missing `config.ini` auto-generated with all default values
3. Missing sections added with defaults, existing sections preserved
4. Invalid file extensions (non-alphanumeric) logged and ignored, defaults used
5. Invalid language codes logged and ignored, "none" used
6. Invalid boolean values converted to safe default with warning
7. Empty string values distinguished from missing values
8. Configuration validation summary logged at startup
9. Validation errors non-fatal: log warning, use default, continue operation
10. All defaults documented in code comments and user documentation

### Story 4.5: Performance Optimization and Metrics

**Story:**
As a SubFast user and developer,
I want performance optimizations and metrics,
so that SubFast operates efficiently on large media libraries.

**Acceptance Criteria:**

1. All regex patterns compiled once at script initialization (not per-file)
2. Episode number caching implemented with dictionary for O(1) lookups
3. File operations batched where possible (single directory scan)
4. CSV export optional to save 14% processing time on large datasets
5. Memory-efficient processing: process files sequentially, don't load all in memory
6. Performance metrics tracked: total execution time, average time per file
7. Console output includes performance summary: "{X} files processed in {Y} seconds"
8. Performance documentation includes: SSD vs HDD impact for embedding, dataset size impact
9. Memory usage optimization: 42% reduction maintained from v2.5.0
10. Large dataset testing: verify performance on 1000+ files remains under 1 second for renaming

### Story 4.6: Registry File Documentation and Troubleshooting

**Story:**
As a SubFast user,
I want clear registry integration documentation,
so that I can install/uninstall context menu correctly and resolve integration issues.

**Acceptance Criteria:**

1. Installation documentation explains registry file purpose and function
2. Administrator privileges requirement documented
3. Step-by-step installation: Run .reg file, approve UAC, verify in Explorer
4. Step-by-step uninstallation: Run remove .reg file, verify removal
5. Context menu not appearing: Troubleshooting guide includes Explorer restart, registry verification
6. Registry file format documented for advanced users
7. Path modification instructions if user wants non-default installation location
8. UAC prompt explanation and approval guidance
9. Verification steps: "Right-click in folder → Look for SubFast menu"
10. Common issues documented: old entries not removed, Python path issues, permission errors

### Story 4.7: Multi-Language Support and Localization Considerations

**Story:**
As a SubFast user in any locale,
I want the tool to work with international characters and various languages,
so that I can manage subtitles regardless of source language.

**Acceptance Criteria:**

1. All file operations use UTF-8 encoding
2. Console output supports Unicode characters (for international filenames)
3. Configuration files parsed with UTF-8 encoding
4. CSV reports generated with UTF-8 BOM for Excel compatibility
5. Filename pattern matching works with non-ASCII characters
6. Language code detection supports all ISO 639-2 codes
7. Error messages display international characters correctly
8. Documentation includes examples with non-English filenames
9. Path handling supports Unicode Windows paths
10. Testing includes files with Arabic, Chinese, Cyrillic, and special characters

### Story 4.8: Release Packaging and Distribution

**Story:**
As a SubFast maintainer,
I want a clear release packaging process,
so that users receive complete, working installations.

**Acceptance Criteria:**

1. Release package includes all required files: scripts, mkvmerge, config, registry files, documentation
2. Directory structure matches documented installation path
3. mkvmerge.exe bundled with appropriate version (latest stable)
4. Two release variants: default and Arabic-preconfigured
5. Arabic variant includes: `renaming_language_suffix = ar`, `embedding_language_code = ara`
6. README specific to each variant (mentions preconfiguration)
7. Version number consistent across: README, config comments, documentation
8. Release notes document changes, migration steps, new features
9. ZIP package extracts to correct directory structure
10. Release checklist includes: version update, testing, documentation review, package creation

---

## Next Steps

### UX Expert Prompt

SubFast v3.0.0 is primarily a command-line utility with Windows Explorer context menu integration. However, if you're considering adding a GUI configuration tool or installer wizard in the future:

**Prompt for UX Expert:**
"Review the SubFast PRD and consider UX improvements for:
1. Configuration management (potential GUI for config.ini editing)
2. Installation wizard to simplify setup process
3. Progress visualization for large batch operations
4. Error reporting and recovery flows
Please create a UI/UX specification if GUI components are desired for future versions."

### Architect Prompt

**Prompt for Architect:**
"Using this SubFast v3.0.0 PRD as input, create a comprehensive architecture document that covers:

1. **Current v3.0.0 Architecture:**
   - Detailed component breakdown for `subfast_rename.py` and `subfast_embed.py`
   - Module architecture and function responsibilities
   - Data flow diagrams for both renaming and embedding workflows
   - Configuration loading and validation architecture
   - File matching engine architecture with caching strategy
   - Subprocess management for mkvmerge integration
   - Error handling and recovery architecture

2. **Technical Implementation Details:**
   - Python module organization and imports
   - Windows Registry integration specifics
   - mkvmerge command building with list-based subprocess pattern
   - Backup management and atomic file operations
   - Performance optimization strategies (regex compilation, caching)
   - CSV reporting architecture

3. **Deployment and Infrastructure:**
   - Installation directory structure and file organization
   - Python Launcher dependency and validation
   - mkvmerge bundling vs. system installation
   - Registry file generation and maintenance

4. **Testing Strategy:**
   - Unit test requirements for pattern matching
   - Integration test scenarios with sample files
   - Manual testing procedures
   - Real-world validation datasets

Please ensure the architecture reflects SubFast as a complete dual-feature product with the correct v3.0.0 structure and paths (C:\subfast\, scripts/ folder, etc.)."

---

**End of PRD**
