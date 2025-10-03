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
As a user, I want the script to create embedded videos with temporary names, then safely move originals to a `backups/` directory after successful merge, so that I don't lose any data and my working directory only contains the final embedded videos.

**Acceptance Criteria:**
1. The embedded file is created with temporary name `[Original_Filename].embedded.mkv`
2. If merge succeeds, a `backups/` directory is created if it doesn't exist
3. Original `[Original_Filename].mkv` is moved to `backups/[Original_Filename].mkv`
4. Original subtitle file is moved to `backups/[Subtitle_Filename].[ext]` (ext = srt/ass/ssa)
5. The temporary `.embedded.mkv` file is renamed to `[Original_Filename].mkv`
6. If merge fails, the temporary `.embedded.mkv` file is deleted and originals remain untouched
7. Sufficient disk space is checked before starting the merge operation
8. Backup collision handling is intelligent:
   - If video already exists in `backups/`: skip video backup
   - If subtitle already exists in `backups/`: skip subtitle backup
   - Each file is checked independently
   - Subtitle is only deleted from working directory if it exists in `backups/`
   - A warning is logged for each skipped backup
9. Users can restore originals from `backups/` directory if needed

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
