# Epic 3: MKV Subtitle Embedding System

**Epic Goal:** Implement the complete subtitle embedding workflow using mkvmerge integration, including automatic language detection, backup management, disk space validation, and batch processing with progress tracking. This epic delivers seamless soft-subtitle embedding accessible via Windows context menu.

## Story 3.1: mkvmerge Integration and Validation

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

## Story 3.2: Language Code Detection and Configuration

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

## Story 3.3: Default Subtitle Track Configuration

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

## Story 3.4: mkvmerge Command Building with List-Based Arguments

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

## Story 3.5: Disk Space Validation and Embedded File Creation

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

## Story 3.6: Backup Management and File Operations

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

## Story 3.7: Batch Embedding with Progress Tracking

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

## Story 3.8: CSV Reporting for Embedding Operations

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
