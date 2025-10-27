# Epic 2: Intelligent Subtitle Renaming System

**Epic Goal:** Build the comprehensive subtitle renaming engine with advanced episode pattern recognition, context-aware matching, movie mode detection, collision handling, and optional CSV reporting. This epic delivers the complete renaming workflow accessible via Windows context menu.

## Story 2.1: Core Episode Pattern Recognition Engine

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

## Story 2.2: Context-Aware File Matching

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

## Story 2.3: Movie Mode Detection and Simple Matching

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

## Story 2.4: Subtitle Renaming with Language Suffix

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

## Story 2.5: Collision Detection and Safe Renaming

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

## Story 2.6: Batch Processing and Progress Reporting

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

## Story 2.7: CSV Reporting for Renaming Operations

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
