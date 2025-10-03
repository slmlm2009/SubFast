# Epic 2: File Discovery & Management

**Epic Goal:** Implement intelligent file matching and safe output management

**Epic Description:**
This epic focuses on the file discovery and management aspects of the subtitle embedding feature. It leverages the existing pattern matching logic from the original renaming script to find and match video-subtitle pairs, implements safe file management with backups, and enables efficient batch processing of multiple files.

**Functional Requirements Covered:** FR2, FR5, FR6

---

## Story 2.1: Implement File Discovery and Video-Subtitle Matching

**Story:**
As a user, I want the script to automatically find and match video files with their corresponding subtitle files, so that I don't have to manually specify pairs.

**Acceptance Criteria:**
1. The script scans the target directory for all `.mkv` video files
2. The script scans the target directory for all subtitle files (`.srt`, `.ass`)
3. The same episode/movie detection logic from `rename_subtitles_to_match_videos_ar.py` is reused
4. Episode patterns (e.g., S01E01, 1x01) are correctly identified and matched
5. Movie patterns are correctly identified and matched
6. Each video file is matched with its corresponding subtitle file(s)
7. Unmatched files are reported to the user (video without subtitle, subtitle without video)
8. The matching results are displayed to the user before processing begins

---

## Story 2.2: Implement Backup and Output File Management

**Story:**
As a user, I want the script to create backups of my original files and generate new merged files safely, so that I don't lose any data if something goes wrong.

**Acceptance Criteria:**
1. Before embedding, original video files are renamed to `[Original_Filename].original.mkv`
2. The new merged file is created with the original filename `[Original_Filename].mkv`
3. If a `.original.mkv` file already exists, the script asks for user confirmation before overwriting
4. If the merge operation fails, the original file remains intact with the `.original` suffix
5. Sufficient disk space is checked before starting the merge operation
6. The output filename pattern is configurable via the config file
7. Users can verify successful merges before manually deleting `.original` backup files

---

## Story 2.3: Add Batch Processing Capabilities

**Story:**
As a user, I want to process all matched video-subtitle pairs in a folder with a single command, so that I can efficiently embed subtitles for my entire media library.

**Acceptance Criteria:**
1. All matched pairs in the directory are processed in a single execution
2. Processing occurs sequentially to avoid resource contention
3. Progress is displayed for each file being processed (e.g., "Processing file 3 of 15...")
4. Users can see which file is currently being processed
5. The total processing time is displayed at the end
6. A summary shows: total files found, successfully processed, and failed operations
7. Failed operations don't stop processing of remaining files
