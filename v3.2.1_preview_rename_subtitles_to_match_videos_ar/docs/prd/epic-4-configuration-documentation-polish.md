# Epic 4: Configuration, Documentation & Polish

**Epic Goal:** Deliver comprehensive documentation, advanced configuration flexibility, robust error handling, and production-ready polish. This epic ensures SubFast is user-friendly, reliable, and maintainable with clear troubleshooting guidance and configuration examples.

## Story 4.1: Comprehensive README Documentation

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

## Story 4.2: Configuration Documentation and Examples

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

## Story 4.3: Advanced Error Handling and Recovery

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

## Story 4.4: Configuration Validation and Safe Defaults

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

## Story 4.5: Performance Optimization and Metrics

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

## Story 4.6: Registry File Documentation and Troubleshooting

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

## Story 4.7: Multi-Language Support and Localization Considerations

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

## Story 4.8: Release Packaging and Distribution

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
