# Requirements

## Functional Requirements

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

## Non-Functional Requirements

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
